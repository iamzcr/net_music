#-*- coding: utf-8 -*-
#encoding=utf-8
import re
import json
import requests
import hashlib
# list去重
def uniq(arr):
    arr2 = list(set(arr))
    arr2.sort(key=arr.index)
    return arr2
default_timeout = 10

class NetEase:

    def __init__(self):
        self.header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'music.163.com',
            'Referer': 'http://music.163.com/',
            'User-Agent': '	Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0'
        }
        self.cookies = {
            'appver': '1.5.2'
        }

    def httpRequest(self, method, action, query=None, urlencoded=None, callback=None, timeout=None):    
        if(method == 'GET'):
            url = action if (query == None) else (action + '?' + query)
            connection = requests.get(url, headers=self.header, timeout=default_timeout)

        elif(method == 'POST'):
            connection = requests.post(
                action,
                data=query,
                headers=self.header,
                timeout=default_timeout
            )

        connection.encoding = "UTF-8"
        connection = json.loads(connection.text)
        return connection

    #获取榜单信息
    def hot_song(self):
        action = 'http://music.163.com/api/toplist/'
        try:
            data = self.httpRequest('GET', action)
            return data['list']
        except:
            return []

    #获取榜单歌曲，此接口不知道是哪一个
    def hot_song_list(self,hot_id):
        action = 'http://music.163.com/api/discover/toplist/?id='+str(hot_id)
        try:
            data = self.httpRequest('GET', action)
            print data
            return data['list']
        except:
            return []

    #获取最热歌手
    def top_artists(self, offset=0, limit=100):
        action = 'http://music.163.com/api/artist/top?offset=' + str(offset) + '&total=false&limit=' + str(limit)
        try:
            data = self.httpRequest('GET', action)
            return data['artists']
        except:
            return []

    #获取歌手曲目
    def artists(self, artist_id):
        action = 'http://music.163.com/api/artist/' + str(artist_id)
        try:
            data = self.httpRequest('GET', action)
            return data['hotSongs']
        except:
            return []

    #获取歌单
    def top_playlists(self, category='全部', order='hot', offset=0, limit=50):
        action = 'http://music.163.com/api/playlist/list?cat=' + category + '&order=' + order + '&offset=' + str(offset) + '&total=' + ('true' if offset else 'false') + '&limit=' + str(limit)
        try:
            data = self.httpRequest('GET', action)
            return data['playlists']
        except:
            return []

    #根据分类获取歌单
    def get_play_category(self,data):
        temp = [];
        for res in data:
            print res['updateTime']
            for tag in res['tags']:
                temp.append(tag)
        return uniq(temp)

    #获取歌单列表
    def get_play_song_list(self,play_id):
        action = 'http://music.163.com/api/playlist/detail?id=' + str(play_id)
        try:
            data = self.httpRequest('GET', action)
            return data['result']['tracks']
        except:
            return []

    #搜索
    def get_search(self, s, stype=1, offset=0, total='true', limit=60):
        action = 'http://music.163.com/api/search/get/web'
        data = {
            's': s,
            'type': stype,
            'offset': offset,
            'total': total,
            'limit': 60
        }
        return self.httpRequest('POST', action, data)

    #用户登录
    def user_login(self, username, password):
        action = 'http://music.163.com/api/login/'
        data = {
            'username': username,
            'password': hashlib.md5( password ).hexdigest(),
            'rememberLogin': 'true'
        }
        try:
            return self.httpRequest('POST', action, data)
        except:
            return False

    #用户歌单
    def user_playlist(self, uid, offset=0, limit=100):
        action = 'http://music.163.com/api/user/playlist/?offset=' + str(offset) + '&limit=' + str(limit) + '&uid=' + str(uid)
        try:
            data = self.httpRequest('GET', action)
            return data['playlist']
        except:
            return []


