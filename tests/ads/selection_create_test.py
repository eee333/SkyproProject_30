import pytest


@pytest.mark.django_db
def test_selection_create(client, member_token, ad):

    data = {
        "name": "Test selection",
        "user": member_token["user_id"],
        "items": [ad.id]
    }
    expected_response = {
        "id": 1,
        "name": "Test selection",
        "user": member_token["user_id"],
        "items": [ad.id]
    }

    response = client.post(
        "/ad/selection/create/",
        data,
        content_type="application/json",
        HTTP_AUTHORIZATION="Bearer " + member_token["access"]
    )

    assert response.status_code == 201
    assert response.data == expected_response
