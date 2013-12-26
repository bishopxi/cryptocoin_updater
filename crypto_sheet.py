#!/usr/bin/python
#/*Copyright (c) 2013 Chris Knorowski <cknorow@gmail.com>
# *
# * This program is free software: you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation, either version 3 of the License, or
# * (at your option) any later version.
# *
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program.  If not, see <http://www.gnu.org/licenses/>.
# */

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
from grab_cryptsy import currency
from grab_cryptsy import coinbasebtc

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

        
  def _InvalidCommandError(self, input):
    print 'Invalid input: %s\n' % (input)
    
  def Run(self, label, logger):
    try:
      self._PromptForSpreadsheet()
    except:
      logger.error("Error: Unable to prompt spreadsheet")
      sys.exit(2)
    try:
      self._PromptForWorksheet()
    except:
      logger.error("Error: Unable to prompt worksheet")
      sys.exit(2)
    for i, coin in enumerate(label):
      price = currency(coin)
      try:
        self._PromptForCellsAction(['update', '1 %i %s'%(i+1,coin)])
        self._PromptForCellsAction(['update', '2 %i %.9f'%(i+1,price)])
      except:
        logger.error("Error: Unable to Update Cells")
        sys.exit(2)
    price = coinbasebtc()  
    try:
      self._PromptForCellsAction(['update', '1 %i USDBTC'%(len(label)+1,)])
      self._PromptForCellsAction(['update', '2 %i %.9f'%(len(label)+1,price)])
    except:
      logger.error("Error: Unable to Update BTC Cells")
      sys.exit(2)

def main():
  #this is an example of the iput file
  user =  ''
  pw   =  ''
  key  =  ''
  sheet_name = 'cryptocoins worksheet'
  #label can be any of the cryptop coins on 
  #cryptsy
  label = ['DGCBTC','DGCLTC','LTCBTC']
  speedy = WorkHorse(user, pw, sheet_name)
  speedy.Run(label)


if __name__ == '__main__':
  main()
