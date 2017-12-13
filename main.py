from datetime import datetime
from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:sudha@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

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


@app.route("/")
def index():
    post_list = Entry.query.all()
    return render_template('allentries.html', title="All Entries", post_list=post_list)



@app.route("/newpost", methods=['POST', 'GET'])
def newpost():
       
    if request.method == 'POST':
        new_title = request.form['title']
        new_body = request.form['body']
        new_post= Entry(new_title, new_body)
        db.session.add(new_post)
        db.session.commit()

    post_list = Entry.query.all()
    
    return render_template('newpost.html',title="New Post", post_list=post_list)

@app.route("/singlepost")
def singlepost():
    entry_id = request.args.get('id')
    if (entry_id):
        entry = Entry.query.get(entry_id)
        return render_template('singlepost.html', title="Blog Entry", entry=entry)

@app.route("/deletepost")
def deletepost():
    return render_template('/deletepost.html', title="Delete Post", post_id=post_id )

if __name__ == '__main__':
    app.run()