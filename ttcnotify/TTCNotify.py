#!/usr/bin/python3
import sys
import os
import argparse
from lib.searchItem import SearchItemManager

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
    removeparser.add_argument('pid', metavar='pid', type=str, help="PID value of search item to remove")
    
    # list options
    listparser = subparsers.add_parser('list', help="list all search items")
    listparser.add_argument('list', action="store_true", default=True, help=argparse.SUPPRESS)
    
    # watch options
    watchparser = subparsers.add_parser('watch', help="watch search item(s)")
    watchparser.add_argument('watch', type=int, default=0, help="Item to watch or blank to watch all")
    
    # quit qut
    quitparser = subparsers.add_parser('quit', help="Quit application")
    quitparser.add_argument('quit', action="store_true", default=True, help=argparse.SUPPRESS)

    # Arguments
    return arguments.parse_args(lineArgs.split())


def main():
    itemManager = SearchItemManager()
    while True:
        arguments = input(">> ")
        try:
            opts = argParse(arguments)
            if hasattr(opts, 'url'):
                itemManager.add(opts)
            elif hasattr(opts, 'list') and opts.list is True:
                itemManager.list()
            elif hasattr(opts, 'pid'):
                itemManager.remove(opts.pid)
            elif hasattr(opts, 'watch'):
                itemManager.watch(opts.watch)
            elif hasattr(opts, 'quit') and opts.quit is True:
                print("Exiting, probably with errors")
                exit()
        except IOError:
            exit()
        except:
            pass

if __name__ == "__main__":
    main()

#Test link
# URL can function with missing POST options
# https://eu.tamrieltradecentre.com/pc/Trade/SearchResult?ItemID=&SearchType=Sell&ItemNamePattern=Spinner%27s+&ItemCategory1ID=1&ItemCategory2ID=2&ItemCategory3ID=12&ItemTraitID=9&ItemQualityID=&IsChampionPoint=false&LevelMin=&LevelMax=&MasterWritVoucherMin=&MasterWritVoucherMax=&AmountMin=&AmountMax=&PriceMin=&PriceMax=&page=2
# view-source:https://eu.tamrieltradecentre.com/pc/Trade/SearchResult?ItemID=&SearchType=Sell&ItemNamePattern=Spinner%27s+&ItemCategory1ID=1&ItemCategory2ID=2&ItemCategory3ID=12&ItemTraitID=9&ItemQualityID=&IsChampionPoint=false&LevelMin=&LevelMax=&MasterWritVoucherMin=&MasterWritVoucherMax=&AmountMin=&AmountMax=&PriceMin=&PriceMax=
