#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
sys.path.append(".")
sys.path.append("..")

from URRobotController import URRobotController as urrobot


__author__ = "Saburo Takahashi"
__copyright__ = "Copyright 2017, Saburo Takahashi"
__license__ = "LGPLv3"


def test():
    try:
        r = urrobot()
        print("### start_freedrive()")
        r.start_freedrive()
        for i in range(30):
            print("### getl(): pose in meter, rad")
            print(r.getl())
            print("### getj(): joints in rad")
            print(r.getj())
            print("### get_force(): TCP force")
            print(r.get_force())
            time.sleep(1)
        print("### end_freedrive()")
        r.end_freedrive()

    except urrobot.URxException:
        print("### Failed. URx exception")
    except Exception as e:
        print("### Failed. Exception: " + format(str(e)))
    finally:
        r.finalize()
        del(r)


if __name__ == '__main__':
    test()
