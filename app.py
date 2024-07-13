# simple blog system backend

from flask import Flask, request, send_from_directory , render_template , redirect , url_for , session , flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random
import string
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SECRET_KEY'] = 'secretFadaly'
db = SQLAlchemy(app)

class Blogs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    author = db.Column(db.String(20))
    imgId = db.Column(db.String(20))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    views = db.Column(db.Integer, default=0)
    likes = db.Column(db.Integer, default=0)
def reandomString():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(10))
@app.route('/')
def index():
    last_blogs = Blogs.query.order_by(Blogs.date_posted.desc()).limit(3).all()
    AllBlogs = Blogs.query.all()
    # rancking the blogs by views
    blogs = sorted(AllBlogs, key=lambda x: x.views, reverse=True)
    return render_template('index.html', blogs=blogs, last_blogs=last_blogs)
@app.route('/blog/<int:id>')
def blog(id):
    blog = Blogs.query.get(id)
    blog.views += 1
    db.session.commit()
    # make he get 5 rendem blogs from the database
    AllBlogs = Blogs.query.all()
    return render_template('blog.html', blog=blog, AllBlogs=AllBlogs)
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
            blogContent = request.form['blogContent']
            blogTitle = request.form['blogTitle']
            # mak he tack blogImage and save it in the static folder and get the image id random
            filename = reandomString()
            blogImage = request.files['blogImage']
            blogImage.save(f'static/{filename}.jpg')
            new_blog = Blogs(title=blogTitle, content=blogContent, author='Fadaly', imgId=filename)
            db.session.add(new_blog)
            db.session.commit()
            return render_template('add.html', msg=f"تم اضافت مقالت {blogTitle} بنجاح")
    return render_template('add.html')

@app.route('/img/<string:id>')
def img(id):
    return send_from_directory('static', f'{id}.jpg')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)