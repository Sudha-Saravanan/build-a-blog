from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:sudha@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'sudha'

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(180))
    body = db.Column(db.String(1000))
    created = db.Column(db.DateTime)

    def __init__(self, title, body, created=None):
        self.title = title
        self.body = body
        if created is None:
            created = datetime.utcnow()
        self.created = created

    def is_valid(self):
        if self.title and self.body:
            return True
        else:
            return False



@app.route("/")
def index():
    #TODO The /blog route displays all the blog posts.
    return redirect("/blog")
    #post_list = Entry.query.all()
    #return render_template('allentries.html', title="All Entries", post_list=post_list)

@app.route("/blog")
def display_blog_entries():
    # TODO refactor to use routes with variables instead of GET parameters
    
    if request.args:
        blogpost_id = request.args.get('id')
        blogpost = Entry.query.get(blogpost_id)
        #post_list = Entry.query.get(new_post).all()
        return render_template('singlepost.html', title="Blog Entry", blogpost=blogpost)

    # if we're here, we need to display all the entries
    # TODO store sort direction in session[] so we remember user's preference
    sort = request.args.get('sort')
    if (sort=="newest"):
        blogpost_list = Entry.query.order_by(Entry.created.DESC()).all()
    else:
        blogpost_list = Entry.query.all()   
    return render_template('allentries.html', title="All Entries", blogpost_list=blogpost_list)

@app.route("/newpost", methods=['POST', 'GET'])
def newpost():

    if request.method =='POST':
        newpost_title = request.form['title']
        newpost_body = request.form['body']
        newpost= Entry(newpost_title, newpost_body)
        
        if newpost.is_valid():
            db.session.add(newpost)
            db.session.commit()
            url = "/blog?id=" + str(newpost.id)
            return redirect(url)
        elif newpost_title =='':
            flash("Title is required to post in the blog")
            return render_template('newpost.html',title="New Post")
        elif (newpost_body == ''):
            flash("Body is required to post in the blog")
            return render_template('newpost.html',title="New Post")
    else:
        return render_template('newpost.html',title="New Post")
        
if __name__ == '__main__':
    app.run()