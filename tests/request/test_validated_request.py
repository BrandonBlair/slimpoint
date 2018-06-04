from requests import Session

import responses
from responses import RequestsMock, GET

from pytest import raises

from slimpoint.request import validated_request
from slimpoint.exceptions import SlimpointException


success_status = 200
fail_status = 500
test_url = 'http://test.url'


def test_validated_req():
    sessn = Session()

    # Successful
    with RequestsMock() as response1:
        response1.add(GET, url=test_url, status=success_status)
        resp = validated_request(
            session=sessn,
            method='get',
            url=test_url,
            expect=success_status
        )
        assert resp.status_code == success_status

    # Fail Status
    with RequestsMock() as response2:
        response2.add(GET, url=test_url, status=fail_status)
        with raises(SlimpointException) as failed_req_exc:
            resp = validated_request(
                session=sessn,
                method='get',
                url=test_url,
                expect=success_status
            )
        assert (f'Expected a response of {success_status}, got {fail_status}' in
                str(failed_req_exc.value))


@responses.activate
def test_cannot_connect():
    sessn = Session()
    with raises(SlimpointException) as cant_connect_exc:
        validated_request(
            session=sessn,
            method='get',
            url=test_url,
            expect=success_status
        )
        assert 'Unable to connect' in str(cant_connect_exc.value)
