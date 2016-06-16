import argparse
import os
import time
import subprocess
import commands


#Date & rime for file
timestamp=time.strftime("%Y_%m_%d_%H_%M")
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-d', '--databases', help="database names like: db1 db2 db3",dest='databases', nargs='+')
parser.add_argument('-u', '--username', help="DB login user",dest='username', default='root')
parser.add_argument('-H', '--host', help="DB hosts ip/hostname",dest='hostname', default='localhost')
parser.add_argument('-p', '--password', help="DB hosts ip/hostname",dest='password')
parser.add_argument('-b', '--backupdir', help="DB backupdirectory",dest='backupdir')
parser.add_argument('-P', '--port', help="mongodb connection port",dest='port', default='27017')

args = parser.parse_args()
#print args.accumulate(args.integers)

if os.geteuid() != 0:
	print "Run script with root user or sudoer privileges"
	exit(1)

if args.password is None or args.databases is None or args.backupdir is None:
	print "\nCheck the password,database & backup directory value, use --help option to know\n"
	print parser.print_help()

if not os.path.exists(args.backupdir):
	os.mkdir(args.backupdir)
	print "Backup directory created"


cmd = 'mysqldump -u '+ args.username +' -h '+args.hostname +' -p'+args.password +' mysql | gzip  > '+ args.backupdir +'/mysql_'+ timestamp+'.sql.gz '
#os.system(cmd)
#print cmd
for i in range(len(args.databases)):
#    cmd = 'mysqldump -u '+ args.username +' -h '+args.hostname +' -p'+args.password +' '+ args.databases[i] +' > '+ args.backupdir +'/'+ args.databases[i] +'_'+ timestamp+'.sql'
    cmd1 = 'mongodump --host '+args.hostname+'--port '+args.port+' --username '+args.username+" --password '"+args.password+"' --db "+args.databases[i]+' --out /tmp/'+args.databases[i]+'_mongo_dump_'+timestamp
    cmd2 = "tar -cz  /tmp/"+args.databases[i]+"_mongo_dump_"+timestamp +"-f "+args.backupdir+"/"+ args.databases[i] +"_mongo_dump_"+ timestamp+".tar.gz"
    try:
        subprocess.check_call(cmd, shell=True)
        subprocess.check_call(cmd2, shell=True)
        print "Backup taken sucessfully: :"+args.backupdir+"/"+ args.databases[i] +"_mongo_dump_"+ timestamp+".tar.gz"
    except subprocess.CalledProcessError as e:
        print e.returncode
        exit(1)
print cmd1
