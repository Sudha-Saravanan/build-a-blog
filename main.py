from flask import Flask, request, redirect, render_template

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:sudha@localhost:8889/build-a-blog'
app.config['SQLAlchemy(app)']

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(180))
    body = db.Column(db.String(1000))
    created = db.Column(db.DateTime)

    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.created = datetime.utcnow()



post_list = []

@app.route('/')
def index():
    return redirect("/allentries")


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():    
    if request.method == 'POST':
        new_title = request.form['title']
        new_body = request.form['body']
        new_post= Entry(new_title, new_body)
        post_list.append(new_post)
    
    return render_template('newpost.html',title="New Post", post_list=post_list)

app.run()