import re
import urllib2
import sys
import time
import MySQLdb
import hashlib
import threading

class Spider(threading.Thread):
    url = ""
    conn = ""
    cur = ""
    def __init__(self,url):
        threading.Thread.__init__(self)
        self.url = url
        self.conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='',port=3306)
        self.cur=self.conn.cursor()
        self.cur.execute("set names utf8;")

    def run(self):
        html = getHtml(self.url)
        if html:
            self.getMagnet(html)
        self.conn.commit()
        self.conn.close()

    def stop(self):
        self.thread_stop = True


    def (self,html):
        trtd = re.compile("<tr>(.*)</tr>")
        trlist = trtd.findall(html)
        magnum = 0
        for tr in trlist:
            namere = re.compile("<td class="name">(.*)</td><tdsclass="size">")
            magnetre = re.compile("magnet:(.*)"stitle=")
            name = namere.findall(tr)
            magnet = magnetre.findall(tr)
            try:
                filename = name[0]
                filemagnet = 'magnet:'+magnet[0]
                magnum = magnum + self.writeFile(filename,filemagnet)
            except:
                nt = 0
        print "--- Get ("+ str(magnum) +") Magnets On ("+self.url+")---n"

    def writeFile(self,name,url):
        md5url = hashlib.md5(url).hexdigest()
        sql = "insert into kitty.magnet(source,name,magnet,md5) values('"+self.url+"','"+name+"','"+url+"','"+md5url+"')"
        try:
            self.cur.execute(sql)
            return 1
        except:
            return 0


def getHtml(url):
    try:
        print "------Try : Begin Get "+url+"------"
        rep = urllib2.Request(url)
        URLLIB2_USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.57 Safari/537.17'
        rep.add_header('User-Agent', URLLIB2_USER_AGENT)
        res = urllib2.urlopen(rep)
        html = res.read()
        res.close()
        return html
    except:
        print "++++++Error : Retry Get "+url+"++++++"
        getHtml(url)


def getPage(url,html):
    lst = []
    plst = []
    pageinfore = re.compile("<divsclass="pagination">(.*)</div>")
    pageinfo = pageinfore.findall(html)
    num = []
    for pagenum in pageinfo:
        numinfo = re.compile("<ashref="(d+)">")
        num = numinfo.findall(pagenum)
    num = list(set(num))
    pagenumbs = 0
    max = 1
    for i in num:
        if int(i) > max:
            max = int(i)
    j=2
    lst.append(url)
    plst.append("1")
    while(j<=int(max)):
        lst.append(url+str(j))
        plst.append(str(j))
        j = j +1
    print "--- Found ("+str(plst)+") Pages----"
    return lst


def datetime_timestamp(dt):
     s = time.mktime(time.strptime(dt, '%Y-%m-%d %H:%M:%S'))
     return int(s)


dt=datetime_timestamp("2012-10-16 00:00:00")


while dt>datetime_timestamp("2007-01-01 00:00:00"):
    dttime =  time.strftime('%Y-%m-%d',time.gmtime(dt))
    html = getHtml('http://www.torrentkitty.com/archive/'+str(dttime)+'/')
    if html:
        PageNum = []
        PageNum = getPage('http://www.torrentkitty.com/archive/'+str(dttime)+'/',html)
        PageNum.append('http://www.torrentkitty.com/archive/'+str(dttime)+'/')
        for i in PageNum:
            thread = getMagnet(i)
            thread.start()

    while(thread.isAlive()):
        time.sleep(10)
    dt = dt-86400