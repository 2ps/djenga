import os
from djenga.test import IntegrationTest
from djenga.core import ConfigBunch


class EnvTest(IntegrationTest):
    def test_01(self):
        config = ConfigBunch(
            'env_test_01.yml',
            'env_test_02.yml',
        )
        self.assert_equal(config.dbs.default.username, 'user')
        self.assert_equal(config.dbs.default.host, 'localhost')
        self.assert_equal(config.dbs.default.port, 3306)
        self.assert_equal(config.dbs.default.password, 'my secret value')
        os.environ['DBS_DEFAULT_PASSWORD'] = 'overridden secret value'
        env = config.env()
        self.assert_equal(env('DBS_DEFAULT_PASSWORD'), 'overridden secret value')
        self.assert_equal(env('DBS_DEFAULT_HOST'), 'localhost')
        value = config.get('dbs.default.not_there', 'default')
        self.assert_equal(value, 'default')
        value = config.setdefault('dbs.default.not_there', 'new value')
        self.assert_equal(value, 'new value')
        config['dbs.default.second'] = 'old value'
        self.assert_equal(config.dbs.default.second, 'old value')
        value = config.setdefault('dbs.default.second', 'new value')
        self.assert_equal(value, 'old value')
