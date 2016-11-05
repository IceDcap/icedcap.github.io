#! /usr/bin/python
# -*- coding:utf-8 -*-
import urllib
import socket
import json
import os
import HTMLParser
import threading
import time
import sys


global jsonstr, hostname, croot, maxtimeout, tryagaincount
global threadcount, currentthreadnum, mutex, thenewest

hostname = r'http://www.ishuhui.net'
chapters = r'/ComicBooks/GetChapterList?id=' + '%d' + '&PageIndex=' + '%d'
details = r'/ComicBooks/ReadComicBooksToIsoV1/' + '%d'
repo = {
    'op': 2,
    'SLAM_DUNK': 38,
    '火影忍者': 4,
    '银魂': 10,
    '妖精的尾巴': 3,
    '名侦探柯南': 1,
    'bleach': 23,
    '黑子的篮球': 6,
    '浪客剑心': 39,
    '结界师': 34
}
arg = '[op, SLAM_DUNK, 火影忍者, 银魂, 妖精的尾巴, 名侦探柯南, bleach, 黑子的篮球, 浪客剑心, 结界师]'
cartoonid = repo['op']
thenewest = 0
currentthreadnum = 0
threadcount = 6
tryagaincount = 5
maxtimeout = 30
croot = os.getcwd()
mutex = threading.Lock()
usage = \
    """
    Usage:
            cartoon_download [args...]

            cartoon_download cartoon
            cartoon_download cartoon path
            cartoon_download cartoon path newestcount
            cartoon_download cartoon path newestcount threadcount

    For example:
            cartoon_download op /home/xxx/onepiece

    Note:
            current version just support Linux/Unix os.
            cartoon = %s
            path can be either absolute or relative, but must be en characters.
            default `newestcount` value is 0 to download all chapters, or
            download the newest value chapters.
    """ % arg


if len(sys.argv) == 1:
    print usage
    sys.exit(0)
if len(sys.argv) >= 2:
    try:
        cartoonid = repo[sys.argv[1]]
    except Exception, e:
        print 'Please select from %s' % arg
        sys.exit(0)
    finally:
        pass
if len(sys.argv) >= 3:
    targetdir = sys.argv[2]
    if not os.path.exists(targetdir):
        os.makedirs(targetdir)
    croot = os.path.abspath(targetdir)
    if len(sys.argv) >= 4:
        thenewest = (int)(sys.argv[3])
    if len(sys.argv) == 5:
        threadcount = (int)(sys.argv[4])


class MyHTMLParser(HTMLParser.HTMLParser):
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.gifs = []
        self.jpgs = []
        self.pngs = []

    def handle_starttag(self, tags, attrs):
        if tags == 'img':
            for attr in attrs:
                for htmlstr in attr:
                    if 'gif' in htmlstr:
                        self.gifs.append(htmlstr)
                    elif 'jpg' in htmlstr:
                        self.jpgs.append(htmlstr)
                    elif 'png' in htmlstr:
                        self.pngs.append(htmlstr)
                    else:
                        pass

    def get_gifs(self):
        return self.gifs

    def get_jpgs(self):
        return self.jpgs

    def get_pngs(self):
        return self.pngs


class DownloadTask(threading.Thread):

    def __init__(self, name, srcurl):
        threading.Thread.__init__(self)
        self.name = name
        self.srcurl = srcurl

    def run(self):
        pic2file(self.srcurl)


def createtask(imgs):
    global mutex, currentthreadnum, threadcount
    print 'current tasks num >> %d' % len(imgs)
    for srcurl in imgs:
        while (currentthreadnum >= threadcount):
            time.sleep(0.5)
        increasethread()
        threadname = '#%s' % srcurl
        task = DownloadTask(threadname, srcurl)
        task.start()
    while (currentthreadnum > 0):
        time.sleep(0.5)
    print 'finished!'
    os.chdir(croot)


def parser2name(picurl):
    names = picurl.split('/')
    result = names[len(names) - 1]
    if '?' in result:
        result = result.split('?')[0]
    return result


def increasethread():
    global currentthreadnum, mutex
    mutex.acquire()
    currentthreadnum += 1
    mutex.release()


