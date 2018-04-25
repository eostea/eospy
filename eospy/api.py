import json as _json
from .http_client import HTTPClient


class ChainApi(HTTPClient):

    @classmethod
    def local_network(cls, timeout=5, **kwargs):
        return cls(hosts=['http://127.0.0.1:8888'],
                   timeout=timeout, **kwargs)

    def __init__(self, hosts, timeout=5, **kwargs):
        """
        :param hosts: ['']
        :param kwargs:
        """
        super().__init__(hosts, timeout=timeout, **kwargs)

    def get_info(self):
        """
        https://eosio.github.io/eos/group__eosiorpc.html#v1chaingetinfo
        :return:
        """
        return self._exec(
            api='chain',
            endpoint='get_info',
            method=self.GET,
            version='v1'
        )

    def get_block(self, block_num_or_id):
        """
        https://eosio.github.io/eos/group__eosiorpc.html#v1chaingetblock
        :param block_num_or_id:
        :return:
        """
        return self._exec(
            api='chain',
            endpoint='get_block',
            method=self.POST,
            version='v1',
            body={
                'block_num_or_id': block_num_or_id
            }
        )

    def get_account(self, account_name):
        """
        https://eosio.github.io/eos/group__eosiorpc.html#v1chaingetaccount
        :param account_name:
        :return:
        """
        return self._exec(
            api='chain',
            endpoint='get_account',
            method=self.POST,
            version='v1',
            body={
                'account_name': account_name
            }
        )

    def get_code(self, account_name):
        """
        :param account_name:
        :return:
        """
        return self._exec(
            api='chain',
            endpoint='get_code',
            method=self.POST,
            version='v1',
            body={
                'account_name': account_name
            }
        )

    def get_table_rows(self, scope: str, code: str, table: str, json: bool=True, lower_bound: int=None,
                       upper_bound: int=None, limit: int=None):
        """
        https://eosio.github.io/eos/group__eosiorpc.html#v1chaingetcode
        :param scope:
        :param code:
        :param table:
        :param json:
        :param lower_bound:
        :param upper_bound:
        :param limit:
        :return:
        """
        body = {
            'scope': scope,
            'code': code,
            'table': table,
            'json': json
        }
        if lower_bound is not None:
            body['lower_bound'] = lower_bound
        if upper_bound is not None:
            body['upper_bound'] = upper_bound
        if limit is not None:
            body['limit'] = limit

        return self._exec(
            api='chain',
            endpoint='get_table_rows',
            method=self.POST,
            version='v1',
            body=body
        )

    def abi_json_to_bin(self, code, action, args: dict):
        """
        https://eosio.github.io/eos/group__eosiorpc.html#v1chainabijsontobin
        :param code:
        :param action:
        :param args:
        :return:
        """
        body = {
            'code': code,
            'action': action,
            'args': _json.dumps(args)
        }
        return self._exec(
            api='chain',
            endpoint='abi_json_to_bin',
            method=self.POST,
            version='v1',
            body=body
        )

    def abi_bin_to_json(self, code, action, bin_args):
        """
        :param code:
        :param action:
        :param bin_args:
        :return:
        """
        body = {
            'code': code,
            'action': action,
            'binargs': bin_args
        }
        return self._exec(
            api='chain',
            endpoint='abi_bin_to_json',
            method=self.POST,
            version='v1',
            body=body
        )

    def push_transaction(self, ref_block_num: str, ref_block_prefix: str, expiration: str, scope: list,
                         actions: list, signatures: list, authorizations: list):
        """
        :param ref_block_num:
        :param ref_block_prefix:
        :param expiration: datetime  iosformat
        :param scope:
        :param actions:
        :param signatures:
        :param authorizations:
        :return:
        """
        body = {
            'ref_block_num': ref_block_num,
            'ref_block_prefix': ref_block_prefix,
            'expiration': expiration,
            'scope': scope,
            'actions': actions,
            "signatures": signatures,
            "authorizations": authorizations
        }
        return self._exec(
            api='chain',
            endpoint='push_transaction',
            method=self.POST,
            version='v1',
            body=body
        )

    def push_transactions(self, body_list: list):
        """
        https://eosio.github.io/eos/group__eosiorpc.html#v1chainpushtransactions
        :param body_list:
        :return:

        >>> self.push_transactions(
            body_list=[{"ref_block_num":"101",
            "ref_block_prefix":"4159312339",
            "expiration":"2017-09-25T06:28:49",
            "scope":["initb","initc"],
            "actions":[{"code":"currency","type":"transfer","recipients":["initb","initc"],
            "authorization":[{"account":"initb","permission":"active"}],"data":"000000000041934b000000008041934be803000000000000"}],
            "signatures":[],"authorizations":[]}, {"ref_block_num":"101","ref_block_prefix":"4159312339",
            "expiration":"2017-09-25T06:28:49","scope":["inita","initc"],
            "actions":[{"code":"currency","type":"transfer","recipients":["inita","initc"],
            "authorization":[{"account":"inita","permission":"active"}],"data":"000000008040934b000000008041934be803000000000000"}],
            "signatures":[],"authorizations":[]}]'

        )
        """
        return self._exec(
            api='chain',
            endpoint='push_transactions',
            method=self.POST,
            version='v1',
            body=body_list
        )

    def get_required_keys(self, transaction: dict, available_keys: list):
        """
        https://eosio.github.io/eos/group__eosiorpc.html#v1chaingetrequiredkeys
        :param transaction:
        :param available_keys:
        :return:
        """
        body = {
            'transaction': transaction,
            'available_keys': available_keys
        }
        return self._exec(
            api='chain',
            endpoint='get_required_keys',
            method=self.POST,
            version='v1',
            body=body
        )


