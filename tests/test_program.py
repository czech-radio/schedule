# -*- coding: utf-8 -*-

import os


def test_arrange_program_entrypoint():
    exit_status = os.system("cro.schedule --help")
    assert exit_status == 0
