import pytest


def test_get_user_posts(user_comments_helper):
    username = "Samantha"
    user_data = user_comments_helper.get_user(username=username)
    posts = user_comments_helper.get_user_posts(user_data['id'])

    assert len(posts) > 0
    pytest.logger.info(f"User {username} has posts: {posts}")
