from urllib import request
import json
import re
import os
import time

class Spider:
    def   __init__(self, keyword, mode):
        self.keyword = keyword
        self.mode = mode
        # least BOOKMARKed
        self.BOOKMARK = 10000
        # set cookie manually
        self.cookie = ''
        
    def check_illust(self, illust_id):
        illust_url = 'https://www.pixiv.net/artworks/%s'%illust_id
        headers = {'Cookie': self.cookie}
        req = request.Request(illust_url, headers=headers)
        resp = request.urlopen(req)
        tmp = resp.read().decode()
        bookmark_count = re.findall(r'"bookmarkCount":(\d+)', tmp)
        if int(bookmark_count[0]) > self.BOOKMARK:
            return re.findall(r'"regular":"(.*?)"', tmp)[0]
        return None
    
    def save_illust(self, illust_id, image_url, num, title):
        path = "./%s"%illust_id
        if not os.path.exists(path):
            os.makedirs(path)
        else:
            return None
        print("saving %s"%illust_id)
        url = image_url.split('_')
        for i in range(0, num):
            if url[1] != 'p0':
                print(image_url)
            url[1] = 'p%s'%i
            image_url = "_".join(url)
            headers = {'referer': 'https://www.pixiv.net/artworks/%s'%illust_id}
            req = request.Request(image_url, headers=headers)
            try:
                resp = request.urlopen(req)
                data = resp.read()
                f = open("./%s/p%s.jpg"%(illust_id, i), 'wb')
                f.write(data)
                f.close()
            except:
                pass
        return None
    
    def search(self, start, end):
        for i in range(start, end+1):
            print("Searching page %s"%i)
            search_url = 'https://www.pixiv.net/ajax/search/artworks/%s?mode=%s&p=%s' % (self.keyword, self.mode, i)
            headers = {'Cookie': self.cookie}
            req = request.Request(search_url, headers=headers)
            resp = request.urlopen(req)
            result = json.loads(resp.read().decode())
            
            for illust in result['body']['illustManga']['data']:
                if 'id' not in illust:
                    continue
                image_url = self.check_illust(illust['id'])
                if image_url:
                    self.save_illust(illust['id'], image_url, illust['pageCount'], illust['title'])
            
            
s = Spider("fate", "r18")
s.search(1, 1000)
