#! /usr/bin/python

import sys
import time
import datetime
from subprocess import call, Popen, PIPE
from threading import Thread, Event
from my_template_matching import *

############################
# Class AdbRobot
############################


class AdbRobot():

##########
# Tables #
##########
    touchActions = {}
    androidActions = {"powerKey": "KEYCODE_POWER",
                            "menuKey": "KEYCODE_MENU",
                            "homeKey": "KEYCODE_HOME",
                            "backKey": "KEYCODE_BACK",
                            "volumeUp": "KEYCODE_VOLUME_UP",
                            "volumeDown": "KEYCODE_VOLUME_DOWN"
                        }
    swipeActions = {}
    adbActions = {"screenCap": "screencap -p /sdcard/screen_%s.png",
                            "pullLog": "adb pull /data/logs log_%s"
                        }

    timestamp_format_commands = ("screenCap", "pullLog", "other_command")

    actions = []
    ACTION_TABLES = ((touchActions, "input tap"), (adbActions, ""),
                     (androidActions, "input keyevent"), (swipeActions, "input swipe"))
    NUM_SCREEN_THREADS = 1
    SCREEN_SHOT_STORE_PATH = "./screen_tmp.png"
    MATCHING_METHOD = "cv2.TM_CCOEFF_NORMED"
#################
# Function Part #
#################

    def __init__(self):
        self.touchActionTableName = "touchActions.tab"
        self.swipeActionTableName = "swipeActions.tab"
        self.repeatProcedureName = ""
        self.stopPatternName = ""
        self.stopPattern = None
        self.cmdInterval = 2
        self.repeatCount = 1
        self.readTable(self.touchActionTableName, self.touchActions)
        self.readTable(self.swipeActionTableName, self.swipeActions)
        self.device = None
        self.cmds = []
        self.names = []
        self.cmd_timings = []
        self.screencapThreads = []
        self.cmdThread = None
        self.matching_threshold = 0.9

    def setDevice(self, device):
        self.device = device

    def getDevice(self):
        return self.device

    def setTouchActionTable(self, table_name):
        self.touchActionTableName = table_name
        self.readTable(table_name, self.touchActions)

    def setSwipeActionTable(self, table_name):
        self.swipeActionTableName = table_name
        self.readTable(table_name, self.swipeActions)

    def setRepeatProcedure(self, procedure_name):
        self.repeatProcedureName = procedure_name
        self.readProcedure()

    def setStopPattern(self, pattern_name):
        self.stopPatternName = pattern_name
        self.stopPattern = self.getCVImage(pattern_name)

    def getCVImage(self, image_path):
        return get_image(image_path)

    def isNeedScreenThread(self):
        return self.stopPattern is not None

    def screenThreadWork(self, thread_name):
        print(thread_name + " start!")
        has_pattern = False
        while not has_pattern and self.cmdThread.isAlive():
            # get screen cap
            self.getScreenShot(self.SCREEN_SHOT_STORE_PATH)
            # check if is there a pattern in the screencap
            has_pattern = is_pattern_in_image(
                self.stopPatternName, self.SCREEN_SHOT_STORE_PATH, self.MATCHING_METHOD, self.matching_threshold, True)
            print("HAS PATTERN ? " + str(has_pattern))
            if has_pattern is True:
                cmd = ["adb"]
                serial = self.device.getSerial()
                if serial != "":
                    cmd.extend(["-s", serial])
                cmd.extend(["shell", "date"])

            adbStdout, err = Popen(cmd, stdout=PIPE).communicate()
            print("date: %s" % adbStdout)

        print(thread_name + " exit!")

    def cmdThreadWork(self, thread_name):
        print(thread_name + " start!")
        for i in range(0, self.repeatCount):
            print("looptimes: " + str(i))
            timeStamp = datetime.datetime.fromtimestamp(
                time.time()).strftime('%Y%m%d%H%M%S')
            for name, cmd, timing in zip(self.names, self.cmds, self.cmd_timings):
                if name in self.timestamp_format_commands:
                    cmd = cmd % timeStamp
                print(name + ": " + cmd)
                print("sleep " + timing)
                self.doAction(cmd.split(" "));
                call(["sleep", timing]);

        print(thread_name + " exit!")

    def createThreads(self, thread_work, thread_name, num_threads=NUM_SCREEN_THREADS):
        threads = [Thread(target=thread_work, args=(thread_name+"-%d" % i,))
                          for i in range(num_threads)]
        return threads

    def setCmdInterval(self, t_interval):
        self.cmdInterval = t_interval

    def getRepeatCound(self):
        return self.repeatCount

    def setRepeatCount(self, count):
        self.repeatCount = count

    def doAction(self, actions):
        self.device.adbAction(actions)

    def getScreenShot(self, store_path):
        self.device.getScreenShot(store_path)

    def getScreenShot(self):
        return self.device.getScreenShot()

    def dumpTable(self, table):
        for k, v in table.items():
            print(k + ": " + v)

    def readTable(self, filename, table):
        table.clear()
        with open(filename) as fd:
            table.update(dict([line.strip().split(": ", 1) for line in fd]))

    def readProcedure(self):
        if self.repeatProcedureName != "" and self.repeatProcedureName != None:
            with open(self.repeatProcedureName) as f:
                self.setActions(f.read().splitlines())

    def setActions(self, actions):
        self.actions = actions

    def getCmds(self):
        return self.cmds

    def convertActionsToCmds(self):
        for action in self.actions:
            if action == "":
                continue
            cmd = None
            timing = self.cmdInterval;
            if "," in action:
                action_list = action.split(",")
                action = action_list[0]
                timing = action_list[1]

            for table, prefix in self.ACTION_TABLES:
                # print(table)
                cmd = table.get(action, None)
                if cmd != None:
                    cmd = prefix + " " + cmd
                    self.cmds.append(cmd)
                    self.names.append(action)
                    self.cmd_timings.append(str(timing))
                    break
            if cmd == None:
                print(table)
                print(
                    "%s is not existed in action tables, it will be igonre" % action)

    def doWork(self):

        self.cmdThread = self.createThreads(
            self.cmdThreadWork, "CmdThread", 1)[0]
        self.cmdThread.setDaemon(True)
        self.cmdThread.start()

        if self.isNeedScreenThread():
            self.screencapThreads = self.createThreads(
                self.screenThreadWork, "ScreenThread")
            # set daemon befor thread start
            list(map(lambda th: th.setDaemon(True), self.screencapThreads))
            list(map(lambda th: th.start(), self.screencapThreads))
            list(map(lambda th: th.join(), self.screencapThreads))
            print("ScreenCap thread stop, exit!")
            return

        exit_flag = Event()
        while self.cmdThread.isAlive():
            exit_flag.wait(timeout=10.0)


