#!/usr/bin/env python

from unittest import TestCase, main
import tempfile

from knimin.lib.configuration import KniminConfig

class ConfigurationTests(TestCase):
    def setUp(self):
        self.config = tempfile.NamedTemporaryFile()
        self.config.write(test_config)
        self.config.seek(0)
        self.config_fp = self.config.name

    def tearDown(self):
        self.config.close()

    def test_init(self):
        KniminConfig(self.config_fp)

        with self.assertRaises(IOError):
            KniminConfig('does not exist')

    def test_get_main(self):
        config = KniminConfig(self.config_fp)
        self.assertTrue(config.debug)

    def test_get_postgres(self):
        config = KniminConfig(self.config_fp)
        self.assertEqual(config.db_user, 'test')
        self.assertEqual(config.db_password, '')
        self.assertEqual(config.db_database, 'knimin')
        self.assertEqual(config.db_host, 'localhost')
        self.assertEqual(config.db_port, 5432)

    def test_get_tornado(self):
        config = KniminConfig(self.config_fp)
        self.assertEqual(config.http_port, 8888)

test_config = """[main]
debug = True

[postgres]
user = test
password =
database = knimin
host = localhost
port = 5432

[tornado]
port = 8888
"""


if __name__ == '__main__':
    main()
