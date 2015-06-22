#coding=utf-8
import urllib
import re
import datetime
import threading
import multiprocessing

#根据文章url来获取文章内容
def url_save_article(url):
    #打开网址中的内容
    url_content = urllib.urlopen(url).read()
    article_start = url_content.find('<!-- 正文开始 -->')
    article_end = url_content.find('<!-- 正文结束 -->')
    article_content = url_content[article_start:article_end]

    #解析标题名作为文件名
    file_name_start = url_content.find('<title>')
    file_name_end = url_content.find('</title>')
    file_name = url_content[file_name_start + 7:file_name_end]
    print file_name

    #解析文章内容
    p = re.compile('<.*>')
    find_tuple = p.split(article_content)

    #将文章内容写入文件
    f = file(file_name, 'w')
    f.write(' '.join(find_tuple))
    f.close

#根据文章目录列表url来爬取每篇文章url
def blog_list_analysis(blog_list_url):
    blog_list_content = urllib.urlopen(blog_list_url).read()
    p = re.compile('<a title=.*</a>')
    blog_address_tuple = p.findall(blog_list_content)
    blog_address_str = ' '.join(blog_address_tuple)

    for blog_address in blog_address_tuple:
        blog_address_start = blog_address.find('href=')
        blog_address_end = blog_address.find('html')
        url_save_article(blog_address[blog_address_start + 6 : blog_address_end + 4])

#根据第一页目录列表来解析其他页目录列表,并调用其他函数
def source_list_analysis(all_blog_list_address_url):
    #all_blog_list_address_url = 'http://blog.sina.com.cn/s/articlelist_1191258123_0_1.html'
    all_blog_list_content = urllib.urlopen(all_blog_list_address_url).read()
    p1 = re.compile('<li>.*<li class="SG_pgnext">')
    all_blog_address_tuple = p1.findall(all_blog_list_content)
    all_blog_address_str = ' '.join(all_blog_address_tuple)
    #print all_blog_address_str
    p2 = re.compile('href=')
    list_address_tuple = p2.split(all_blog_address_str)
    address_list = ['http://blog.sina.com.cn/s/articlelist_1191258123_0_1.html']
    for unchanged_address in list_address_tuple:
        changed_address_start = unchanged_address.find('http:')
        changed_address_end = unchanged_address.find('html')
        changed_address = unchanged_address[changed_address_start : changed_address_end + 4]
        if changed_address:
            address_list.append(changed_address)
        else:
            pass
    for address in address_list:
        #blog_list_analysis(address)
        proc = multiprocessing.Process(target = blog_list_analysis, args = (address,))
        process.append(proc)
    for p in process:
        p.start()
    for p in process:
        p.join()

process = []
starttime = datetime.datetime.now()
source_list_url = 'http://blog.sina.com.cn/s/articlelist_1191258123_0_1.html'
source_list_analysis(source_list_url)
endtime = datetime.datetime.now()
print "本次下载所消耗的时间为:" + str((endtime - starttime).seconds) + "s"
