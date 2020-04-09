#!/usr/bin/python
#===============================================================================================
# Imports
#===============================================================================================
import sys
import os
import argparse
import time
import datetime
if sys.platform.startswith('win32'):
    from win10toast import ToastNotifier
else:
    import notify2
from HtmlParser import TTCHTMLParser

def argParse(lineArgs):
    # Arguments
    arguments = argparse.ArgumentParser(description='Simple python tool to notify of item in specific price range.')

    subparsers = arguments.add_subparsers(help='sub-command help')
    
    # Add options
    addparser = subparsers.add_parser('add', help="add search item")
    addparser.add_argument('url', metavar='L', type=str, help="Url of search")
    addparser.add_argument('-p', '--max-price', dest='max', type=int, help="Max unit price to search")
    addparser.add_argument('-u', '--max-units', dest='unitsmax', type=int, help="Max amount of units")
    addparser.add_argument('-m', '--min-units', dest='unitsmin', type=int, help="Min amount of units")
    addparser.add_argument('-r', '--refresh-time', dest='refresh', type=int, default=90, help="How often to refresh in seconds")
    
    # Remove options
    removeparser = subparsers.add_parser('remove', help="remove search item")
    removeparser.add_argument('indx', metavar='indx', type=str, help="Indx value of search item")
    
    # list options
    listparser = subparsers.add_parser('list', help="list all search items")
    listparser.add_argument('list', action="store_true", default=True, help=argparse.SUPPRESS)
    
    # watch options
    watchparser = subparsers.add_parser('watch', help="watch search item(s)")
    watchparser.add_argument('watch', type=int, default=0, help="Item to watch or blank to watch all")

    # Arguments
    return arguments.parse_args(lineArgs.split())


def notify(item):
    summary = "{}:{}. {} being sold for {}. {} minutes ago. {}".format(item['where'], item['guild'],
                                                               item['units'], item['totalprice'], item['seen'], item['link'])
    if sys.platform.startswith('win32'):
        toaster = ToastNotifier()
        toaster.show_toast(item['name'],summary, duration=30)
        print("Windows notify")
    else:
        notify2.init('ESO Item Notify')
        n = notify2.Notification(item['name'], summary)
        n.set_urgency(notify2.URGENCY_NORMAL)
        n.show()
        n.set_timeout(60)


def cmpTradeLists(prev, current):
   
    newTradeCount = 0
    for item in current:
        if item['link'] == prev[0]['link']:
            break
        else:
            newTradeCount += 1
    
    for i in range(0,newTradeCount):
        print(current[i])
        notify(current[i])


def searchItems(opts):
    parsed = TTCHTMLParser()
    prevTradeList = ()

    while True:
        parsed.resetTradeList()
        parsed.requestUrl(opts)
        parsed.feed(parsed.webContent)
        print("%s: Scanning..." % datetime.datetime.now().strftime("%H:%M:%S"))
        if prevTradeList and parsed.tradeList:
            cmpTradeLists(prevTradeList, parsed.tradeList)
        if not parsed.tradeList:
            print("Failed to discover trade list, puasing 5 minutes to reverse human check")
            time.sleep(300)
        else:
            prevTradeList = parsed.tradeList
            time.sleep(opts.refresh)


def main():
    while True:
        arguments = input(">>")
        try:
            opts = argParse(arguments)
            if opts.url is not None:
                searchItems(opts)
        except:
            pass

if __name__ == "__main__":
    main()

#Test link
# URL can function with missing POST options
# https://eu.tamrieltradecentre.com/pc/Trade/SearchResult?ItemID=&SearchType=Sell&ItemNamePattern=Spinner%27s+&ItemCategory1ID=1&ItemCategory2ID=2&ItemCategory3ID=12&ItemTraitID=9&ItemQualityID=&IsChampionPoint=false&LevelMin=&LevelMax=&MasterWritVoucherMin=&MasterWritVoucherMax=&AmountMin=&AmountMax=&PriceMin=&PriceMax=&page=2
# view-source:https://eu.tamrieltradecentre.com/pc/Trade/SearchResult?ItemID=&SearchType=Sell&ItemNamePattern=Spinner%27s+&ItemCategory1ID=1&ItemCategory2ID=2&ItemCategory3ID=12&ItemTraitID=9&ItemQualityID=&IsChampionPoint=false&LevelMin=&LevelMax=&MasterWritVoucherMin=&MasterWritVoucherMax=&AmountMin=&AmountMax=&PriceMin=&PriceMax=
