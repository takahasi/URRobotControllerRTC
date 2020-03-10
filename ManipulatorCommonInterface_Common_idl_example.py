#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file ManipulatorCommonInterface_Common_idl_examplefile.py
 @brief Python example implementations generated from ManipulatorCommonInterface_Common.idl
 @date $Date$


"""

import omniORB
from omniORB import CORBA, PortableServer
import JARA_ARM
import JARA_ARM__POA

import ManipulatorCommonInterface_DataTypes_idl as DATATYPES_IDL
import ManipulatorCommonInterface_Common_idl as COMMON_IDL
import math


class ManipulatorCommonInterface_Common_i (JARA_ARM__POA.ManipulatorCommonInterface_Common):
    """
    @class ManipulatorCommonInterface_Common_i
    Example class implementing IDL interface JARA_ARM.ManipulatorCommonInterface_Common
    """

    _controller = None

    def __init__(self):
        """
        @brief standard constructor
        Initialise member variables here
        """
        self._axisnum = 6
        self._limit_joint_deg = [[360, -360], [360, -360],
                                 [360, -360], [360, -360],
                                 [360, -360], [360, -360]]

    def set_controller(self, controller):
        self._controller = controller

    def unset_controller(self):
        self._controller = None

    def set_middle(self, middle):
        self._middle = middle

    def unset_middle(self):
        self._middle = None

    def _make_return_id(self, okng, comment):
        if okng == "NG":
            ret = DATATYPES_IDL._0_JARA_ARM.NG
        else:
            ret = DATATYPES_IDL._0_JARA_ARM.OK
        return DATATYPES_IDL._0_JARA_ARM.RETURN_ID(ret, comment)

    # RETURN_ID clearAlarms()
    def clearAlarms(self):
        raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result

    # RETURN_ID getActiveAlarm(out AlarmSeq alarms)
    def getActiveAlarm(self):
        raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result, alarms

    # RETURN_ID getFeedbackPosJoint(out JointPos pos)
    def getFeedbackPosJoint(self):
        if self._controller:
            return self._make_return_id("OK", ''),  self._controller.getj()
        else:
            return self._make_return_id("NG", ''),  []

    # RETURN_ID getManipInfo(out ManipInfo mInfo)
    def getManipInfo(self):
        return self._make_return_id("OK", ''),  COMMON_IDL._0_JARA_ARM.ManipInfo('Universal Robots A/S', 'UR5', self._axisnum, 1, True)

    # RETURN_ID getSoftLimitJoint(out LimitSeq softLimit)
    def getSoftLimitJoint(self):
        limit_joint = []

        for i in range(self._axisnum):
            limit_joint.append(DATATYPES_IDL._0_JARA_ARM.LimitValue(math.radians(
                self._limit_joint_deg[i][0]), math.radians(self._limit_joint_deg[i][1])))

        return self._make_return_id("OK", ''), limit_joint

    # RETURN_ID getState(out ULONG state)
    def getState(self):
        # only get 0x02(moving) 0x10(pause)
        state = 0

        if not self._controller or not self._middle:
            return self._make_return_id("NG", ''), state

        # check moving
        if self._controller.is_moving:
            state = state | 0x01

        # check pause
        if self._middle._middle_idl_state == self._middle.MIDDLE_IDL_STATE_PAUSE:
            state = state | 0x10

        return self._make_return_id("OK", ''), state

    # RETURN_ID servoOFF()
    def servoOFF(self):
        print("servoOFF")
        return self._make_return_id("OK", '')
        # raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result

    # RETURN_ID servoON()
    def servoON(self):
        print("ServoON")
        return self._make_return_id("OK", '')
        # raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result

    # RETURN_ID setSoftLimitJoint(in LimitSeq softLimit)
    def setSoftLimitJoint(self, softLimit):
        raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result


if __name__ == "__main__":
    import sys

    # Initialise the ORB
    orb = CORBA.ORB_init(sys.argv)

    # As an example, we activate an object in the Root POA
    poa = orb.resolve_initial_references("RootPOA")

    # Create an instance of a servant class
    servant = ManipulatorCommonInterface_Common_i()

    # Activate it in the Root POA
    poa.activate_object(servant)

    # Get the object reference to the object
    objref = servant._this()

    # Print a stringified IOR for it
    print(orb.object_to_string(objref))

    # Activate the Root POA's manager
    poa._get_the_POAManager().activate()

    # Run the ORB, blocking this thread
    orb.run()
