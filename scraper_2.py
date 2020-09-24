from bs4 import BeautifulSoup as soup, BeautifulSoup
from urllib.request import urlopen as uReq
from datetime import date
import re
from urllib.request import Request, urlopen


yrs = ['2020','2019','2018','2010']
mths = ['january','february','march', 'april', 'may','june','july','august','september','october','november','december']

my_url = input("site: ")
#save year
yr_url = ""
mth_url = ""
for y in yrs:
    if y in my_url:
        yr_url = y
#save month
for m in mths:
    if m in my_url:
        mth_url = m

print(re.findall(r'\d+', my_url))


#webscrape each year
for yr_position in range(len(yrs)):
    new_url_y = my_url.replace(yr_url, yrs[yr_position])
    #create file
    fileName = input("file name: ")
    f = open(fileName, "w")
    headers = "news_title, news_date, news_author, news_paragraphs \n"
    f.write(headers)
    for mth_position in range(len(mths)):
        try:
            new_url = new_url_y.replace(mth_url, mths[mth_position])
            print(new_url)
            req = Request(new_url, headers={'User-Agent': 'Mozilla/5.0'})
            page_html = urlopen(req).read()
            req.close()
            page_soup = soup(page_html, "lxml")
            container = page_soup.find("ul",{"class":"inline-list indent"})
            print(container)
            for article in container.findAll('li'):
                title_date = article.text.split("(")
                article_title = title_date[0]
                article_date_1 = title_date[1].split(")")[0].split(",")
                article_date = article_date_1[0]+article_date_1[1]

                print(article_title)
                print(article_date)
        except:
            raise
