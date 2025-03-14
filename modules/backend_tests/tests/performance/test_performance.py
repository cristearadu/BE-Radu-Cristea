import pytest
import time

from modules.backend_tests.tests.test_data.test_user_comments_data import VALID_USERS


@pytest.mark.performance
@pytest.mark.regression
@pytest.mark.parametrize("test_case, username", VALID_USERS)
def test_large_api_response(user_comments_helper, test_case, username):
    """
    Verify that the API correctly handles large response sizes (many posts with many comments).
    """
    user_data = user_comments_helper.get_user_with_posts(username=username)
    assert "posts" in user_data, "User has no posts."

    total_comments = 0
    for post in user_data["posts"]:
        post_id = post["id"]
        comments = user_comments_helper.get_post_comments(post_id)

        total_comments += len(comments)

    assert total_comments > 10, f"Expected more comments in large response, but got only {total_comments}"
    pytest.logger.info(f"Total comments retrieved across posts: {total_comments}")


@pytest.mark.smoke
@pytest.mark.performance
@pytest.mark.regression
@pytest.mark.parametrize("test_case, username", VALID_USERS)
def test_api_response_time(user_comments_helper, test_case, username):
    """
    Measure API response time for all posts of the user.
    """
    user_data = user_comments_helper.get_user_with_posts(username=username)
    assert "posts" in user_data, "User has no posts."

    for post in user_data["posts"]:
        post_id = post["id"]
        start_time = time.time()
        _ = user_comments_helper.get_post_comments(post_id)
        response_time = (time.time() - start_time) * 1000  # convert to ms
        assert response_time < 500, f"API response time too slow for post {post_id}: {response_time:.2f}ms"
        pytest.logger.info(f"API response time for post {post_id}: {response_time:.2f}ms")
