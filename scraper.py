from bs4 import BeautifulSoup as soup, BeautifulSoup
from urllib.request import urlopen as uReq
from datetime import date
import re

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
            uClient = uReq(new_url)
            page_html_new = uClient.read()
            uClient.close()
            page_soup = soup(page_html_new, "lxml")
            print("finding ul")
            container = page_soup.find("ul",{"class":"inline-list indent"})
            print("ul found")
            #print(new_url)
            try:
                for link in container.findAll('a', href=True):
                    print("dddddd " + link.get('href'))
                    article_link = link.get('href')
                    article = uReq(article_link)
                    print("article read")
                    print(article_link)
                    soup_article: BeautifulSoup = soup(article, 'lxml')
                    print("parsed article")

                    # get title
                    if soup_article.find("header",{"class":"article-header"}):
                        title = soup_article.find("header",{"class":"article-header"}).h1
                        #print("got title")
                        news_title: str = title.get_text()
                        print(news_title)
                    if soup_article.find("h2",{"class":"contentItem__title"}):
                        title = soup_article.find("h2",{"class":"contentItem__title"})
                        #print("got title")
                        news_title: str = title.get_text()
                        print(news_title)
                    # get date
                    if soup_article.find('span', {"data-dateformat": "date1"}):
                        art_date = soup_article.find('span', {"data-dateformat": "date1"})
                        news_date = art_date.get_text()
                        print(news_date)
                    # get author
                    if soup_article.find('div',{'class':'author'}):
                        art_author = soup_article.find('div',{'class':'author'})
                        news_author = art_author.get_text()
                        print(news_author)
                        #body = soup_article.find_all('p')
                    # store paragraphs
                    #list_paragraphs = []
                   # news_made = ""
                    #for p in range(len(body)):
                    #    paragraph = body[p].get_text()
                    #    par = re.sub("[^0-9a-za-z]+", "|", paragraph)
                    #    # print(paragraph)
                    #    news_made = news_made + par
                    #    news_made.strip()
                    #    list_paragraphs.append(paragraph)
                    #    # print("next paragraph{} ".format(p))
                    #    final_article = " ".join(list_paragraphs)
                    #news_contents.append(final_article)
                    #print("got paragraphs")
                    f.write(news_title.replace(",", "|").strip() + "," + news_date.replace(",","|").strip() + "," + news_author.replace(",","|").strip() + "," + "\n")
            except Exception as e:
                print("didn't work, moving to finding li")
                for article in container.findAll('li'):

                    title_date = article.text.split("(")
                    print(title_date)
                    article_title = title_date[0]
                    article_date_1 = title_date[1].split(")")[0].split(",")
                    print(article_date_1)
                    article_date = article_date_1[0]+article_date_1[1]
                    news_title = article_title
                    news_date = article_date
                    print(article_title)

                    f.write(news_title.replace(",", "|").strip() + "," + news_date.replace(",","|").strip() + "\n")
        except Exception as e:
            pass
    f.close()