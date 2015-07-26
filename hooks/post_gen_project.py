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


print "Attempting to create pyenv virtualenv {{cookiecutter.package_name}}"

if which("pyenv"):
    cmd = ["pyenv", "virtualenv"]
    out, err, errcode = run_command(cmd)

    if 'virtualenv name given' in err:

        cmd = ["pyenv", "versions"]
        out, err, errcode = run_command(cmd)

        if errcode == 0 and "{{cookiecutter.package_name}}" not in out:
            cmd = ["pyenv", "virtualenv", "{{cookiecutter.package_name}}"]
            out, err, errcode = run_command(cmd)

            if errcode == 0:
                print "Created virtualenv {{cookiecutter.package_name}}"

                cmd = ["pyenv", "local", "{{cookiecutter.package_name}}"]
                out, err, errcode = run_command(cmd)

                if errcode == 0:
                    print "Set `pyenv local {{cookiecutter.package_name}}`"
                else:
                    print ("An error occurred trying to set "
                           "`pyenv local {{cookiecutter.package_name}}`")
            else:
                print ("An error occurred trying to create virtualenv "
                       "{{cookiecutter.package_name}}.  Please check your "
                       "pyenv installation.")
        else:
            print ("An error occurred looking for a virtualenv "
                   "named {{cookiecutter.package_name}}.  It looks like you "
                   "already have a virtualenv installed "
                   "named {{cookiecutter.package_name}}. Please manually "
                   "remove it. Skipping.")
    else:
        print ("An error occurred trying to create virtualenv "
               "{{cookiecutter.package_name}}. Do you have the pyenv "
               "virtualenv, plugin installed?")


print "Finished creating virtualenv {{cookiecutter.package_name}}\n"

print "Attempting to copy over teamocil file"

if os.path.isfile("etc/{{cookiecutter.package_name}}.yml") and os.path.exists(os.path.expanduser("~/.teamocil")):
    if not os.path.isfile(os.path.expanduser("~/.teamocil/{{cookiecutter.package_name}}.yml")):
        shutil.move("etc/{{cookiecutter.package_name}}.yml",
                    os.path.expanduser("~/.teamocil/{{cookiecutter.package_name}}.yml"))
        print "Teamocil directory found, copied over teamocil file"
    else:
        print "Teamocil file already exists. Skipping."

print "Finished copying over teamocil file\n"

# vim: filetype=python