############################
# Class AdbDevice
############################

class AdbDevice():

    nonShellCmds = {"root", "remount", "devices", "kill-server",
        "wait-for-device", "bugreport", "pull", "push"}
    TEMP_SCREENCAP_PATH = "/sdcard/temp_screen.png"

    def __init__(self):
        self.serial = None

    def setSerial(self, serial):
        self.serial = serial

    def getSerial(self):
        return self.serial

    def getDevices(self):
        adbStdout, err = Popen(["adb", "devices"], stdout=PIPE).communicate()
        adbStdoutList = adbStdout.splitlines()
        adbDevices = []
        print(adbStdoutList)
        for item in adbStdoutList:
            print(item)
            temp = item.decode().split('\t')
            if len(temp) == 2 and temp[1] == "device":
                adbDevices.append(temp[0])

        if len(adbDevices) > 1:
            while(1):
                for device in adbDevices:
                    print(adbDevices.index(device)+1, ")", device)
                deviceInput = sys.stdin.readline()
                if int(deviceInput) < len(adbDevices)+1 and int(deviceInput) >= 1:
                    break
            return adbDevices[int(deviceInput)-1]
        elif len(adbDevices) == 1:
            return adbDevices[0]
        else:
            # print "No devices is connected."
            # exit()
            return None

    def adbAction(self, action):
        cmd = ["adb"]
        if self.serial != None:
            cmd.extend(["-s", self.serial])
        if self.isNeedShell(action):
            cmd.append("shell")
        cmd.extend(action)
        print(cmd)
        call(cmd)
    
    def isNeedShell(self, action):
        for cmd in self.nonShellCmds:
            if cmd in action:  # find a cmd without "shell" prefix
                return False
        return True
    
    def getScreenShot(self, store_path):
        self.adbAction(["screencap -p", self.TEMP_SCREENCAP_PATH])
        self.pull(self.TEMP_SCREENCAP_PATH, store_path)
        self.adbAction(["rm", self.TEMP_SCREENCAP_PATH])
    
    def getScreenShot(self):
        adbStdout, err = Popen(["adb", "shell", "screencap", "-p"], stdout=PIPE).communicate()
        return adbStdout

    def pull(self, stuff_path, local_path):
        self.adbAction(["pull", stuff_path, local_path])

    def push(self, stuff, device_path):
        self.adbAction(["push", stuff_path, device_path])
