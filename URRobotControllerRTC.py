#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file URRobotControllerRTC.py
 @brief Controller RTC for Universal Robot URx
 @date $Date$


"""
import sys

# Import RTM module
import RTC
import OpenRTM_aist

import ManipulatorCommonInterface_Middle_idl
import ManipulatorCommonInterface_Common_idl

# Import Service implementation class
# <rtc-template block="service_impl">
from ManipulatorCommonInterface_Middle_idl_example import *
from ManipulatorCommonInterface_Common_idl_example import *

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>

from URRobotController import URRobotController as urrobot

# This module's spesification
# <rtc-template block="module_spec">
urrobotcontrollerrtc_spec = [
    "implementation_id", "URRobotControllerRTC",
    "type_name",         "URRobotControllerRTC",
    "description",       "Controller RTC for Universal Robot URx",
    "version",           "1.0.0",
    "vendor",            "takahasi",
    "category",          "Manipulation",
    "activity_type",     "STATIC",
    "max_instance",      "1",
    "language",          "Python",
    "lang_type",         "SCRIPT",
    "conf.default.ip_address", "192.168.1.101",
    "conf.__widget__.ip_address", "text",
    "conf.__type__.ip_address", "string",
    ""]
# </rtc-template>

##
# @class URRobotControllerRTC
# @brief Controller RTC for URx
#
#


class URRobotControllerRTC(OpenRTM_aist.DataFlowComponentBase):

    ##
    # @brief constructor
    # @param manager Maneger Object
    #
    def __init__(self, manager):
        OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

        self._d_mode = RTC.TimedOctet(RTC.Time(0, 0), 0)
        self._modeIn = OpenRTM_aist.InPort("mode", self._d_mode)

        self._d_in_joint = RTC.TimedFloatSeq(RTC.Time(0, 0), [])
        self._in_jointIn = OpenRTM_aist.InPort("in_joint", self._d_in_joint)

        self._d_in_pose = RTC.TimedPose3D(RTC.Time(0, 0),
                                          RTC.Pose3D(RTC.Point3D(0,
                                                                 0,
                                                                 0),
                                                     RTC.Orientation3D(0,
                                                                       0,
                                                                       0))
                                          )
        self._in_poseIn = OpenRTM_aist.InPort("in_pose", self._d_in_pose)

        self._d_grip = RTC.TimedOctet(RTC.Time(0, 0), 0)
        self._gripIn = OpenRTM_aist.InPort("grip", self._d_grip)

        self._d_out_joint = RTC.TimedFloatSeq(RTC.Time(0, 0), [])
        self._out_jointOut = OpenRTM_aist.OutPort(
            "out_joint", self._d_out_joint)

        self._d_out_pose = RTC.TimedPose3D(RTC.Time(0, 0),
                                           RTC.Pose3D(RTC.Point3D(0,
                                                                  0,
                                                                  0),
                                                      RTC.Orientation3D(0,
                                                                        0,
                                                                        0))
                                           )
        self._out_poseOut = OpenRTM_aist.OutPort("out_pose", self._d_out_pose)

        self._d_is_moving = RTC.TimedBoolean(RTC.Time(0, 0), False)
        self._is_movingOut = OpenRTM_aist.OutPort("is_moving",
                                                  self._d_is_moving)

        self._d_force = RTC.TimedFloatSeq(RTC.Time(0, 0), [])
        self._forceOut = OpenRTM_aist.OutPort("force", self._d_force)

        self._middlePort = OpenRTM_aist.CorbaPort("middle")
        self._commonPort = OpenRTM_aist.CorbaPort("common")

        self._middle = ManipulatorCommonInterface_Middle_i()
        self._common = ManipulatorCommonInterface_Common_i()

        # initialize of configuration-data.
        # <rtc-template block="init_conf_param">
        """
        - Name:  ip_address
        - DefaultValue: 192.168.1.101
        """
        self._ip_address = ['192.168.1.101']

        # </rtc-template>

        self._controller = None
        instance = OpenRTM_aist.Manager.instance()
        self._log = instance.getLogbuf("URRobotController")

    ##
    #
    # The initialize action (on CREATED->ALIVE transition)
    # formaer rtc_init_entry()
    #
    # @return RTC::ReturnCode_t
    #
    #
    def onInitialize(self):
        # Bind variables and configuration variable
        self.bindParameter("ip_address", self._ip_address, "192.168.1.101")

        # Set InPort buffers
        self.addInPort("mode", self._modeIn)
        self.addInPort("in_joint", self._in_jointIn)
        self.addInPort("in_pose", self._in_poseIn)
        self.addInPort("grip", self._gripIn)

        # Set OutPort buffers
        self.addOutPort("out_joint", self._out_jointOut)
        self.addOutPort("out_pose", self._out_poseOut)
        self.addOutPort("is_moving", self._is_movingOut)
        self.addOutPort("force", self._forceOut)

        # Set service provider to Ports
        self._middlePort.registerProvider(
            "JARA_ARM_ManipulatorCommonInterface_Middle", "JARA_ARM::ManipulatorCommonInterface_Middle",
            self._middle)
        self._commonPort.registerProvider(
            "JARA_ARM_ManipulatorCommonInterface_Common", "JARA_ARM::ManipulatorCommonInterface_Common",
            self._common)

        # Set service consumers to Ports

        # Set CORBA Service Ports
        self.addPort(self._middlePort)
        self.addPort(self._commonPort)

        return RTC.RTC_OK

    ##
    #
    # The finalize action (on ALIVE->END transition)
    # formaer rtc_exiting_entry()
    #
    # @return RTC::ReturnCode_t
    #
    #
    # def onFinalize(self):
    #
    #   return RTC.RTC_OK

    ##
    #
    # The startup action when ExecutionContext startup
    # former rtc_starting_entry()
    #
    # @param ec_id target ExecutionContext Id
    #
    # @return RTC::ReturnCode_t
    #
    #
    # def onStartup(self, ec_id):
    #
    #   return RTC.RTC_OK

    ##
    #
    # The shutdown action when ExecutionContext stop
    # former rtc_stopping_entry()
    #
    # @param ec_id target ExecutionContext Id
    #
    # @return RTC::ReturnCode_t
    #
    #
    # def onShutdown(self, ec_id):
    #
    #   return RTC.RTC_OK

    ##
    #
    # The activated action (Active state entry action)
    # former rtc_active_entry()
    #
    # @param ec_id target ExecutionContext Id
    #
    # @return RTC::ReturnCode_t
    #
    #
    def onActivated(self, ec_id):
        self._controller = urrobot(ip=self._ip_address[0])
        if not self._controller.robot_available:
            self._log.RTC_ERROR("URx robot is not available")
            self._controller = None
            return RTC.RTC_ERROR

        if not self._controller.gripper_available:
            self._log.RTC_WARN("URx gripper is not available")

        self._middle.set_controller(self._controller)
        self._common.set_controller(self._controller)

        return RTC.RTC_OK

    ##
    #
    # The deactivated action (Active state exit action)
    # former rtc_active_exit()
    #
    # @param ec_id target ExecutionContext Id
    #
    # @return RTC::ReturnCode_t
    #
    #
    def onDeactivated(self, ec_id):
        if self._controller:
            self._controller.finalize()
            self._controller = None
            self._middle.unset_controller()
            self._common.unset_controller()

        return RTC.RTC_OK

    ##
    #
    # The execution action that is invoked periodically
    # former rtc_active_do()
    #
    # @param ec_id target ExecutionContext Id
    #
    # @return RTC::ReturnCode_t
    #
    #
    def onExecute(self, ec_id):

        # check controller exixts
        if not self._controller:
            self._log.RTC_ERROR("robot is not yet initialized")
            return RTC.RTC_ERROR

        # update mode
        self._update_mode()

        # move by pose
        self._move_by_pose()

        # move by joints
        self._move_by_joints()

        # control gripper
        self._control_gripper()

        # output joints information
        self._output_joints()

        # output pose information
        self._output_pose()

        # output force information
        self._output_force()

        # output moving information
        self._output_moving()

        return RTC.RTC_OK

    ##
    #
    # The aborting action when main logic error occurred.
    # former rtc_aborting_entry()
    #
    # @param ec_id target ExecutionContext Id
    #
    # @return RTC::ReturnCode_t
    #
    #
    # def onAborting(self, ec_id):
    #
    #   return RTC.RTC_OK

    ##
    #
    # The error action in ERROR state
    # former rtc_error_do()
    #
    # @param ec_id target ExecutionContext Id
    #
    # @return RTC::ReturnCode_t
    #
    #
    # def onError(self, ec_id):
    #
    #   return RTC.RTC_OK

    ##
    #
    # The reset action that is invoked resetting
    # This is same but different the former rtc_init_entry()
    #
    # @param ec_id target ExecutionContext Id
    #
    # @return RTC::ReturnCode_t
    #
    #
    # def onReset(self, ec_id):
    #
    #   return RTC.RTC_OK

    ##
    #
    # The state update action that is invoked after onExecute() action
    # no corresponding operation exists in OpenRTm-aist-0.2.0
    #
    # @param ec_id target ExecutionContext Id
    #
    # @return RTC::ReturnCode_t
    #

    #
    # def onStateUpdate(self, ec_id):
    #
    #   return RTC.RTC_OK

    ##
    #
    # The action that is invoked when execution context's rate is changed
    # no corresponding operation exists in OpenRTm-aist-0.2.0
    #
    # @param ec_id target ExecutionContext Id
    #
    # @return RTC::ReturnCode_t
    #
    #
    # def onRateChanged(self, ec_id):
    #
    #    return RTC.RTC_OK

    def _update_mode(self):
        # update mode
        if self._modeIn.isNew():
            mode = self._modeIn.read().data
            self._log.RTC_INFO("mode: " + str(mode))
            if mode == 10:
                self._log.RTC_INFO("start freedrive mode")
                self._controller.start_freedrive(time=120)
            elif mode == 2:
                self._log.RTC_INFO("start slow mode")
                self._controller.end_freedrive()
                self._controller.acc = 0.3
                self._controller.vel = 0.3
            else:
                self._log.RTC_INFO("start normal mode")
                self._controller.end_freedrive()
                self._controller.acc = 0.6
                self._controller.vel = 0.6

    def _move_by_pose(self):
        # move by pose
        if self._in_poseIn.isNew():
            pose = self._in_poseIn.read().data
            self._log.RTC_INFO("in_pose: " + str(pose))
            px = pose.position.x
            py = pose.position.y
            pz = pose.position.z
            rp = pose.orientation.p
            rr = pose.orientation.r
            ry = pose.orientation.y
            self._controller.movel((px, py, pz, rp, rr, ry))

    def _move_by_joints(self):
        # move by joints
        if self._in_jointIn.isNew():
            joints = self._in_jointIn.read().data
            self._log.RTC_INFO("in_joint: " + str(joints))
            if len(joints) == 6:
                self._controller.movej(joints)

    def _control_gripper(self):
        # control gripper
        if self._gripIn.isNew():
            grip = self._gripIn.read().data
            self._log.RTC_INFO("grip: " + str(grip))
            if grip == 0:
                self._controller.open_gripper()
            elif grip == 1:
                self._controller.close_gripper()

    def _output_joints(self):
        # output joints information
        joints = self._controller.getj()
        self._log.RTC_DEBUG("out_joint: " + str(joints))
        self._d_out_joint.data = joints
        self._out_jointOut.write()

    def _output_pose(self):
        # output pose information
        pose = self._controller.getl()
        self._log.RTC_DEBUG("out_pose: " + str(pose))
        self._d_out_pose.data = RTC.Pose3D(RTC.Point3D(pose[0],
                                                       pose[1],
                                                       pose[2]),
                                           RTC.Orientation3D(pose[3],
                                                             pose[4],
                                                             pose[5]))
        self._out_poseOut.write()

    def _output_force(self):
        # output force information
        force = self._controller.get_force()
        self._log.RTC_DEBUG("force: " + str(force))
        self._d_force.data = [force]
        self._forceOut.write()

    def _output_moving(self):
        # output moving information
        moving = self._controller.is_moving
        self._log.RTC_DEBUG("is_moving: " + str(moving))
        self._d_is_moving.data = moving
        self._is_movingOut.write()


def URRobotControllerRTCInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=urrobotcontrollerrtc_spec)
    manager.registerFactory(profile,
                            URRobotControllerRTC,
                            OpenRTM_aist.Delete)


def MyModuleInit(manager):
    URRobotControllerRTCInit(manager)

    # Create a component
    manager.createComponent("URRobotControllerRTC")


def main():
    mgr = OpenRTM_aist.Manager.init(sys.argv)
    mgr.setModuleInitProc(MyModuleInit)
    mgr.activateManager()
    mgr.runManager()


if __name__ == "__main__":
    main()
