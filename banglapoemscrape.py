from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq  # Web client
from urllib.request import Request, urlopen
import urllib.request
import io

class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"

opener = AppURLopener()
# URl to web scrape from. Page contains the links to the list of poems
page_url = "https://www.bangla-kobita.com/ishwarchandragupta/"
response = opener.open(page_url)

# parses html into a soup data structure to traverse html
# as if it were a json data type.
page_soup = soup(response.read(), "html.parser")

# table contains the link to each poem of the poet
table = page_soup.find("table", {"class": "post-list"})
url_list = table.find_all("meta",  itemprop="url")

# name the output file to write to local disk
fname = "data/bangla_literature_corpus.txt"
f = io.open(fname, "a", encoding="utf-8")

#loop to scrape multiple pages from the url list. Each page contains one poem.
for i in range(len(url_list)):
    string = ""
    #content tag contains the url to the poem page
    url = url_list[i]['content']
    responses = opener.open(url)
    page_soups = soup(responses.read(), "html.parser")
    #extracts the text of the poem
    a = page_soups.find("div",{"class":"post-content"})
    text = a.find_all("p")
    #writing the text extracted to a txt file
    for j in range(len(text)):
        string += text[j].get_text("\n")
        string +="\n"
    string+="\n\n\n"
    f.write(string)
