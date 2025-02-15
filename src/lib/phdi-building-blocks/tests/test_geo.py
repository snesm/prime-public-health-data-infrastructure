import json
import pathlib
import copy
from unittest import mock

from smartystreets_python_sdk.us_street.candidate import Candidate
from smartystreets_python_sdk.us_street.metadata import Metadata
from smartystreets_python_sdk.us_street.components import Components

from phdi_building_blocks.geo import (
    geocode,
    geocode_patient_address,
    GeocodeResult,
)


def test_geocode():
    """
    Make sure to return the correct dict attribs from the SmartyStreets
    response object on a successful call
    """

    # SmartyStreets fills in a request object inline, so let's fake that
    candidate = Candidate({})
    candidate.delivery_line_1 = "123 FAKE ST"
    candidate.metadata = Metadata(
        {
            "latitude": 45.123,
            "longitude": -70.234,
            "county_fips": "36061",
            "county_name": "New York",
            "precision": "Zip9",
        }
    )

    candidate.components = Components(
        {"zipcode": "10001", "city_name": "New York", "state_abbreviation": "NY"}
    )

    # Provide a function that adds results to the existing object
    def fill_in_result(*args, **kwargs):
        args[0].result = [candidate]

    client = mock.Mock()
    client.send_lookup.side_effect = fill_in_result

    assert {
        "address": ["123 FAKE ST"],
        "city": "New York",
        "state": "NY",
        "lat": 45.123,
        "lng": -70.234,
        "county_fips": "36061",
        "county_name": "New York",
        "zipcode": "10001",
        "precision": "Zip9",
    } == geocode(client, "123 Fake St, New York, NY 10001")

    client.send_lookup.assert_called()


def test_failed_geocode():
    """If it doesn't fill in results, return None"""
    assert geocode(mock.Mock(), "123 Nowhere St, Atlantis GA") is None


@mock.patch("phdi_building_blocks.geo.geocode")
def test_geocode_patient_address(patched_geocoder):
    raw_bundle = json.load(
        open(pathlib.Path(__file__).parent / "assets" / "patient_bundle.json")
    )
    geocoded_response = GeocodeResult(
        address=["123 FAKE ST"],
        city="New York",
        state="NY",
        lat=45.123,
        lng=-70.234,
        county_fips="36061",
        county_name="New York",
        zipcode="10001",
        precision="Zip9",
    )

    standardized_bundle = copy.deepcopy(raw_bundle)
    patient = standardized_bundle["entry"][1]["resource"]
    address = patient["address"][0]
    address["line"] = geocoded_response.address
    address["city"] = geocoded_response.city
    address["state"] = geocoded_response.state
    address["postalCode"] = geocoded_response.zipcode
    address["extension"] = []
    address["extension"].append(
        {
            "url": "http://hl7.org/fhir/StructureDefinition/geolocation",
            "extension": [
                {"url": "latitude", "valueDecimal": geocoded_response.lat},
                {"url": "longitude", "valueDecimal": geocoded_response.lng},
            ],
        }
    )

    patient["extension"] = []
    patient["extension"].append(
        {
            "url": "http://usds.gov/fhir/phdi/StructureDefinition/address-was-standardized",  # noqa
            "valueBoolean": True,
        }
    )
    patched_geocoder.return_value = geocoded_response

    assert geocode_patient_address(raw_bundle, mock.Mock()) == standardized_bundle
