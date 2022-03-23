import pytest


@pytest.mark.django_db
def test_user_create(client):

    data = {
        "username": "member",
        "password": "1234",
        "email": "qqq@qqq.qq",
        "birth_date": "1995-01-01"
    }

    response = client.post(
        "/user/create/",
        data,
        content_type="application/json"
    )

    assert response.status_code == 201


@pytest.mark.django_db
def test_wrong_user_create(client):

    data = {
        "username": "member",
        "password": "1234",
        "email": "qqq@qqq.qq",
        "birth_date": "2018-01-01"
    }

    response = client.post(
        "/user/create/",
        data,
        content_type="application/json"
    )

    assert response.status_code == 400
