from flask import Flask, render_template, request, url_for, flash, redirect
import sqlite3
import random
from string import ascii_letters, digits
from werkzeug.exceptions import abort


def generate_key(length=10):
    chars = ascii_letters + digits
    return ''.join(random.choices(chars, k=length))

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
app.config['SECRET_KEY'] = generate_key()

@app.route('/')
def index():
    with get_db_connection() as conn:
        posts = conn.execute('SELECT * FROM posts').fetchall()
        
    return render_template('index.html', posts=posts)


@app.route('/blog_post/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            with get_db_connection() as conn:
                conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
                conn.commit()

            return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/blog_post/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            with get_db_connection() as conn:
                conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
                conn.commit()
        
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)


@app.route('/blog_post/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    with get_db_connection() as conn:
        conn.execute('DELETE FROM posts WHERE id = ?', (id,))
        conn.commit()

    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))