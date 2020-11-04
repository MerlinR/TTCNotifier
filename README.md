# TTCNotifier
Simple python script that periodically scans Tamriel Trade Centre with set prices, creating a notification when a new item has been posted that meets the search terms.
The script is interactive, so run once and insert as many items you wish to track using the "add" command.

This script is no longer maintained, as ESO become the laggest game in history, thanks Zenimax.

## ToDo
 - Implement the Watch. This is to better view results of item searches
 - Create setup.py for installation

## Requirements
```
pip install -r requirements.txt
```

## Usage
```
usage: TTCNotify.py [-h] {add,remove,list,watch,quit} ...

Simple python tool to notify of item in specific price range.

positional arguments:
  {add,remove,list,watch,quit}
                        sub-command help
    add                 add search item
    remove              remove search item
    list                list all search items
    watch               watch search item(s)
    quit                Quit application

optional arguments:
  -h, --help            show this help message and exit
```

## Example
The simple script requires a URL to alter, for this initially search TTC for the item. Copy the URL into the
script as shown below, uing Arguments as shown above.
```
Searching for Dreugh Wax and showing new posts that unit prices are 7500 or less

Python3 TTCNotify.py
>> add https://eu.tamrieltradecentre.com/pc/Trade/SearchResult?ItemID=211&SortBy=LastSeen&Order=desc -p 7500
```
