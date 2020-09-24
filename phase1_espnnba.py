from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
from datetime import date
import re

my_url = "https://espn.com/nba/"
url_ = "https://espn.com"
# opening and grabbing page
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

# html parse
page_soup = soup(page_html, "lxml")

containers = page_soup.findAll("section", {"class": "contentItem__content"})

container = page_soup.find("section", {"id": "news-feed"})

print(len(container.find_all("a")))
containers_1 = page_soup.findAll("article")

news_contents = []

fileName = "espn_nba.csv"
f = open(fileName, "w")

headers = "news_title, news_date, news_paragraphs \n"
f.write(headers)
for link in container.findAll('a', href=True):
    print("dddddd " + link.get('href'))
    try:


        # read article content
        article_link = str(url_) + str(link.get('href'))
        article = uReq(article_link)

        soup_article = soup(article, 'lxml')

        #get title
        title = soup_article.find('header',{"class": "article-header"}).h1
        news_title = title.get_text()
        print(news_title)

        #get date

        if (soup_article.find('span',{"data-dateformat": "date1"})):
            art_date =  soup_article.find('span',{"data-dateformat": "date1"})
            news_date = art_date.get_text()
        else:
            today = date.today()
            news_date = today.strftime("%B %d, %Y")
        print(news_date)

        body = soup_article.find_all('p')

        #store paragraphs
        list_paragraphs = []
        news_made = ""
        for p in range(len(body)):
            paragraph = body[p].get_text()
            par = re.sub("[^0-9a-zA-Z]+", "|",paragraph)
            print(paragraph)
            news_made = news_made + par
            news_made.strip()
            list_paragraphs.append(paragraph)
            #print("next paragraph{} ".format(p))
            final_article = " ".join(list_paragraphs)
        news_contents.append(final_article)
        print("got paragraphs")

        f.write(news_title.replace(",", "|").strip() + "," + news_date.replace(",", "|").strip() + "," + news_made.replace(",", "|").strip() + "\n")

    except:
        pass

f.close()