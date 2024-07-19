import pytest
from django.urls import reverse
from rest_framework import status

@pytest.mark.django_db
def test_api_parse_succeeds(client):
    address_string = '123 main st chicago il'
    response = client.get(reverse('address-parse'), {'address': address_string})
    
    # Status code assertion
    assert response.status_code == status.HTTP_200_OK

    # Ensure all expected keys are in the response
    expected_keys = {'input_string', 'address_components', 'address_type'}
    assert expected_keys.issubset(response.data)

    # Ensure the input string matches
    assert response.data['input_string'] == address_string

    # Ensure address components are correctly parsed
    address_components = response.data['address_components']
    assert isinstance(address_components, dict)
    assert 'AddressNumber' in address_components
    assert address_components['AddressNumber'] == '123'
    assert 'StreetName' in address_components
    assert address_components['StreetName'] == 'main'
    assert 'PlaceName' in address_components
    assert address_components['PlaceName'] == 'chicago'
    assert 'StateName' in address_components
    assert address_components['StateName'] == 'il'

    # Ensure address type is a string
    assert isinstance(response.data['address_type'], str)


@pytest.mark.django_db
def test_api_parse_raises_error(client):
    address_string = '123 main st chicago il 123 main st'
    response = client.get(reverse('address-parse'), {'address': address_string})
    
    # Status code assertion
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Ensure 'detail' key is in the response
    assert 'detail' in response.data
    assert response.data['detail'] == 'Invalid address: contains repeated components'



