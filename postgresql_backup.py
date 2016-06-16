#!/usr/bin/env python

#This script perform postgres DB backup.
#Example to run script with parameter
#./postgresql_backup.sh  -u <username> -h <db hostname> -p '<password>' -d <database1> <database2> <databaseN> -b <backupdirectory path>
#sudo python postgresql_backup.py -d posgres testing_db -b /tmp/postgres -u postgres -p 'machine'

import argparse
import os
import time
import subprocess


#Date & rime for file
timestamp=time.strftime("%Y_%m_%d_%H_%M")
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-d', '--databases', help="database names like: db1 db2 db3",dest='databases', nargs='+')
parser.add_argument('-u', '--username', help="DB login user",dest='username', default='root')
parser.add_argument('-H', '--host', help="DB hosts ip/hostname",dest='hostname', default='localhost')
parser.add_argument('-p', '--password', help="DB hosts ip/hostname",dest='password')
parser.add_argument('-b', '--backupdir', help="DB backupdirectory",dest='backupdir')

args = parser.parse_args()

if os.geteuid() != 0:
	print "Run script with root user or sudoer privileges"
	exit(1)

if args.password is None or args.databases is None or args.backupdir is None:
	print "\nCheck the password,database & backup directory value, use --help option to know\n"
	print parser.print_help()

if not os.path.exists(args.backupdir):
	os.mkdir(args.backupdir)
	print "Backup directory created"


#Generate command & take DB backup
for i in range(len(args.databases)):
    cmd = 'PGPASSWORD="'+ args.password+'" pg_dump -U '+ args.username +' -h '+args.hostname +' '+ args.databases[i] +' > '+ args.backupdir +'/'+ args.databases[i] +'_'+ timestamp+'.sql'
    try:
        subprocess.check_call(cmd, shell=True)
        subprocess.check_call("gzip "+ args.backupdir +'/'+ args.databases[i] +'_'+ timestamp+'.sql', shell=True)
        print cmd
    except subprocess.CalledProcessError as e:
        print e.returncode
        exit(1)

