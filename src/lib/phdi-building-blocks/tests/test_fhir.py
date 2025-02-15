import io
import pytest
import polling
import requests

from datetime import datetime, timezone
from unittest import mock

from azure.identity import DefaultAzureCredential

from phdi_building_blocks.fhir import (
    get_fhirserver_cred_manager,
    upload_bundle_to_fhir_server,
    export_from_fhir_server,
    _compose_export_url,
    download_from_export_response,
)


@mock.patch("requests.post")
def test_upload_bundle_to_fhir_server(mock_fhir_post):
    upload_bundle_to_fhir_server(
        {
            "resourceType": "Bundle",
            "id": "some-id",
            "entry": [
                {
                    "resource": {"resourceType": "Patient", "id": "pat-id"},
                    "request": {"method": "PUT", "url": "Patient/pat-id"},
                }
            ],
        },
        "some-token",
        "https://some-fhir-url",
    )

    mock_fhir_post.assert_called_with(
        "https://some-fhir-url",
        headers={
            "Authorization": "Bearer some-token",
            "Accept": "application/fhir+json",
            "Content-Type": "application/fhir+json",
        },
        data='{"resourceType": "Bundle", "id": "some-id", "entry": [{"resource": '
        '{"resourceType": "Patient", "id": "pat-id"}, "request": '
        '{"method": "PUT", "url": "Patient/pat-id"}}]}',
    )


@mock.patch.object(DefaultAzureCredential, "get_token")
def test_get_access_token_reuse(mock_get_token):

    mock_access_token = mock.Mock()
    mock_access_token.token = "my-token"
    mock_access_token.expires_on = datetime.now(timezone.utc).timestamp() + 2399

    mock_get_token.return_value = mock_access_token

    fhirserver_cred_manager = get_fhirserver_cred_manager("https://fhir-url")
    token1 = fhirserver_cred_manager.get_access_token()

    # Use the default token reuse tolerance, which is less than
    # the mock token's time to live of 2399
    fhirserver_cred_manager.get_access_token()
    mock_get_token.assert_called_once_with("https://fhir-url/.default")
    assert token1.token == "my-token"


@mock.patch.object(DefaultAzureCredential, "get_token")
def test_get_access_token_refresh(mock_get_token):

    mock_access_token = mock.Mock()
    mock_access_token.token = "my-token"
    mock_access_token.expires_on = datetime.now(timezone.utc).timestamp() + 2399

    mock_get_token.return_value = mock_access_token

    fhirserver_cred_manager = get_fhirserver_cred_manager("https://fhir-url")
    token1 = fhirserver_cred_manager.get_access_token()

    # This time, use a very high token reuse tolerance to
    # force another refresh for the new call
    fhirserver_cred_manager.get_access_token(2500)
    mock_get_token.assert_has_calls(
        [mock.call("https://fhir-url/.default"), mock.call("https://fhir-url/.default")]
    )
    assert token1.token == "my-token"


@mock.patch("requests.get")
def test_export_from_fhir_server(mock_get):
    access_token = "my-token"
    fhir_url = "https://fhir-url"

    poll_step = 0.1
    poll_timeout = 0.5

    mock_export_response = mock.Mock()
    mock_export_response.status_code = 202

    mock_export_response.headers = {"Content-Location": "https://export-download-url"}

    mock_export_download_response_accepted = mock.Mock()
    mock_export_download_response_accepted.status_code = 202

    mock_export_download_response_ok = mock.Mock()
    mock_export_download_response_ok.status_code = 200
    mock_export_download_response_ok.json.return_value = {
        "output": [
            {"type": "Patient", "url": "https://export-download-url/_Patient"},
            {"type": "Observation", "url": "https://export-download-url/_Observation"},
        ]
    }

    mock_get.side_effect = [
        mock_export_response,
        mock_export_download_response_accepted,
        mock_export_download_response_accepted,
        mock_export_download_response_accepted,
        mock_export_download_response_ok,
    ]

    export_from_fhir_server(
        access_token=access_token,
        fhir_url=fhir_url,
        poll_step=poll_step,
        poll_timeout=poll_timeout,
    )

    mock_get.assert_has_calls(
        [
            mock.call(
                f"{fhir_url}/$export",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/fhir+json",
                    "Prefer": "respond-async",
                },
            ),
            mock.call(
                "https://export-download-url",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/fhir+ndjson",
                },
            ),
            mock.call(
                "https://export-download-url",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/fhir+ndjson",
                },
            ),
            mock.call(
                "https://export-download-url",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/fhir+ndjson",
                },
            ),
            mock.call(
                "https://export-download-url",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/fhir+ndjson",
                },
            ),
        ]
    )
    assert mock_get.call_count == 5


