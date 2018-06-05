from pytest import raises

from requests import Session

from responses import RequestsMock, GET, POST, PUT, PATCH, DELETE

from slimpoint.service import Endpoint


test_base_url = 'https://notimportant.doesnotexist'
success_status = 200
fail_status = 500
test_url = 'http://test.url'
test_header = {'TEST': 'UNIMPORTANT'}


def test_can_create_endpoint():
    # Base URL provided
    test_endpoint = Endpoint(base_url=test_base_url)
    assert test_endpoint.base_url == test_base_url

    # No path should be added, so url should just be base_url
    assert test_endpoint.url == test_base_url

    # Base URL baked-in as class attribute
    class FakeEndpoint(Endpoint):
        _base_url = test_base_url

    test_endpoint = FakeEndpoint()
    assert test_endpoint.base_url == test_base_url

    # Path is automatically appended to base_url to form URL
    stub_path = '/stub'

    class FakeEndpointWithPath(Endpoint):
        _base_url = test_base_url
        _path = stub_path

    test_endpoint = FakeEndpointWithPath()
    assert test_endpoint.url == f'{test_base_url}{stub_path}'

    # Base URL not provided
    with raises(ValueError) as no_base_exc:
        Endpoint()
    assert 'Must provide a base_url' in str(no_base_exc.value)


def test_endpoint_requests():
    sessn = Session()

    test_endpoint = Endpoint(base_url=test_base_url)

    # GET
    with RequestsMock() as get_resp:
        sessn.headers.update(test_header)  # Used to validate the session we passed in was used

        get_resp.add(GET, url=test_endpoint.url, status=success_status)

        resp = test_endpoint.get(session=sessn)
        assert resp.status_code == success_status
        assert resp.request.headers == sessn.headers

    # POST
    with RequestsMock() as post_rep:
        post_rep.add(POST, url=test_endpoint.url, status=success_status)

        resp = test_endpoint.post()
        assert resp.status_code == success_status

    # PUT
    with RequestsMock() as put_resp:
        put_resp.add(PUT, url=test_endpoint.url, status=success_status)

        resp = test_endpoint.put()
        assert resp.status_code == success_status

    # PATCH
    with RequestsMock() as patch_resp:
        patch_resp.add(PATCH, url=test_endpoint.url, status=success_status)

        resp = test_endpoint.patch()
        assert resp.status_code == success_status

    # DELETE
    with RequestsMock() as del_resp:
        del_resp.add(DELETE, url=test_endpoint.url, status=success_status)

        resp = test_endpoint.delete()
        assert resp.status_code == success_status


def test_endpoint_with_query_string():
    sessn = Session()
    test_endpoint = Endpoint(base_url=test_base_url)

    arg_key = 'arg_key'
    arg_value = 'arg_value'
    url_w_args = f'{test_endpoint.url}?{arg_key}={arg_value}'

    with RequestsMock() as get_resp:
        get_resp.add(GET, url=url_w_args, status=success_status)

        resp = test_endpoint.get(session=sessn, qs_args={arg_key: arg_value})
        assert resp.request.url.replace('/?', '?') == url_w_args  # Account for resp URL format
