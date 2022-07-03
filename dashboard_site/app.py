from flask import Flask, render_template
import sqlite3
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    with sqlite3.connect('../pool_apr.db') as conn:
       cur = conn.cursor()
       cur.execute("""
SELECT name FROM sqlite_schema
WHERE type='table'
ORDER BY name;
                """)
       name_list = cur.fetchall()
    return render_template('index.html', name_list=name_list)
