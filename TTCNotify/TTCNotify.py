#!/usr/bin/python
#===============================================================================================
# Imports
#===============================================================================================
import sys
import os
import argparse
import time
import notify2
from HtmlParser import TTCHTMLParser

def argParse():
    # Arguments
    arguments = argparse.ArgumentParser(description='Simple python tool to notify of item in specific price range.')

    # Core Bullet Arguments
    arguments.add_argument('url', metavar='L', type=str, nargs=1, help="Url of search")
    arguments.add_argument('-p', '--max-price', dest='max', type=int, help="Max unit price to search")
    arguments.add_argument('-u', '--max-units', dest='units', type=int, help="Max amount of units")
    arguments.add_argument('-r', '--refresh-time', dest='refresh', type=int, default=45, help="How often to refresh in seconds")

    # Arguments
    args = arguments.parse_args()
    
    return args


def notify(item):
    notify2.init('ESO Item Notify')
    summary = "{}:{}. {} being sold for {}. {} minutes ago. {}".format(item['where'], item['guild'],
                                                                item['units'], item['totalprice'], item['seen'], item['link'])
    n = notify2.Notification(item['name'],
                             summary)
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


def searchItems(config):
    parsed = TTCHTMLParser()
    prevTradeList = ()

    while True:
        parsed.resetTradeList()
        parsed.requestUrl(config)
        parsed.feed(parsed.webContent)
        
        if prevTradeList:
            cmpTradeLists(prevTradeList, parsed.tradeList)
        prevTradeList = parsed.tradeList 

        time.sleep(config.refresh)


def main():
    config = argParse()
    searchItems(config)


if __name__ == "__main__":
    main()

#Test link
# URL can function with missing POST options
# https://eu.tamrieltradecentre.com/pc/Trade/SearchResult?ItemID=&SearchType=Sell&ItemNamePattern=Spinner%27s+&ItemCategory1ID=1&ItemCategory2ID=2&ItemCategory3ID=12&ItemTraitID=9&ItemQualityID=&IsChampionPoint=false&LevelMin=&LevelMax=&MasterWritVoucherMin=&MasterWritVoucherMax=&AmountMin=&AmountMax=&PriceMin=&PriceMax=&page=2
# view-source:https://eu.tamrieltradecentre.com/pc/Trade/SearchResult?ItemID=&SearchType=Sell&ItemNamePattern=Spinner%27s+&ItemCategory1ID=1&ItemCategory2ID=2&ItemCategory3ID=12&ItemTraitID=9&ItemQualityID=&IsChampionPoint=false&LevelMin=&LevelMax=&MasterWritVoucherMin=&MasterWritVoucherMax=&AmountMin=&AmountMax=&PriceMin=&PriceMax=
