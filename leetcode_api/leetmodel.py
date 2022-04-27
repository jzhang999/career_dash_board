from requests import Session
from config import us
import json


class Graphql_API:
    def __init__(self, username, password, resolve=us):

        self.session = Session()
        self.api = resolve
        response = self.session.get(self.api["login"], headers={
            "X-Requested-With": 'XMLHttpRequest',
            "X-CSRFToken": ""
        })

        self.usernameame = username

        self.tokens = {"csrf": response.cookies.get_dict()['csrftoken']}
        self.tokens["LEETCODE_SESSION"] = "abcd"

        hd = self.request_header(self.api["login"])
        payload = {"csrfmiddlewaretoken": self.tokens["csrf"], "login": username, "password": password}

        response2 = self.session.post(self.api["login"], headers=hd, data=payload)
        self.tokens["session"] = response2.cookies.get_dict()["LEETCODE_SESSION"]

    def request_header(self, referer=None):
        if referer == None:
            referer = self.api["base"]

        hd = {'User-Agent': 'Mozilla/5.0',
              "X-Requested-With": 'XMLHttpRequest', 'Referer': referer,
              "Cookie": "LEETCODE_SESSION=${Helper.credit.session};csrftoken=${Helper.credit.csrfToken}"}

        if "csrf" in self.tokens:
            hd["X-CSRFToken"] = self.tokens["csrf"]

        if "session" in self.tokens:
            hd["Cookie"] = "LEETCODE_SESSION=%s;csrftoken=%s;" % (self.tokens["session"], self.tokens["csrf"])

        return hd



    def getRecentSubs(self, user):
        op = {"operationName": "getRecentSubmissionList",
              "variables": json.dumps({"username": user}),
              "query": "query getRecentSubmissionList($username: String!, $limit: Int) {\n  recentSubmissionList(username: $username, limit: $limit) {\n    title\n    titleSlug\n    timestamp\n    statusDisplay\n    lang\n    __typename\n  }\n  languageList {\n    id\n    name\n    verboseName\n    __typename\n  }\n}\n"}

        hd = self.request_header(self.api["profile"](user))

        s = self.session.post(self.api["graphql"], headers=hd, data=op)

        return json.loads(s.content)["data"]["recentSubmissionList"]
