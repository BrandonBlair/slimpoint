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

    def get(self, *args, expect=200, **kwargs):
        return self._request(method='get', *args, expect=expect, **kwargs)

    def post(self, *args, expect=200, **kwargs):
        return self._request(method='post', *args, expect=expect, **kwargs)

    def put(self, *args, expect=200, **kwargs):
        return self._request(method='put', *args, expect=expect, **kwargs)

    def patch(self, *args, expect=200, **kwargs):
        return self._request(method='patch', *args, expect=expect, **kwargs)

    def delete(self, *args, expect=200, **kwargs):
        return self._request(method='delete', *args, expect=expect, **kwargs)

    def _request(self, method, *args, **kwargs):
        resp = validated_request(
            url=self.url,
            method=method,
            *args,
            **kwargs
        )

        return resp
