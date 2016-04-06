#-*- coding: utf-8 -*-
#encoding=utf-8
import hashlib
from flask import Flask,render_template,url_for,request,flash,redirect,session
from api import NetEase
app = Flask(__name__)
app.secret_key = 'my is  some_secret'
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

@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        if username and password:
            data = NetEase.user_login(NetEase(),username,password)
            if data is not True:
                session['username'] = username
                return redirect(url_for('user_song_list'))
            else:
                flash('Password or Phone is not ture')
                return redirect(url_for('login'))
        else:
            flash('field can not be empty')
            return redirect(url_for('login'))
    else:
        return render_template('login.html')

@app.route('/user_song_list',methods=['GET', 'POST'])
def user_song_list():
    return render_template('user_song_list.html')

@app.route('/search',methods=['GET', 'POST'])
def search():
    if request.method == "GET":
        s = request.args.get('s')
        search_list = NetEase.get_search(NetEase(),s)
        file_handle = open('test.json','a+')
        for search in search_list:
            print  search
            file_handle.write(search)
        file_handle.close()

        return render_template('search.html',search_list = search_list.songs)
    else:
        return render_template('search.html')

if __name__ == '__main__':
	app.debug = True
	app.run()