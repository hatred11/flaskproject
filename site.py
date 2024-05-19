from flask import Flask, request, render_template
import sqlite3


log = True
name = ""
app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    if log:
        return render_template("home.html", param=True)
    return render_template("home.html", param=False)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/news")
def news():
    if log:
        return render_template("news.html", param=True)
    return render_template("news.html", param=False)

@app.route("/prof")
def prof():
    global name
    return render_template("prof.html", name=name)

@app.route("/sport")
def sport():
    return render_template("sport.html")

@app.route("/politics")
def politics():
    return render_template("politics.html")

@app.route("/science")
def science():
    return render_template("science.html")

db_lp = sqlite3.connect('login_password.db')
cursor_db = db_lp.cursor()
sql_create = '''CREATE TABLE if not exists passwords(
login TEXT PRIMARY KEY,
password TEXT NOT NULL);'''

cursor_db.execute(sql_create)
db_lp.commit()

cursor_db.close()
db_lp.close()

@app.route('/authorization', methods=['GET', 'POST'])
def form_authorization():
   if request.method == 'POST':
       Login = request.form.get('Login')
       Password = request.form.get('Password')
       global name
       name = Login

       db_lp = sqlite3.connect('login_password.db')
       cursor_db = db_lp.cursor()
       cursor_db.execute(('''SELECT password FROM passwords
                                               WHERE login = '{}';
                                               ''').format(Login))
       pas = cursor_db.fetchall()

       cursor_db.close()
       try:
           if pas[0][0] != Password:
               return render_template('auth_bad.html')
       except:
           return render_template('auth_bad.html')

       db_lp.close()
       global log
       log = False
       return render_template('successfulauth.html')

   return render_template('authorization.html')

@app.route('/registration', methods=['GET', 'POST'])
def form_registration():

   if request.method == 'POST':
       Login = request.form.get('Login')
       Password = request.form.get('Password')

       db_lp = sqlite3.connect('login_password.db')
       cursor_db = db_lp.cursor()
       sql_insert = '''INSERT INTO passwords VALUES('{}','{}');'''.format(Login, Password)

       cursor_db.execute(sql_insert)

       cursor_db.close()

       db_lp.commit()
       db_lp.close()

       return render_template('successfulregis.html')

   return render_template('registration.html')

if __name__ == "__main__":
    app.run()