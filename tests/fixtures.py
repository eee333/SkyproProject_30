import pytest

@pytest.fixture()
@pytest.mark.django_db
def member_token(client, django_user_model):
    username = "member"
    password = "1234"
    email = "qqq@qqq.qq"

    user = django_user_model.objects.create_user(
        username=username, password=password, email=email
    )

    response = client.post(
        "/user/token/",
        {"username": username, "password": password},
        format="json"
    )

    return {
        "access": response.data["access"],
        "user_id": user.id
    }
