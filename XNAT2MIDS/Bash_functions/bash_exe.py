# -*- coding: utf-8 -*-

###############################################################################
# Imports
###############################################################################
import shlex
import subprocess

###############################################################################
# Functions
###############################################################################

"""
this function aloww the user execute instructions in bash
STDOUT y STDERR
"""
def bash_command(command_line):
    args = shlex.split(command_line)
    #print ((command_line))
    #print((args))
    try:
        if '*' in command_line:
            raise OSError
        proc = subprocess.Popen(args, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    except OSError:
        #print("bash command is executed by shell=True")
        proc = subprocess.Popen(command_line, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, shell=True)
        out, err = proc.communicate()
    return [out.decode('utf-8'), err.decode('utf-8')]
