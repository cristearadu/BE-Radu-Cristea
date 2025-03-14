VALID_USERS = [
    ("Fetching posts for user Samantha", "Samantha"),
]

INVALID_POST_IDS = [
    ("Fetching comments for a non-existent post ID", 9999),
    ("Fetching comments for an invalid post ID (string)", "abc"),
    ("Fetching comments for an empty post ID", ""),
    ("Fetching comments for an arbitrary invalid post ID", "asdad"),
    ("Fetching comments for less than minimum value for post ID", 0),
    ("Fetching comments for a negative value for POST ID", -1),
]
