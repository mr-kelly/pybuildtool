#!/usr/bin/env python
# -*- coding: utf-8 -*-

import platform
import fileinput
import subprocess
import os
import sys
reload(sys)

import system
import svn
import shutil
from shutil import *
import unity_realtime_log as unity

sys.setdefaultencoding('utf-8')


print """
****************************
author:
    Peilin Kelly Chan <https://github.com/mr-kelly>

description:
    Useful python build tool scripts, for command line control
***************************


"""


def run_command(cmd, cwd=None):
    print '\n\n'
    print '*****************************************************************************'
    print '========== [Run Command] ' + ' '.join(cmd) + '=========='
    print '*****************************************************************************'
    print '\n'
    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=cwd
    )
    while True:
        out = process.stdout.read(1)
        if out == '' and process.poll() != None:
            break
        if out != '':
            sys.stdout.write(out)
            sys.stdout.flush()


def fullpath(relative_path):
    return os.path.abspath(os.path.expanduser(relative_path))


def copytree(src, dst, symlinks=False, ignore=None):
    """
    auto overwrite tree
    """
    names = os.listdir(src)
    if ignore is not None:
        ignored_names = ignore(src, names)
    else:
        ignored_names = set()

    if not os.path.isdir(dst): # This one line does the trick
        os.makedirs(dst)
    errors = []
    for name in names:
        if name in ignored_names:
            continue
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if symlinks and os.path.islink(srcname):
                linkto = os.readlink(srcname)
                os.symlink(linkto, dstname)
            elif os.path.isdir(srcname):
                copytree(srcname, dstname, symlinks, ignore)
            else:
                # Will raise a SpecialFileError for unsupported file types
                copy2(srcname, dstname)
        # catch the Error from the recursive copytree so that we can
        # continue with other files
        except Exception, err:
            errors.extend(err.args[0])
        except EnvironmentError, why:
            errors.append((srcname, dstname, str(why)))
    try:
        shutil.copystat(src, dst)
    except OSError, why:
        if WindowsError is not None and isinstance(why, WindowsError):
            # Copying file access times may fail on Windows
            pass
        else:
            errors.extend((src, dst, str(why)))
    if errors:
        raise Exception, errors
