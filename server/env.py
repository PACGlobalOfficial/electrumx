# Copyright (c) 2016, Neil Booth
#
# All rights reserved.
#
# See the file "LICENCE" for information about the copyright
# and warranty status of this software.

'''Class for handling environment configuration and defaults.'''


from os import environ

from lib.coins import Coin
from lib.util import LoggedClass


class Env(LoggedClass):
    '''Wraps environment configuration.'''

    class Error(Exception):
        pass

    def __init__(self):
        super().__init__()
        coin_name = self.default('COIN', 'Bitcoin')
        network = self.default('NETWORK', 'mainnet')
        self.coin = Coin.lookup_coin_class(coin_name, network)
        self.db_dir = self.required('DB_DIRECTORY')
        self.utxo_MB = self.integer('UTXO_MB', 1000)
        self.hist_MB = self.integer('HIST_MB', 300)
        self.host = self.default('HOST', 'localhost')
        self.reorg_limit = self.integer('REORG_LIMIT', self.coin.REORG_LIMIT)
        self.daemon_url = self.required('DAEMON_URL')
        # Server stuff
        self.tcp_port = self.integer('TCP_PORT', None)
        self.ssl_port = self.integer('SSL_PORT', None)
        if self.ssl_port:
            self.ssl_certfile = self.required('SSL_CERTFILE')
            self.ssl_keyfile = self.required('SSL_KEYFILE')
        self.rpc_port = self.integer('RPC_PORT', 8000)
        self.max_subscriptions = self.integer('MAX_SUBSCRIPTIONS', 10000)
        self.banner_file = self.default('BANNER_FILE', None)
        self.anon_logs = self.default('ANON_LOGS', False)
        self.log_sessions = self.default('LOG_SESSIONS', 3600)
        # The electrum client takes the empty string as unspecified
        self.donation_address = self.default('DONATION_ADDRESS', '')
        self.db_engine = self.default('DB_ENGINE', 'leveldb')
        # Server limits to help prevent DoS
        self.max_send = self.integer('MAX_SEND', 1000000)
        self.max_subs = self.integer('MAX_SUBS', 250000)
        self.max_session_subs = self.integer('MAX_SESSION_SUBS', 50000)
        # IRC
        self.report_tcp_port = self.integer('REPORT_TCP_PORT', self.tcp_port)
        self.report_ssl_port = self.integer('REPORT_SSL_PORT', self.ssl_port)
        self.report_host = self.default('REPORT_HOST', self.host)
        self.irc_nick = self.default('IRC_NICK', None)
        self.irc = self.default('IRC', False)
        # Debugging
        self.force_reorg = self.integer('FORCE_REORG', 0)

    def default(self, envvar, default):
        return environ.get(envvar, default)

    def required(self, envvar):
        value = environ.get(envvar)
        if value is None:
            raise self.Error('required envvar {} not set'.format(envvar))
        return value

    def integer(self, envvar, default):
        value = environ.get(envvar)
        if value is None:
            return default
        try:
            return int(value)
        except:
            raise self.Error('cannot convert envvar {} value {} to an integer'
                             .format(envvar, value))
