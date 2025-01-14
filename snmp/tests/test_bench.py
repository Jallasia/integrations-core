# (C) Datadog, Inc. 2018
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

import pytest

from .common import TABULAR_OBJECTS, create_check, generate_instance_config

pytestmark = pytest.mark.usefixtures("dd_environment")


def test_tabular_enforce(benchmark):
    instance = generate_instance_config(TABULAR_OBJECTS)
    check = create_check(instance)

    benchmark(check.check, instance)


def test_tabular_no_enforce(benchmark):
    instance = generate_instance_config(TABULAR_OBJECTS)
    instance["enforce_mib_constraints"] = False
    check = create_check(instance)

    benchmark(check.check, instance)
