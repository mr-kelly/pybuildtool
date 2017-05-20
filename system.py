

import sys, os, platform

def is_macos():
    return 'Darwin' in platform.platform()


def is_windows():
    return 'Windows' in platform.platform()

def is_linux():
    return 'Linux' in platform.platform()
