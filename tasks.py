from celery.task import task
import os
from celery import Celery
from fake_headers import Headers
import dpath.util
from bs4 import BeautifulSoup
import sys
import requests

# celery = Celery()
# celery.config_from_object('celeryconfig')

app = Celery('tasks' , backend='redis://localhost:6379/0' , broker='amqp://localhost:5672')

old_lines = 0
lastModify = 0
lastModify_new = 0
count_line = 0

count = 1
requests_count = 0
tree = {}

@app.task(name='task.reading_file')
def reading_file():
        global lastModify
        global count_line
        filename = 'urls.txt'
        try:
            statbuf = os.stat(filename)
            lastModify_new = statbuf.st_mtime
            print('lastModify_new' + lastModify_new.__str__())
        except:
            # logger.error("Exception occurred", exc_info=True)
            print('file not found')

        if (lastModify != lastModify_new):
            print('changing_lastMo')
            with open('urls.txt', 'r+') as f:
                lineList =  f.readlines()
            f.close()
            count_line_new = len(lineList)
            if (count_line_new > count_line):
                print('new lines : ' + count_line_new.__str__())
                print('old lines : ' + count_line.__str__())

                new_urls = lineList[count_line:count_line_new]
                count_line = count_line_new
                lastModify = lastModify_new
                return new_urls
                # print(new_urls)

            count_line = count_line_new
            lastModify = lastModify_new


def Add_to_main_tree(new_dict, keylist, splited, depth):
    global tree
    x = ''
    if len(keylist) == 0:
        if '\'' not in splited[0]:
            dpath.util.new(tree, splited[0], new_dict[splited[0]])


    else:
        for n in range(len(keylist)):
            x = keylist[n] + "/"
        dpath.util.new(tree, x + splited[depth], new_dict[splited[depth]])
    print(tree)


def is_in_tree(url):
    url.replace(" ", "")
    splited = url.split('/')
    global tree
    temp_dict = tree
    for i in range(len(splited)):
        if (splited[i] in temp_dict.keys()):
            if (i == len(splited) - 1):
                return 1
            temp_dict = temp_dict[splited[i]]
            continue

        else:
            depth = i
            new_dict = {}
            for j in range(len(splited) - 1, i - 1, -1):
                temp = new_dict
                new_dict = {}
                new_dict[splited[j]] = temp
            Add_to_main_tree(new_dict, splited[:depth], splited, depth)
            return 0



@app.task(name='tasks.')
def send_request(body):
    header = Headers(
        browser="chrome",  # Generate only Chrome UA
        os="win",  # Generate ony Windows platform
        headers=True  # generate misc headers
    )
    headers = header.generate()
    # response = http_pool.get_url('http://www.' + body.decode("utf-8"), headers)

    response = requests.get('http://www.' + body.decode("utf-8") , params = headers)
    # response = http.request('GET',  , fields=headers , timeout=5)
    print("response body  " + str(response.data.decode('utf-8')))
    print('after request')
    global requests_count
    requests_count += 1
    soup = BeautifulSoup(str(response.data), 'html.parser')
    links = soup.find_all('a', href=True)
    print(len(links))
    for el in links:
        print(el)
        try:
            url = el['href'].__str__()
        except:
            sys.exit()
        if ((url == '') or ('#' not in url)):
            continue
        url = url.replace(' ', '')
        url = url.replace('www.', '')
        url = url.replace('https:', '')
        url = url.replace('http:', '')
        url = url.replace('//', '')
        if (('#' in url) and ('/' not in url)):
            url = body.decode('utf-8') + '/' + url
        in_tree = is_in_tree(url)
        if (in_tree == 0):
            count += 1
            # server.publish(url)
            # print(count.__str__() + '\' th unique url')