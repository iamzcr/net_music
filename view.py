#-*- coding: utf-8 -*-
#encoding=utf-8
import hashlib
from flask import Flask,render_template,url_for,request,flash,redirect,session
from api import NetEase
app = Flask(__name__)
app.secret_key = 'my is  some_secret'

#首页，获取榜单信息
@app.route('/')
def index():
    hot_music_list = NetEase.hot_song(NetEase())
    return render_template("index.html",hot_music_list = hot_music_list)
#获取榜单歌曲，此接口不知道是哪一个
@app.route('/top_music_list/<hot_id>',methods=['GET', 'POST'])
def top_music_list(hot_id):
    hot_music_list = NetEase.hot_song_list(NetEase(),hot_id)
    return render_template("top_music_list.html",hot_music_list = hot_music_list)

#获取歌手信息
@app.route('/singer')
def singer():
    singer_list = NetEase.top_artists(NetEase())
    return render_template("singer.html",singer_list = singer_list)

#获取歌手歌曲列表
@app.route('/song_list',methods=['GET', 'POST'])
def song_list():
    singer_id = request.args.get('singer_id')
    song_list = NetEase.artists(NetEase(),singer_id)
    return render_template("song_list.html",song_list = song_list)

#获取歌单
@app.route('/play_list',methods=['GET', 'POST'])
def play_list():
    cate = '全部'
    if request.method == "POST":
        cate = request.form['cate']
    play_song_list = NetEase.top_playlists(NetEase(),cate)
    categoty = NetEase.get_play_category(NetEase(),play_song_list)
    return render_template('play_list.html',play_song_list = play_song_list,categoty = categoty,now_cate=cate)

#获取某个歌单歌曲列表
@app.route('/play_song_list',methods=['GET', 'POST'])
def play_song_list():
    play_id = request.args.get('play_id')
    song_list = NetEase.get_play_song_list(NetEase(),play_id)
    return render_template("song_list.html",song_list = song_list)

#搜索
@app.route('/search',methods=['GET', 'POST'])
def search():
    if request.method == "GET":
        s = request.args.get('s')
        search_list = NetEase.get_search(NetEase(),s)
        return render_template('search.html',search_list = search_list['result']['songs'])
    else:
        return render_template('search.html',search_list = None)

#登录
@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        phone = request.form['phone']
        password = request.form['password']
        if phone and password:
            data = NetEase.user_login(NetEase(),phone,password)
            if data is not True:
                session['phone'] = phone
                return redirect(url_for('user_song_list'))
            else:
                flash('Password or Phone is not ture')
                return redirect(url_for('login'))
        else:
            flash('field can not be empty')
            return redirect(url_for('login'))
    else:
        return render_template('login.html')

#获取用户歌单
@app.route('/user_song_list',methods=['GET', 'POST'])
def user_song_list():
    return render_template('user_song_list.html')

if __name__ == '__main__':
	app.debug = True
	app.run()