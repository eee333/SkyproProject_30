import pytest
from ads.models import Ad


@pytest.mark.django_db
def test_ad_list(client, ad):

    expected_response = {
        "count": 1,
        "next": None,
        "previous": None,
        "results": [{
            "id": ad.pk,
            "name": "Test name 2",
            "price": "200",
            "description": "Test description",
            "user": ad.user_id,
            "category": None,
            "is_published": False,
            "image": None,
        }]
    }

    response = client.get("/ad/")
    assert response.status_code == 200
    assert response.data == expected_response
