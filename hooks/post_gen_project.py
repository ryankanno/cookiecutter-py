#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path
import shutil
import subprocess


def which(program):
    try:
        devnull = open(os.devnull)
        subprocess.Popen(
            [program],
            stdout=devnull,
            stderr=devnull).communicate()
    except OSError as e:
        if e.errno == os.errno.ENOENT:
            return False
    return True


def run_command(cmd):
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)

    out, err = process.communicate()
    errcode = process.returncode
    return (out, err, errcode)


print "Attempting to create pyenv virtualenv {{cookiecutter.module_name}}"

if which("pyenv"):
    cmd = ["pyenv", "virtualenv"]
    out, err, errcode = run_command(cmd)

    if 'virtualenv name given' in err:

        cmd = ["pyenv", "versions"]
        out, err, errcode = run_command(cmd)

        if errcode == 0 and "{{cookiecutter.module_name}}" not in out:
            cmd = ["pyenv", "virtualenv", "{{cookiecutter.module_name}}"]
            out, err, errcode = run_command(cmd)

            if errcode == 0:
                print "Created virtualenv {{cookiecutter.module_name}}"

                cmd = ["pyenv", "local", "{{cookiecutter.module_name}}"]
                out, err, errcode = run_command(cmd)

                if errcode == 0:
                    print "Set `pyenv local {{cookiecutter.module_name}}`"
                else:
                    print ("An error occurred trying to set "
                           "`pyenv local {{cookiecutter.module_name}}`")
            else:
                print ("An error occurred trying to create virtualenv "
                       "{{cookiecutter.module_name}}.  Please check your "
                       "pyenv installation.")
        else:
            print ("An error occurred looking for a virtualenv "
                   "named {{cookiecutter.module_name}}.  It looks like you "
                   "already have a virtualenv installed "
                   "named {{cookiecutter.module_name}}. Please manually "
                   "remove it. Skipping.")
    else:
        print ("An error occurred trying to create virtualenv "
               "{{cookiecutter.module_name}}. Do you have the pyenv "
               "virtualenv, plugin installed?")


print "Finished creating virtualenv {{cookiecutter.module_name}}\n"

print "Attempting to copy over teamocil file"

if os.path.isfile("etc/{{cookiecutter.module_name}}.yml") and os.path.exists(os.path.expanduser("~/.teamocil")):
    if not os.path.isfile(os.path.expanduser("~/.teamocil/{{cookiecutter.module_name}}.yml")):
        shutil.move("etc/{{cookiecutter.module_name}}.yml",
                    os.path.expanduser("~/.teamocil/{{cookiecutter.module_name}}.yml"))
        print "Teamocil directory found, copied over teamocil file"
    else:
        print "Teamocil file already exists. Skipping."

print "Finished copying over teamocil file\n"

# vim: filetype=python
