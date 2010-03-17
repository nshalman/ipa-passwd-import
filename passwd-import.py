#!/usr/bin/python

import csv
import subprocess

def ipa_adduser(uid, gid, gecos, homedir, shell, username):
	firstname, lastname = gecos.split(" ")
	command = ['ipa-adduser', '--setattr', 'uidnumber=%s' % uid,\
	'--setattr', 'gidnumber=%s' % gid, '-c', gecos, '-d', homedir, '-s',\
	shell, "-f", firstname, "-l", lastname, username]
	print " ".join(command)
	subprocess.call(command)

def ipa_moduser(username, gid):
	command = ['ipa-moduser', '--setattr', 'gidnumber=%s' % gid,\
	username]
	print " ".join(command)
	subprocess.call(command)

passwd_reader = csv.reader( open('passwd'), delimiter=':')

for entry in passwd_reader:
	username,password,uid,gid,gecos,homedir,shell = entry
	ipa_adduser(uid, gid, gecos, homedir, shell, username)
	ipa_moduser(username, gid)
