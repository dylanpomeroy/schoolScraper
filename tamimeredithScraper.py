from lxml import html
import requests
import urllib

page = requests.get('http://www.tamimeredith.ca/academic/csci-3136/')
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

for i, item in enumerate(items):
    url = str(item.xpath("@href")[0])
    name = url.split('/')[-1]
    try:
        urllib.request.urlretrieve(url, "/var/www/html/schoolScraper/3136/"+name)
    except urllib.error.URLError:
        pass