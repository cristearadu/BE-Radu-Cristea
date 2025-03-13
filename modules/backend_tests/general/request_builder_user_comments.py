from enum import Enum
from core import JSONPLACEHOLDER_BASE_URL
from functools import partial
from core.request_builder import http_request


class JSONPlaceholderEndpoints(Enum):
    GET_USERS = ("GET", f"{JSONPLACEHOLDER_BASE_URL}/users", "GET_USERS")
    GET_POSTS = ("GET", f"{JSONPLACEHOLDER_BASE_URL}/posts/{{user_id}}", "GET_POSTS")
    GET_COMMENTS = ("GET", f"{JSONPLACEHOLDER_BASE_URL}/comments?postId={{post_id}}", "GET_COMMENTS")

    def __init__(self, request_type, path, switcher):
        self.request_type = request_type
        self.path = path
        self.switcher = switcher


class JSONPlaceholderController:
    def jsonplaceholder_request_controller(self, key, headers=None, request_body=None, **kwargs):
        switcher = {
            JSONPlaceholderEndpoints.GET_USERS.switcher: partial(
                http_request,
                JSONPlaceholderEndpoints.GET_USERS.request_type,
                JSONPlaceholderEndpoints.GET_USERS.path,
                headers
            ),
            JSONPlaceholderEndpoints.GET_POSTS.switcher: partial(
                http_request,
                JSONPlaceholderEndpoints.GET_POSTS.path.format(user_id=kwargs.get("user_id")),
                headers
            ),
            JSONPlaceholderEndpoints.GET_COMMENTS.switcher: partial(
                http_request,
                JSONPlaceholderEndpoints.GET_COMMENTS.path.format(post_id=kwargs.get("post_id")),
                headers
            ),
        }

        if key in switcher:
            return switcher[key]()
        else:
            raise ValueError(f"Invalid key: {key}")
