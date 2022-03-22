import pytest
from ads.models import Ad


@pytest.mark.django_db
def test_ad_list(client):
    ad = Ad.objects.create(
        name="Test name",
        price=200,
        description="Test description",
    )

    expected_response = {
        "count": 1,
        "next": None,
        "previous": None,
        "results": [{
            "id": ad.pk,
            "name": "Test name",
            "price": "200",
            "description": "Test description",
            "user": None,
            "category": None,
            "is_published": False,
            "image": None,
        }]
    }

    response = client.get("/ad/")
    assert response.status_code == 200
    assert response.data == expected_response
