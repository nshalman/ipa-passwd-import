#!/usr/bin/python

import csv
import subprocess

#DEBUG = False
DEBUG = True

def mycall(command):
	print " ".join(command)
	if not DEBUG:
		subprocess.call(command)

def ipa_addgroup(gid, description, groupname):
	command = ['ipa-addgroup', '--gid=%s' % gid,\
	'--description=%s' % description,\
	groupname]
	mycall(command)

def ipa_adduser(uid, gid, gecos, homedir, shell, username):
	firstname, lastname = gecos.split(" ")
	command = ['ipa-adduser', '--setattr', 'uidnumber=%s' % uid,\
	'--setattr', 'gidnumber=%s' % gid, '-c', gecos, '-d', homedir, '-s',\
	shell, "-f", firstname, "-l", lastname, username]
	mycall(command)

def ipa_moduser(username, gid):
	command = ['ipa-moduser', '--setattr', 'gidnumber=%s' % gid,\
	username]
	mycall(command)

def ipa_modgroup(username, groupname):
	command = ['ipa-modgroup', '--add', username,\
	groupname]
	mycall(command)

passwd_reader = csv.reader( open('passwd'), delimiter=':')
groups = []
group_reader = csv.reader( open('group'), delimiter=':')
for entry in group_reader:
	groups.append(entry)

for entry in groups:
	groupname,password,gid,members = entry
	ipa_addgroup(gid, groupname, groupname)

for entry in passwd_reader:
	username,password,uid,gid,gecos,homedir,shell = entry
	ipa_adduser(uid, gid, gecos, homedir, shell, username)
	ipa_moduser(username, gid)

for entry in groups:
	groupname,password,gid,members = entry
	for user in members.split(','):
		if user <> '':
			ipa_modgroup(user, groupname)
