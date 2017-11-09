# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

from textwrap import dedent

import pytest

from click.testing import CliRunner

from bumpr.log import init_logging


def pytest_configure():
    init_logging()


DEFAULT_VERSION = '1.2.3.dev'


class Workspace(object):
    def __init__(self, root, version):
        self.module_name = 'fake'
        self.root = root
        self.version = version
        self.module = self.write('{0}.py'.format(self.module_name), '''\
            # -*- coding: utf-8 -*-

            __version__ = '{version}'
        ''')
        self.readme = self.write('README', '''\
            README

            Version: {version}
            Lorem ipsum dolor sit amet, consectetur adipisicing elit.
            Non, ad, facilis, vel voluptas fugiat sit debitis iusto
            numquam quasi aliquid cum quod laborum assumenda quia
        ''')

    def write(self, filename, content):
        target = self.root / filename
        with target.open('wb') as f:
            content = dedent(content).format(**self.__dict__)
            f.write(content.encode('utf8'))
        return target

    def mkdir(self, dirname):
        try:
            self.root.mkdir(dirname)
        except FileExistsError as exc:
            pass

    def chdir(self):
        self.root.chdir()

    def bumpr(self, params=''):
        from bumpr.cli import cli
        runner = CliRunner()
        return runner.invoke(cli, params.split())


@pytest.fixture
def workspace(request, tmpdir):
    marker = request.node.get_marker('version')
    version = marker.args[0] if marker else DEFAULT_VERSION
    wksp = Workspace(tmpdir, version)
    wksp.chdir()

    yield wksp
