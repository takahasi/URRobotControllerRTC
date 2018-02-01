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

p0 = [0.4499896971299584, 0.010868012647159229, 0.42582105267981735, 1.9594021624255316, -2.4458589591229, -0.010335049876509362]
p1 = [0.4475587119903788, -0.2827557257978153, 0.42585290981810753, 1.9593681101464684, -2.446007745533187, -0.010273222638616878]
p2 = [0.447637978406461, -0.5683245782151384, 0.4257649741698107, 1.9594274354944727, -2.4459466754895915, -0.010458876339814299]

j0 = [0.2728744447231293, -1.4523699919330042, -1.6953614393817347, -1.575341526662008, 1.5762203931808472, 0.49057650566101074]
j1 = [-0.3515561262713831, -1.6438754240619105, -1.5085118452655237, -1.5705683867083948, 1.5701439380645752, -0.13378745714296514]
j2 = [-0.7486026922809046, -2.151830498372213, -0.8255012671100062, -1.743802849446432, 1.5667164325714111, -0.5313523451434534]

def test_singleton(r):
    print("### check sigleton")
    p = urrobot()
    if id(r) == id(p):
    	print("OK")
    else:
    	print("NG")



def test_getl(r):
    print("### call getl")
    print(r.getl())


def test_getj(r):
    print("### call getj")
    print(r.getj())


def test_get_force(r):
    print("### call get_force")
    print(r.get_force())


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


def test_gripper(r):
    print("### open_gripper()")
    r.open_gripper()
    time.sleep(5)
    print("### close_gripper_()")
    r.close_gripper()
    time.sleep(5)


def test_reallocate_object(r):
    r.finalize()
    return urrobot()


def test():

    print("### Start test for URRobotController")
    try:
        r = urrobot()

        test_singleton(r)

        r.set_sync_mode()

        test_getl(r)
        test_getj(r)
        test_get_force(r)
        test_set_payload(r)
        test_movel(r)
        test_movej(r)
        test_movels(r)

        r = test_reallocate_object(r)

        test_translate_tool(r)
        test_async_mode(r)
        test_freedrive(r)
        test_gripper(r)

        r.finalize()

        # checks afetr close
        test_getl(r)
        test_getj(r)
        test_get_force(r)
        test_set_payload(r)
        test_movel(r)
        test_movej(r)
        test_movels(r)
        test_translate_tool(r)
        test_async_mode(r)
        test_freedrive(r)
        test_gripper(r)

        del(r)

    except urrobot.URxException:
        print("### Failed. URx exception")
    except Exception as e:
        print("### Failed. Exception: " + format(str(e)))
    else:
        print("### Passed.")


if __name__ == '__main__':
    test()
