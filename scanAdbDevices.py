#!/usr/bin/python

import sys
from subprocess import call, Popen, PIPE

call(["adb", "devices"])

adbStdout, err = Popen(["adb", "devices"], stdout=PIPE).communicate()

print(adbStdout)


adbStdoutList = adbStdout.splitlines()
print(adbStdoutList)
adbDevices = []
for item in adbStdoutList:
	temp = item.split('\t')
	if len(temp) == 2 and temp[1] == "device":
		print(temp[0])
		adbDevices.append(temp[0])

if len(adbDevices) > 1:
	while(1):
		for device in adbDevices:
			print(adbDevices.index(device), ")" , device)
		deviceInput = sys.stdin.readline()
		if int(deviceInput) < len(adbDevices) and int(deviceInput) >= 0:
			break	
	serial = adbDevices[int(deviceInput)]
elif len(adbDevices) == 1:
	serial = adbDevices[0]
else:
	print("No device is connected.")
	exit()
print(serial)
