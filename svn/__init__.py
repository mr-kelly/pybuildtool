#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pybuildtool as tool
import platform
import subprocess
import os, re
from svn_unversioned_rm import do_svn, remove_link

def run_command(*args):
    return tool.run_command(*args)

def svn_unversioned_rm(*args):
    return rm_unversioned(*args)

def rm_unversioned(path, ignorepath=None):
    """
    移除不受版本控制的文件
    :param path:
    :param ignorepath:
    :return:
    """
    do_svn(path, ignorepath)


def svn_revert(*args):
    return revert(*args)

def revert(localpath):
    """
    回退修改，保持版本不变
    :param localpath:
    :return:
    """
    # os.chdir(localpath)

    revert_cmd= ['svn', 'revert', localpath, '--depth', 'infinity']
    result = run_command(revert_cmd)
    print "The local path is %s,revert status:%s" % (localpath, result)


def add(*args):
    return svn_add(*args)

def svn_add(localpath):
    """
    增加文件
    :param localpath:
    :return:
    """
    os.chdir(localpath)

    svn_add_cmd = ['svn', 'add', localpath, '--force']
    run_command(svn_add_cmd)


def svn_checkout(*args):
    return checkout(*args)

def checkout(svnurl, localpath):
    cmd = ['svn', 'co', svnurl, localpath]
    run_command(cmd)

def svn_switch(*args):
    return switch(*args)

def switch(svnurl, path, revision=None):
    """
    svn switch
    :return:
    """
    svn_up_cmd = ['svn', 'switch', svnurl, path, '--accept', 'theirs-full', '--force']

    if revision:
        svn_up_cmd.append('-r')
        svn_up_cmd.append(revision)

    if 'Windows' in platform.platform():
        path += '\\'
        run_command(svn_up_cmd)
    else:
        run_command(svn_up_cmd)

def svn_up(path):
    """
    svn up
    :return:
    """
    svn_up_cmd = ['svn', 'up', path]
    if 'Windows' in platform.platform():
        path += '\\'
        run_command(svn_up_cmd)
    else:
        run_command(svn_up_cmd)


def find_svn_rm_files(find_path):
    """
    找出所有要删除的文件名
    :param find_path:
    :return:
    """
    os.chdir(find_path)
    miss_match = re.compile(r'^!')
    svn_rm_files = []
    status_cmd = ['svn', 'status']

    result = subprocess.Popen(status_cmd, shell=True, stdout=subprocess.PIPE)
    result_output = result.stdout.readlines()

    for result_line in result_output:
        if miss_match.match(result_line):
            filename = result_line.split()[-1].strip()
            svn_rm_files.append(filename)
    return svn_rm_files


def svn_rm(rm_path, all_files):
    """
     svn rm file
    :param rm_path:
    :param all_files:
    :return:
    """
    os.chdir(rm_path)

    for rm_file in all_files:
        rm_cmd = ['svn', 'rm', rm_file]
        run_command(rm_cmd)

def svn_commit(local_path, message):
    if type(local_path) == str:
        paths = [local_path]
    else:
        paths = local_path

    commit_cmd = ['svn', 'commit'] + paths + ['-m', message]


    run_command(commit_cmd)


def commit(*args):
    return svn_commit(*args)
    


def up_all(workspace, svn_url, clean_ignore):
    """
    Auto Checkout + Unversioned Remove + Revert + Switch
    """
    print 'Up all -> Working dir: %s' % workspace
    if not os.path.isdir(workspace):
        print 'check out new product...'
        tool.svn.svn_checkout(svn_url, workspace)

    tool.svn.svn_unversioned_rm(workspace, clean_ignore)
    tool.svn.svn_revert(workspace)
    tool.svn.switch(svn_url,workspace)