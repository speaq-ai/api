import requests
from requests import HTTPError
from message.constants import (
    WATSON_ASSISTANT_BASE_URL,
    WATSON_ASSISTANT_API_KEY,
    WATSON_TTS_API_KEY,
    WATSON_TTS_BASE_URL,
    WATSON_STT_BASE_URL,
    WATSON_STT_API_KEY,
)
from message.utils.enums import ActionNames, WatsonEntities
import base64

from message.utils.osm import get_location_coords

actionRequirements = {
    ActionNames.AddFilter: [
        WatsonEntities.FilterField,
        WatsonEntities.FilterComparison,
        WatsonEntities.Number,
        WatsonEntities.DatasetName,
    ],
    ActionNames.LoadDataset: [WatsonEntities.DatasetName],
    ActionNames.Clear: [WatsonEntities.DatasetName],
    ActionNames.ChangeViewMode: [WatsonEntities.DatasetName, WatsonEntities.ViewMode],
    ActionNames.ViewAction: [WatsonEntities.ViewActions],
    ActionNames.GotoAction: [WatsonEntities.Location],
    ActionNames.LocationFilter: [WatsonEntities.DatasetName, WatsonEntities.Location],
    ActionNames.AddDatetimeFilterUnary: [
        WatsonEntities.FilterComparison,
        WatsonEntities.Date,
        WatsonEntities.DatasetName,
    ],
    ActionNames.AddDatetimeFilterBinary: [
        WatsonEntities.FilterComparison,
        WatsonEntities.StartDate,
        WatsonEntities.EndDate,
        WatsonEntities.DatasetName,
    ],
}


class AssistantAPI:
    def __init__(self, profile, datasets):
        self.profile = profile
        self.datasets = datasets

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
        content_type="application/json",
        **kwargs,
    ):
        url = f"{base_url}{url}"
        return requests.request(
            method,
            url,
            **{
                "auth": ("apikey", api_key),
                "headers": {"Content-Type": content_type},
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
    def is_complete(self, watsonResponse):
        assistantContext = watsonResponse["context"]
        if "user_defined" not in assistantContext["skills"]["main skill"]:
            return False

        contextVariables = assistantContext["skills"]["main skill"]["user_defined"]

        # if we fill the response with the only dataset that we see, we must then quit the conversation
        # so that watson doesn't continue asking for the dataset.
        # however, we must do that only when we return true - if they are missing other params, don't need
        # to clear the conversation tree yet
        quitConversation = False
        if "action" in contextVariables and contextVariables["action"] is not None:
            actionEnum = ActionNames(contextVariables["action"])
            requirements = actionRequirements[actionEnum]

            for required in requirements:
                if (
                    required.value not in contextVariables
                    or contextVariables[required.value] is None
                ):
                    if (
                        required == WatsonEntities.DatasetName
                        and len(self.datasets) == 1
                    ):
                        contextVariables[required.value] = self.datasets[0]
                        # don't return here, need to check the rest of required
                        quitConversation = True
                    else:
                        return False

            if quitConversation:
                # get the next response in the chain and return with current response
                new_response = self.message("Everything")
                if len(watsonResponse["output"]["generic"]):
                    watsonResponse["output"]["generic"][0]["text"] = new_response["text"]
                else:
                    watsonResponse["output"]["generic"] = [{"text": new_response["text"]}]

            return True

        else:
            return False

    def preprocess(self, context):
        if "location" in context:
            context["location"] = get_location_coords(context["location"])
        return context

    def patch_context(self, watson_response):
        """
        patch udf context variables in cases where watson can detect an intent 
        that requires multiple context assignments but fails to actually assign values.
        """
        entities = watson_response["output"]["entities"]
        context_variables = watson_response["context"]["skills"]["main skill"][
            "user_defined"
        ]
        action = context_variables.get("action")
        if (
            action is not None
            and ActionNames(action) == ActionNames.AddDatetimeFilterBinary
        ):
            date_objs = filter(lambda e: e["entity"] == "sys-date", entities)
            dates = list(map(lambda e: e["value"], date_objs))
            dates.sort()
            if not len(dates):
                return  # shouldn't be possible, but may want to raise an error here
            context_variables[(WatsonEntities.StartDate.value)] = dates[0]
            context_variables[WatsonEntities.EndDate.value] = dates[-1]

    # Formats the response to the client. Includes any parameters and respective actions if this is a complete
    # response.
    def format_response(self, watsonResponse):
    
        response = {"action": None, "variables": {}, "text": None}

        # patch context for date ranges missed by Watson
        self.patch_context(watsonResponse)
        if self.is_complete(watsonResponse):
            contextVariables = watsonResponse["context"]["skills"]["main skill"][
                "user_defined"
            ]

            contextVariables = self.preprocess(contextVariables)
            actionEnum = ActionNames(contextVariables["action"])
            requirements = actionRequirements[actionEnum]

            response["action"] = actionEnum.value

            for required in requirements:
                response["variables"][required.value] = contextVariables[required.value]

        # moved this to the end of the method b/c we need to see if original text is updated in is_complete
        if len(watsonResponse["output"]["generic"]) > 0:
            response["text"] = watsonResponse["output"]["generic"][0]["text"]
        else:
            response["text"] = None

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
            base_url=WATSON_TTS_BASE_URL,
            api_key=WATSON_TTS_API_KEY,
            params={"voice": "en-GB_KateVoice"},
            json={"text": text},
        )
        try:
            res.raise_for_status()
        except HTTPError as e:
            self.process_error(e)
        return base64.b64encode(res.content).decode("utf-8")

    def speech_to_text(self, speech, mime_type="audio/flac"):
        data = base64.b64decode(speech)
        res = self.request(
            "POST",
            "",
            base_url=WATSON_STT_BASE_URL,
            api_key=WATSON_STT_API_KEY,
            content_type=mime_type,
            data=data,
        )
        try:
            res.raise_for_status()
        except HTTPError as e:
            self.process_error(e)

        return res.json()["results"][0]["alternatives"][0]["transcript"]
