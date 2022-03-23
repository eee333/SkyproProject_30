import pytest


@pytest.mark.django_db
def test_ad_create(client, member_token):

    data = {
        "name": "Test name 2",
        "price": "200",
        "description": "Test description"}
    expected_response = {
        "id": 1,
        "name": "Test name 2",
        "price": "200",
        "description": "Test description",
        "user": None,
        "category": None,
        "is_published": False,
        "image": None
    }

    response = client.post(
        "/ad/create/",
        data,
        content_type="application/json",
        HTTP_AUTHORIZATION="Bearer " + member_token["access"]
    )

    assert response.status_code == 201
    assert response.data == expected_response
