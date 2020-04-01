# TTCNotifier
Simple python script that periodically scans Tamriel Trade Centre with set prices, creating a notifcation when a new item has been posted that meets the search terms.

## Install
```
pip install -r requirements.txt
```

## Useage
```
positional arguments:
  L                     Url of search

optional arguments:
  -h, --help            show this help message and exit
  -p MAX, --max-price MAX
                        Max unit price to search
  -u UNITS, --max-units UNITS
                        Max amount of units
  -r REFRESH, --refresh-time REFRESH
                        How often to refresh in seconds
```

## Example
The simple script requires a URL to alter, for this initially search TTC for the item. Copy the URL into the
script as shown below, uing Arguments as shown above.
```
Searching for Dreugh Wax and showing new posts that unit prices are 7500 or less
Python3 TTCNotify.py https://eu.tamrieltradecentre.com/pc/Trade/SearchResult?ItemID=211&SortBy=LastSeen&Order=desc -p 7500
```
