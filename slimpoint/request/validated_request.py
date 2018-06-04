import requests
from requests.exceptions import ConnectionError


from slimpoint.exceptions import SlimpointException


FAILED_RQST_MSG = """Expected a response of {exp}, got {act}\n
                    While trying to: {desc}\n
                    Req URL: {url}\n
                    Req Headers: {hdrs}\n
                    Req Body: {body}\n
                    Response: {resp}"""


def validated_request(method, url, expect, desc='', session=None, *args, **kwargs):
    """Performs HTTP request and validates the response against an expected status code. Shrinks
    code via DRY principle and provides actionable, readable Exceptions when things do not go as
    expected.

    Args:
        session (requests.Session): A session, presumably headers are already in desired state
        method (str): GET, POST, PUT, DELETE, etc.
        url (str): Request URL
        expect (int): Expected status code
        desc (str): Description of what request is attempting to accomplish, e.g. 'Publish an LTK'
        args: Passed through to Request
        kwargs: Passed through to Request

    Returns:
        resp (requests.Response)
    """

    session = session or requests.Session()

    try:
        resp = session.request(method, url=url, *args, verify=True, **kwargs)
    except ConnectionError:
        raise SlimpointException(f'Unable to connect to {url}. Is it available?')

    if resp.status_code != expect:
        raise SlimpointException(
            FAILED_RQST_MSG.format(
                exp=expect,
                act=resp.status_code,
                desc=desc,
                url=url,
                hdrs=session.headers,
                body=resp.request.body,
                resp=resp.text[:500]
            )
        )
    return resp
