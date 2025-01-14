import io
import logging

from FhirServerExport import main
from phdi_building_blocks.fhir import AzureFhirserverCredentialManager

from unittest import mock

ENVIRONMENT = {
    "FHIR_URL": "https://some-fhir-url",
    "FHIR_EXPORT_POLL_INTERVAL": "0.1",
    "FHIR_EXPORT_POLL_TIMEOUT": "1",
}


@mock.patch("FhirServerExport.fhir.download_from_export_response")
@mock.patch("FhirServerExport.fhir.export_from_fhir_server")
@mock.patch.object(AzureFhirserverCredentialManager, "get_access_token")
@mock.patch.dict("os.environ", ENVIRONMENT)
def test_main(mock_get_access_token, mock_export, mock_download):
    logging.basicConfig(level=logging.DEBUG)
    req = mock.Mock()
    req.params = {
        "export_scope": "",
        "since": "",
        "type": "",
    }

    mock_access_token = mock.Mock()
    mock_access_token.token = "some-token"
    mock_get_access_token.return_value = mock_access_token

    export_return_value = {
        "output": [
            {"type": "Patient", "url": "https://some-export-url/_Patient"},
            {"type": "Observation", "url": "https://some-export-url/_Observation"},
        ]
    }

    mock_export.return_value = export_return_value

    patient_response = io.TextIOWrapper(
        io.BytesIO(
            b'{"resourceType": "Patient", "id": "patient-id1"}\n'
            + b'{"resourceType": "Patient", "id": "patient-id2"}'
        ),
        encoding="utf-8",
        newline="\n",
    )
    patient_response.seek(0)

    observation_response = io.TextIOWrapper(
        io.BytesIO(
            b'{"resourceType": "Observation", "id": "observation-id1"}\n'
            + b'{"resourceType": "Observation", "id": "observation-id2"}'
        ),
        encoding="utf-8",
        newline="\n",
    )
    observation_response.seek(0)

    main(req)

    mock_export.assert_called_with(
        access_token="some-token",
        fhir_url="https://some-fhir-url",
        export_scope="",
        since="",
        resource_type="",
        container="fhir-exports",
        poll_step=0.1,
        poll_timeout=1.0,
    )
