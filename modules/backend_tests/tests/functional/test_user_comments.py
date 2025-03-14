import pytest
from modules.backend_tests.tests.test_data.test_user_comments_data import VALID_USERS


@pytest.mark.smoke
@pytest.mark.functional
@pytest.mark.regression
@pytest.mark.parametrize("test_case, username", VALID_USERS)
def test_get_user_with_posts(user_comments_helper, test_case, username):
    """
    Fetch user details and their posts dynamically.
    """
    user_comments_helper.get_user_with_posts(username=username)


@pytest.mark.smoke
@pytest.mark.functional
@pytest.mark.regression
@pytest.mark.parametrize("test_case, username", VALID_USERS)
def test_get_comments_for_valid_posts(user_comments_helper, test_case, username):
    """
    Verify that GET /comments?postId={post_id} returns 200 OK for all posts of the user.
    Also, ensure that at least one comment is returned.
    """
    user_data = user_comments_helper.get_user_with_posts(username=username)
    assert "posts" in user_data, "User has no posts."

    for post in user_data["posts"]:
        post_id = post["id"]
        comments = user_comments_helper.get_post_comments(post_id)

        assert comments, f"Expected comments for post {post_id}, but got an empty response."
        assert isinstance(comments, list), f"Response body for post {post_id} is not a JSON array."

        pytest.logger.info(f"Post {post_id} returned {len(comments)} comments.")
