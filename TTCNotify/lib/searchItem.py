#!/usr/bin/python
import sys
import time
import datetime
import multiprocessing
import logging
import urllib.parse
if sys.platform.startswith('win32'):
    from win10toast import ToastNotifier
else:
    import notify2
from lib.htmlParser import TTCHTMLParser

class SearchItemManager:
    _threads = []
    listenKey = False

    def add(self, item):

        searchProcess = multiprocessing.Process(name = self._getSearchItemName(item), target = SearchItemProcess, args=(item,))
        self._threads.append(searchProcess)
        searchProcess.start()

    def list(self):
        print("\tPID\tName")
        for item in self._threads:
            if item.is_alive():
                print("\t%s\t%s" % (item.pid, item.name))

    # Pretty shitty, but ehhhhh
    def watch(self):
        self.listen = True
        input("\tPress Enter to stop======================")
        self.listen = False

    def remove(self, pid):
        for item in self._threads:
            if int(item.pid) == int(pid):
                print("\tEnding: %s:%s" % (item.pid, item.name))
                item.terminate()
                item.join()

    def _getSearchItemName(self, item):
        parseUrl = urllib.parse.urlparse(item.url)
        urlPost = urllib.parse.parse_qs(parseUrl.query, keep_blank_values=True)
        return urlPost["ItemNamePattern"][0]

class SearchItemProcess:

    def __init__(self, item):
        self._name = multiprocessing.current_process().name
        self._pid = multiprocessing.current_process().pid
        self.searchItem(item)

    def notify(self, item, summary):
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
    
    def cmpTradeLists(self, prev, current):
        newTradeCount = 0
        for item in current:
            if item['link'] == prev[0]['link']:
                break
            else:
                newTradeCount += 1
        
        for i in range(0,newTradeCount):
            summarylink = "{}, {}x{} for {} at {}:{}. {} minutes ago. {}".format(current[i]['name'], current[i]['unitprice'], current[i]['units'],
                                    current[i]['totalprice'], current[i]['where'], current[i]['guild'], current[i]['seen'], current[i]['link'])
            summary = "{}, {}x{} for {} at {}:{}. {} minutes ago.".format(current[i]['name'], current[i]['unitprice'], current[i]['units'],
                                    current[i]['totalprice'], current[i]['where'], current[i]['guild'], current[i]['seen'])
            print(summary)
            self.notify(current[i], summarylink)

    def searchItem(self, opts):
        parsed = TTCHTMLParser()
        prevTradeList = ()
        while True:
            parsed.resetTradeList()
            parsed.requestUrl(opts)
            parsed.feed(parsed.webContent)
            print("%s:%s: Scanning..." % (datetime.datetime.now().strftime("%H:%M:%S"), self._name))
            if prevTradeList and parsed.tradeList:
                self.cmpTradeLists(prevTradeList, parsed.tradeList)
            if not parsed.tradeList:
                print("Failed to discover trade list, pausing 5 minutes to reverse human check")
                time.sleep(300)
            else:
                prevTradeList = parsed.tradeList
                time.sleep(opts.refresh)

