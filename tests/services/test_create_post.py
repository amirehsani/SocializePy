import pytest
from apps.blog.services.post import create_post


@pytest.mark.django_db
def test_create_post(user2, user1, subscription1, profile1, post1):
    a = create_post(user=user1, title="foo", content="bar")

    assert a.author == user1
    assert a.title == "foo"
    assert a.content == "bar"
