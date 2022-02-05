from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq  # Web client
from urllib.request import Request, urlopen
import urllib.request
import io

# URl to web scrape from.
base_url = "https://www.tagoreweb.in/Novels/"
response = uReq.get(base_url)

# parses html into a soup data structure to traverse html
# as if it were a json data type.
page_soup = soup(response.read(), "html.parser")
uClient.close()

# finds all the links to each novel in the page
link = page_soup.find("div", {"class": "suchi_patra_area"})
url_list = link.find_all('a', href=True)

#traverses through the url list to get url for each novel and then extract the text from there
for url in url_list:
    # name the output file to write to local disk
    fname = url['href'][8:]+".txt"
    f = io.open(fname, "a", encoding="utf-8")
    url_ = "https://www.tagoreweb.in"+url['href']

    #soup data structure for each novel page
    response_ = uReq(url_)
    page_ = soup(response_.read(), "html.parser")

    #extract heading of the novel and write it to text file
    heading = page_.find("h2").text
    f.write(heading)

    #find the name of the url after the url was clicked from the novel homepage
    ul = page_.find("ul", {"class": "pagination"})
    btn = ul.find_all("button")
    page_link = btn[0]['onclick'].split("'")[1]
    page_link = "https://www.tagoreweb.in"+page_link

    #remove the number from the end of the link
    page_link = page_link[:-1]
    #scraping across multiple web pages by using a for loop
    for i in range(1,100):
        #checks if the page is empty or not by check if the subheading exists or not, if it
        #is empty then we have reached the end of the novel
        sub_heading = page_.find("h3")
        if sub_heading== None:
            break

        #extracting the content of the novel
        content = page_.find("div", {"class": "content-right"})
        text = content.find_all("p")
        string=""
        for text_ in text:
            string += text_.get_text()
        f.write(string+"\n")

        #appending number to get the link of the next page
        next_page_link = page_link+str(i+1)
        response_ = uReq(next_page_link)
        page_ = soup(response_.read(), "html.parser")

        #checks for invalid link
        error = page_.find("ul", {"class": "breadcrumb"}).find_all("li")[1].text.strip()
        if error == "Error":
            break
