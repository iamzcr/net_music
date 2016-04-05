#-*- coding: utf-8 -*-
#encoding=utf-8
from flask import Flask,render_template
from api import NetEase
app = Flask(__name__)
@app.route('/index')
def index():
    user = { 'nickname': 'Miguel' } # fake user
    return render_template("index.html",title = 'Home',user = user)

if __name__ == '__main__':
	app.debug = True
	app.run()