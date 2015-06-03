#coding: utf-8

import string, urllib2
import re
'''
def spideURL(url):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = { 'User-Agent' : user_agent }
    req = urllib2.Request(url, headers = headers)
    myResponse = urllib2.urlopen(req)
    myPage = myResponse.read()
    #encode的作用是将unicode编码转换成其他编码的字符串
    #decode的作用是将其他编码的字符串转换成unicode编码
    unicodePage = myPage.decode("utf-8")
    #myItems = re.findall('<div.*?class="content">(.*?)<.*?></div>',unicodePage,re.S)
    myItems = re.findall('</a></span><p><img src=(.*?)/></p>.*?<div',unicodePage,re.S)

    items = []
    for item in myItems:
        print item
    #f = open("qiu.txt",'w+')
    #f.write(myPage)
    #f.close()
    print("done.")


#spideURL("http://www.qiushibaike.com/text")
spideURL("http://jandan.net/ooxx/page-1413#comments")
'''

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from pyquery import PyQuery as pq
from time import ctime
import time
import re
import os
import urllib

def main(page_start, page_end, flag):
    file_path_pre = 'D:/Download/Python/'
    folder_name = 'ooxx' if flag else 'pic'
    page_url = 'http://jandan.net/' + folder_name + '/page-'
    folder_name = file_path_pre + folder_name + '/' + str(page_start) + '-' + str(page_end) + '/'
    for page_num in range(page_start,page_end + 1):
        crawl_page(page_url, page_num, folder_name)

def crawl_page(page_url, page_num, folder_name):
    page_url = page_url + str(page_num)
    print 'start handle', page_url
    print '', 'starting at', ctime()
    t0 = time.time()

    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    headers = { 'User-Agent' : user_agent }
    req = urllib2.Request(page_url, headers = headers)
    page_html = pq(url = req)
    #myResponse = urllib2.urlopen(req)
    #page_html = pq(url = page_url,headers = headers)
    comment_id_patt = r'<li id="comment-(.+?)">'
    #comment_ids = re.findall(comment_id_patt, myPage)
    comment_ids = re.findall(comment_id_patt, page_html.html())
    name_urls = {}
    for comment_id in comment_ids:
        name_url = dispose_comment(page_html,comment_id)
        if name_url:
            name_urls.update(name_url)
    if not os.path.exists(folder_name):
        print '','new folder',folder_name
        os.makedirs(folder_name)
    for name_url in name_urls.items():
        file_path = folder_name + 'page-' + str(page_num) + name_url[0]
        img_url = name_url[1]
        if not os.path.exists(file_path):
            print '', 'start download', file_path
            #print '','img_url is',img_url
            urllib.urlretrieve(img_url, file_path)
        else:
            print '', file_path, 'is already downloaded'
    print 'finished at', ctime(), ',total time', time.time()-t0, 'ms'

def dispose_comment(page_html, comment_id):
    name_url_dict = {}
    id = '#comment-'+comment_id
    comment_html = page_html(id)
    oo_num = int(comment_html(id + ' #cos_support-' + comment_id).text())
    xx_num = int(comment_html(id + ' #cos_unsupport-'  + comment_id).text())
    oo_to_xx = oo_num/xx_num if xx_num != 0 else oo_num
    if oo_num > 1 and oo_to_xx > 0:
        imgs = comment_html(id + ' img')
        for i in range(0, len(imgs)):
            org_src = imgs.eq(i).attr('org_src')
            src = imgs.eq(i).attr('src')
            img_url = org_src if org_src else src
            if img_url:
                img_suffix = img_url[-4:]
                if not img_suffix.startswith('.'):
                    img_suffix = '.jpg'
                img_name = id + '_oo' + str(oo_num) + '_xx' + str(xx_num) + (('_' + str(i)) if i != 0 else '') + img_suffix
                name_url_dict[img_name] = img_url
            else:
                print '***url not exist'
    return name_url_dict

if __name__ == '__main__':
    page_start = int(raw_input('Input  start page number: '))
    page_end   = int(raw_input('Input  end   page number: '))
    is_ooxx    = int(raw_input('Select 0: wuliao 1: meizi '))
    main(page_start, page_end, is_ooxx)