import pytest
from modules.backend_tests.tests.test_data.test_user_comments_data import VALID_USERS, INVALID_POST_IDS
from core import HTTPStatusCodes


@pytest.mark.negative
@pytest.mark.regression
@pytest.mark.parametrize("test_case, post_id", INVALID_POST_IDS)
def test_get_comments_for_invalid_post_id(user_comments_helper, test_case, post_id):
    """
    Verify that the API handles invalid or non-existent postId by returning 200 OK and an empty JSON array.
    """
    comments = user_comments_helper.get_post_comments(post_id)
    assert comments == [], f"Expected empty list for postId {post_id}, but got: {comments}"
    pytest.logger.info(f"Invalid postId '{post_id}' correctly returned an empty list.")


@pytest.mark.negative
@pytest.mark.regression
@pytest.mark.parametrize("test_case, username", VALID_USERS)
def test_unexpected_status_codes(user_comments_helper, test_case, username):
    """
    Verify that the API does not return unexpected HTTP status codes.
    """
    user_data = user_comments_helper.get_user_with_posts(username=username)
    assert "posts" in user_data, "User has no posts."

    for post in user_data["posts"]:
        post_id = post["id"]
        response = user_comments_helper.controller.jsonplaceholder_request_controller(
            "GET_COMMENTS", post_id=post_id
        )

        assert response.status_code == HTTPStatusCodes.OK.value, f"Unexpected status code {response.status_code} for post {post_id}"

        pytest.logger.info(f"Post {post_id} returned expected status code 200.")


@pytest.mark.negative
@pytest.mark.regression
@pytest.mark.parametrize("test_case, username", VALID_USERS)
def test_unexpected_server_errors(user_comments_helper, test_case, username):
    """
    Verify that the API does not return unexpected 5XX errors or rate limits (429).
    """
    user_data = user_comments_helper.get_user_with_posts(username=username)
    assert "posts" in user_data, "User has no posts."

    for post in user_data["posts"]:
        post_id = post["id"]
        response = user_comments_helper.controller.jsonplaceholder_request_controller(
            "GET_COMMENTS", post_id=post_id
        )

        assert response.status_code not in {
            HTTPStatusCodes.TOO_MANY_REUQESTS.value,
            HTTPStatusCodes.INTERNAL_SERVER_ERROR.value,
            HTTPStatusCodes.SERVICE_UNAVAILABLE.value}, \
            f"Unexpected server error {response.status_code} for post {post_id}"

        pytest.logger.info(f"Post {post_id} did not trigger any unexpected server errors.")
