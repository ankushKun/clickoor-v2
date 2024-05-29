import os

lines = os.popen("sudo iwlist wlan0 scan").read().split("\n")
for line in lines:
    line = line.rstrip()
    if line != "" and "ESSID" in line:
        name = line.split('"')[1]
        print(name)
