import requests
from bs4 import BeautifulSoup
import os
import re
import threading
import time
#https://guoxue.httpcn.com/book/b62639b63ed94ffbbed05b3868ebfb53/

headers = {
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
    #'Cookie': 'xqat=3e14cc861fdd960a5d84e7316165286b1bfeafe3;',
}


def get_src():
    h_url = 'https://guoxue.httpcn.com/book/b62639b63ed94ffbbed05b3868ebfb53/'
    newslist = requests.get(h_url, headers=headers)
    soup = BeautifulSoup(newslist.text, "lxml")
    return soup


title_list = dict()
def get_hancheng(soup):
    datalist = soup.find_all(class_="catelog_book")
    for list in datalist:
        data = list.find_all('a')
        print(data)
        for mm in data:
            m_href = mm['href']
            m_title = mm.get_text()
            title_list.setdefault(m_title, [])
            title_list[m_title].append(m_href)
        print(title_list)

def run():
    for li in title_list:
        for m_url in title_list[li]:
            m_url = m_url.replace('//', 'http://')
            t1 = threading.Thread(target=get_content, args=(m_url, li, ))
            t1.start()
            time.sleep(8)
            t1.join()

lock = threading.Lock()
def get_content(m_url, m_title):
    newslist = requests.get(m_url, headers=headers)
    soup = BeautifulSoup(newslist.text, "lxml")
    datalist = soup.find_all(class_='contentBox')
    print(datalist)
    m_str = "" #内容 m_name章节
    for list in datalist:
        list.find_all('p')
        for font in list:
            matchObj = re.search(r'<p>(.*?)</p>', str(font), re.M | re.I)
            # matchObj = re.research(r'<p>(.*?)</p>', str(font))
            if matchObj:
                m_font = matchObj.group()
                m_font = m_font.replace('<p>', '')
                m_font = m_font.replace('</p>', '')
                m_str = m_str + m_font
        print(m_str)

    # datalist2 = soup.find_all(class_='yd-list yd-list-theme1 ')
    # m_zhu = ""
    # m_yi = "" #注释 译文
    # for list in datalist2:
    #     m_zhu = m_yi
    #     m_yi = list.get_text()


    lock.acquire()
    filename = "孙子兵法.txt"
    with open(filename, "a+", encoding='utf-8') as f:
        f.write(m_title + "\n")
        f.write(m_str + "\n \n")
        # f.write("注释: \n" + m_zhu + "\n")
        # f.write("译文: \n" + m_yi + "\n")
        f.write("\n\n")
    lock.release()


if __name__ == '__main__':
    soup = get_src() #get孙子兵法
    get_hancheng(soup)
    run()
    print("end")
