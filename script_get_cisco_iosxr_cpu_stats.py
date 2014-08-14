#!/usr/bin/env python
# -*- coding: utf8 -*-

__author__ = "Arnis Civciss (arnis.civciss@gmail.com)"
__copyright__ = "Copyright (c) 2013 Arnis Civciss"

import subprocess
import re
import sys

DEBUG = 0
HOST = sys.argv[1]
COMMUNITY = sys.argv[2]
IDX_OID = 'snmpwalk -v2c -c %s %s .1.3.6.1.4.1.9.9.109.1.1.1.1.2' % (COMMUNITY, HOST)
NAME_OID = 'snmpget -v2c -c %s %s .1.3.6.1.2.1.47.1.1.1.1.7.%s'
CPU5_OID = 'snmpget -v2c -c %s %s .1.3.6.1.4.1.9.9.109.1.1.1.1.8.%s'

def get_cpu_index():
  reparse = re.compile('\.(\d+)\s\=\sINTEGER\:\s(\d+)')
  re_nameoid = re.compile('\.(\d+)\s\=\sSTRING\:\s\"([^\"]+)\"')
  #disabled only works for > 2.7
  #out = subprocess.check_output(IDX_OID, shell=True)
  #for python < 2.7
  out = subprocess.Popen(['snmpwalk', '-v2c', '-c', COMMUNITY, HOST, '.1.3.6.1.4.1.9.9.109.1.1.1.1.2'], stdout=subprocess.PIPE).communicate()[0]
  if DEBUG: print out
  out = out.split('\n')
  dic = {}
  idx_number = -1
  for line in out:
    if 'num_indexes' in sys.argv[3]:
      idx_number += 1
      continue
    
    if reparse.search(line):
      cpu_idx = reparse.search(line).group(1)
      if 'index' in sys.argv[3]:
        print cpu_idx
        continue
      cpu_phyname_idx = reparse.search(line).group(2)
      if DEBUG: print cpu_idx, cpu_phyname_idx
      #disabled only works for > 2.7
      #get_out = subprocess.check_output(NAME_OID % (COMMUNITY, HOST, cpu_phyname_idx), shell=True)
      #for python < 2.7
      get_out = subprocess.Popen(['snmpget', '-v2c', '-c', COMMUNITY, HOST, '.1.3.6.1.2.1.47.1.1.1.1.7.%s' % cpu_phyname_idx], stdout=subprocess.PIPE).communicate()[0]
      if DEBUG: print get_out
      get_out = get_out.split('\n')
      for na in get_out:
        if re_nameoid.search(na):
          name_idx = re_nameoid.search(na).group(1)
          name = re_nameoid.search(na).group(2)
          dic[cpu_idx] = name
  if 'num_indexes' in sys.argv[3]:
    return idx_number
  elif 'index' in sys.argv[3]:
    return
  else:
    return dic

def get_index(idx):
  reparse = re.compile('\.(\d+)\s\=\sGauge32\:\s(\d+)', re.DOTALL)
  #disabled only works for > 2.7
  #out = subprocess.check_output(CPU5_OID % (COMMUNITY, HOST, idx), shell=True)
  #for python < 2.7
  out = subprocess.Popen(['snmpget', '-v2c', '-c', COMMUNITY, HOST, '.1.3.6.1.4.1.9.9.109.1.1.1.1.8.%s' % idx], stdout=subprocess.PIPE).communicate()[0]
  if reparse.search(out):
    return reparse.search(out).group(2)
  return '0'

if __name__ == "__main__":
  DEBUG =0
  tip = sys.argv[3]
  if 'query' in tip:
    indexes = get_cpu_index()
    for each in indexes:
      if 'index' in sys.argv[4]:
        print '%s:%s' % (each, each)
      else:
        print '%s:%s' % (each, indexes[each])
  elif 'get' in tip:
    print get_index(sys.argv[5])
  elif 'num_indexes' in tip:
    print get_cpu_index()
  elif 'index' in tip:
    get_cpu_index()
  else:
    print ''' 
script_get_cisco_iosxr_cpu_stats.py 1.1.1.1 public query index
script_get_cisco_iosxr_cpu_stats.py 1.1.1.1 public get index 66
'''

