from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from form_enter import UrlShorten
import hashlib
import random
from flask_bcrypt import Bcrypt
from passlib.hash import sha256_crypt


app=Flask(__name__)
app.config['SECRET_KEY']= 'dbaa09eac8718d1ef5667cee9d05d3f0b839b6fa'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///urls.db'
db = SQLAlchemy(app)


class User(db.Model):     #Database model
	original_url=db.Column(db.String(100),primary_key=True,nullable=False)
	hashed_url=db.Column(db.String(120),unique=True,nullable=False)

	def __repr__(self):
		return f"User('{self.original_url}','{self.hashed_url}')"



def random_id(length=6):                 #Generating a random string for appending in the Hashed Url
    	number = '0123456789'
    	alpha = 'abcdefghijklmnopqrstuvwxyz'
    	id = ''
    	for i in range(0,length,2):
        	id += random.choice(number)
        	id += random.choice(alpha)
    	return id


@app.route('/', methods=['GET'])
def home():
	return render_template('home.html')
	

@app.route("/url_shorten", methods=['GET','POST'])
def url_shortener():
	form_enter= UrlShorten()
	result=hashlib.md5('form_enter.url.data'.encode())
	result1=result.hexdigest()

	if(form_enter.validate_on_submit()):
		user1=User.query.filter_by(original_url=form_enter.url.data).all()
		if(len(user1)>0):
			return render_template('link_gen.html', title='URL SHORTEN', form_enter=user1[0].hashed_url)
			flash('Your Hash Has Been Generated you can now use it', 'success')

		else:
			while(len(User.query.filter_by(hashed_url=result1[0:6]).all())!=0):
				strt=random_id(6)
				result=hashlib.md5(('form_enter.url.data'+strt).encode())
				result1=result.hexdigest()

			user=User(original_url=form_enter.url.data,hashed_url=result1[0:6])
			db.session.add(user)
			db.session.commit()
			return render_template('link_gen.html', title='URL SHORTEN', form_enter=result1[0:6])
			flash('Your Hash Has Been Generated you can now use it', 'success')	

	return render_template('url_shorten.html', title='URL SHORTEN', form_enter=form_enter)


@app.route('/url_shorten/<data>')
def redirect_data(data):
    user21=User.query.filter_by(hashed_url=data).all()
    return redirect(user21[0].original_url)


if __name__ == '__main__':
	app.run(debug=True)