import pprint
import logging
import os
from datetime import datetime
from unittest import mock

import pytest
import pytz

from latigo.utils import (
    merge,
    load_yaml,
    save_yaml,
    parse_event_hub_connection_string,
    datetime_to_utc_as_str, local_datetime_to_utc_as_str)

logger = logging.getLogger("latigo.utils")


# TODO: Actually manage this
writable_working_dir = "/tmp/"


def merge_test_worker(skip, expected):
    # fmt: off
    a={
        'both':'AAAA',
        'only_a':'AAAA',
        'both_none':None,
        'only_a_none':None,
    }
    b={
        'both':'BBBB',
        'only_b':'BBBB',
        'both_none':None,
        'only_b_none':None,
    }
    # fmt: on
    # print("a:")
    # print(pprint.pformat(a))
    # print("b:")
    # print(pprint.pformat(b))
    merge(a, b, skip)
    # print("res:")
    # print(pprint.pformat(b))
    assert b == expected


def test_merge_with_skip_none():
    # fmt: off
    expected={
        'both':'AAAA',
        'only_a':'AAAA',
        'only_b':'BBBB',
        'both_none':None,
        'only_b_none':None,
    }
    # fmt: on
    merge_test_worker(True, expected)
    return True


def test_merge_without_skip_none():
    # fmt: off
    expected={
        'both':'AAAA',
        'only_a':'AAAA',
        'only_b':'BBBB',
        'both_none':None,
        'only_a_none':None,
        'only_b_none':None,
    }
    # fmt: on
    merge_test_worker(False, expected)
    return True


def test_save_load_yaml():
    config_filename = writable_working_dir + "test_config_save_load.yaml"
    # fmt: off
    original_config={
        'both':'AAAA',
        'only_a':'AAAA',
        'both_none':None,
        'only_a_none':None,
    }
    # fmt: on
    save_yaml(config_filename, original_config, True)
    assert os.path.exists(config_filename)
    config, failure = load_yaml(config_filename, True)
    if os.path.exists(config_filename):
        os.remove(config_filename)
    assert failure == None
    assert original_config == config


@pytest.mark.skip
def test_load_config():
    config_filename = writable_working_dir + "test_config_load_config.yaml"
    # fmt: off
    original_config={
        'both':'FILE',
        'only_file':'FILE',
        'both_none':None,
        'only_file_none':None,
    }
    overlay_config={
        'both':'OVERLAY',
        'only_overlay':'OVERLAY',
        'both_none':None,
        'only_overlay_none':None,
    }
    expected={
        'both': 'OVERLAY',
        'both_none': None,
        'only_file': 'FILE',
        'only_file_none': None,
        'only_overlay': 'OVERLAY',
    }
    # fmt: on
    save_yaml(config_filename, original_config)
    config = load_config(config_filename, overlay_config, True)
    # print("loaded config:")
    # print(pprint.pformat(config))
    if os.path.exists(config_filename):
        os.remove(config_filename)
    assert config == expected


def test_parse_event_hub_connection_string():
    input = "Endpoint=sb://some.test.domain.com/;SharedAccessKeyName=some-key-name;SharedAccessKey=SomeKindOfKey2345=;EntityPath=some-topic"
    output = parse_event_hub_connection_string(input)
    # logger.info("RESULT:")
    # logger.info(pprint.pformat(output))
    output_expected = {
        "endpoint": "some.test.domain.com",
        "entity_path": "some-topic",
        "shared_access_key": "SomeKindOfKey2345=",
        "shared_access_key_name": "some-key-name",
    }
    assert output == output_expected


EXPECTED_DATETIME = "2020-04-03T05:00:07.086149+00:00"
NOW_UTC_DATETIME = "2020-04-03T10:00:00.000000"


@pytest.mark.parametrize(
    "target, now_resp, is_pytz",
    [
        ("2020-04-03T05:00:07.086149+00:00", "2020-04-03T04:00:00.000000", False),
        ("2020-04-03T05:00:07.086149", "2020-04-03T14:00:00.000000", False),
        ("2020-04-03T08:00:07.086149+03:00", "2020-04-03T13:00:00.000000", False),
        ("2020-04-02T23:00:07.086149-06:00", "2020-04-03T04:00:00.000000", False),
        ("2020-04-02T23:00:07.086149-06:00", "", True),
    ],
)
@mock.patch("latigo.utils.datetime.datetime")
def test_local_datetime_to_utc_as_str(datetime_mocked, target: str, now_resp: str, is_pytz: bool):
    target = datetime.fromisoformat(target)

    if is_pytz:
        target = target.astimezone(pytz.utc)
    else:
        datetime_mocked.utcnow.return_value = datetime.fromisoformat(NOW_UTC_DATETIME)
        datetime_mocked.now.return_value = datetime.fromisoformat(now_resp)

    res = local_datetime_to_utc_as_str(target)
    assert res == EXPECTED_DATETIME


@pytest.mark.parametrize(
    "target, is_pytz",
    [
        ("2020-04-03T05:00:07.086149+00:00", False),
        ("2020-04-03T05:00:07.086149", False),
        ("2020-04-03T10:00:07.086149+05:00", False),
        ("2020-04-02T23:00:07.086149-06:00", False),
        ("2020-04-02T23:00:07.086149-06:00", True),
    ],
)
def test_datetime_to_utc_as_str(target: str, is_pytz: bool):
    target = datetime.fromisoformat(target)

    if is_pytz:
        target = target.astimezone(pytz.utc)

    res = datetime_to_utc_as_str(target)
    assert res == EXPECTED_DATETIME
