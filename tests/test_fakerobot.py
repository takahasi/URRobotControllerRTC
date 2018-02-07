#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append(".")
sys.path.append("..")

import unittest
import test_robot


__author__ = "Saburo Takahashi"
__copyright__ = "Copyright 2017, Saburo Takahashi"
__license__ = "LGPLv3"


class TestURRobotFake(test_robot.TestURRobot):
    use_robot = False


def test():
    unittest.main(verbosity=2)


if __name__ == '__main__':
    test()
