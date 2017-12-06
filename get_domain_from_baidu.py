#!/usr/bin/env python
# encoding: utf-8

"""
@version: V1.0
@author: johnson<514208140@qq.com>
@file: get_domain_from_baidu.py
@time: 12/4/17 3:13 PM
"""

"""
使程序支持Unicode编码
"""
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

import argparse
import requests
import getopt
from bs4 import BeautifulSoup

#利用beautifulSoup提取页面中需要的值
def get_html_bs(html_content):
    domains = []
    break_html = html_content

    soup = BeautifulSoup(break_html,"html.parser")
    div_text = soup.find_all(attrs={'class':'f13'})
    for text in div_text:
        a_text = text.find('a')
        for result in a_text:
            result = unicode(result)  #将NavigableString转为unicode
            domains.append(result)
    return domains

def get_site(key_word, hack_url, hack_page):
    key = hack_url
    sites = []
    if hack_page == 0:
        hack_page = 10
    for i in range(hack_page):
        print "The google hacking page %d" % i
        pn = i * 10
        url = "http://www.baidu.com.cn/s?wd=" + key_word + ":" + key + "&cl=3&pn=%s" % pn
        response = requests.get(url).content
        subdomains = get_html_bs(response)
        sites += list(subdomains)  #将每个界面的十个URL添加到sites中去
        site = list(set(sites))  #利用set实现去重

    for i in site:
        print i

#利用beautifulSoup提取页面中需要的值
def getUrlOfBsToInurlKeyword(html_content):
    domains = []
    break_html = html_content
    soup = BeautifulSoup(break_html,"html.parser")
    div_text = soup.find_all(attrs={'class':'f13'})
    for text in div_text:
        # print text
        a_text = text.find('a')
        # print a_text['href']  #获取a标签内的href
        resultOfHref = unicode(a_text['href'])  # 将NavigableString转为unicode
        url_result = get_realUrl(resultOfHref)  #获取真实的URL地址
        domains.append(url_result)
    return domains

def get_realUrl(url):
    real_url = requests.get(url.rstrip())  #rstrip()删除编码字符串末尾的空格
    return real_url.url


def print_help():
    parser = argparse.ArgumentParser(description="Search URL of google hacking")
    parser.add_argument("-k", "--keyword", help="Keyword is google hacking syntax.ex:site,inurl", required=True)
    parser.add_argument('-u', "--url", help="You want search URL", required=True)
    parser.add_argument("-p", "--page", help="The page you want search.Default is 10", required=False)
    parser.parse_args()

def main(argv):
    keyword = ""
    page = 10
    url = ""
    if len(argv) < 1:
        print_help()
        sys.exit(3)
    try:
        opts, args = getopt.getopt(argv, "hk:u:p:", ["keyword=", "url=" ,"page="])
    except getopt.GetoptError:
        print 'get_domain_from_baidu1.py [-h] -k <keyword> -u <url> -p <page=10>'
        sys.exit(3)
    for opt,arg in opts:
        if opt == "-h" or opt == "--help":
            print_help()
            sys.exit(3)
        elif opt in ("-k", "--keyword"):
            keyword = arg
        elif opt in ("-u", "--url"):
            url = arg
        elif opt in ("-p", "--page"):
            page = int(arg)
        else:
            print 'get_domain_from_baidu2.py [-h] -k <keyword> -u <url> -p <page=10>'
    if page == None:
        page = 10
    get_site(keyword, url, page)


if __name__ == '__main__':
    main(sys.argv[1:])
