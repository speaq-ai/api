import requests
from requests import HTTPError
from message.constants import WATSON_ASSISTANT_BASE_URL, WATSON_ASSISTANT_API_KEY


class AssistantAPI:
    def __init__(self, session_id=None):
        self.session_id = (
            session_id if session_id is not None else self.create_session()
        )

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

    def delete_session(self):
        res = self.request("DELETE", f"/sessions/{self.session_id}")
        try:
            res.raise_for_status()
        except HTTPError as e:
            self.process_error(e)

    def message(self, text):
        res = self.request(
            "POST",
            f"/sessions/{self.session_id}/message",
            json={"input": {"text": text}},
        )
        if res.status_code == 404:
            self.session_id = self.create_session()
            return self.message(text)

        try:
            res.raise_for_status()
        except HTTPError as e:
            self.process_error(e)
        return res.json()
