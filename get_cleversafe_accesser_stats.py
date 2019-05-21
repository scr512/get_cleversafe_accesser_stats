#!/usr/bin/python

import urllib2
import json
import time
import os
import sys
from socket import socket

CARBON_SERVER='carbon-relay.your.domain.com'
CARBON_PORT=2003
time = int( time.time() )

sock = socket()
try:
  sock.connect( (CARBON_SERVER,CARBON_PORT) )
except:
  print "Couldn't connect to %(server)s on port %(port)d, is carbon-agent.py running?" % { 'server':CARBON_SERVER, 'port':CARBON_PORT }
  sys.exit(1)

# Statistics API query
#```
#curl -sk "http://cleversafe-accesser-01.your.domain.com:8192/statistic" | python -mjson.tool
#```

# Stuff in JSON I care about
# accesserRtt
# accesserVault
# core
#  http
#   connectionsCurrent
#   connectionsMax
#   permitsWriters
#   permitsReaders
#  memory
#   system
#    totalBytes
#    usedBytes
#    percentUsed
# load
# loadX
#  average1
#  average5
#  average15
#  processesRunning
#  processesTotal
# network
#  bond0
#   in
#   out

accesser_name = (sys.argv[1])

# If you just want to hardcode your accesser rather than taking stdin input at execution.
#accesser_name = 'cleversafe-accesser-01.your.domain.com'

accesser_name_clean = accesser_name.replace(".","_")

r_device_statistics = urllib2.urlopen('http://{0}:8192/statistic'.format(accesser_name))
json_out_sp = json.load(r_device_statistics)
lines = []

# core->http
for key,value in json_out_sp['core']['http'].items():
  lines.append("cleversafe." + "accessor." + str(accesser_name_clean) + "." + "http." + str(key) + " " + str(value) + " " + str(time))

# accesserRequest->POST
for key,value in json_out_sp['accesserRequest']['POST'].iteritems():
  for subkey,subvalue in value.iteritems():
    lines.append("cleversafe." + "accesser." + str(accesser_name_clean) + "." + "request.post." + str(key) + "." + str(subkey) + " " + str(subvalue) + " " + str(time))

# accesserRequest->PUT
for key,value in json_out_sp['accesserRequest']['PUT'].iteritems():
  for subkey,subvalue in value.iteritems():
    lines.append("cleversafe." + "accesser." + str(accesser_name_clean) + "." + "request.put." + str(key) + "." + str(subkey) + " " + str(subvalue) + " " + str(time))

# accesserRequest->HEAD
for key,value in json_out_sp['accesserRequest']['HEAD'].iteritems():
  for subkey,subvalue in value.iteritems():
    lines.append("cleversafe." + "accesser." + str(accesser_name_clean) + "." + "request.head." + str(key) + "." + str(subkey) + " " + str(subvalue) + " " + str(time))

# accesserRequest->GET
for key,value in json_out_sp['accesserRequest']['GET'].iteritems():
  for subkey,subvalue in value.iteritems():
    lines.append("cleversafe." + "accesser." + str(accesser_name_clean) + "." + "request.get." + str(key) + "." + str(subkey) + " " + str(subvalue) + " " + str(time))


# Need to implement a lookup table for vault GUID to human name. You can enable if you're ok with GUIDs :)`
# accesserRtt
#for key,value in json_out_sp['accesserRtt'].iteritems():
#  for subkey,subvalue in value.iteritems():
#    lines.append("cleversafe." + "accesser." + str(accesser_name_clean) + "." + "accesserRtt." + str(key) + "." + str(subkey) + " " + str(subvalue) + " " + str(time))

# Same here
# accesserVault
#for key,value in json_out_sp['accesserVault'].iteritems():
#  for subkey,subvalue in value.iteritems():
#    lines.append("cleversafe." + "accesser." + str(accesser_name_clean) + "." + "accesserVault." + str(key) + "." + str(subkey) + " " + str(subvalue) + " " + str(time))

# network
for key,value in json_out_sp['network'].iteritems():
  for subkey,subvalue in value.iteritems():
    lines.append("cleversafe." + "accesser." + str(accesser_name_clean) + "." + "network." + str(key) + "." + str(subkey) + " " + str(subvalue) + " " + str(time))

# load
for key,value in json_out_sp['loadX'].iteritems():
  lines.append("cleversafe." + "accesser." + str(accesser_name_clean) + "." + "load." + str(key) + " " + str(value) + " " + str(time))

# memory
for key,value in json_out_sp['core']['memory'].iteritems():
    for subkey,subvalue in value.iteritems():
      lines.append("cleversafe." + "accesser." + str(accesser_name_clean) + "." + "memory." + str(key) + "." + str(subkey) + " " + str(subvalue) + " " + str(time))

message = '\n'.join(lines) + '\n' 
sock.sendall(message)
# Test appended output by printing out.
#print(message)
