#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append(".")
sys.path.append("..")

import time
import unittest
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

test_target = "fake"
ipaddress = "localhost"
use_realtime = False


class TestURRobot(unittest.TestCase):

    def setUp(self):
        print("### setUp")
        self._r = urrobot(ip=ipaddress, realtime=use_realtime)

    def tearDown(self):
        print("### tearDown")
        self._r.finalize()
        del(self._r)

    def test_singleton(self):
        print("### check sigleton")
        p = urrobot(ip="localhost", realtime=False)
        self.assertEqual(id(self._r), id(p))

    def test_getl(self):
        print("### call getl")
        self.assertIsNotNone(self._r.getl())

    def test_getj(self):
        print("### call getj")
        self.assertIsNotNone(self._r.getj())

    def test_get_force(self):
        if test_target == "real":
            print("### call get_force")
            self.assertIsNotNone(self._r.get_force())

    def test_set_payload(self):
        print("### set payload")
        self.assertTrue(self._r.set_payload(0.5))
        self.assertTrue(self._r.finalize())
        self.assertFalse(self._r.set_payload(0.5))

    def test_async_mode(self):
        print("### start sync_mode")
        self.assertFalse(self._r.is_sync_mode())
        self.assertTrue(self._r.set_sync_mode())
        self.assertTrue(self._r.is_sync_mode())
        self.assertTrue(self._r.set_async_mode())
        self.assertFalse(self._r.is_sync_mode())

    def test_movel(self):
        print("### start movel")
        if test_target == "real":
            self.assertTrue(self._r.set_sync_mode())
        self.assertTrue(self._r.movel(p0))
        self.assertTrue(self._r.movel(p1, v=0.4))
        self.assertTrue(self._r.movel(p2, a=0.4))
        self.assertTrue(self._r.movel(p0, v=0.6, a=0.2))
        self.assertTrue(self._r.finalize())
        self.assertFalse(self._r.movel(p0))

    def test_movej(self):
        print("### start movej")
        if test_target == "real":
            self.assertTrue(self._r.set_sync_mode())
        self.assertTrue(self._r.movej(j0))
        self.assertTrue(self._r.movej(j1, v=0.4))
        self.assertTrue(self._r.movej(j2, a=0.4))
        self.assertTrue(self._r.movej(j0, v=0.6, a=0.2))
        self.assertTrue(self._r.finalize())
        self.assertFalse(self._r.movej(j0))

    def test_movels(self):
        l = list()
        l.append(p0)
        l.append(p1)
        l.append(p2)
        l.append(p0)
        print("### call movels")
        if test_target == "real":
            self.assertTrue(self._r.set_sync_mode())
        self.assertTrue(self._r.movels(l, v=0.6, a=0.4))
        self.assertTrue(self._r.finalize())
        self.assertFalse(self._r.movels(l, v=0.6, a=0.4))

    def test_translate_tool(self):
        if test_target == "real":
            self.assertTrue(self._r.set_sync_mode())
        print("### tool up")
        self.assertTrue(self._r.translate_tool((0, 0, 0.05), a=0.3))
        print("### tool down")
        self.assertTrue(self._r.translate_tool((0, 0, -0.05), v=0.6))
        self.assertTrue(self._r.finalize())
        self.assertFalse(self._r.translate_tool((0, 0, -0.05)))

    def test_freedrive(self):
        print("### start_freedrive()")
        self.assertTrue(self._r.start_freedrive(time=30))
        if test_target == "real":
            time.sleep(20)
        print("### end_freedrive()")
        self.assertTrue(self._r.end_freedrive())
        self.assertTrue(self._r.finalize())
        self.assertFalse(self._r.start_freedrive())
        self.assertFalse(self._r.end_freedrive())

    def test_gripper(self):
        print("### open_gripper()")
        self.assertTrue(self._r.open_gripper())
        if test_target == "real":
            time.sleep(3)
        print("### close_gripper_()")
        self.assertTrue(self._r.close_gripper())
        if test_target == "real":
            time.sleep(3)
        self.assertTrue(self._r.finalize())
        self.assertFalse(self._r.open_gripper())
        self.assertFalse(self._r.close_gripper())

    def test_reallocate_object(self):
        self.assertTrue(self._r.finalize())
        self._r = urrobot(ip="localhost", realtime=False)
        self.assertIsNotNone(self._r)


def test(target="real"):
    global test_target, ipaddress, use_realtime

    if target == "real":
        print("### Test type: real")
        test_target = "real"
        use_realtime = True
        ipaddress = "192.168.1.101"
    else:
        print("### Test type: fake")
        test_target = "fake"
        use_realtime = False
        ipaddress = "localhost"

    unittest.main()


if __name__ == '__main__':
    test(target="fake")
