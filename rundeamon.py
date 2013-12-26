#!/usr/bin/env python
# Copyright (c) 2013 Chris Knorowski <cknorow@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
# 
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
# 
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 

import sys, time
import getopt
import getpass
from daemon import Daemon
import crypto_sheet as crypto
import logging
import random


class MyDaemon(Daemon):
    def run(self):
        speedy = crypto.WorkHorse(self.user, self.pw, self.sheet_name)
        logger = logging.getLogger("DaemonLog")
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler = logging.FileHandler("/tmp/crypt_daemon.log")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        while True:
            speedy.Run(self.label, logger)
            if random.random() <.05:
                logger.info("Daemon Running Properly")
            time.sleep(30)


if __name__ == "__main__":
	# parse command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ["user=",
            "pw=","currency=","s=","c="])
    except getopt.error, msg:
        print '--c [start|stop] --user [username] --pw [password] --s [worksheet name] --currency [DGCLTC,LTCBTC]'
        sys.exit(2)
    user = ''
    pw = ''
    sheet_name = ''
    label = ''
    c = ""
    # Process options
    for o, a in opts:
        if o == "--user":
            user = a
        elif o == "--s":
            sheet_name = a
        elif o == "--currency":
            label = a.split(',')
        elif o == "--c":
            c = a
    if c  == 'start':
        pw = getpass.getpass('\nPassword: ')
        if user == '' or pw == '' or sheet_name == '':
            print '--user [username] --s [sheet name]'
            sys.exit(2)
        daemon = MyDaemon('/tmp/crypto_daemon.pid', user = user, pw = pw ,
                sheet_name = sheet_name, label = label)
        daemon.start()
        print "Daemon started"
    elif c == 'stop':
        print 'Daemon is stopping please wait'
        daemon = MyDaemon('/tmp/crypto_daemon.pid')
        daemon.stop()
    else:
        print "error daemon must either start or stop --c [start|stop]"
        sys.exit(2)
