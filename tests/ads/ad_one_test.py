import pytest

from ads.serializers import AdSerializer


@pytest.mark.django_db
def test_ad_one(client, member_token, ad):

    expected_response = AdSerializer(ad).data

    response = client.get(f"/ad/{ad.pk}/", HTTP_AUTHORIZATION="Bearer " + member_token["access"])
    assert response.status_code == 200
    assert response.data == expected_response
