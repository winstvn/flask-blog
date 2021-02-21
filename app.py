from flask import Flask, render_template
import sqlite3
from werkzeug.exceptions import abort


def get_post(post_id):
    with get_db_connection() as conn:
        post = conn.execute('SELECT * FROM posts WHERE id = ?',
                            (post_id,)).fetchone()
        
    if post is None:
        abort(404)
    return post


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


app = Flask(__name__)


@app.route('/')
def index():
    with get_db_connection() as conn:
        posts = conn.execute('SELECT * FROM posts').fetchall()
        
    return render_template('index.html', posts=posts)


@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)