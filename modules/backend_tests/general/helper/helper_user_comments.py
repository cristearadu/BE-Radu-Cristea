import pytest
from modules.backend_tests.general.request_builder_user_comments import (JSONPlaceholderController,
                                                                         JSONPlaceholderEndpoints)
from core import HTTPStatusCodes


class HelperUserComments:

    def __init__(self):
        self.controller = JSONPlaceholderController()

    def get_user(self, expected_status_code: int = HTTPStatusCodes.OK.value, **filters) -> dict:
        """
        Fetch user details based on dynamic filters.

        Args:
            expected_status_code (int): Expected status code for request (E.g. 200, 201 etc.)
            **filters: Arbitrary keyword arguments to filter users by. Supported filters include:
                - name (str, optional): The full name of the user.
                - username (str, optional): The username of the user.
                - email (str, optional): The email address of the user.
                - phone (str, optional): The phone number of the user.
                - website (str, optional): The website associated with the user.
                - company (str, optional): The company name associated with the user.
                - address_city (str, optional): The city of the user's address.

        Returns:
            dict: The full user details if found.
        """
        response = self.controller.jsonplaceholder_request_controller(
            JSONPlaceholderEndpoints.GET_USERS.switcher
        )

        assert response.status_code == expected_status_code, \
            (f"Failed to fetch users. Expected status code {expected_status_code}. "
             f"Actual status code: {response.status_code}")
        users = response.json()

        for user in users:
            match = all(
                str(user.get(key.split("_")[0], "")).lower() == str(value).lower()
                if "_" not in key else
                str(user.get(key.split("_")[0], {}).get(key.split("_")[1], "")).lower() == str(value).lower()
                for key, value in filters.items()
            )
            if match:
                pytest.logger.info(f"User found: {user}")
                return user

        pytest.logger.error(f"No user found matching criteria: {filters}")

    def get_user_posts(self, user_id: int, expected_status_code: str = HTTPStatusCodes.OK.value) -> list:
        """
        Fetch posts for a given user ID.

        Args:
            user_id (int): The ID of the user whose posts need to be fetched.
            expected_status_code (str): Expected status code for request (E.g. 200, 201 etc.)

        Returns:
            list: A list of post
        """
        response = self.controller.jsonplaceholder_request_controller(
            JSONPlaceholderEndpoints.GET_USER_POSTS.switcher, user_id=user_id
        )

        assert response.status_code == expected_status_code, \
            (f"Failed to fetch user {user_id} posts. Expected status code {expected_status_code}. "
             f"Actual status code: {response.status_code}")
        posts = response.json()
        pytest.logger.info(f"User {user_id} has {len(posts)} posts.")
        return posts

    def get_post_comments(self, post_id: int, expected_status_code: str = HTTPStatusCodes.OK.value) -> list:
        """
        Fetch comments for a given post ID.

        Args:
            post_id (int): The ID of the post whose comments need to be fetched.
            expected_status_code (str): Expected status code for request (E.g. 200, 201 etc.)

        Returns:
            list: A list of comments associated with the given post.

        Raises:
            AssertionError: If the post has no comments or the request fails.
        """
        response = self.controller.jsonplaceholder_request_controller(
            JSONPlaceholderEndpoints.GET_POST_COMMENTS.switcher, post_id=post_id
        )

        assert response.status_code == expected_status_code, \
            (f"Failed to fetch comments for post id {post_id}. Expected status code {expected_status_code}. "
             f"Actual status code: {response.status_code}")
        comments = response.json()
        pytest.logger.info(f"Post {post_id} has {len(comments)} comments.")

        return comments

    def get_user_with_posts(self, expected_status_code: int = HTTPStatusCodes.OK.value, **filters) -> dict:
        """
        Fetch user details and their posts in a single method.

        Args:
            expected_status_code (int): Expected status code for request.
            **filters: Arbitrary keyword arguments to filter users by.

        Returns:
            dict: A dictionary containing user details and their posts.
        """
        user = self.get_user(expected_status_code, **filters)
        assert user, f"User not found with given filters {filters}"

        posts = self.get_user_posts(user["id"], expected_status_code)
        assert posts, f"User {user['username']} has no posts!"
        return {
            "user": user,
            "posts": posts
        }
