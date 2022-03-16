from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors





app = Flask(__name__)


app.secret_key = 'XYZ'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'delta3'
app.config['MYSQL_DB'] = 'trisect'
db = MySQL(app)



@app.route('/', methods=['GET', 'POST'])
def main():
    myc = db.connection.cursor(MySQLdb.cursors.DictCursor)
    myc.execute("SELECT * from  articles")
    all_articles=myc.fetchall()

   
    return render_template('main.htm', articles = all_articles)

@app.route('/new', methods=['GET'])
def new():
   
    
    return render_template('new.htm')


@app.route('/new/add', methods=['POST'])
def add():
    
    myc = db.connection.cursor(MySQLdb.cursors.DictCursor)
    
    title = request.form['title']
    body = request.form['body'].strip()
    print(title + body)
    myc.execute("INSERT into articles (title, body) values (%s,%s)", (title, body))
    db.connection.commit()

    
    return main()

@app.route("/delete/<id>", methods=["GET","POST"])
def delete(id):
    print(id)
    myc = db.connection.cursor(MySQLdb.cursors.DictCursor)
    myc.execute("DELETE from articles WHERE id =(%s)",(id))
    db.connection.commit()
    return main()

@app.route("/edit/<id>", methods=["GET","POST"])
def edit(id):

    myc = db.connection.cursor(MySQLdb.cursors.DictCursor)
    print(id)
    myc.execute("Select * from articles WHERE id =(%s)",(id))
    my_article = myc.fetchone()
    


    return render_template('update.htm', article = my_article)  

@app.route('/update', methods = ["POST"])
def update():
    myc = db.connection.cursor(MySQLdb.cursors.DictCursor)
    id = request.form['id']
    title = request.form['title']
    body = request.form['body']
    
    myc.execute("UPDATE articles set title =(%s), body =(%s) where id =(%s)", (title, body, id))
    db.connection.commit()

    return main()

if __name__ == '__main__' :
    app.run(debug=True)