def decreasethread():
    global currentthreadnum, mutex
    mutex.acquire()
    currentthreadnum -= 1
    mutex.release()


def pic2file(picurl, times=0):
    protocol = picurl.split('/')[0]
    if not(protocol == 'http:' or protocol == 'https:'):
        decreasethread()
        return
    filename = parser2name(picurl)
    if(os.path.exists(filename)):
        decreasethread()
        return
    try:
        pic = urllib.urlopen(picurl)
        data = pic.read()
        picfile = open('%s' % filename, 'wb')
        picfile.write(data)
        picfile.close()
        decreasethread()
    except socket.timeout:
        if times < tryagaincount:
            print "Download '%s' timeout, Trying again." % filename
            pic2file(picurl, times + 1)
        else:
            decreasethread()
            print "Tried %d times, but still failed to %s." %\
                (tryagaincount, filename)
    except Exception as e:
        print('---pic2file error---', e)
        if times < tryagaincount:
            print "Download '%s' timeout, Trying again." % filename
            pic2file(picurl, times + 1)
        else:
            decreasethread()
            print "Task '%s' failed after tring %d times" %\
                (picurl, tryagaincount)
    finally:
        pass


def fixurl(picurl):
    piece = picurl.split('/')
    url = 'http:'
    for p in xrange(1, len(piece)):
        url += '/%s' % piece[p]
    return url


def fetchres(detailurl, dirpath, times=0):
    try:
        if not os.path.exists(dirpath):
            os.mkdir(dirpath)
        os.chdir(dirpath)
        curdir = os.getcwd()
        print 'Download for ' + curdir
        detailbook = urllib.urlopen(detailurl).read()
        htmlfile = open('%s.html' % parser2name(curdir), 'wb')
        htmlfile.write(detailbook)
        htmlfile.close()
        parser = MyHTMLParser()
        parser.feed(detailbook)
        jpgs = parser.get_jpgs()
        pngs = parser.get_pngs()
        gifs = parser.get_gifs()
        imgs = jpgs + pngs + gifs
        createtask(imgs)
    except socket.timeout:
        print "Fetch '%s' timeout." % detailurl
        if times < tryagaincount:
            print "The no.%d times to try." % (times + 2)
            fetchres(detailurl, dirpath, times + 1)
        else:
            print "Tried %d times, but still failed."
            print "####Please check network!####"
    except Exception, e:
        print(e)
    finally:
        pass


def jsonparse():
    encodejson = json.loads(jsonstr)
    result = encodejson["Return"]["List"]
    if thenewest > 0:
        for i in xrange(0, thenewest):
            parserandsavehtml(result[i])
        return False
    else:
        for x in result:
            parserandsavehtml(x)
        return len(result)


def parserandsavehtml(item):
    bookid = item["Id"]
    detailurl = hostname + details % bookid + '.html'
    chapterno = item["ChapterNo"]
    title = item["Title"]
    dirname = '%d %s' % (chapterno, title)
    # Here cause an error `UnicodeEncodeError` when
    # the 'croot' include chinese characters.
    # details info can seach for http://www.cnblogs.com/abcat/p/3389531.html
    targetpath = os.path.join(croot, dirname)
    fetchres(detailurl, targetpath)


def calculatetime(used):
    if used <= 60:
        print 'Total used time is %ds.' % used
    elif used <= 3600:
        print 'Total used time is %dmins %ds.' % (used / 60, used % 60)
    else:
        print 'Total used time is %dhrs %dmins %ds.' %\
            (used / 3600, (used % 3600) / 60, (used % 3600) % 60)


if __name__ == '__main__':
    os.chdir(croot)
    socket.setdefaulttimeout(maxtimeout)
    start = time.time()
    try:
        i = 0
        isbreak = True
        while isbreak:
            targetweb = hostname + chapters % (cartoonid, i)
            webfile = urllib.urlopen(targetweb)
            jsonstr = webfile.read()
            isbreak = jsonparse()
            i = i + 1
        end = time.time()
        calculatetime(int(end - start))
    except socket.timeout:
        print('timeout')
    except Exception as e:
        print('error', e)
    finally:
        pass
