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

import os
import sys
import urllib2

marketid = {"LTCBTC":"3",
"FTCBTC":"5",
"MNCBTC":"7",
"CNCBTC":"8",
"BQCBTC":"10",
"YACBTC":"11",
"ELCBTC":"12",
"NVCBTC":"13",
"WDCBTC":"14",
"CNCLTC":"17",
"WDCLTC":"21",
"YACLTC":"22",
"BTBBTC":"23",
"DGCBTC":"26",
"TRCBTC":"27",
"PPCBTC":"28",
"NMCBTC":"29",
"GLDBTC":"30",
"PXCBTC":"31",
"NBLBTC":"32",
"FRKBTC":"33",
"LKYBTC":"34",
"JKCLTC":"35",
"GLDLTC":"36",
"RYCLTC":"37",
"IXCBTC":"38",
"FRCBTC":"39",
"AMCBTC":"43",
"FSTBTC":"44",
"MECBTC":"45",
"DBLLTC":"46",
"ARGBTC":"48",
"BTEBTC":"49",
"BTGBTC":"50",
"SBCBTC":"51",
"DVCLTC":"52",
"CAPBTC":"53",
"NRBBTC":"54",
"EZCLTC":"55",
"MEMLTC":"56",
"ALFBTC":"57",
"CRCBTC":"58",
"IFCLTC":"60",
"FLOLTC":"61",
"MSTLTC":"62",
"XPMBTC":"63",
"KGCBTC":"65",
"ANCBTC":"66",
"XNCLTC":"67",
"CSCBTC":"68",
"EMDBTC":"69",
"CGBBTC":"70",
"QRKBTC":"71",
"DMDBTC":"72",
"CMCBTC":"74",
"ORBBTC":"75",
"GLCBTC":"76",
"GLXBTC":"78",
"HBNBTC":"80",
"SPTBTC":"81",
"GDCBTC":"82",
"GMELTC":"84",
"ZETBTC":"85",
"PHSBTC":"86",
"REDLTC":"87",
"SRCBTC":"88",
"NECBTC":"90",
"CPRLTC":"91",
"PYCBTC":"92",
"ELPLTC":"93",
"ADTLTC":"94",
"CLRBTC":"95",
"DGCLTC":"96",
"SXCLTC":"98",
"MECLTC":"100",
"PXCLTC":"101",
"BUKBTC":"102",
"TIXXPM":"103",
"NETXPM":"104",
"IFCXPM":"105",
"XPMLTC":"106",
"TIXLTC":"107",
"NETLTC":"108",
"COLLTC":"109",
"COLXPM":"110",
"ASCLTC":"111",
"ASCXPM":"112",
"ADTXPM":"113",
"TEKBTC":"114",
"XJOBTC":"115",
"LK7BTC":"116",
"TAGBTC":"117",
"PTSBTC":"119",
"Point":"120",
"ANCLTC":"121",
"DVCXPM":"122",
"CGBLTC":"123",
"FSTLTC":"124",
"PPCLTC":"125",
"QRKLTC":"126",
"ZETLTC":"127",
"SBCLTC":"128",
"BETBTC":"129",
"TGCBTC":"130",
"DEMBTC":"131",
"DOGEBTC":"132",
"UNOBTC":"133"}


def currency(label):
	#get dgc to btc price
    try:
        r = urllib2.urlopen('http://pubapi.cryptsy.com/api.php?method=singlemarketdata&marketid=%s'%marketid[label])
        s = r.readlines()[0]
        tp = s.rfind('lasttradeprice')
        coin =  float(s[tp:tp+35].split('"')[2])
        print label, coin
        return coin
    except:
        return "noupdate"


def coinbasebtc():
	#get btc to usd price
    try:
        r = urllib2.urlopen('https://coinbase.com/api/v1/currencies/exchange_rates')
        s = r.readlines()[0]
        tp = s.rfind('btc_to_usd')
        BtcUsd =  float(s[tp:tp+35].split('"')[2])
        print "Coinbase BTCUSD", BtcUsd
        return BtcUsd
    except:
        return "noupdate"


def mtgoxbtc():
	#get btc to usd price
    try:
        r = urllib2.urlopen('https://data.mtgox.com/api/2/BTCUSD/money/ticker')
        s = r.readlines()[0]
        tp = s.rfind('"last"')
        BtcUsd =  float(s[tp:tp+35].split('"')[5])
        print "MTGox BTCUSD", BtcUsd
        return BtcUsd
    except:
        print 'mtgox failed'
        return "noupdate"
