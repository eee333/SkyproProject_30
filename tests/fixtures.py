import pytest

@pytest.fixture()
@pytest.mark.django_db
def member_token(client, django_user_model):
    username = "member"
    password = "1234"
    email = "qqq@qqq.qq"

    django_user_model.objects.create_user(
        username=username, password=password, email=email
    )

    response = client.post(
        "/user/token/",
        {"username": username, "password": password},
        format="json"
    )

    return response.data["access"]
