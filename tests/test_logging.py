# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import logging

from bumpr.log import BumprLogger, DRYRUN, DIFF


def test_bumpr_logger(caplog):
    logger = logging.getLogger(__name__)
    assert isinstance(logger, BumprLogger)
    logger.debug('debug')
    logger.dryrun('dryrun')
    logger.diff('diff')
    logger.info('info')
    logger.warning('warning')
    logger.error('error')
    logger.critical('critical')

    assert caplog.record_tuples == [
        ('test_logging', logging.DEBUG, 'debug'),
        ('test_logging', DRYRUN, 'dryrun'),
        ('test_logging', DIFF, 'diff'),
        ('test_logging', logging.INFO, 'info'),
        ('test_logging', logging.WARNING, 'warning'),
        ('test_logging', logging.ERROR, 'error'),
        ('test_logging', logging.CRITICAL, 'critical'),
    ]
