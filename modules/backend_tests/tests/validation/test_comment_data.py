import pytest
import re

from modules.backend_tests.tests.test_data.test_user_comments_data import VALID_USERS
from core import COMMENT_STRUCTURE, EMAIL_REGEX


@pytest.mark.smoke
@pytest.mark.validation
@pytest.mark.regression
@pytest.mark.parametrize("test_case, username", VALID_USERS)
def test_validate_comment_structure(user_comments_helper, test_case, username):
    """
    Verify that each comment contains the required fields, postId matches,
    and each field has the correct data type.
    """
    user_data = user_comments_helper.get_user_with_posts(username=username)
    assert "posts" in user_data, "User has no posts."

    for post in user_data["posts"]:
        post_id = post["id"]
        comments = user_comments_helper.get_post_comments(post_id)

        assert comments, f"Expected comments for post {post_id}, but got an empty response."

        seen_comment_ids = set()
        for comment in comments:
            for field, expected_type in COMMENT_STRUCTURE.items():
                assert field in comment, f"Missing '{field}' field in comment {comment}"
                assert isinstance(comment[field], expected_type), \
                    (f"Field '{field}' in comment {comment} has incorrect type. Expected: {expected_type}, "
                     f"Got: {type(comment[field])}")

            assert comment["postId"] == post_id, f"postId mismatch in comment: {comment}"

            assert comment["id"] not in seen_comment_ids, f"Duplicate comment ID found: {comment['id']}"
            seen_comment_ids.add(comment["id"])

        pytest.logger.info(f"All comments for post {post_id} passed structure validation.")


@pytest.mark.smoke
@pytest.mark.validation
@pytest.mark.regression
@pytest.mark.parametrize("test_case, username", VALID_USERS)
def test_validate_comment_values(user_comments_helper, test_case, username):
    """
    Verify that each comment has meaningful values:
    - `postId` should match the requested post.
    - `id` should be a positive integer.
    - `name`, `email`, and `body` should be non-empty strings.
    """
    user_data = user_comments_helper.get_user_with_posts(username=username)
    assert "posts" in user_data, "User has no posts."

    for post in user_data["posts"]:
        post_id = post["id"]
        comments = user_comments_helper.get_post_comments(post_id)

        assert comments, f"Expected comments for post {post_id}, but got an empty response."

        for comment in comments:
            # postId is valid and matches
            assert isinstance(comment["postId"], int), f"Invalid postId type: {comment['postId']}"
            assert comment["postId"] == post_id, f"postId mismatch in comment: {comment}"

            # id is a valid positive integer
            assert isinstance(comment["id"], int), f"Invalid id type: {comment['id']}"
            assert comment["id"] > 0, f"Comment id should be positive: {comment['id']}"

            # name, email, and body are non-empty
            assert isinstance(comment["name"], str) and comment["name"].strip(), f"Invalid name: {comment['name']}"
            assert isinstance(comment["email"], str) and comment["email"].strip(), f"Invalid email: {comment['email']}"
            assert isinstance(comment["body"], str) and comment["body"].strip(), f"Invalid body: {comment['body']}"

        pytest.logger.info(f"All comments for post {post_id} passed value validation.")


@pytest.mark.validation
@pytest.mark.regression
@pytest.mark.parametrize("test_case, username", VALID_USERS)
def test_comments_missing_required_fields(user_comments_helper, test_case, username):
    """
    Verify that all comments returned contain required fields.
    If any required field is missing, the test should fail.
    """
    user_data = user_comments_helper.get_user_with_posts(username=username)
    assert "posts" in user_data, "User has no posts."

    for post in user_data["posts"]:
        post_id = post["id"]
        comments = user_comments_helper.get_post_comments(post_id)

        assert comments, f"Expected comments for post {post_id}, but got an empty response."

        for comment in comments:
            missing_fields = [field for field in COMMENT_STRUCTURE if field not in comment]
            assert not missing_fields, f"Comment {comment} is missing required fields: {missing_fields}"

        pytest.logger.info(f"All comments for post {post_id} contain required fields.")


@pytest.mark.validation
@pytest.mark.regression
@pytest.mark.parametrize("test_case, username", VALID_USERS)
def test_comments_unexpected_extra_fields(user_comments_helper, test_case, username):
    """
    Verify that API does not return unexpected extra fields in comments.
    If extra fields appear, we log them as a warning.
    """
    user_data = user_comments_helper.get_user_with_posts(username=username)
    assert "posts" in user_data, "User has no posts."

    for post in user_data["posts"]:
        post_id = post["id"]
        comments = user_comments_helper.get_post_comments(post_id)

        assert comments, f"Expected comments for post {post_id}, but got an empty response."

        for comment in comments:
            extra_fields = [field for field in comment if field not in COMMENT_STRUCTURE]
            if extra_fields:
                pytest.logger.warning(f"Comment {comment} contains unexpected fields: {extra_fields}")

        pytest.logger.info(f"Checked for unexpected fields in comments for post {post_id}.")


@pytest.mark.validation
@pytest.mark.regression
@pytest.mark.parametrize("test_case, username", VALID_USERS)
def test_validate_email_format_in_comments(user_comments_helper, test_case, username):
    """
    Verify that all emails in comments follow the proper format and have required content.
    """

    user_data = user_comments_helper.get_user_with_posts(username=username)
    assert "posts" in user_data, "User has no posts."

    for post in user_data["posts"]:
        post_id = post["id"]
        comments = user_comments_helper.get_post_comments(post_id)

        if not comments:
            pytest.skip(f"Skipping test: No comments returned for post {post_id}")

        for comment in comments:
            assert re.match(EMAIL_REGEX, comment["email"]), f"Invalid email format: {comment['email']}"
            assert comment["name"].strip(), f"Name should not be empty: {comment}"
            assert comment["email"].strip(), f"Email should not be empty: {comment}"
            assert comment["body"].strip(), f"Body should not be empty: {comment}"

        pytest.logger.info(f"All emails in comments for post {post_id} are valid.")


@pytest.mark.validation
@pytest.mark.regression
@pytest.mark.parametrize("test_case, username", VALID_USERS)
def test_no_duplicate_comments(user_comments_helper, test_case, username):
    """
    Verify that the API does not return duplicate comments for any post.
    """
    user_data = user_comments_helper.get_user_with_posts(username=username)
    assert "posts" in user_data, "User has no posts."

    for post in user_data["posts"]:
        post_id = post["id"]
        comments = user_comments_helper.get_post_comments(post_id)

        assert comments, f"Expected comments for post {post_id}, but got an empty response."

        unique_comments = set()
        for comment in comments:
            comment_tuple = (comment["id"], comment["postId"], comment["name"], comment["email"], comment["body"])
            assert comment_tuple not in unique_comments, f"Duplicate comment found: {comment}"
            unique_comments.add(comment_tuple)

        pytest.logger.info(f"All comments for post {post_id} are unique.")
