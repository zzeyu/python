import urllib.request
from bs4 import BeautifulSoup
import urllib.parse
import re
import os

#添加一个URL到集合
def add_new_url(url):
    if url not in new_urls and url not in old_urls:
        new_urls.add(url)

#添加多个URL到集合		
def add_urls(urls):
    if urls is None:
        return
    for url in urls:
        add_new_url(url)

#判断URL集合是否为空
def has_url():
    return len(new_urls)!=0

#从集合中取出一个URL	
def get_new_url():
    url=new_urls.pop()
    old_urls.add(url)
    return url
	
#获得当前网页的多个URL，返回URL集合
def _get_new_urls(url,soup):
    new_urls=set()
    links=soup.find_all('a',href=re.compile('www.umei.cc/meinvtupian/meinvxiezhen/'))
    for link in links:
        new_url=link['href']
        new_full_url= urllib.parse.urljoin(url,new_url)
        new_urls.add(new_full_url)
    return new_urls

#获得当前网页的图片信息
def _get_new_img(url,soup):
    datas={}
    title=soup.find('div',class_="ArticleTitle").find('strong')
    datas['title']=title.get_text()                    #图片名字
    
    link=soup.find('a',href=re.compile("htm"))
    datas['src']=link.find('img')['src']               #图片网址
    
    return datas

#解析网页内容，返回URLS，图片信息	
def parse(html_const,url):
    soup=BeautifulSoup(html_const,'html.parser',from_encoding='utf-8')
    urls=_get_new_urls(url,soup)
    datas=_get_new_img(url,soup)
    
    return urls,datas

#创建文件夹
def create_dir(dir_name):
    try:
        os.mkdir(dir_name)
    except FileExistsError:
        print('文件夹已存在')

if __name__ == '__main__':
    new_urls=set()
    old_urls=set()
    datas=[]
    url='http://www.umei.cc/meinvtupian/meinvxiezhen/198141.htm'
    dir_name='photo'
    create_dir(dir_name)
    add_new_url(url)
    cnt=1
    while has_url():
        try:
            new_url=get_new_url()
            html_const=urllib.request.urlopen(new_url)
            urls,data=parse(html_const,new_url)
            add_urls(urls)
            urllib.request.urlretrieve(data['src'],dir_name+'/'+data['title']+'.jpg')
            if cnt == 100:
                break
            cnt+=1
        except:
            print('error')