@mock.patch("requests.get")
def test_export_from_fhir_server_timeout(mock_get):
    access_token = "my-token"
    fhir_url = "https://fhir-url"

    poll_step = 0.1
    poll_timeout = 0.5

    mock_export_response = mock.Mock()
    mock_export_response.status_code = 202

    mock_export_response.headers = {"Content-Location": "https://export-download-url"}

    mock_export_download_response_accepted = mock.Mock()
    mock_export_download_response_accepted.status_code = 202

    mock_get.side_effect = [
        mock_export_response,
        mock_export_download_response_accepted,
        mock_export_download_response_accepted,
        mock_export_download_response_accepted,
        mock_export_download_response_accepted,
        mock_export_download_response_accepted,
        mock_export_download_response_accepted,
    ]

    with pytest.raises(polling.TimeoutException):
        export_from_fhir_server(
            access_token=access_token,
            fhir_url=fhir_url,
            poll_step=poll_step,
            poll_timeout=poll_timeout,
        )

    assert mock_get.call_count == 7


@mock.patch("requests.get")
def test_export_from_fhir_server_error(mock_get):
    access_token = "my-token"
    fhir_url = "https://fhir-url"

    poll_step = 0.1
    poll_timeout = 0.5

    mock_export_response = mock.Mock()
    mock_export_response.status_code = 202

    mock_export_response.headers = {"Content-Location": "https://export-download-url"}

    mock_export_download_response_error = mock.Mock()
    mock_export_download_response_error.status_code = 500

    mock_get.side_effect = [
        mock_export_response,
        mock_export_download_response_error,
    ]

    with pytest.raises(requests.HTTPError):
        export_from_fhir_server(
            access_token=access_token,
            fhir_url=fhir_url,
            poll_step=poll_step,
            poll_timeout=poll_timeout,
        )

    assert mock_get.call_count == 2


def test_compose_export_url():
    fhir_url = "https://fhir-url"
    assert _compose_export_url(fhir_url) == f"{fhir_url}/$export"
    assert _compose_export_url(fhir_url, "Patient") == f"{fhir_url}/Patient/$export"
    assert (
        _compose_export_url(fhir_url, "Group/group-id")
        == f"{fhir_url}/Group/group-id/$export"
    )
    assert (
        _compose_export_url(fhir_url, "Patient", "2022-01-01T00:00:00Z")
        == f"{fhir_url}/Patient/$export?_since=2022-01-01T00:00:00Z"
    )
    assert (
        _compose_export_url(
            fhir_url, "Patient", "2022-01-01T00:00:00Z", "Patient,Observation"
        )
        == f"{fhir_url}/Patient/$export?_since=2022-01-01T00:00:00Z"
        + "&_type=Patient,Observation"
    )
    assert (
        _compose_export_url(
            fhir_url,
            "Patient",
            "2022-01-01T00:00:00Z",
            "Patient,Observation",
            "some-container",
        )
        == f"{fhir_url}/Patient/$export?_since=2022-01-01T00:00:00Z"
        + "&_type=Patient,Observation&_container=some-container"
    )
    assert (
        _compose_export_url(fhir_url, "Patient", None, "Patient,Observation")
        == f"{fhir_url}/Patient/$export?_type=Patient,Observation"
    )

    with pytest.raises(ValueError):
        _compose_export_url(fhir_url, "InvalidExportScope")


@mock.patch("phdi_building_blocks.fhir._download_export_blob")
def test_download_from_export_response(mock_download_export_blob):
    mock_download_export_blob.side_effect = [
        io.TextIOWrapper(
            io.BytesIO(
                b'{"resourceType": "Patient", "id": "some-id"}\n'
                + b'{"resourceType": "Patient", "id": "some-id2"}\n'
            ),
            encoding="utf-8",
            newline="\n",
        ),
        io.TextIOWrapper(
            io.BytesIO(
                b'{"resourceType": "Observation", "id": "some-id"}\n'
                + b'{"resourceType": "Observation", "id": "some-id2"}\n'
            ),
            encoding="utf-8",
            newline="\n",
        ),
    ]

    export_response = {
        "output": [
            {"type": "Patient", "url": "https://export-download-url/_Patient"},
            {
                "type": "Observation",
                "url": "https://export-download-url/_Observation",
            },
        ]
    }

    for type, output in download_from_export_response(export_response=export_response):
        if type == "Patient":
            assert (
                output.read()
                == '{"resourceType": "Patient", "id": "some-id"}\n'
                + '{"resourceType": "Patient", "id": "some-id2"}\n'
            )
        elif type == "Observation":
            assert (
                output.read()
                == '{"resourceType": "Observation", "id": "some-id"}\n'
                + '{"resourceType": "Observation", "id": "some-id2"}\n'
            )

    mock_download_export_blob.assert_has_calls(
        [
            mock.call(blob_url="https://export-download-url/_Patient"),
            mock.call(blob_url="https://export-download-url/_Observation"),
        ]
    )
