URRobotControllerRTC
=====================

This is RT-Component(RTC) for Universal Robot(URx)

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
```
$ python test/test_robot.py
```

Unit Test (Use dummy server)
-----------
```
$ git clone https://github.com/SintefRaufossManufacturing/python-urx
$ python python-urx/tools/fakerobot.py
$ python tests/test_robot.py
```

Integration Test
----------------
```
$ sh tests/test_component.sh
```