class WalletApi(HTTPClient):
    def __init__(self, hosts: list, timeout=5, **kwargs):
        super().__init__(hosts, timeout, **kwargs)
        FutureWarning('Incomplete and not tested')

    @classmethod
    def local_network(cls, timeout=5, **kwargs):
        return cls(hosts=['http://127.0.0.1:8888'],
                   timeout=timeout, **kwargs)

    def create(self, wallet_name: str):
        """
        https://eosio.github.io/eos/group__eosiorpc.html#v1walletcreate
        :param wallet_name:
        :return:
        """
        return self._exec(
            api='wallet',
            endpoint='create',
            method=self.POST,
            version='v1',
            body=wallet_name
        )

    def open(self, wallet_name: str):
        """
        https://eosio.github.io/eos/group__eosiorpc.html#v1walletopen
        :param wallet_name:
        :return:
        """
        return self._exec(
            api='wallet',
            endpoint='open',
            method=self.POST,
            version='v1',
            body=wallet_name
        )

    def lock(self, wallet_name: str):
        """
        https://eosio.github.io/eos/group__eosiorpc.html#v1walletlock
        :param wallet_name:
        :return:
        """
        return self._exec(
            api='wallet',
            endpoint='lock',
            method=self.POST,
            version='v1',
            body=wallet_name
        )

    def lock_all(self):
        """
        https://eosio.github.io/eos/group__eosiorpc.html#v1walletlockall
        :return:
        """
        return self._exec(
            api='wallet',
            endpoint='lock_all',
            method=self.POST,
            version='v1',
        )

    def unlock(self, wallet_name: str, password: str):
        """
        :param wallet_name:
        :param password:
        :return:
        """
        return self._exec(
            api='wallet',
            endpoint='unlock',
            method=self.POST,
            version='v1',
            body=[wallet_name, password]
        )

    def import_key(self, wallet_name: str, password: str):
        """
        https://eosio.github.io/eos/group__eosiorpc.html#v1walletimportkey
        :param wallet_name:
        :param password:
        :return:
        """
        return self._exec(
            api='wallet',
            endpoint='import_key',
            method=self.POST,
            version='v1',
            body=[wallet_name, password]
        )

    def list_wallets(self):
        """
        https://eosio.github.io/eos/group__eosiorpc.html#v1walletlist
        :return:
        """
        return self._exec(
            api='wallet',
            endpoint='list_wallets',
            method=self.GET,
            version='v1',
        )

    def list_keys(self):
        """
        https://eosio.github.io/eos/group__eosiorpc.html#v1walletlistkeys
        :return:
        """
        return self._exec(
            api='wallet',
            endpoint='list_keys',
            method=self.GET,
            version='v1',
        )

    def get_public_keys(self):
        """
        https://eosio.github.io/eos/group__eosiorpc.html#v1walletgetpublickeys
        :return:
        """
        return self._exec(
            api='wallet',
            endpoint='get_public_keys',
            method=self.GET,
            version='v1',
        )

    def set_timeout(self, timeout: int):
        """
        https://eosio.github.io/eos/group__eosiorpc.html#v1walletsettimeout
        :param timeout:
        :return:
        """
        return self._exec(
            api='wallet',
            endpoint='set_timeout',
            method=self.POST,
            version='v1',
            body=str(timeout)
        )

    def sign_transaction(self, transaction_list: list):
        """

        :param transaction_list:
        :return:
        """
        raise NotImplementedError()
