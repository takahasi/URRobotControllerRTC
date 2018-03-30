#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file ManipulatorCommonInterface_Middle_idl_examplefile.py
 @brief Python example implementations generated from ManipulatorCommonInterface_Middle.idl
 @date $Date$


"""

import omniORB
from omniORB import CORBA, PortableServer
import JARA_ARM
import JARA_ARM__POA

import ManipulatorCommonInterface_DataTypes_idl as DATATYPES_IDL
import ManipulatorCommonInterface_Common_idl as COMMON_IDL
import math


class ManipulatorCommonInterface_Middle_i (JARA_ARM__POA.ManipulatorCommonInterface_Middle):
    """
    @class ManipulatorCommonInterface_Middle_i
    Example class implementing IDL interface JARA_ARM.ManipulatorCommonInterface_Middle
    """

    _controller = None

    def __init__(self):
        """
        @brief standard constructor
        Initialise member variables here
        """
        self._joint_max_speed_deg = [180, 180, 180, 180, 180, 180]
        self._home = [0, -1.57, 0, -1.57, 0, 0]

        self.MIDDLE_IDL_STATE_NORMAL = 0
        self.MIDDLE_IDL_STATE_PAUSE = 1
        self.MIDDLE_IDL_STATE_STOP = 2
        self._middle_idl_state = self.MIDDLE_IDL_STATE_NORMAL

        self._joints_goal = []

    def set_controller(self, controller):
        self._controller = controller

    def unset_controller(self):
        self._controller = None

    @property
    def middle_idl_state(self):
        return self._middle_idl_state

    # RETURN_ID closeGripper()
    def closeGripper(self):
        if self._controller:
            self._controller.close_gripper()
            return DATATYPES_IDL._0_JARA_ARM.RETURN_ID(DATATYPES_IDL._0_JARA_ARM.OK, '')
        else:
            return DATATYPES_IDL._0_JARA_ARM.RETURN_ID(DATATYPES_IDL._0_JARA_ARM.NG, '')

    # RETURN_ID getBaseOffset(out HgMatrix offset)
    def getBaseOffset(self):
        raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result, offset

    # RETURN_ID getFeedbackPosCartesian(out CarPosWithElbow pos)
    def getFeedbackPosCartesian(self):
        raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result, pos

    # RETURN_ID getMaxSpeedCartesian(out CartesianSpeed speed)
    def getMaxSpeedCartesian(self):
        raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result, speed

    # RETURN_ID getMaxSpeedJoint(out DoubleSeq speed)
    def getMaxSpeedJoint(self):
        max_speed_joint = []

        for deg in self._joint_max_speed_deg:
            max_speed_joint.append(math.radians(deg))

        return DATATYPES_IDL._0_JARA_ARM.RETURN_ID(DATATYPES_IDL._0_JARA_ARM.OK, ''), max_speed_joint

    # RETURN_ID getMinAccelTimeCartesian(out double aclTime)
    def getMinAccelTimeCartesian(self):
        raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result, aclTime

    # RETURN_ID getMinAccelTimeJoint(out double aclTime)
    def getMinAccelTimeJoint(self):
        raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result, aclTime

    # RETURN_ID getSoftLimitCartesian(out LimitValue xLimit, out LimitValue yLimit, out LimitValue zLimit)
    def getSoftLimitCartesian(self):
        raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result, xLimit, yLimit, zLimit

    # RETURN_ID moveGripper(in ULONG angleRatio)
    def moveGripper(self, angleRatio):
        if self._controller:
            self._controller.gripper_action(int((100 - angleRatio) * 0.01 * 255))  # 255 is close complete.
            return DATATYPES_IDL._0_JARA_ARM.RETURN_ID(DATATYPES_IDL._0_JARA_ARM.OK, '')
        else:
            return DATATYPES_IDL._0_JARA_ARM.RETURN_ID(DATATYPES_IDL._0_JARA_ARM.NG, '')

    # RETURN_ID moveLinearCartesianAbs(in CarPosWithElbow carPoint)
    def moveLinearCartesianAbs(self, carPoint):

        pos_x = carPoint.carPos[0][3]
        pos_y = carPoint.carPos[1][3]
        pos_z = carPoint.carPos[2][3]

        theta = math.acos(((carPoint.carPos[0][0] + carPoint.carPos[1][1] + carPoint.carPos[2][2]) - 1) / 2)
        multi = 1 / (2 * math.sin(theta))

        rad_x = multi * (carPoint.carPos[2][1] - carPoint.carPos[1][2]) * theta
        rad_y = multi * (carPoint.carPos[0][2] - carPoint.carPos[2][0]) * theta
        rad_z = multi * (carPoint.carPos[1][0] - carPoint.carPos[0][1]) * theta

        if self._controller:
            self._controller.movel([pos_x, pos_y, pos_z, rad_x, rad_y, rad_z])
            return DATATYPES_IDL._0_JARA_ARM.RETURN_ID(DATATYPES_IDL._0_JARA_ARM.OK, '')
        else:
            return DATATYPES_IDL._0_JARA_ARM.RETURN_ID(DATATYPES_IDL._0_JARA_ARM.NG, '')

        # RETURN_ID moveLinearCartesianRel(in CarPosWithElbow carPoint)
    def moveLinearCartesianRel(self, carPoint):

        __, current_pose = self._controller.get_pos()

        pos_x = carPoint.carPos[0][3] + current_pose[0]
        pos_y = carPoint.carPos[1][3] + current_pose[1]
        pos_z = carPoint.carPos[2][3] + current_pose[2]

        print('pos_x = {}, pos_y = {}, pos_z = {}'.format(pos_x, pos_y, pos_z))

        theta = math.acos(((carPoint.carPos[0][0] + carPoint.carPos[1][1] + carPoint.carPos[2][2]) - 1) / 2)
        multi = 1 / (2 * math.sin(theta))

        rad_x = multi * (carPoint.carPos[2][1] - carPoint.carPos[1][2]) * theta
        rad_y = multi * (carPoint.carPos[0][2] - carPoint.carPos[2][0]) * theta
        rad_z = multi * (carPoint.carPos[1][0] - carPoint.carPos[0][1]) * theta

        if self._controller:
            self._controller.movel([pos_x, pos_y, pos_z, rad_x, rad_y, rad_z])
            return DATATYPES_IDL._0_JARA_ARM.RETURN_ID(DATATYPES_IDL._0_JARA_ARM.OK, '')
        else:
            return DATATYPES_IDL._0_JARA_ARM.RETURN_ID(DATATYPES_IDL._0_JARA_ARM.NG, '')

    # RETURN_ID movePTPCartesianAbs(in CarPosWithElbow carPoint)
    def movePTPCartesianAbs(self, carPoint):
        raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result

    # RETURN_ID movePTPCartesianRel(in CarPosWithElbow carPoint)
    def movePTPCartesianRel(self, carPoint):
        raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result

    # RETURN_ID movePTPJointAbs(in JointPos jointPoints)
    def movePTPJointAbs(self, jointPoints):
        if self._controller:
            self._controller.movej(jointPoints)
            return DATATYPES_IDL._0_JARA_ARM.RETURN_ID(DATATYPES_IDL._0_JARA_ARM.OK, '')
        else:
            return DATATYPES_IDL._0_JARA_ARM.RETURN_ID(DATATYPES_IDL._0_JARA_ARM.NG, '')

    # RETURN_ID movePTPJointRel(in JointPos jointPoints)
    def movePTPJointRel(self, jointPoints):
        if self._controller:
            get_pos = self._controller.getj()
            joints = [i + j for (i, j) in zip(get_pos, jointPoints)]
            self._controller.movej(joints)
            return DATATYPES_IDL._0_JARA_ARM.RETURN_ID(DATATYPES_IDL._0_JARA_ARM.OK, '')
        else:
            return DATATYPES_IDL._0_JARA_ARM.RETURN_ID(DATATYPES_IDL._0_JARA_ARM.NG, '')

    # RETURN_ID openGripper()
    def openGripper(self):
        if self._controller:
            self._controller.open_gripper()
            return DATATYPES_IDL._0_JARA_ARM.RETURN_ID(DATATYPES_IDL._0_JARA_ARM.OK, '')
        else:
            return DATATYPES_IDL._0_JARA_ARM.RETURN_ID(DATATYPES_IDL._0_JARA_ARM.NG, '')

    # RETURN_ID pause()
    def pause(self):
        if self._middle_idl_state > 0:
            msg = 'robot is already pause or stop'
            return DATATYPES_IDL._0_JARA_ARM.RETURN_ID(DATATYPES_IDL._0_JARA_ARM.OK, msg)

        if self._controller:
            self._controller.pause()
            self._joints_goal = self._controller.get_joints_goal()
            self._middle_idl_state = self.MIDDLE_IDL_STATE_PAUSE
            return DATATYPES_IDL._0_JARA_ARM.RETURN_ID(DATATYPES_IDL._0_JARA_ARM.OK, '')
        else:
            return DATATYPES_IDL._0_JARA_ARM.RETURN_ID(DATATYPES_IDL._0_JARA_ARM.NG, '')

    # RETURN_ID resume()
    def resume(self):
        if self._middle_idl_state == self.MIDDLE_IDL_STATE_PAUSE and self._controller:
            self._middle_idl_state = self.MIDDLE_IDL_STATE_NORMAL
            self._controller.resume()
            self._controller.movej(self._joints_goal)
        return DATATYPES_IDL._0_JARA_ARM.RETURN_ID(DATATYPES_IDL._0_JARA_ARM.OK, '')

    # RETURN_ID stop()
    def stop(self):
        if self._controller:
            self._controller.stopj()
            self._middle_idl_state = self.MIDDLE_IDL_STATE_NORMAL
            self._controller.resume()
            return DATATYPES_IDL._0_JARA_ARM.RETURN_ID(DATATYPES_IDL._0_JARA_ARM.OK, '')
        else:
            return DATATYPES_IDL._0_JARA_ARM.RETURN_ID(DATATYPES_IDL._0_JARA_ARM.NG, '')

    # RETURN_ID setAccelTimeCartesian(in double aclTime)
    def setAccelTimeCartesian(self, aclTime):
        raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result

    # RETURN_ID setAccelTimeJoint(in double aclTime)
    def setAccelTimeJoint(self, aclTime):
        raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result

    # RETURN_ID setBaseOffset(in HgMatrix offset)
    def setBaseOffset(self, offset):
        raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result

    # RETURN_ID setControlPointOffset(in HgMatrix offset)
    def setControlPointOffset(self, offset):
        raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result

    # RETURN_ID setMaxSpeedCartesian(in CartesianSpeed speed)
    def setMaxSpeedCartesian(self, speed):
        raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result

    # RETURN_ID setMaxSpeedJoint(in DoubleSeq speed)
    def setMaxSpeedJoint(self, speed):
        raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result

    # RETURN_ID setMinAccelTimeCartesian(in double aclTime)
    def setMinAccelTimeCartesian(self, aclTime):
        raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result

    # RETURN_ID setMinAccelTimeJoint(in double aclTime)
    def setMinAccelTimeJoint(self, aclTime):
        raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result

    # RETURN_ID setSoftLimitCartesian(in LimitValue xLimit, in LimitValue yLimit, in LimitValue zLimit)
    def setSoftLimitCartesian(self, xLimit, yLimit, zLimit):
        raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result

    # RETURN_ID setSpeedCartesian(in ULONG spdRatio)
    def setSpeedCartesian(self, spdRatio):
        raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result

    # RETURN_ID setSpeedJoint(in ULONG spdRatio)
    def setSpeedJoint(self, spdRatio):
        raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result

    # RETURN_ID moveCircularCartesianAbs(in CarPosWithElbow carPointR, in CarPosWithElbow carPointT)
    def moveCircularCartesianAbs(self, carPointR, carPointT):
        raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result

    # RETURN_ID moveCircularCartesianRel(in CarPosWithElbow carPointR, in CarPosWithElbow carPointT)
    def moveCircularCartesianRel(self, carPointR, carPointT):
        raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result

    # RETURN_ID setHome(in JointPos jointPoint)
    def setHome(self, jointPoint):
        self._home = jointPoint
        return DATATYPES_IDL._0_JARA_ARM.RETURN_ID(DATATYPES_IDL._0_JARA_ARM.OK, '')

    # RETURN_ID getHome(out JointPos jointPoint)
    def getHome(self):
        return DATATYPES_IDL._0_JARA_ARM.RETURN_ID(DATATYPES_IDL._0_JARA_ARM.OK, ''), self._home

    # RETURN_ID goHome()
    def goHome(self):
        if self._controller:
            self._controller.movej(self._home)
            return DATATYPES_IDL._0_JARA_ARM.RETURN_ID(DATATYPES_IDL._0_JARA_ARM.OK, '')
        else:
            return DATATYPES_IDL._0_JARA_ARM.RETURN_ID(DATATYPES_IDL._0_JARA_ARM.NG, '')

if __name__ == "__main__":
    import sys

    # Initialise the ORB
    orb = CORBA.ORB_init(sys.argv)

    # As an example, we activate an object in the Root POA
    poa = orb.resolve_initial_references("RootPOA")

    # Create an instance of a servant class
    servant = ManipulatorCommonInterface_Middle_i()

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
