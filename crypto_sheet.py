#!/usr/bin/python
#/*Copyright (c) 2013 Chris Knorowski <cknorow@gmail.com>
# *
# * This program is free software: you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
 #* the Free Software Foundation, either version 3 of the License, or
 #* (at your option) any later version.
 #*
 #* This program is distributed in the hope that it will be useful,
 #* but WITHOUT ANY WARRANTY; without even the implied warranty of
 #* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 #* GNU General Public License for more details.
 #*
 #* You should have received a copy of the GNU General Public License
 #* along with this program.  If not, see <http://www.gnu.org/licenses/>.
 #*/

__author__ = 'cknorow@gmail.com (Chris knorowski)'
#motiated by google data sample spreadsheetsample.py 
#__author__ = 'api.laurabeth@gmail.com (Laura Beth Lincoln)'



try:
  from xml.etree import ElementTree
except ImportError:
  from elementtree import ElementTree
import gdata.spreadsheet.service
import gdata.service
import atom.service
import gdata.spreadsheet
import atom
import getopt
import sys
import string
import time
import logging
import getpass
from grab_rate import currency
from grab_rate import coinbasebtc
from grab_rate import mtgoxbtc

class WorkHorse:

  def __init__(self, email, password, sheet_name):
    self.gd_client = gdata.spreadsheet.service.SpreadsheetsService()
    self.gd_client.email = email
    self.gd_client.password = password
    self.gd_client.source = 'Spreadsheets GData Sample'
    self.gd_client.ProgrammaticLogin()
    self.curr_key = ''
    self.curr_wksht_id = ''
    self.list_feed = None
    self.sheet_name = sheet_name
    
  def _PromptForSpreadsheet(self):
    # Get the list of spreadsheets
    feed = self.gd_client.GetSpreadsheetsFeed()
    in_index = self._FindFeed(feed)
    id_parts = feed.entry[string.atoi(in_index)].id.text.split('/')
    self.curr_key = id_parts[len(id_parts) - 1]

  def _PromptForWorksheet(self):
    # Get the list of worksheets
    feed = self.gd_client.GetWorksheetsFeed(self.curr_key)
    input = '0'
    id_parts = feed.entry[string.atoi(input)].id.text.split('/')
    self.curr_wksht_id = id_parts[len(id_parts) - 1]
  
  def _PromptForCellsAction(self, command = ''):
    if command == '':
      print ('dump\n'
           'update {row} {col} {input_value}\n'
           '\n')
      input = raw_input('Command: ')
      command = input.split(' ', 1)
    if command[0] == 'dump':
      self._CellsGetAction()
    elif command[0] == 'update':
      parsed = command[1].split(' ', 2)
      if len(parsed) == 3:
        self._CellsUpdateAction(parsed[0], parsed[1], parsed[2])
      else:
        self._CellsUpdateAction(parsed[0], parsed[1], '')
    else:
      self._InvalidCommandError(input)
  
  def _CellsGetAction(self):
     # Get the feed of cells
    feed = self.gd_client.GetCellsFeed(self.curr_key, self.curr_wksht_id)
    self._PrintFeed(feed)
    
  def _CellsUpdateAction(self, row, col, inputValue):
    entry = self.gd_client.UpdateCell(row=row, col=col, inputValue=inputValue, 
        key=self.curr_key, wksht_id=self.curr_wksht_id)
    #if isinstance(entry, gdata.spreadsheet.SpreadsheetsCell):
    #  print 'Updated!'
        
  def _ListGetAction(self):
    # Get the list feed
    self.list_feed = self.gd_client.GetListFeed(self.curr_key, self.curr_wksht_id)
    self._PrintFeed(self.list_feed)
    
  def _FindFeed(self, feed):
    for i, entry in enumerate(feed.entry):
      if isinstance(feed, gdata.spreadsheet.SpreadsheetsCellsFeed):
        print '%s %s\n' % (entry.title.text, entry.content.text)
      elif isinstance(feed, gdata.spreadsheet.SpreadsheetsListFeed):
        print '%s %s %s' % (i, entry.title.text, entry.content.text)
        # Print this row's value for each column (the custom dictionary is
        # built using the gsx: elements in the entry.)
        print 'Contents:'
        for key in entry.custom:  
          print '  %s: %s' % (key, entry.custom[key].text) 
        print '\n',
      else:
        if entry.title.text == self.sheet_name:
          return '%i'%i

  def Run(self, label, logger=False):
    try:
      self._PromptForSpreadsheet()
    except:
      # tell the program to relogin
      logger.error("Error: Unable to prompt spreadsheet")
      return True
    try:
      self._PromptForWorksheet()
    except:
      # tell the program to relogin
      logger.error("Error: Unable to prompt worksheet")
      return True
    # Get coinbase btc price
    price = coinbasebtc()
    if price != 'noupdate':
      try:
        self._PromptForCellsAction(['update', '2 1  Coinbase'])
        self._PromptForCellsAction(['update', '2 2  %.9f'%(price)])
      except:
        logger.error("Error: Unable to Update coinbase BTC Cells")
    else:
        logger.error("Error: Unable to Update Currency Price Coinbase")
    # Get MTgox btc price
    price = mtgoxbtc()
    if price != 'noupdate':
      try:
        self._PromptForCellsAction(['update', '3 1  MTgox'])
        self._PromptForCellsAction(['update', '3 2  %.9f'%(price)])
      except:
        logger.error("Error: Unable to Update mtgox BTC Cells")
    else:
        logger.error("Error: Unable to Update Currency Price MTgox")
    for i, coin in enumerate(label):
      price = currency(coin)
      if price != 'noupdate':
        try:
          self._PromptForCellsAction(['update', '1 %i %s'%(i+3,coin)])
          self._PromptForCellsAction(['update', '2 %i %.9f'%(i+3,price)])
        except:
          logger.error("Error: Unable to Update %s Cells"%coin)
      else:
          logger.error("Error: Unable to Update Currency Price %s"%coin)
    return False

def main():
  #Run this if you don't want to run as a daemon
  #Instead run the script ina python shell
    logger = logging.getLogger("DaemonLog")
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler = logging.FileHandler("/tmp/crypt_python.log")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.info("log Started")
    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ["user=",
            "pw=","currency=","s=","c="])
    except:
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
    #label can be any of the cryptop coins on 
    #cryptsy
    label = ['DGCBTC','DGCLTC','LTCBTC']
    pw = getpass.getpass('\nPassword: ')
    if user == '' or pw == '' or sheet_name == '':
        print '--user [username] --s [sheet name]'
        sys.exit(2)
    speedy = WorkHorse(user, pw, sheet_name)
    while True:
        if speedy.Run(label,logger):
            try:
                speedy = WorkHorse(user, pw, sheet_name)
            except:
                logger.error("Error: First relogin attaempt fail trying agin")
                logger.error("Error: If this fails please report the bug")
                speedy = WorkHorse(user, pw, sheet_name)
                logger.info("Second Attempt Succesful")
        print 'updated prices '
        time.sleep(30)


if __name__ == '__main__':
  main()
