import pytest
import json
from django.urls import reverse


@pytest.mark.django_db
def test_empty_subs_api(api_client, user1, subscription1, profile1, post1):
    url_ = reverse("api:blog:subscribe")

    response = api_client.get(url_, content_type="application/json")
    data = json.loads(response.content)

    assert response.status_code == 200
    assert data.get('results') == []
    assert data.get('limit') == 10
