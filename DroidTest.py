#! /usr/bin/env python2

import sys
import argparse
from adbutils import AdbRobot, AdbDevice

if __name__ == '__main__':
    args = [ str(argv) for argv in sys.argv ]


    __author__ = 'Balaji Muhammad'

    #configure parser
    parser = argparse.ArgumentParser(description='This is broken from Baliji, but crashed by Muhammand')
    parser.add_argument('actions',metavar='ACTION', nargs='*', help='actions to be performed in a single flow. Format: action_name,delay_ms', default='')
    parser.add_argument('-s','--serial', help='serial# of the device, use this argument if you have 2+ devices', required=False, dest='serial', default=None)
    parser.add_argument('--touch-table', metavar='TOUCH_ACTION_TABLE', help='the name of touch action table. default: touchActions.tab', required=False, dest='touchTable', default='touchActions.tab')
    parser.add_argument('--swipe-table',metavar='SWIPE_ACTION_TABLE', help='the name of swipe action table. default: swipeActions.tab', required=False, dest='swipeTable', default='swipeActions.tab')
    parser.add_argument('--interval', metavar='ACTION_INTERVAL', help='the internal between two actions. default: 2s', required=False, dest='interval', default='2')
    parser.add_argument('-t', '--repeat', metavar='REPEAT_COUNT', help='the number of times to repeat assigned actions. default: 1', required=False, dest='repeatCount', default=1, type=int)
    parser.add_argument('-p', metavar='PROCEDURE', help='the name of repeat procedure. ex: example.procedure', required=False, dest='repeatProcedure', default='')
    parser.add_argument('--stop-pattern',metavar='STOP_PATTERN', help='the path of stop pattern which can triger droid stop. ex: ./pattern.png', required=False, dest='stopPatternPath', default='')
    
    args = parser.parse_args()
    
    adb_robot = AdbRobot()
    adb_device = AdbDevice()
    
    if args.serial is None:
        serial = adb_device.getDevices()
        if serial is None:
            print("No devices is connected.")
            exit()
    adb_device.setSerial(serial)   
    adb_robot.setDevice(adb_device)

    repeatCount = args.repeatCount
    adb_robot.setRepeatCount(repeatCount)
    adb_robot.setTouchActionTable(args.touchTable)
    adb_robot.setSwipeActionTable(args.swipeTable)
    default_timing = args.interval
    adb_robot.setCmdInterval(default_timing)
    stopPatternPath = args.stopPatternPath
    adb_robot.setStopPattern(stopPatternPath)
    
    ## show values ##
    #print args
    
    #dumpTable(touchActions)
    #dumpTable(swipeActions)
    
    #show procedure actions
    #print args.actions
    adb_robot.setActions(args.actions)
    adb_robot.setRepeatProcedure(args.repeatProcedure)

    adb_robot.convertActionsToCmds()
    if adb_robot.getCmds() == []:
    	parser.print_help()
    	exit()
    
    adb_robot.doWork()

	    
