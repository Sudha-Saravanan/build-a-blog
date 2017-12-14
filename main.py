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
        if self.title and self.body and self.created:
            return True
        else:
            return False



@app.route("/")
def index():
    return redirect("/blog")
    #post_list = Entry.query.all()
    #return render_template('allentries.html', title="All Entries", post_list=post_list)

@app.route("/blog")
def display_blog_entries():
    # TODO refactor to use routes with variables instead of GET parameters
    entry_id = request.args.get('id')
    if (entry_id):
        new_post = Entry.query.all(entry_id)
        #post_list = Entry.query.get(new_post).all()
        return render_template('singlepost.html', title="Blog Entry", new_post=new_post)

    # if we're here, we need to display all the entries
    # TODO store sort direction in session[] so we remember user's preference
    sort = request.args.get('sort')
    if (sort=="newest"):
        post_list = Entry.query.order_by(Entry.created.desc()).all()
    else:
        post_list = Entry.query.all()   
        return render_template('allentries.html', title="All Entries", post_list=post_list)

@app.route("/newpost", methods=['POST', 'GET'])
def newpost():
       
    if request.method == 'POST':
        new_title_post = request.form['title']
        new_body_post = request.form['body']
        new_post= Entry(new_title_post, new_body_post)

        if new_post.is_valid():
            db.session.add(new_post)
            db.session.commit()

            url = "/blog?id=" + str(new_post.id)
            return redirect(url)
        else:
            flash("Title and Body are required to post in the blog")
            return render_template('newpost.html', title="New Post", new_title_post=new_title_post, new_body_post=new_body_post)

    else:
        return render_template('newpost.html',title="New Post")

#@app.route("/singlepost")
#def singlepost():
    #post_list = Entry.query.all()
    #return render_template('singlepost.html', title="Single Post", post_list=post_list)

    #if request.args:
     #   newpost_id = request.args.get('id')
      #  newpost_body = Entry.query.get(newpost_id)
       # newpost_title = Entry.query.get(newpost_id)
        #latest_post = Entry(newpost_title, newpost_body)
    #return render_template('singlepost.html', title='Single Post', latest_post=latest_post)
    #if request.method == 'POST':
     #   new_title = request.form['title']
      #  new_body = request.form['body']
       # new_post= Entry(new_title, new_body)
        #new_id = request.args.get('id')
        #if (new_id == newpost_id):
            #entry = Entry.query.get(entry_id)
         #   return render_template('singlepost.html', title="Blog Entry", new_post=new_post)



if __name__ == '__main__':
    app.run()