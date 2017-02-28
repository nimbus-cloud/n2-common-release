#!/usr/bin/env python
import time
import sys
import os.path
import re

def drbd_state():

  drbd = {"connection_state": "not running", "role": "", "disk_state": "", "sync_state": ""}

  if os.path.exists("/proc/drbd"):
    with open("/proc/drbd", 'r') as file:
      for line in file:

        m = re.search("cs:(\S+)\s+ro:(\S+)\s+ds:(\S+)", line)
        if m:
          drbd["connection_state"] = m.group(1)
          drbd["role"] = m.group(2)
          drbd["disk_state"] = m.group(3)

        m = re.search("\s*[\[\>\.\]]+\s*sync'ed:\s*(.+)", line)
        if m:
          drbd["sync_state"] = m.group(1)

        m = re.search("^\s*(finish:.+)$", line)
        if m:
          drbd["sync_state"] = drbd["sync_state"] + m.group(1)

  return drbd

def log(message):
  print "%s: %s" % (time.strftime("%c"), message)

def fail(message):
  print "%s: %s" % (time.strftime("%c"), message)
  sys.exit(1)

def main():
  log("Checking drbd status...")
  drbd = drbd_state()
  if drbd["connection_state"] != "Connected":
    fail("Failed: connection state incorrect... current state is %s" % drbd["connection_state"])
  if drbd["disk_state"] != "UpToDate/UpToDate":
    fail("Failed: disk state is not uptodate... current state is %s" % drbd["disk_state"])
  log("...all good")
  sys.exit(0)

main()
