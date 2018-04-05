URRobotControllerRTC
=====================

This is RT-Component(RTC) for Universal Robot(URx)

Service Port
------------
ManipulatorCommonInterfaceIDL
- ManipulatorCommonInterface

|InterfaceName|Support|
----|----
|clearAlarms||
|getActiveAlarm||
|getFeedbackPosJoint|○|
|getManipInfo|○|
|getSoftLimitJoint|○|
|getState|○|
|servoOFF||
|servoON||
|setSoftLimitJoint||

- ManipulatorMiddleInterface

|InterfaceName|Support|
----|----
|closeGripper|○|
|getBaseOffset|○|
|getFeedBackPosCartesian||
|getMaxSpeedCartesian||
|getMaxSpeedJoint|○|
|getMinAccelTimeCartesian||
|getMinAccelTimeJoint||
|getSoftLimitCartesian||
|moveGripper|○|
|moveLinearCartesianAbs||
|moveLinearCartesianRel||
|movePTPJointAbs|○|
|movePTPJointRel|○|
|openGripper|○|
|pause|○|
|resume|○|
|stop|○|
|setAccelTimeJoint||
|setBaseOffset||
|setControlPointOffset||
|setMaxSpeedCartesian||
|setMaxSpeedJoint||
|setMinAccelTimeCartesian||
|setMinAccelTimeJoint||
|setSoftLimitCartesian||
|setSpeedCartesian||
|setSpeedJoint||
|moveCircularCartesianAbs||
|moveCircularCartesianRel||
|setHome|○|
|getHome|○|
|goHome|○|

Preparation
-----------
```
$ sudo pip install urx
$ sudo pip install math3d
```

Required version: urx >= 0.11

Usage
-----------
```
$ python URRobotControllerRTC.py
```

Unit Test (Use real robot)
-----------
Connects actual URx robot via network
```
$ python test/test_robot.py
```

Unit Test (Use dummy server)
-----------
```
$ git clone https://github.com/SintefRaufossManufacturing/python-urx
$ python python-urx/tools/fakerobot.py
$ python tests/test_fakerobot.py
```

Integration Test
----------------
```
$ sh tests/test_component.sh
```
