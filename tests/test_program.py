# -*- coding: utf-8 -*-

import os


def test_that_program_can_be_executed():
    exit_status = os.system("cro.schedule --help")
    assert exit_status == 0
