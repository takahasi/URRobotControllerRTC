# -*- coding: utf-8 -*-
"""Universal Robot (URx) controller RTC.
"""

import sys
import logging
import urx
from urx.robotiq_two_finger_gripper import Robotiq_Two_Finger_Gripper

__author__ = "Saburo Takahashi"
__copyright__ = "Copyright 2017, Saburo Takahashi"
__license__ = "LGPLv3"


class URRobotController(object):
    """Universal Robot (URx) controller RTC.

        This class is using urx package.
    """
    # Exceptions
    URxException = urx.urrobot.RobotException

    # Private member
    __instance = None
    __robot = None
    __gripper = None
    __sync_mode = False
    _accel = 0.4
    _velocity = 0.5

    # singleton
    def __new__(cls, ip):
        if not cls.__instance:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self, ip="192.168.1.101"):
        if self.__robot:
            logging.info("instance is already exist")
            return

        logging.basicConfig(format='%(asctime)s:%(levelname)s: %(message)s',
                            level=logging.INFO)

        logging.info("Create URRobotController IP: " + ip)

        try:
            self.__robot = urx.Robot(ip, use_rt=True)
            self.__robot.set_tcp((0, 0, 0, 0, 0, 0))
            self.__robot.set_payload(0, (0, 0, 0))
        except self.URxException:
            logging.error("URx exception was ooccured in init robot")
            self.__robot = None
            return
        except Exception as e:
            logging.error("exception: " + format(str(e)) + " in init robot")
            self.__robot = None
            return

        try:
            self.__gripper = Robotiq_Two_Finger_Gripper(self.__robot)
        except self.URxException:
            logging.error("URx exception was ooccured in init gripper")
            self.__gripper = None
        except Exception as e:
            logging.error("exception: " + format(str(e)) + " in init gripper")
            self.__gripper = None

    def __del__(self):
        self.finalize()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.finalize()

    def is_robot_available(self):
        """Get robot instance is available or not.

        Note:
            None.

        Args:
            None.

        Returns:
            True: Available.
            False: NOT available.
        """
        if self.__robot:
            return True
        else:
            return False

    def is_gripper_available(self):
        """Get gripper instance is available or not.

        Note:
            None.

        Args:
            None.

        Returns:
            True: Available.
            False: NOT available.
        """
        if self.__gripper:
            return True
        else:
            return False

    def get_acc_vel(self, a=None, v=None):
        """Set accel and velocity for move.

        Note:
            None.

        Args:
            None.

        Returns:
            a: Target acceleration.
            v: Target velocity.
        """
        if a:
            acc = a
        else:
            acc = self._accel
        if v:
            vel = v
        else:
            vel = self._velocity
        return acc, vel

    def set_acc_vel(self, a=None, v=None):
        """Get accel and velocity for move.

        Note:
            None.

        Args:
            a: Target acceleration.
            v: Target velocity.

        Returns:
            None.
        """
        if a:
            self._accel = a
        if v:
            self._velocity = v

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
        else:
            logging.error("robot is not initialized in " +
                          sys._getframe().f_code.co_name)

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
        else:
            logging.error("robot is not initialized in " +
                          sys._getframe().f_code.co_name)

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
            r = self.__robot
            return r.is_running() and r.is_program_running()
        else:
            logging.error("robot is not initialized in " +
                          sys._getframe().f_code.co_name)
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
            ac, vl = self.get_acc_vel(a, v)
            self.__robot.movel(pos, acc=ac, vel=vl, wait=self.__sync_mode)
        else:
            logging.error("robot is not initialized in " +
                          sys._getframe().f_code.co_name)

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
            ac, vl = self.get_acc_vel(a, v)
            self.__robot.movej(joints, acc=ac, vel=vl, wait=self.__sync_mode)
        else:
            logging.error("robot is not initialized in " +
                          sys._getframe().f_code.co_name)

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
            ac, vl = self.get_acc_vel(a, v)
            self.__robot.movels(poslist, acc=ac, vel=vl, wait=self.__sync_mode)
        else:
            logging.error("robot is not initialized in " +
                          sys._getframe().f_code.co_name)

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
            ac, vl = self.get_acc_vel(a, v)
            self.__robot.translate_tool(
                vec, acc=ac, vel=vl, wait=self.__sync_mode)
        else:
            logging.error("robot is not initialized in " +
                          sys._getframe().f_code.co_name)

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
            logging.error("robot is not initialized in " +
                          sys._getframe().f_code.co_name)
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
            logging.error("robot is not initialized in " +
                          sys._getframe().f_code.co_name)
            return (0, 0, 0, 0, 0, 0)

    def get_force(self):
        """Get TCP force.

        Note:
            None.

        Args:
            None.

        Returns:
            force: value of force
        """
        if self.__robot:
            return self.__robot.get_force()
        else:
            logging.error("robot is not initialized in " +
                          sys._getframe().f_code.co_name)
            return 0

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
        else:
            logging.error("robot is not initialized in " +
                          sys._getframe().f_code.co_name)

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
        else:
            logging.error("robot is not initialized in " +
                          sys._getframe().f_code.co_name)

    def open_gripper(self):
        """Open gripper.

        Note:
            None.

        Args:
            None.

        Returns:
            None.
        """
        if self.__robot and self.__gripper:
            try:
                self.__gripper.open_gripper()
            except self.URxException:
                logging.error("URx exception was ooccured in " +
                              sys._getframe().f_code.co_name)
            except Exception as e:
                logging.error("except: " + format(str(e)) +
                              " in " + sys._getframe().f_code.co_name)
        else:
            logging.error("robot or gripper is not initialized in " +
                          sys._getframe().f_code.co_name)

    def close_gripper(self):
        """Close gripper.

        Note:
            None.

        Args:
            None.

        Returns:
            None.
        """
        if self.__robot and self.__gripper:
            try:
                self.__gripper.close_gripper()
            except self.URxException:
                logging.error("URx exception was ooccured in " +
                              sys._getframe().f_code.co_name)
            except Exception as e:
                logging.error("except: " + format(str(e)) +
                              " in " + sys._getframe().f_code.co_name)
        else:
            logging.error("robot or gripper is not initialized in " +
                          sys._getframe().f_code.co_name)


if __name__ == '__main__':
    URRobotController()
