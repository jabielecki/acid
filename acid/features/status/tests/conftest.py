# -*- coding: utf-8 -*-
import os
import json
from random import randint

import pytest

from flask import current_app

from ..model import Buildset, Job, Queue, TimeTracker


@pytest.fixture
def time_tracker():
    return TimeTracker(start=randint(1000, 100000),  # noqa
                       elapsed=randint(1000, 100000),  # noqa
                       remaining=randint(1000, 100000),  # noqa
                       estimated=randint(1000, 100000))  # noqa


@pytest.fixture
def job():
    return Job(name="test_name", result="test_result",
               url="http://fake_url", report_url="http://fake_url",
               canceled=False, voting=False, retry=False,
               worker={"name": "fake_name"}, zuul_url="http://zuul_url",
               time_tracker=time_tracker())


@pytest.fixture
def jobs():
    def jobs(count):
        return [job() for _ in range(count)]
    return jobs


@pytest.fixture
def buildset():
    return Buildset(name="test_name", buildset_id="12345,6", jobs=[],
                    enqueue_time=randint(1000, 100000),  # noqa
                    owner={'name': 'John smith'}, ref='12345',
                    review_url="http://fake_url")


@pytest.fixture
def status_request(mocker):
    current_dir = os.path.dirname(os.path.realpath(__file__))

    def _status_request(filename=None, status_code=200):
        filename = filename or current_app.config['zuul']['status_endpoint']
        result = mocker.MagicMock()
        result.status_code = status_code
        with open(f'{current_dir}/static/{filename}.json') as json_data:
            result.json = mocker.MagicMock(return_value=json.load(json_data))
        return mocker.MagicMock(return_value=result)

    return _status_request


@pytest.fixture
def load_status_data():
    def _load_status_data(name):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        with open(f'{current_dir}/static/{name}.json', "r") as data:
            return json.load(data)
    return _load_status_data


@pytest.fixture
def queue(load_status_data):
    resources = load_status_data(
        name='status_pipeline_with_couple_buildsets_in_queue')
    queue = Queue.create(
        resources['pipelines'][0]['change_queues'][0], 'http://zuul_url')
    return queue
