import pytest
from modules.backend_tests.general.request_builder_user_comments import (JSONPlaceholderController,
                                                                         JSONPlaceholderEndpoints)


class HelperUserComments:

    def __init__(self):
        self.controller = JSONPlaceholderController()

    def get_user(self, **filters) -> dict:
        """
        Fetch user details based on dynamic filters.

        Args:
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

        Raises:
            AssertionError: If no user matches the given filters.
        """
        response = self.controller.jsonplaceholder_request_controller(
            JSONPlaceholderEndpoints.GET_USERS.switcher
        )

        assert response.status_code == 200, f"Failed to fetch users. Expected status code 200. Actual status code: {response.status_code}"
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

        raise AssertionError(f"No user found matching criteria: {filters}")

    def get_user_posts(self, user_id: int) -> list:
        """
        Fetch posts for a given user ID.

        Args:
            user_id (int): The ID of the user whose posts need to be fetched.

        Returns:
            list: A list of post IDs associated with the given user.

        Raises:
            AssertionError: If the user has no posts or the request fails.
        """
        response = self.controller.jsonplaceholder_request_controller(
            JSONPlaceholderEndpoints.GET_POSTS.switcher, user_id=user_id
        )

        assert response.status_code == 200, f"Failed to fetch posts, Status: {response.status_code}"
        posts = response.json()

        assert len(posts) > 0, f"User {user_id} has no posts!"
        pytest.logger.info(f"User {user_id} has {len(posts)} posts.")

        return [post["id"] for post in posts]  # Return list of post IDs

    def get_post_comments(self, post_id: int) -> list:
        """
        Fetch comments for a given post ID.

        Args:
            post_id (int): The ID of the post whose comments need to be fetched.

        Returns:
            list: A list of comments associated with the given post.

        Raises:
            AssertionError: If the post has no comments or the request fails.
        """
        response = self.controller.jsonplaceholder_request_controller(
            JSONPlaceholderEndpoints.GET_COMMENTS.switcher, post_id=post_id
        )

        assert response.status_code == 200, f"Failed to fetch comments, Status: {response.status_code}"
        comments = response.json()

        assert len(comments) > 0, f"No comments found for post {post_id}!"
        pytest.logger.info(f"Post {post_id} has {len(comments)} comments.")

        return comments
