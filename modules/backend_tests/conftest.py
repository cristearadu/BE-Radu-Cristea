import pytest

from modules.backend_tests.general.helper.helper_user_comments import HelperUserComments


@pytest.fixture(scope="session")
def user_comments_helper():
    yield HelperUserComments()
