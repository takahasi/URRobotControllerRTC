#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urx
import logging

__author__ = "Saburo Takahashi"
__copyright__ = "Copyright 2017, Saburo Takahashi"
__license__ = "LGPLv3"


class URRobotController():
    # Exceptions
    URxException = urx.urrobot.RobotException

    # Private constant value
    _DEFAULT_ACC = 0.4
    _DEFAULT_VEL = 0.5

    # Private member
    _robot = None
    _sync_mode = False

    def __init__(self, ip="192.168.1.101", realtime=False):
        logging.basicConfig(format='%(asctime)s:%(levelname)s: %(message)s',
                            level=logging.INFO)

        logging.info("Create URRobotController IP: " + ip + " RTPort: " + str(realtime))
        self._robot = urx.Robot(ip, use_rt=realtime)
        self._robot.set_tcp((0, 0, 0, 0, 0, 0))
        self._robot.set_payload(0, (0, 0, 0))

    def __del__(self):
        self.finalize()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.finalize()

    def _get_acc_vel(self, a, v):
        if not a:
            acc = self._DEFAULT_ACC
        else:
            acc = a
        if not v:
            vel = self._DEFAULT_VEL
        else:
            vel = v
        return acc, vel

    def finalize(self):
        if self._robot:
            self._robot.close()
            self._robot = None

    def set_payload(self, weight, vector=(0, 0, 0)):
        if self._robot:
            # set payload in kg & cog
            self._robot.set_payload(weight, vector)

    def is_moving(self):
        if self._robot:
            return self._robot.is_running() and self._robot.is_program_running()
        else:
            return False

    def set_sync_mode(self):
        self._sync_mode = True

    def set_async_mode(self):
        self._sync_mode = False

    def is_sync_mode(self):
        return self._sync_mode

    def movel(self, pos, a=None, v=None):
        if self._robot:
            ac, vl = self._get_acc_vel(a, v)
            self._robot.movel(pos, acc=ac, vel=vl, wait=self._sync_mode)

    def movej(self, joints, a=None, v=None):
        if self._robot:
            ac, vl = self._get_acc_vel(a, v)
            self._robot.movej(joints, acc=ac, vel=vl, wait=self._sync_mode)

    def movels(self, poslist, a=None, v=None):
        if self._robot:
            ac, vl = self._get_acc_vel(a, v)
            self._robot.movels(poslist, acc=ac, vel=vl, wait=self._sync_mode)

    def translate_tool(self, vec, a=None, v=None):
        if self._robot:
            ac, vl = self._get_acc_vel(a, v)
            self._robot.translate_tool(vec, acc=ac, vel=vl, wait=self._sync_mode)

    def getl(self):
        if self._robot:
            return self._robot.getl()
        else:
            return (0, 0, 0, 0, 0, 0)

    def getj(self):
        if self._robot:
            return self._robot.getj()
        else:
            return (0, 0, 0, 0, 0, 0)

    def start_freedrive(self, time=60):
        if self._robot:
            self._robot.set_freedrive(True, timeout=time)

    def end_freedrive(self):
        if self._robot:
            self._robot.set_freedrive(None)


if __name__ == '__main__':
    URRobotController()
