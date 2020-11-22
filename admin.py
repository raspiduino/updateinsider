#!/usr/bin/env python
# -*- coding: utf-8; mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vim: fileencoding=utf-8 tabstop=4 expandtab shiftwidth=4

# (C) COPYRIGHT © Preston Landers 2010
# Released under the same license as Python 2.6.5

# Got from https://stackoverflow.com/questions/19672352/how-to-run-python-script-with-elevated-privilege-on-windows
# Edited by raspiduino for Python 3

import os
import win32con
from win32com.shell import shellcon
from win32com.shell.shell import ShellExecuteEx

def isUserAdmin():
    if os.name == 'nt':
        import ctypes
        # WARNING: requires Windows XP SP2 or higher!
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            traceback.print_exc()
            print("Admin check failed, assuming not an admin.")
            return False
    elif os.name == 'posix':
        # Check for root on Posix
        return os.getuid() == 0
    else:
        raise RuntimeError("Unsupported operating system for this module: %s" % (os.name,))

def runAsAdmin(cmdLine=None):
    # Run the given cmdLine as Admin (Windows) or root (Linux/MacOS)
    if os.name == "nt":
        # For Windows
        procInfo = ShellExecuteEx(nShow=win32con.SW_SHOWNORMAL,
                                  fMask=shellcon.SEE_MASK_NOCLOSEPROCESS,
                                  lpVerb="runas",
                                  lpFile=cmdLine.split(" ")[0],
                                  lpParameters=" ".join(cmdLine.split(" ")[1:]))
    else:
        # For Linux and MacOS
        os.system("sudo " + cmdLine)
