#!/usr/bin/python

import csv
import subprocess

def ipa_addgroup(gid, description, groupname):
	command = ['ipa-addgroup', '--gid=%s' % gid,\
	'--description=%s' % description,\
	groupname]
	print " ".join(command)
	subprocess.call(command)

group_reader = csv.reader( open('group'), delimiter=':')

for entry in group_reader:
	print entry
	groupname,password,gid,members = entry
	ipa_addgroup(gid, groupname, groupname)

