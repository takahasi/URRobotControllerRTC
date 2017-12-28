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
import JARA_ARM, JARA_ARM__POA


class ManipulatorCommonInterface_Common_i (JARA_ARM__POA.ManipulatorCommonInterface_Common):
    """
    @class ManipulatorCommonInterface_Common_i
    Example class implementing IDL interface JARA_ARM.ManipulatorCommonInterface_Common
    """

    def __init__(self):
        """
        @brief standard constructor
        Initialise member variables here
        """
        pass

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
        raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result, pos

    # RETURN_ID getManipInfo(out ManipInfo mInfo)
    def getManipInfo(self):
        raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result, mInfo

    # RETURN_ID getSoftLimitJoint(out LimitSeq softLimit)
    def getSoftLimitJoint(self):
        raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result, softLimit

    # RETURN_ID getState(out ULONG state)
    def getState(self):
        raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result, state

    # RETURN_ID servoOFF()
    def servoOFF(self):
        raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result

    # RETURN_ID servoON()
    def servoON(self):
        raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
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
    print orb.object_to_string(objref)

    # Activate the Root POA's manager
    poa._get_the_POAManager().activate()

    # Run the ORB, blocking this thread
    orb.run()

