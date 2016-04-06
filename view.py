#-*- coding: utf-8 -*-
#encoding=utf-8
import hashlib
from flask import Flask,render_template,url_for,request
from api import NetEase
app = Flask(__name__)
@app.route('/')
def index():
	net_music_list = NetEase.top_artists(NetEase())
	print net_music_list
	return render_template("index.html")

@app.route('/singer')
def singer():
	singer_list = NetEase.top_artists(NetEase())
	return render_template("singer.html",singer_list = singer_list)

@app.route('/song_list',methods=['GET', 'POST'])
def song_list():
    singer_id = request.args.get('singer_id')
    song_list = NetEase.artists(NetEase(),singer_id)
    return render_template("song_list.html",song_list = song_list)
    # 登录

@app.route('/login',methods=['GET', 'POST'])
def login():

    username = request.form['username']
    password = request.form['username']
    NetEase.login(NetEase(),username,password)
    action = 'http://music.163.com/api/login/'
    data = {
         'username': username,
         'password': hashlib.md5( password ).hexdigest(),
         'rememberLogin': 'true'
    }
    try:
        return NetEase().httpRequest('POST', action, data)
    except:
        return {'code': 501}
@app.route('/user_song_list',methods=['GET', 'POST'])
def user_song_list():
    return render_template('user_song_list.html')

@app.route('/search',methods=['GET', 'POST'])
def search():
    return render_template('user_song_list.html')

if __name__ == '__main__':
	app.debug = True
	app.run()