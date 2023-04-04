import requests
from bs4 import BeautifulSoup
import os
import re
import time

headers = {
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
    #'Cookie': 'xqat=3e14cc861fdd960a5d84e7316165286b1bfeafe3;',
}


def get_src():
    #f12 手机端
    h_url = 'http://gx.httpcn.com/book/daodejing/quanwen/'
    newslist = requests.get(h_url, headers=headers)
    soup = BeautifulSoup(newslist.text, "lxml")
    return soup


title_list = dict()
def get_hancheng(soup):
    datalist = soup.find_all(class_="dushu_cont")
    for list in datalist:
        data = list.find_all('a')
        for mm in data:
            m_href = mm['href']
            matchObj = re.search('<i>(.*?)</i>', str(mm), re.M|re.I)
            if matchObj:
                m_title = matchObj.group()
                m_title = m_title.replace('<i>', '')
                m_title = m_title.replace('</i>', '')
                title_list.setdefault(m_title, [])
                title_list[m_title].append(m_href)

def run():
    for li in title_list:
        for m_url in title_list[li]:
            m_url = m_url.replace('//', 'http://')
            get_content(m_url, li)
            time.sleep(8)

def get_content(m_url, m_name):

    newslist = requests.get(m_url, headers=headers)
    soup = BeautifulSoup(newslist.text, "lxml")
    datalist = soup.find_all(class_='ly_combine')
    m_str = "" #内容 m_name章节
    for list in datalist:
        list.find_all('b')
        for font in list:
            matchObj = re.search('<b>(.*?)</b>', str(font), re.M | re.I)
            if matchObj:
                m_font = matchObj.group()
                m_font = m_font.replace('<b>', '')
                m_font = m_font.replace('</b>', '')
                m_str = m_str + m_font


    datalist2 = soup.find_all(class_='lunyu_jies')
    m_zhu = ""
    m_yi = "" #注释 译文
    for list in datalist2:
        m_zhu = m_yi
        m_yi = list.get_text()


    filename = "道德经.txt"
    with open(filename, "a+", encoding='utf-8') as f:
        f.write(str(m_name) + "\n")
        f.write(m_str + "\n \n")
        f.write("注释: \n" + m_zhu + "\n")
        f.write("译文: \n" + m_yi + "\n")
        f.write("\n\n\n")


if __name__ == '__main__':
    soup = get_src() #get 道德经
    get_hancheng(soup)
    run()
    print("end")
