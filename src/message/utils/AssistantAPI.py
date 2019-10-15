import requests
from requests import HTTPError
from message.constants import (
    WATSON_ASSISTANT_BASE_URL,
    WATSON_ASSISTANT_API_KEY,
    WATSON_TTS_API_KEY,
    WATSON_TTS_BASE_URL,
    WATSON_STT_BASE_URL,
)
from message.utils.enums import ActionNames, WatsonEntities
import base64

actionRequirements = {
    ActionNames.AddFilter: [
        WatsonEntities.FilterField,
        WatsonEntities.FilterComparison,
        WatsonEntities.Number,
        WatsonEntities.DatasetName,
    ],
    ActionNames.LoadDataset: [WatsonEntities.DatasetName],
    ActionNames.Clear: [WatsonEntities.DatasetName],
    ActionNames.ChangeViewMode: [WatsonEntities.ViewMode],
    ActionNames.ViewAction: [WatsonEntities.ViewActions]
}


class AssistantAPI:
    def __init__(self, profile):
        self.profile = profile

        if not self.profile.assistant_session:
            self.profile.assistant_session = self.create_session()
            self.profile.save()

    # static methods below

    @classmethod
    def request(
        cls,
        method,
        url,
        base_url=WATSON_ASSISTANT_BASE_URL,
        api_key=WATSON_ASSISTANT_API_KEY,
        **kwargs,
    ):
        url = f"{base_url}{url}"
        return requests.request(
            method,
            url,
            **{
                "auth": ("apikey", api_key),
                "headers": {"Content-Type": "application/json"},
                "params": {"version": "2019-02-28"},
                **kwargs,
            },
        )

    @classmethod
    def process_error(cls, e):
        # log error, print, etc.
        print(e)
        raise e

    @classmethod
    def create_session(cls):
        res = cls.request("POST", "/sessions")
        try:
            res.raise_for_status()
        except HTTPError as e:
            cls.process_error(e)
        return res.json()["session_id"]

    # private methods below

    # check the response by comparing the intent to the actions it can take
    # then, check and see if any of the actions have all required parameters in the context (by using actionRequirements)
    # returns T/F
    def is_complete(self, assistantContext):
        if "user_defined" not in assistantContext["skills"]["main skill"]:
            return False

        contextVariables = assistantContext["skills"]["main skill"]["user_defined"]

        if "action" in contextVariables and contextVariables["action"] is not None:
            actionEnum = ActionNames(contextVariables["action"])
            requirements = actionRequirements[actionEnum]

            for required in requirements:
                if (
                    required.value not in contextVariables
                    or contextVariables[required.value] is None
                ):
                    return False

            return True

        else:
            return False

    # Formats the response to the client. Includes any parameters and respective actions if this is a complete
    # response.
    def format_response(self, watsonResponse):
        if len(watsonResponse["output"]["generic"]) > 0:
            text = watsonResponse["output"]["generic"][0]["text"]
        else:
            text = None

        response = {"action": None, "variables": {}, "text": text}

        if self.is_complete(watsonResponse["context"]):
            contextVariables = watsonResponse["context"]["skills"]["main skill"][
                "user_defined"
            ]
            actionEnum = ActionNames(contextVariables["action"])
            requirements = actionRequirements[actionEnum]

            response["action"] = actionEnum.value

            for required in requirements:
                response["variables"][required.value] = contextVariables[required.value]

        return response

    # public methods below

    def delete_session(self):
        res = self.request("DELETE", f"/sessions/{self.session_id}")
        try:
            res.raise_for_status()
        except HTTPError as e:
            self.process_error(e)

    def message(self, text):
        res = self.request(
            "POST",
            f"/sessions/{self.profile.assistant_session}/message",
            json={"input": {"text": text, "options": {"return_context": True}}},
        )

        if res.status_code == 404:
            self.profile.assistant_session = self.create_session()
            self.profile.save()
            return self.message(text)

        try:
            res.raise_for_status()
        except HTTPError as e:
            self.process_error(e)

        json = res.json()

        return self.format_response(json)

    def text_to_speech(self, text):
        res = self.request(
            "POST",
            "",
            params={"voice": "en-GB_KateVoice"},
            json={"text": text},
            base_url=WATSON_TTS_BASE_URL,
            api_key=WATSON_TTS_API_KEY,
        )
        try:
            res.raise_for_status()
        except HTTPError as e:
            self.process_error(e)
        return base64.b64encode(res.content).decode("utf-8")

    def speech_to_text(self, speech):
        pass
