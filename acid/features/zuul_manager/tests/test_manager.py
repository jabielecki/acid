# -*- coding: utf-8 -*-
import unittest
from unittest.mock import patch

import pytest

from ..manager import ZuulManager
from ..exceptions import ZuulManagerConfig
from .fixtures import path_to_test_file


@pytest.mark.unit
class TestZuulConnector(unittest.TestCase):
    def test_raise_when_no_user_key_file(self):
        with self.assertRaises(ZuulManagerConfig):
            ZuulManager(host="host",
                        username="user",
                        user_key_file="there/is/no/file",
                        host_key_file=path_to_test_file("host_key.pub"),
                        tenant="tenant",
                        trigger="trigger",
                        project="project",
                        policy="AutoAddPolicy")

    def test_raise_when_no_host_keys_file(self):
        with self.assertRaises(ZuulManagerConfig):
            ZuulManager(host="host",
                        username="user",
                        user_key_file=path_to_test_file("insecure_user_key"),
                        host_key_file="there/is/no/file",
                        tenant="tenant",
                        trigger="trigger",
                        project="project",
                        policy="AutoAddPolicy")

    def test_can_set_autoadd_policy(self):
        ZuulManager(host="host",
                    username="user",
                    user_key_file=path_to_test_file("insecure_user_key"),
                    host_key_file=path_to_test_file("host_key.pub"),
                    tenant="tenant",
                    trigger="trigger",
                    project="project",
                    policy="AutoAddPolicy")

    def test_can_set_reject_policy(self):
        ZuulManager(host="host",
                    username="user",
                    user_key_file=path_to_test_file("insecure_user_key"),
                    host_key_file=path_to_test_file("host_key.pub"),
                    tenant="tenant",
                    trigger="trigger",
                    project="project",
                    policy="RejectPolicy")

    def test_raise_when_try_to_set_not_exists_policy(self):
        with self.assertRaises(ZuulManagerConfig):
            ZuulManager(host="host",
                        username="user",
                        user_key_file=path_to_test_file("insecure_user_key"),
                        host_key_file=path_to_test_file("host_key.pub"),
                        tenant="tenant",
                        trigger="trigger",
                        project="project",
                        policy="no-policy")

    @patch.object(ZuulManager, '_run_command')
    def test_enqueue_generate_correct_command(self, run_command):
        zuul = ZuulManager(host="host",
                           username="user",
                           user_key_file=path_to_test_file("insecure_user_key"),
                           host_key_file=path_to_test_file("host_key.pub"),
                           tenant="tenant",
                           trigger="trigger",
                           project="project",
                           policy="AutoAddPolicy")
        zuul.enqueue(pipeline="periodic-nightly", branch="master")

        run_command.assert_called_with(
            'zuul enqueue-ref --tenant tenant --trigger trigger --pipeline '
            'periodic-nightly --project project --ref refs/head/master '
            '> /dev/null 2>&1 &')

    @patch.object(ZuulManager, '_run_command')
    def test_dequeue_generate_correct_command(self, run_command):
        zuul = ZuulManager(host="host",
                           username="user",
                           user_key_file=path_to_test_file("insecure_user_key"),
                           host_key_file=path_to_test_file("host_key.pub"),
                           tenant="tenant",
                           trigger="trigger",
                           project="project",
                           policy="AutoAddPolicy")
        zuul.dequeue(pipeline="periodic-nightly", branch="master")

        run_command.assert_called_with(
            'zuul dequeue --tenant tenant --pipeline periodic-nightly '
            '--project project --ref refs/head/master > /dev/null 2>&1 &')

    @patch.object(ZuulManager, '_run_command')
    def test_enqueue_correct_escape_insecure_args(self, run_command):
        zuul = ZuulManager(host="host",
                           username="user",
                           user_key_file=path_to_test_file("insecure_user_key"),
                           host_key_file=path_to_test_file("host_key.pub"),
                           tenant="TENANT",
                           trigger="TRIGGER",
                           project="PROJECT",
                           policy="AutoAddPolicy")
        zuul.enqueue(pipeline="periodic`who`", branch="master???*")

        run_command.assert_called_with(
            'zuul enqueue-ref --tenant TENANT '
            '--trigger TRIGGER --pipeline \'periodic`who`\' --project PROJECT '
            '--ref \'refs/head/master???*\' > /dev/null 2>&1 &')

    @patch.object(ZuulManager, '_run_command')
    def test_dequeue_correct_escape_insecure_args(self, run_command):
        zuul = ZuulManager(host="host",
                           username="user",
                           user_key_file=path_to_test_file("insecure_user_key"),
                           host_key_file=path_to_test_file("host_key.pub"),
                           tenant="TENANT",
                           trigger="TRIGGER",
                           project="PROJECT",
                           policy="AutoAddPolicy")
        zuul.dequeue(pipeline="rm -r /", branch="master*/~")

        run_command.assert_called_with(
            'zuul dequeue --tenant TENANT --pipeline \'rm -r /\' --project '
            'PROJECT --ref \'refs/head/master*/~\' > /dev/null 2>&1 &')