# -*- coding: utf-8 -*-
"""Universal Robot (URx) controller RTC.
"""

import sys
import logging
from datetime import datetime
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
    _accel = 0.6
    _velocity = 0.6

    # singleton
    def __new__(cls, ip="192.168.1.101", realtime=True):
        if not cls.__instance:
            cls.__instance = object.__new__(cls, ip, realtime)
        return cls.__instance

    def __init__(self, ip="192.168.1.101", realtime=True):
        if self.__robot:
            logging.info("instance is already exist")
            return

        logging.basicConfig(format='%(asctime)s:%(levelname)s: %(message)s',
                            level=logging.INFO)

        # not use realtime port in stub mode
        if ip == "localhost":
            self.__realtime = False
        else:
            self.__realtime = realtime

        logging.info("Create URRobotController IP: " + ip, self.__realtime)

        try:
            self.__robot = urx.Robot(ip, use_rt=self.__realtime)
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

        self._update_send_time()

        # use pause() for service port
        self._joints_goal = []
        self._pause = False

    def __del__(self):
        self.finalize()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.finalize()

    def _update_send_time(self):
        self.__latest_send_time = datetime.now()

    def _expire_send_time(self):
        diff = datetime.now() - self.__latest_send_time
        # prevent control until 100ms after
        if diff.microseconds > 100000:
            return True
        else:
            return False

    def set_middle(self, middle):
        self._middle = middle

    def unset_middle(self):
        self._middle = None

    @property
    def robot_available(self):
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

    @property
    def gripper_available(self):
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

    @property
    def vel(self):
        """Get velocity for move.

        Note:
            None.

        Args:
            None.

        Returns:
            v: Target velocity.
        """
        return self._velocity

    @vel.setter
    def vel(self, v=None):
        """Set velocity for move.

        Note:
            None.

        Args:
            None.

        Returns:
            v: Target velocity.
        """
        if v:
            self._velocity = v

    @property
    def acc(self):
        """Set accel and velocity for move.

        Note:
            None.

        Args:
            None.

        Returns:
            a: Target acceleration.
        """
        return self._accel

    @acc.setter
    def acc(self, a=None):
        """Get accel and velocity for move.

        Note:
            None.

        Args:
            a: Target acceleration.

        Returns:
            True: Success.
        """
        if a:
            self._accel = a

    def finalize(self):
        """Finalize URRobotController instance.

        Note:
            None.

        Args:
            None.

        Returns:
            True: Success.
            False: Failed.
        """
        if self.__robot:
            self.__robot.close()
            self.__robot = None
            return True
        else:
            logging.error("robot is not initialized in " +
                          sys._getframe().f_code.co_name)
            return False

    def set_payload(self, weight, vector=(0, 0, 0)):
        """Set payload in kg and cog.

        Note:
            None.

        Args:
            weight: Weight in kg.
            vector: Center of gravity in 3d vector.

        Returns:
            True: Success.
            False: Failed.
        """
        if self.__robot:
            # set payload in kg & cog
            self.__robot.set_payload(weight, vector)
            self._update_send_time()
            return True
        else:
            logging.error("robot is not initialized in " +
                          sys._getframe().f_code.co_name)
            return False

    @property
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
            return r.is_program_running() or not self._expire_send_time()
        else:
            logging.error("robot is not initialized in " +
                          sys._getframe().f_code.co_name)
            return False

    @property
    def sync_mode(self):
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

    @sync_mode.setter
    def sync_mode(self, val):
        """Set synchronous mode (wait until program ends).

        Note:
            None.

        Args:
            None.

        Returns:
            True: Success.
        """
        self.__sync_mode = val

    def movel(self, pos, a=None, v=None):
        """Move the robot in a linear path.

        Note:
            None.

        Args:
            a: Target acceleration.
            v: Target velocity.

        Returns:
            True: Success.
            False: Failed.
        """
        if self.__robot:
            self.acc = a
            self.vel = v
            self.__robot.movel(pos,
                               acc=self.acc,
                               vel=self.vel,
                               wait=self.sync_mode)
            self._update_send_time()
            return True
        else:
            logging.error("robot is not initialized in " +
                          sys._getframe().f_code.co_name)
            return False

    def movej(self, joints, a=None, v=None):
        """Move the robot by joint movement.

        Note:
            None.

        Args:
            a: Target acceleration.
            v: Target velocity.

        Returns:
            True: Success.
            False: Failed.
        """
        if self._pause:
            return False

        if self.__robot:
            self._joints_goal = joints
            self.acc = a
            self.vel = v
            self.__robot.movej(joints,
                               acc=self.acc,
                               vel=self.vel,
                               wait=self.sync_mode)
            self._update_send_time()
            return True
        else:
            logging.error("robot is not initialized in " +
                          sys._getframe().f_code.co_name)
            return False

    def movels(self, poslist, a=None, v=None):
        """Sequential move the robot in a linear path.

        Note:
            None.

        Args:
            poslist: Target position list
            a: Target acceleration.
            v: Target velocity.

        Returns:
            True: Success.
            False: Failed.
        """
        if self.__robot:
            self.acc = a
            self.vel = v
            self.__robot.movels(poslist,
                                acc=self.acc,
                                vel=self.vel,
                                wait=self.sync_mode)
            self._update_send_time()
            return True
        else:
            logging.error("robot is not initialized in " +
                          sys._getframe().f_code.co_name)
            return False

    def translate_tool(self, vec, a=None, v=None):
        """Move tool in base coordinate, keeping orientation.

        Note:
            None.

        Args:
            poslist: Target position list
            a: Target acceleration.
            v: Target velocity.

        Returns:
            True: Success.
            False: Failed.
        """
        if self.__robot:
            self.acc = a
            self.vel = v
            self.__robot.translate_tool(vec,
                                        acc=self.acc,
                                        vel=self.vel,
                                        wait=self.sync_mode)
            self._update_send_time()
            return True
        else:
            logging.error("robot is not initialized in " +
                          sys._getframe().f_code.co_name)
            return False

    def getl(self):
        """Get TCP position.

        Note:
            None.

        Args:
            None.

        Returns:
            position: list of TCP position (X, Y, Z, Rx, Ry, Rz)
                      if failed to get, return (0, 0, 0, 0, 0, 0)
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
                      if failed to get, return (0, 0, 0, 0, 0, 0)
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
            force: value of TCP force
                   if failed to get, return 0
        """
        if not self.__realtime:
            logging.info("cannot use realtime port in " +
                         sys._getframe().f_code.co_name)
            return 0
        elif self.__robot:
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
            True: Success.
            False: Failed.
        """
        if self.__robot:
            self.__robot.set_freedrive(True, timeout=time)
            self._update_send_time()
            return True
        else:
            logging.error("robot is not initialized in " +
                          sys._getframe().f_code.co_name)
            return False

    def end_freedrive(self):
        """End freedrive mode.

        Note:
            None.

        Args:
            None.

        Returns:
            True: Success.
            False: Failed.
        """
        if self.__robot:
            self.__robot.set_freedrive(None)
            self._update_send_time()
            return True
        else:
            logging.error("robot is not initialized in " +
                          sys._getframe().f_code.co_name)
            return False

    def open_gripper(self):
        """Open gripper.

        Note:
            None.

        Args:
            None.

        Returns:
            True: Success.
            False: Failed.
        """
        if self.__robot and self.__gripper:
            try:
                self.__gripper.open_gripper()
                self._update_send_time()
            except self.URxException:
                logging.error("URx exception was ooccured in " +
                              sys._getframe().f_code.co_name)
                return False
            except Exception as e:
                logging.error("except: " + format(str(e)) +
                              " in " + sys._getframe().f_code.co_name)
                return False
        else:
            logging.error("robot or gripper is not initialized in " +
                          sys._getframe().f_code.co_name)
            return False

        return True

    def gripper_action(self, value):
        """gripper action.

        Note:
            None.

        Args:
            value: value from 0 to 255.
                   0 is open, 255 is close.

        Returns:
            True: Success.
            False: Failed.
        """
        if value < 0 or value > 255:
            return False

        if self.__robot and self.__gripper:
            try:
                self.__gripper.gripper_action(value)
                self._update_send_time()
            except self.URxException:
                logging.error("URx exception was ooccured in " +
                              sys._getframe().f_code.co_name)
                return False
            except Exception as e:
                logging.error("except: " + format(str(e)) +
                              " in " + sys._getframe().f_code.co_name)
                return False
        else:
            logging.error("robot or gripper is not initialized in " +
                          sys._getframe().f_code.co_name)
            return False

        return True

    def close_gripper(self):
        """Close gripper.

        Note:
            None.

        Args:
            None.

        Returns:
            True: Success.
            False: Failed.
        """
        if self.__robot and self.__gripper:
            try:
                self.__gripper.close_gripper()
                self._update_send_time()
            except self.URxException:
                logging.error("URx exception was ooccured in " +
                              sys._getframe().f_code.co_name)
                return False
            except Exception as e:
                logging.error("except: " + format(str(e)) +
                              " in " + sys._getframe().f_code.co_name)
                return False
        else:
            logging.error("robot or gripper is not initialized in " +
                          sys._getframe().f_code.co_name)
            return False

        return True

    def pause(self):
        """Pause.

        Note:
            None.

        Args:
            None.

        Returns:
            True: Success.
            False: Failed.
        """
        if self.__robot:
            self._pause = True
            self.__robot.stopj(self.acc)

            self._update_send_time()
            return True
        else:
            logging.error("robot is not initialized in " +
                          sys._getframe().f_code.co_name)
            return False

    def resume(self):
        """Resume.

        Note:
            None.

        Args:
            None.

        Returns:
            True: Success.
            False: Failed.
        """
        if self.__robot:
            self._pause = False
            return True
        else:
            logging.error("robot is not initialized in " +
                          sys._getframe().f_code.co_name)
            return False

    def stopj(self, a=None):
        """Decelerate joint speeds to zero.

        Note:
            None.

        Args:
            a: joint acceleration [rad/s^2]

        Returns:
            True: Success.
            False: Failed.
        """
        if self.__robot:
            self.acc = a
            self.__robot.stopj(self.acc)

            self._update_send_time()
            return True
        else:
            logging.error("robot is not initialized in " +
                          sys._getframe().f_code.co_name)
            return False

    def get_pos(self):
        """get current transform from base to to tcp

        Note:
            None.

        Args:
            None.

        Returns:
            True: Success.
            False: Failed.
        """
        pose = []
        if self.__robot:
            pose = self.__robot.get_pos()
            self._update_send_time()
            return True, pose
        else:
            logging.error("robot is not initialized in " +
                          sys._getframe().f_code.co_name)
            return False, pose

    def get_joints_goal(self):
        return self._joints_goal


if __name__ == '__main__':
    URRobotController()
