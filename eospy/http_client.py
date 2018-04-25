import json
from abc import abstractmethod
from requests.sessions import Session
from urllib.parse import urlparse, ParseResult
from requests.exceptions import BaseHTTPError, RequestException
from .exceptions import ParameterError, HostConnectionError
from .log import logger


session = None


def get_session() -> Session:
    global session
    if not session:
        session = Session()
    return session


class HTTPClient:

    GET = 'GET'
    POST = 'POST'

    def __init__(self, hosts=None, timeout=5, **kwargs):
        """
        :param hosts: ['']
        :param kwargs:
        """
        self.client = get_session()
        if isinstance(hosts, str):
            self.hosts = [hosts]
        self.hosts = hosts
        self.host_index = 0
        self.timeout = timeout
        self.previous_available_host_index = 0

    @classmethod
    @abstractmethod
    def local_network(cls):
        pass

    def _check_host(self) -> bool:
        """
        :return:
        """
        if isinstance(self.hosts, list):
            for h in self.hosts:
                p: ParseResult = urlparse(h)
                if not (p.scheme in ['http', 'https'] and p.path == '/'):
                    return False
        elif isinstance(self.hosts, str):
            p: ParseResult = urlparse(self.hosts)
            if not (p.scheme in ['http', 'https'] and p.path == '/'):
                return False
        else:
            return False
        return True

    @property
    def current_host(self) -> str:
        """
        :return:
        """
        return self.hosts[self.host_index]

    def _next_host(self) -> str:
        """
        :return:
        """
        if self.host_index >= len(self.hosts) - 1:
            self.host_index = 0
        else:
            self.host_index += 1
        return self.hosts[self.host_index]

    def _is_last_host(self):
        if self.host_index == len(self.hosts) - 1:
            return True
        return False

    def _exec(self, api: str, endpoint: str, method: str, version: str = 'v1',
              body: dict or list or str=None, params: dict=None):
        """
        :param api: one of ['chain', 'wallet']
        :param endpoint:
        :param body:
        :param method:
        :return:
        """
        url = self.current_host + version + '/' + api + '/' + endpoint
        if method.upper() not in [self.GET, self.POST]:
            raise ParameterError('Method not supported: {}'.format(method))
        try:
            resp = self.client.request(method=method, url=url,
                                       params=params, data=json.dumps(body) if body is not None else None,
                                       timeout=self.timeout)
            self.previous_available_host_index = self.host_index
            if resp.status_code in [200, 500, 404]:
                return resp.json()
            return dict()
        except (RequestException, BaseHTTPError) as err:
            logger.warning(err)
            logger.debug(f'Switched to {self._next_host()}')
            if self.host_index == self.previous_available_host_index:
                raise HostConnectionError('No connectable server')
            return self._exec(api, endpoint, method, version, body, params)
