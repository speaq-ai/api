import requests
from requests import HTTPError
from message.constants import WATSON_ASSISTANT_BASE_URL, WATSON_ASSISTANT_API_KEY
from message.utils.enums import ActionNames, WatsonEntities

actionRequirements = {
    ActionNames.AddFilter: [WatsonEntities.FilterField, WatsonEntities.FilterComparison, WatsonEntities.Number],
    ActionNames.LoadDataset: [WatsonEntities.DatasetName],
    ActionNames.Clear: []
}

class AssistantAPI:
    def __init__(self, profile):
        self.profile = profile

        if not self.profile.assistant_session:
            self.profile.assistant_session = self.create_session()
            self.profile.save()

    # static methods below

    @classmethod
    def request(cls, method, url, **kwargs):
        url = f"{WATSON_ASSISTANT_BASE_URL}{url}"
        return requests.request(
            method,
            url,
            **{
                "auth": ("apikey", WATSON_ASSISTANT_API_KEY),
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
        pass

    # Formats the response to the client. Includes any parameters and respective actions if this is a complete
    # response.
    def format_response(self, assistantContext):
        pass

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
            json={"input": {"text": text, "options": { "return_context": True }}},
        )
        if res.status_code == 404:
            self.profile.assistant_session = self.create_session()
            self.profile.save()
            return self.message(text)

        try:
            res.raise_for_status()
        except HTTPError as e:
            self.process_error(e)
        return res.json()
