# -*- coding: utf-8 -*-
"""Universal Robot (URx) controller RTC.
"""

import urx
import logging

__author__ = "Saburo Takahashi"
__copyright__ = "Copyright 2017, Saburo Takahashi"
__license__ = "LGPLv3"


class URRobotController():
    """Universal Robot (URx) controller RTC.

        This class is using urx package.
    """
    # Exceptions
    URxException = urx.urrobot.RobotException

    # Private constant value
    _DEFAULT_ACC = 0.4
    _DEFAULT_VEL = 0.5

    # Private member
    __robot = None
    __sync_mode = False

    def __init__(self, ip="192.168.1.101", realtime=False):
        logging.basicConfig(format='%(asctime)s:%(levelname)s: %(message)s',
                            level=logging.INFO)

        logging.info("Create URRobotController IP: " +
                     ip + " RTPort: " + str(realtime))
        self.__robot = urx.Robot(ip, use_rt=realtime)
        self.__robot.set_tcp((0, 0, 0, 0, 0, 0))
        self.__robot.set_payload(0, (0, 0, 0))

    def __del__(self):
        self.finalize()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.finalize()

    def _get_acc_vel(self, a=None, v=None):
        acc = a or self._DEFAULT_ACC
        vel = v or self._DEFAULT_VEL
        return acc, vel

    def finalize(self):
        """Finalize URRobotController instance.

        Note:
            None.

        Args:
            None.

        Returns:
            None.
        """
        if self.__robot:
            self.__robot.close()
            self.__robot = None

    def set_payload(self, weight, vector=(0, 0, 0)):
        """Set payload in kg and cog.

        Note:
            None.

        Args:
            weight: Weight in kg.
            vector: Center of gravity in 3d vector.

        Returns:
            None.
        """
        if self.__robot:
            # set payload in kg & cog
            self.__robot.set_payload(weight, vector)

    def is_moving(self):
        """Get status of runnning program.

        Note:
            None.

        Args:
            None.

        Returns:
            True: Program is running.
            False: Program is NOT running.
        """
        if self.__robot:
            return self.__robot.is_running() and self.__robot.is_program_running()
        else:
            return False

    def set_sync_mode(self):
        """Set synchronous mode (wait until program ends).

        Note:
            None.

        Args:
            None.

        Returns:
            None.
        """
        self.__sync_mode = True

    def set_async_mode(self):
        """Set asynchronous mode (NOT wait until program ends).

        Note:
            None.

        Args:
            None.

        Returns:
            None.
        """
        self.__sync_mode = False

    def is_sync_mode(self):
        """Get synchronous mode.

        Note:
            None.

        Args:
            None.

        Returns:
            True: Synchronous mode.
            False: Asynchronous mode.
        """
        return self.__sync_mode

    def movel(self, pos, a=None, v=None):
        """Move the robot in a linear path.

        Note:
            None.

        Args:
            a: Target acceleration.
            v: Target velocity.

        Returns:
            None.
        """
        if self.__robot:
            ac, vl = self._get_acc_vel(a, v)
            self.__robot.movel(pos, acc=ac, vel=vl, wait=self.__sync_mode)

    def movej(self, joints, a=None, v=None):
        """Move the robot by joint movement.

        Note:
            None.

        Args:
            a: Target acceleration.
            v: Target velocity.

        Returns:
            None.
        """
        if self.__robot:
            ac, vl = self._get_acc_vel(a, v)
            self.__robot.movej(joints, acc=ac, vel=vl, wait=self.__sync_mode)

    def movels(self, poslist, a=None, v=None):
        """Sequential move the robot in a linear path.

        Note:
            None.

        Args:
            poslist: Target position list
            a: Target acceleration.
            v: Target velocity.

        Returns:
            None.
        """
        if self.__robot:
            ac, vl = self._get_acc_vel(a, v)
            self.__robot.movels(poslist, acc=ac, vel=vl, wait=self.__sync_mode)

    def translate_tool(self, vec, a=None, v=None):
        """Move tool in base coordinate, keeping orientation.

        Note:
            None.

        Args:
            poslist: Target position list
            a: Target acceleration.
            v: Target velocity.

        Returns:
            None.
        """
        if self.__robot:
            ac, vl = self._get_acc_vel(a, v)
            self.__robot.translate_tool(
                vec, acc=ac, vel=vl, wait=self.__sync_mode)

    def getl(self):
        """Get TCP position.

        Note:
            None.

        Args:
            None.

        Returns:
            position: list of TCP position (X, Y, Z, Rx, Ry, Rz)
        """
        if self.__robot:
            return self.__robot.getl()
        else:
            return (0, 0, 0, 0, 0, 0)

    def getj(self):
        """Get joint position.

        Note:
            None.

        Args:
            None.

        Returns:
            position: list of joint position (J0, J1, J2, J3, J4, J5)
        """
        if self.__robot:
            return self.__robot.getj()
        else:
            return (0, 0, 0, 0, 0, 0)

    def start_freedrive(self, time=60):
        """Start freedrive mode.

        Note:
            None.

        Args:
            time: Time to keep freedrive mode in seconds (default=60s).

        Returns:
            None.
        """
        if self.__robot:
            self.__robot.set_freedrive(True, timeout=time)

    def end_freedrive(self):
        """End freedrive mode.

        Note:
            None.

        Args:
            None.

        Returns:
            None.
        """
        if self.__robot:
            self.__robot.set_freedrive(None)


if __name__ == '__main__':
    URRobotController()
