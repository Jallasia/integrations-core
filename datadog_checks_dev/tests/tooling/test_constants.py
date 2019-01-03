# (C) Datadog, Inc. 2018
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import os
import mock

from datadog_checks.dev.tooling.constants import (
    get_agent_release_requirements, get_agent_requirements, get_root, set_root
)


def test_get_agent_release_requirements():
    with mock.patch('datadog_checks.dev.tooling.constants.get_root', return_value='foo'):
        expected = os.path.join('foo', 'requirements-agent-release.txt')
        assert get_agent_release_requirements() == expected


def test_get_agent_requirements():
    with mock.patch('datadog_checks.dev.tooling.constants.get_root', return_value='foo'):
        expected = os.path.join(
            'foo', 'datadog_checks_base', 'datadog_checks', 'base', 'data', 'agent_requirements.in'
        )
        assert get_agent_requirements() == expected


def test_get_root():
    assert get_root() == ''
    set_root('foo')
    assert get_root() == 'foo'