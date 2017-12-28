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
    "conf.default.use_realtime_port", "0",
    "conf.__widget__.ip_address", "text",
    "conf.__widget__.use_realtime_port", "radio",
    "conf.__constraints__.use_realtime_port", "(0,1)",
    "conf.__type__.ip_address", "string",
    "conf.__type__.use_realtime_port", "short",
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

        self._d_in_joint = RTC.TimedFloatSeq(RTC.Time(0, 0), [])
        self._in_jointIn = OpenRTM_aist.InPort("in_joint", self._d_in_joint)
        self._d_in_pose = RTC.TimedPose3D(RTC.Time(0, 0),
                                          RTC.Pose3D(RTC.Point3D(0, 0, 0),
                                                     RTC.Orientation3D(0, 0, 0))
                                          )
        self._in_poseIn = OpenRTM_aist.InPort("in_pose", self._d_in_pose)
        self._d_out_joint = RTC.TimedFloatSeq(RTC.Time(0, 0), [])
        self._out_jointOut = OpenRTM_aist.OutPort(
            "out_joint", self._d_out_joint)

        self._d_out_pose = RTC.TimedPose3D(RTC.Time(0, 0),
                                           RTC.Pose3D(RTC.Point3D(0, 0, 0),
                                                      RTC.Orientation3D(0, 0, 0))
                                           )
        self._out_poseOut = OpenRTM_aist.OutPort("out_pose", self._d_out_pose)

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

        """
        - Name:  use_realtime_port
        - DefaultValue: 0
        """
        self._use_realtime_port = [0]

        # </rtc-template>

        self._controller = None
        self._log = OpenRTM_aist.Manager.instance().getLogbuf("URRobotController")

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

        # Set InPort buffers
        self.addInPort("in_joint", self._in_jointIn)
        self.addInPort("in_pose", self._in_poseIn)

        # Set OutPort buffers
        self.addOutPort("out_joint", self._out_jointOut)
        self.addOutPort("out_pose", self._out_poseOut)

        # Set service provider to Ports
        self._middlePort.registerProvider(
            "middle", "JARA_ARM::ManipulatorCommonInterface_Middle", self._middle)
        self._commonPort.registerProvider(
            "common", "JARA_ARM::ManipulatorCommonInterface_Common", self._common)

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
        if self._use_realtime_port[0] == 1:
            use_rt = True
        else:
            use_rt = False

        try:
            self._controller = urrobot(ip=self._ip_address[0], realtime=use_rt)
        except urrobot.URxException:
            self._log.RTC_ERROR("URx exception was ooccured")
            return RTC.RTC_ERROR
        except Exception as e:
            self._log.RTC_ERROR("exception: " + format(str(e)))
            return RTC.RTC_ERROR

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
            return RTC.RTC_ERROR

        # move by pose
        if self._in_poseIn.isNew():
            self._d_in_pose = self._in_poseIn.read()
            self._log.RTC_INFO("in_pose: " + str(self._d_in_pose.data))
            px = self._d_in_pose.data.position.x
            py = self._d_in_pose.data.position.y
            pz = self._d_in_pose.data.position.z
            rp = self._d_in_pose.data.orientation.p
            rr = self._d_in_pose.data.orientation.r
            ry = self._d_in_pose.data.orientation.y
            self._controller.movel((px, py, pz, rp, rr, ry))

        # move by joints
        if self._in_jointIn.isNew():
            self._d_in_joint = self._in_jointIn.read()
            self._log.RTC_INFO("in_joint: " + str(self._d_in_joint.data))
            joints = self._d_in_joint.data
            self._controller.movej(joints)

        # output joints information
        joints = self._controller.getj()
        self._log.RTC_DEBUG("out_joint: " + str(joints))
        self._d_out_joint.data = joints
        self._out_jointOut.write()

        # output pose information
        pose = self._controller.getl()
        self._log.RTC_DEBUG("out_pose: " + str(pose))
        self._d_out_pose.data = RTC.Pose3D(RTC.Point3D(pose[0], pose[1], pose[2]),
                                           RTC.Orientation3D(pose[3], pose[4], pose[5]))
        self._out_poseOut.write()

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
