from urllib.parse import urlencode

from slimpoint.request import validated_request


class Endpoint(object):
    """Class representing a single endpoint of a web service.

    This class provides dynamic URL generation using base URL and paths, and improves
    the expressiveness of code when communicating with web services.

    NOTE: base_url must be provided as an attribute or argument, but path may remain blank.
    """

    _base_url = None
    _path = ''

    def __init__(self, base_url=None, path=None):
        self.base_url = base_url or self._base_url
        self.path = path or self._path

        if not self.base_url:
            raise ValueError('Must provide a base_url in __init__ call or as a class attribute')

    @property
    def url(self):
        """Builds URL structure to an endpoint"""

        url = self.base_url + self.path
        return url

    def get(self, *args, qs_args=None, expect=200, **kwargs):
        return self._request(method='get', *args, qs_args=qs_args, expect=expect, **kwargs)

    def post(self, *args, qs_args=None, expect=200, **kwargs):
        return self._request(method='post', *args, qs_args=qs_args, expect=expect, **kwargs)

    def put(self, *args, qs_args=None, expect=200, **kwargs):
        return self._request(method='put', *args, qs_args=qs_args, expect=expect, **kwargs)

    def patch(self, *args, qs_args=None, expect=200, **kwargs):
        return self._request(method='patch', *args, qs_args=qs_args, expect=expect, **kwargs)

    def delete(self, *args, qs_args=None, expect=200, **kwargs):
        return self._request(method='delete', *args, qs_args=qs_args, expect=expect, **kwargs)

    def _request(self, method, *args, qs_args, **kwargs):
        url = self._url_with_query_string(qs_args) if qs_args else self.url
        resp = validated_request(
            url=url,
            method=method,
            *args,
            **kwargs
        )

        return resp

    def _url_with_query_string(self, qs_args):
        """Appends query string arguments to URL

        Args:
            qa_args (dict): Map of query string args as key-value pairs
        """

        query_string = urlencode(qs_args)
        url_with_qs = f"{self.url}?{query_string}"
        return url_with_qs
