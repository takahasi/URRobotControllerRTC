#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
sys.path.append(".")
sys.path.append("..")

from URRobotController import URRobotController as urrobot

__author__ = "Saburo Takahashi"
__copyright__ = "Copyright 2017, Saburo Takahashi"
__license__ = "LGPLv3"

p0 = [0.0902, -0.6437, 0.3808, -3.0154, 0.4781, 0.0619]
p1 = [-0.1929, -0.6305, 0.3072, -2.9113, 1.1439, 0.0399]
p2 = [0.5388, -0.3699, 0.3586, 2.9431, 0.7792, -0.0169]
j0 = [1.5434, -1.1797, 1.207, -1.5047, -1.597, -2.8515]
j1 = [1.1094, -1.1491, 1.3715, -1.7811, -1.595, -2.8519]
j2 = [2.3783, -1.1966, 1.3288, -1.7788, -1.6285, -2.8519]


def test_getl(r):
    print("### call getl")
    print(r.getl())


def test_getj(r):
    print("### call getj")
    print(r.getj())


def test_set_payload(r):
    print("### set payload")
    r.set_payload(0.5)


def test_movel(r):
    print("### start movel")
    r.movel(p0)
    r.movel(p1, v=0.4)
    r.movel(p2, a=0.4)
    r.movel(p0, v=0.6, a=0.2)


def test_movej(r):
    print("### start movej")
    r.movej(j0)
    r.movej(j1, v=0.4)
    r.movej(j2, a=0.4)
    r.movej(j0, v=0.6, a=0.2)


def test_movels(r):
    l = list()
    l.append(p0)
    l.append(p1)
    l.append(p2)
    l.append(p0)
    print("### call movels")
    r.movels(l, v=0.6, a=0.4)


def test_translate_tool(r):
    print("### tool up")
    r.translate_tool((0, 0, 0.05), a=0.3)
    print("### tool down")
    r.translate_tool((0, 0, -0.05), v=0.6)


def test_async_mode(r):
    print("### sync_mode is " + str(r.is_sync_mode()))
    r.set_async_mode()
    print("### sync_mode is " + str(r.is_sync_mode()))
    r.movel(p1, a=0.4)
    while r.is_moving():
        time.sleep(0.1)
    r.set_sync_mode()
    print("### sync_mode is " + str(r.is_sync_mode()))
    r.movel(p0)


def test_freedrive(r):
    print("### start_freedrive()")
    r.start_freedrive(time=30)
    time.sleep(20)
    print("### end_freedrive()")
    r.end_freedrive()


def test_reallocate_object(r):
    r.finalize()
    return urrobot()


def test():

    print("### Start test for URRobotController")
    try:
        r = urrobot()
        r.set_sync_mode()

        test_getl(r)
        test_getj(r)
        test_set_payload(r)
        test_movel(r)
        test_movej(r)
        test_movels(r)

        r = test_reallocate_object(r)

        test_translate_tool(r)
        test_async_mode(r)
        test_freedrive(r)

        r.finalize()

        # checks afetr close
        test_getl(r)
        test_getj(r)
        test_set_payload(r)
        test_movel(r)
        test_movej(r)
        test_movels(r)
        test_translate_tool(r)
        test_async_mode(r)
        test_freedrive(r)

    except urrobot.URxException:
        print("### Failed. URx exception")
    except Exception as e:
        print("### Failed. Exception: " + format(str(e)))
    else:
        print("### Passed.")


if __name__ == '__main__':
    test()
