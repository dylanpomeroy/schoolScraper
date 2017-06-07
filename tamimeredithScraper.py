from lxml import html
import requests
import urllib
import time
import socket
import shutil
import os
from subprocess import call
import platform

# these are overridden before every batch scrape process with values in arguments.txt
verbose = 0
urlToScrape = ""
requestTimeout = 0 #seconds
pathToStoreFiles = ""
sleepTimeBetweenScraping = 0 #seconds
convertPPTXToPDF = 0
PPTXToPDFUnixCmd = ""
PPTXToPDFWindowsCmd = ""

# used to specify location of arguments
argumentsFile = "arguments.txt"

startTime = time.time()
requestCounter = 1
totalItemsDownloaded = 0

def getArguments():
    # read arguments file
    f = open(argumentsFile, 'r+')
    fileContents = f.readlines()
    f.close()
    fileContents = [x for x in fileContents if not x.startswith('#') and not x.startswith('\n')]
    arguments = {}
    for item in fileContents:
        arguments[item.split(' : ')[0].strip()] = item.split(' : ')[1].strip() 
    
    # assign arguments to variables
    global verbose, urlToScrape, requestTimeout, pathToStoreFiles, sleepTimeBetweenScraping, convertPPTXToPDF, PPTXToPDFUnixCmd, PPTXToPDFWindowsCmd
    verbose = int(arguments["verbose"])
    urlToScrape = arguments["urlToScrape"]
    requestTimeout = int(arguments["requestTimeout"])
    pathToStoreFiles = arguments["pathToStoreFiles"]
    sleepTimeBetweenScraping = int(arguments["sleepTimeBetweenScraping"])
    convertPPTXToPDF = int(arguments["convertPPTXToPDF"])
    PPTXToPDFUnixCmd = arguments["PPTXToPDFUnixCmd"]
    PPTXToPDFWindowsCmd = arguments["PPTXToPDFWindowsCmd"]

def waitUntilNextScrape():
    time.sleep(sleepTimeBetweenScraping)

def convertPowerPointFiles():
    # call system independant command
    if platform.system() == "Linux" or platform.system() == "Darwin":
        os.system(PPTXToPDFUnixCmd)
    elif platform.system() == 'Windows':
        os.system(PPTXToPDFWindowsCmd)

    # remove converted pptx files
    for root, dirs, files in os.walk("files"):
        for f in files:
            if f.lower().endswith(".pptx"):
                os.remove(root+"/"+f)

while(True):
    # update arguments so we can adapt runtiime behaviour at each iteration
    getArguments()

    # set time to wait for http responses      
    socket.setdefaulttimeout(requestTimeout)
    
    # get url containing all downloadable items
    if verbose: print('Getting tamimeredith url.')
    page = requests.get(urlToScrape)
    tree = html.fromstring(page.content)
    items = tree.xpath(
        "body"
        "/div[@id='wrapper']"
        "/div[@id='main']"
        "/div[@id='container']"
        "/div[@id='content']"
        "/div[@id='post-927']"
        "/div[@class='entry-content']"
        "/ul"
        "/item"
        "/a")

    # get each item
    for i, item in enumerate(items):
        url = str(item.xpath("@href")[0])
        name = url.split('/')[-1]
        try:
            if verbose: print("Downloading file: {0}.".format(name))
            urllib.request.urlretrieve(url, pathToStoreFiles+name)
        except urllib.error.URLError:
            if verbose: print("Failed to obtain file: {0}.".format(name))
            pass
    totalItemsDownloaded += len(items)
    if verbose:
        print("Attempt #{0}. Time elapsed: {1}.".format(requestCounter, (time.time() - startTime)))
        print("Items downloaded: {0}.".format(len(items)))
        print("Total items downloaded: {0}.".format(totalItemsDownloaded))
        print("Process finished. Waiting {0} seconds before scraping again.\n\n".format(sleepTimeBetweenScraping))
    requestCounter += 1
    
    # convert powerpoint files to pdf and delete old pptx
    if convertPPTXToPDF:
        if verbose: print("Converting pptx files to pdf.")
        convertPowerPointFiles()

    waitUntilNextScrape()
    