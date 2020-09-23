#!/usr/bin/env python3
#build 1
import platform                     # For getting the operating system name
from subprocess import PIPE, run    # For executing a shell command
import json                         # For writing json file
import concurrent.futures           # For scheduling threads


# This script will...
# Requirements: -

# Copyright (C) 2020 Sleeping Coconut https://sleepingcoconut.com

#----------VARIABLES----------
HOSTS_FILE='machines.txt'
REPORT_FILE='copinger_report.json'

DEBUG=0
SIMULTANEOUS_PINGS=4
REPORT_INDENT=2

# Zero Clause BSD license {{{
#
# Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL 
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, 
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN 
# AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE 
# OF THIS SOFTWARE.
# }}}

#----------FUNCTIONS----------
def allIsGood():
    print('-> All done.')

def debug(any):
    if DEBUG:
        print('DEBUG:',any)

def checkLen(matrix):
    for row in matrix:
        for column in row:
            #debug('pass on '+str(row)+' -> '+str(column))
            if not column:
                raise NameError('Error processing hosts file: malformed. Field may be missing.')

def readFile():
    try:
        reader=open(HOSTS_FILE, 'r')
    except:
        raise NameError('Error opening hosts file')
    else:
        for line in reader:
            try:
                currentline = line.strip().split(',')
                #debug(currentline[0]+'-'+currentline[1])
                hosts.append([currentline[0],currentline[1]])
            except IndexError:
                raise NameError('Error processing hosts file: malformed. Field or comma separator may be missing.')
        checkLen(hosts)

def ping(ip):
    debug('executing ping to '+ip)
    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower()=='windows' else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', ip]

    result = run(command, stdout=PIPE, stderr=PIPE, text=True)
    return result.returncode

def launchPings(matrix):
    for row in matrix:
        if ping(row[1]):
            results.append([row[0],False])
        else:
            results.append([row[0],True])

def launchAsyncPings(matrix):
    with concurrent.futures.ThreadPoolExecutor(max_workers = SIMULTANEOUS_PINGS) as executor:
        for row in matrix:
            debug('submitting '+row[1])
            executor.submit(pinger, row)

def pinger(host):
    debug('pinger '+host[1])
    if ping(host[1]):
        results.append([host[0],False])
    else:
        results.append([host[0],True])

def writeReport():
    try:
        writer=open(REPORT_FILE, 'w')
    except:
        raise NameError('Error opening report file')
    else:
        json.dump(results, writer, indent = REPORT_INDENT)

#----------SCRIPT----------
hosts = []
threads = []
results = []

print("-> Working...")
try:
    readFile()
    #launchPings(hosts)
    launchAsyncPings(hosts)
    writeReport()
except Exception as err:
    print("-----> Script execution stopped:",err)
else:
    allIsGood()