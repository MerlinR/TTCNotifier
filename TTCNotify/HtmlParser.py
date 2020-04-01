#!/usr/bin/python
import sys
import os
import urllib.request, urllib.error, urllib.parse
from html.parser import HTMLParser
from html.entities import name2codepoint


class TTCHTMLParser(HTMLParser):
    tradeList = [{}]
    _BARETAMURL = "https://eu.tamrieltradecentre.com/" 
    _TAMURL = _BARETAMURL + "pc/Trade/SearchResult?" 
    _TRADETAG = "trade-list-table"
    _SEPTAG = "row-separator"
    _ELAPSETAG = "data-mins-elapsed"
    _LINKTAG = "data-on-click-link"
    
    _inTable = False
    _skipHeader = False
    _inTrades = False
    webContent = ""
    _indxVal = 0
    _indxCont = 0
    _url = ""

    # urllib.parse.urljoin (LINK)
    def requestUrl(self, config):
        if self._url == "":
            self._url = self._alterURL(config)
        
        self.webContent = ""

        with urllib.request.urlopen(self._url) as response:
         for line in response:
             self.webContent = self.webContent + line.decode('utf-8')  # Decoding the binary data to text.


    def _alterURL(self, config):
        url = ""
        parseUrl = urllib.parse.urlparse(config.url[0])
        urlPost = urllib.parse.parse_qs(parseUrl.query, keep_blank_values=True)
        
        if config.max is not None:
            urlPost["PriceMax"] = config.max
        if config.units is not None:
            urlPost["AmountMax"] = config.units

        newQuery = urllib.parse.urlencode(urlPost, doseq=True)
        
        return self._TAMURL + newQuery

    def resetTradeList(self):
        self._indxVal = 0
        self._indxCont = 0
        self.tradeList = [{}]

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            for attr in attrs:
                if self._TRADETAG in attr[1]:
                    self._inTable = True
        if self._inTrades and (tag == "tr" or tag == "td"):
            if tag == "td":
                for attr in attrs:
                    if self._ELAPSETAG in attr[0]:
                        #print("Last Seen: ", attr[1])
                        self.tradeList[self._indxVal]['seen'] = int(attr[1])
            if tag == "tr":
                for attr in attrs:
                    if self._SEPTAG in attr[1]:
                        #print("------SPLIT------")
                        self.tradeList.append({})
                        self._indxVal += 1
                        self._indxCont = 0
                    if self._LINKTAG in attr[0]:
                        #print("Link: ", attr[1])
                        self.tradeList[self._indxVal]['link'] = self._BARETAMURL + attr[1]
                        break

    def handle_endtag(self, tag):
        if tag == "thead" and self._inTable:
            self._inTrades = True
        if tag == "table" and self._inTrades:
            self._inTrades = False
        if tag == "html":
            self.tradeList = sorted(filter(None, self.tradeList), key = lambda i: i['seen']) 


    def handle_data(self, data):
        if data.strip() == "": return
        if self._inTrades:
            #print("Data     :", data.strip())
            # This is shit but fucks given is exceeded
            if self._indxCont == 0:
                self.tradeList[self._indxVal]['name'] = data.strip()
            elif self._indxCont == 2:
                self.tradeList[self._indxVal]['level'] = int(data.strip())
            elif self._indxCont == 3:
                self.tradeList[self._indxVal]['who'] = data.strip()
            elif self._indxCont == 4:
                self.tradeList[self._indxVal]['where'] = data.strip()
            elif self._indxCont == 5:
                self.tradeList[self._indxVal]['guild'] = data.strip()
            elif self._indxCont == 6:
                self.tradeList[self._indxVal]['unitprice'] = float(data.strip().replace(",", ""))
            elif self._indxCont == 8:
                self.tradeList[self._indxVal]['units'] = int(data.strip().replace(",", ""))
            elif self._indxCont == 10:
                self.tradeList[self._indxVal]['totalprice'] = int(data.strip().replace(",", ""))
            self._indxCont += 1
