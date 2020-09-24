from bs4 import BeautifulSoup as soup, BeautifulSoup
from urllib.request import urlopen as uReq
from datetime import date
import re

my_url = input("site: ")
if my_url.__contains__("com"):
    url_ = my_url.partition("com")[0]
    url_ = url_ + "com"
elif my_url.__contains__("ca"):
    url_ = my_url.partition("ca")[0]
    url_ = url_ + "ca"

print(url_)
# opening and grabbing page
# opening and grabbing page
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

# html parse
page_soup = soup(page_html, "lxml")

containers = page_soup.findAll("section", {"class": "contentItem__content"})

if page_soup.find("section", {"id": "news-feed"}):
    container = page_soup.find("section", {"id": "news-feed"})
elif page_soup.find("div", {"class": "content-main"}):
    container = page_soup.find("div", {"class": "content-main"})
elif page_soup.find("div", {"class": "template--article__content"}):
    container = page_soup.find("div", {"class": "template--article__content"})
    print(len(container.find_all("a")))
    print("elif")
elif page_soup.find("section", {"class": "grid__content grid__content--cards"}):
    container = page_soup.find("section", {"class": "grid__content grid__content--cards"})
    print("new ")
elif page_soup.find("ul",{"id":"archive-latestStories"}):
    container = page_soup.find("ul",{"id":"archive-latestStories"})
    print("global news")
else:
    container = page_soup
    print("else")
    print(len(container))

if page_soup.findAll("article"):
    containers_1 = page_soup.findAll("article")

news_contents = []

fileName = input("file name: ")
f = open(fileName, "w")

headers = "news_title, news_date, news_paragraphs \n"
f.write(headers)

for link in container.findAll('a', href=True):
    print("dddddd " + link.get('href'))
    try:
        article_link = str(url_) + str(link.get('href'))
        if "com" or "ca" in str(link.get('href')):
            if "http" in str(link.get('href')):
                article_link = str(link.get('href'))
                print("has http in it already")
        # read article content
        article = uReq(article_link)
        print("article read")
        print(article_link)
        soup_article: BeautifulSoup = soup(article, 'lxml')
        print("parsed article")
        # get title
        if soup_article.h1:
            title = soup_article.h1
            print("got title")
            news_title: str = title.get_text()
        print(news_title)
        try:
            if soup_article.find('header', {"class": "article-header"}).h1:
                title = soup_article.find('header', {"class": "article-header"}).h1
                news_title = title.get_text()
            print(news_title)
        except:
            pass
        try:
            if soup_article.find('div', {"class": "headline"}).h1:
                title = soup_article.find('div', {"class": "headline"}).h1
                news_title = title.get_text()
            print(news_title)
        except:
            pass


        # get date

        if (soup_article.find('span', {"data-dateformat": "date1"})):
            art_date = soup_article.find('span', {"data-dateformat": "date1"})
            news_date = art_date.get_text()
        elif (soup_article.find('div', {"class": "date"})):
            art_date = soup_article.find('div', {"class": "date"})
            news_date = art_date.get_text()
        elif (soup_article.find('time')):
            art_date = soup_article.find('time')
            if "/" in art_date:
                news_date = art_date.get_text().strip()
                news_date = news_date.strftime("%B %d, %Y")
            else:
                today = date.today()
                news_date = today.strftime("%B %d, %Y")
        else:
            today = date.today()
            news_date = today.strftime("%B %d, %Y")
        print(news_date)

        body = soup_article.find_all('p')

        # store paragraphs
        list_paragraphs = []
        news_made = ""
        for p in range(len(body)):
            paragraph = body[p].get_text()
            par = re.sub("[^0-9a-zA-Z]+", "|", paragraph)
            # print(paragraph)
            news_made = news_made + par
            news_made.strip()
            list_paragraphs.append(paragraph)
            # print("next paragraph{} ".format(p))
            final_article = " ".join(list_paragraphs)
        news_contents.append(final_article)
        print("got paragraphs")

        if len(list_paragraphs) > 2:
            print(len(list_paragraphs))
            f.write(news_title.replace(",", "|").strip() + "," + news_date.replace(",",
                                                                                   "|").strip() + "," + news_made.replace(
                ",", "|").strip() + "\n")

    except Exception as e:
        pass

if "nba" in url_:
    pages = [2, 3, 4, 5, 6, 7, 8]
    for page in pages:

        my_url_mult = 'https://ca.nba.com/all/news/page/{}'.format(page)
        # opening and grabbing page
        uClient = uReq(my_url_mult)
        page_html = uClient.read()
        uClient.close()

        # html parse
        page_soup = soup(page_html, "html.parser")

        container = page_soup.find("section", {"class": "grid__content grid__content--cards"})
        len(container)
        for link in container.findAll('a', href=True):
            print("dddddd " + link.get('href'))
            try:
                article_link = str(url_) + str(link.get('href'))
                if "com" or "ca" in str(link.get('href')):
                    article_link = str(link.get('href'))
                    print("has http in it already")
                # read article content
                article = uReq(article_link)
                print("article read")
                print(article_link)
                soup_article: BeautifulSoup = soup(article, 'lxml')
                print("parsed article")
                # get title
                if soup_article.h1:
                    title = soup_article.h1
                    print("got title")
                    news_title: str = title.get_text()
                try:
                    if soup_article.find('header', {"class": "article-header"}).h1:
                        title = soup_article.find('header', {"class": "article-header"}).h1
                        news_title = title.get_text()
                except:
                    pass
                try:
                    if soup_article.find('div', {"class": "headline"}).h1:
                        title = soup_article.find('div', {"class": "headline"}).h1
                        news_title = title.get_text()
                except:
                    pass
                print(news_title)

                # get date

                if soup_article.find('span', {"data-dateformat": "date1"}):
                    art_date = soup_article.find('span', {"data-dateformat": "date1"})
                    news_date = art_date.get_text()
                elif soup_article.find('div', {"class": "date"}):
                    art_date = soup_article.find('div', {"class": "date"})
                    news_date = art_date.get_text()
                elif soup_article.find('time'):
                    art_date = soup_article.find('time')
                    news_date = art_date.get_text().strip()
                else:
                    today = date.today()
                    news_date = today.strftime("%B %d, %Y")
                print(news_date)

                body = soup_article.find_all('p')

                # store paragraphs
                list_paragraphs = []
                news_made = ""
                for p in range(len(body)):
                    paragraph = body[p].get_text()
                    par = re.sub("[^0-9a-zA-Z]+", "|", paragraph)
                    # print(paragraph)
                    news_made = news_made + par
                    news_made.strip()
                    list_paragraphs.append(paragraph)
                    # print("next paragraph{} ".format(p))
                    final_article = " ".join(list_paragraphs)
                news_contents.append(final_article)
                print("got paragraphs")
                if len(list_paragraphs)>2:
                    f.write(news_title.replace(",", "|").strip() + "," + news_date.replace(",","|").strip() + "," + news_made.replace(",", "|").strip() + "\n")

            except Exception as e:
                raise

f.close()
