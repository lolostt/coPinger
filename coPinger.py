#!/usr/bin/env python3
#build 6

# This script will read HOSTS_FILE and ping machines on it. It will generate a json report.
# Requirements: 
# - Plain text file with comma separated entries. Ex: router,192.168.1.1

# Copyright (C) 2025 Sleeping Coconut https://sleepingcoconut.com

#----VARIABLES--------------------------------------------------------------------------------------
#Files
HOSTS_FILE = 'machines.txt'
REPORT_FILE = 'copinger_report.json'

#Script behaviour
DEBUG=0
SIMULTANEOUS_PINGS=4
SIMULTANEOUS_PINGS_LIMIT=51
REPORT_INDENT=2

# Zero Clause BSD license {{{
#
# Permission to use, copy, modify, and/or distribute this software for any purpose with or without 
# fee is hereby granted.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS 
# SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE
# AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
# NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE
# OF THIS SOFTWARE.
# }}}

#----HARDCODED VARIABLES----------------------------------------------------------------------------
#Requirements
PYTHON_REQUIRED_VERSION=(3,3)
REQUIRED_TOOLS=(['ping'])

#----PYTHON VERSION CHECK---------------------------------------------------------------------------
import sys
if sys.version_info < PYTHON_REQUIRED_VERSION:
    sys.stderr.write('Python {}.{} is required. Current version: {}.{}\n'.format(
        PYTHON_REQUIRED_VERSION[0],
        PYTHON_REQUIRED_VERSION[1],
        sys.version_info[0],
        sys.version_info[1])
    )
    sys.exit(1)

#----DEPENDENCIES CHECK-----------------------------------------------------------------------------
from shutil import which
for tool in REQUIRED_TOOLS:
    if which(tool) is None:
        sys.stderr.write('One o more required tools are missing in your system. ' \
                        'Please install them or make them avaiable in PATH.\n' \
                        'Required tools: ')
        for tool in REQUIRED_TOOLS:
            sys.stderr.write(tool)
            if tool is not REQUIRED_TOOLS[-1]:
                sys.stderr.write(', ')
            else:
                sys.stderr.write('.\n')
        exit(1)

#----IMPORTS----------------------------------------------------------------------------------------
import platform                     # For getting the operating system name
import os                           # For getting absolute paths
from subprocess import PIPE, run    # For executing a shell command
import json                         # For writing json file
import concurrent.futures           # For scheduling threads

#----FUNCTIONS--------------------------------------------------------------------------------------
def allIsGood(): # main support: only executed if no exceptions raised.
    print('-> All done.')

def debug(any): # main support: debug mode
    if DEBUG:
        print('DEBUG:',any)

def checkLen(matrix): # readFile support: empty fields detection
    for row in matrix:
        for column in row:
            if not column:
                raise NameError('Error processing hosts file: malformed. Field may be missing.')

def readFile(): # reads file
    try:
        reader=open(HOSTS_FILE_FULLPATH, 'r')
    except:
        raise NameError('Error opening hosts file')
    else:
        for line in reader:
            try:
                currentline = line.strip().split(',')
                hosts.append([currentline[0],currentline[1]])
            except IndexError:
                raise NameError('Error processing hosts file: malformed. ' \
                                'Field or comma separator may be missing.')
        checkLen(hosts)

def ping(ip): # executes ping to 'ip' argument.
              # Modified from: https://stackoverflow.com/questions/2953462/pinging-servers-in-python
    debug('executing ping to '+ip)
    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower()=='windows' else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', ip]

    result = run(command, stdout=PIPE, stderr=PIPE, text=True)
    return result.returncode

def launchPings(matrix): # launches sequential pings
    for row in matrix:
        if ping(row[1]):
            results.append([row[0],False])
        else:
            results.append([row[0],True])

def launchAsyncPings(matrix): # launches asynchronous pings using 'pinger' function
    with concurrent.futures.ThreadPoolExecutor(max_workers = SIMULTANEOUS_PINGS) as executor:
        for row in matrix:
            debug('submitting '+row[1])
            executor.submit(pinger, row)

def pinger(host): # launchAsyncPings support
    debug('pinger '+host[1])
    if ping(host[1]):
        results.append([host[0],False])
    else:
        results.append([host[0],True])

def writeReport(): # writes JSON report
    try:
        writer=open(REPORT_FILE_FULLPATH, 'w')
    except:
        raise NameError('Error opening report file')
    else:
        json.dump(results, writer, indent = REPORT_INDENT)

#----SCRIPT-----------------------------------------------------------------------------------------
hosts = []      # stores read data
results = []    # stores data before write
HOSTS_FILE_FULLPATH = os.path.dirname(os.path.realpath(__file__)) + '/' + HOSTS_FILE
REPORT_FILE_FULLPATH = os.path.dirname(os.path.realpath(__file__)) + '/' + REPORT_FILE

try:
    readFile()
    if SIMULTANEOUS_PINGS >= SIMULTANEOUS_PINGS_LIMIT:
        raise NameError('unsafe simultaneous pings amount. Stopping.')
    elif SIMULTANEOUS_PINGS >= 2:
        print('-> Working (async mode)...')
        launchAsyncPings(hosts)
    elif SIMULTANEOUS_PINGS == 1:
        print('-> Working (sync mode)...')
        launchPings(hosts)
    else:
        raise NameError('invalid "SIMULTANEOUS_PINGS" variable')
    writeReport()
except Exception as err:
    print('-> Script execution stopped:',err)
else:
    allIsGood()