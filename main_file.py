from flask import Flask, render_template, url_for, request, redirect
#from sklearn.externals import joblib
import joblib
import os
import numpy as np
import pickle
import sqlite3

DATABASE = "Heart-Disease.db"

#con = sqlite3.connect(DATABASE)

app = Flask(__name__, static_folder='static')


@app.route("/")
def index():
    # con = sqlite3.connect(DATABASE)
    # con.row_factory = sqlite3.Row
    #
    # cur = con.cursor()
    # cur.execute("select * from users")
    #
    # row = cur.fetchall()
    # print(row[0]['username'])
    return render_template('index.html')


@app.route('/login',methods=['POST','GET'])
def login():
    username = ""
    password = ""
    msg = ""
    if(request.method == "POST"):
        username = request.form['username']
        password = request.form['password']

        print(username,password)

        con = sqlite3.connect(DATABASE)
        con.row_factory = sqlite3.Row

        cur = con.cursor()
        cur.execute('select * from users where username = ? and password = ?',[username,password])

        row = cur.fetchall()

        count = len(row)
        print(count)

        if count > 0:
                print("user found")
                cur.close()
                con.close()
                return render_template('home.html')

        msg = "Check your username and password!!!"
        cur.close()
        con.close()
    return render_template('login.html',msg = msg)


@app.route('/signup',methods=["POST","GET"])
def signup():
    msg = ''
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        print(username,password)

        if(isUserExist(username)):
            msg = "Username exist"
        else:
            con = sqlite3.connect(DATABASE)
            cur = con.execute("INSERT INTO USERS(USERNAME,PASSWORD) values (?,?)",[username,password])
            con.commit()
            msg = "Signed in Successfully...!!!. Login to your account"
            cur.close()
            con.close()
    return render_template('signup.html',msg = msg)


@app.route('/result', methods=['POST', 'GET'])
def result():
    age = int(request.form['age'])
    sex = int(request.form['sex'])
    trestbps = float(request.form['trestbps'])
    chol = float(request.form['chol'])
    restecg = float(request.form['restecg'])
    thalach = float(request.form['thalach'])
    exang = int(request.form['exang'])
    cp = int(request.form['cp'])
    fbs = float(request.form['fbs'])
    x = np.array([age, sex, cp, trestbps, chol, fbs, restecg,
                  thalach, exang]).reshape(1, -1)

    scaler_path = os.path.join(os.path.dirname(__file__), 'models/scaler.pkl')
    scaler = None
    with open(scaler_path, 'rb') as f:
        scaler = pickle.load(f)

    x = scaler.transform(x)

    model_path = os.path.join(os.path.dirname(__file__), 'models/rfc.sav')
    clf = joblib.load(model_path)

    y = clf.predict(x)
    print(y)

    # No heart disease
    if y == 0:
        return render_template('nodisease.html')

    # y=1,2,4,4 are stages of heart disease
    else:
        return render_template('heartdisease.htm', stage=int(y))


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/stage1')
def stage1():
    return render_template('stage1.html')


@app.route('/stage2')
def stage2():
    return render_template('stage2.html')


@app.route('/stage3')
def stage3():
    return render_template('stage3.html')


@app.route('/stage4')
def stage4():
    return render_template('stage4.html')


@app.route('/types')
def types():
    return render_template('types.html')


@app.route('/symptoms')
def symptoms():
    return render_template('symptoms.html')


@app.route('/prediction')
def prediction():
    return render_template('prediction.html')


@app.route('/prevention')
def prevention():
    return render_template('prevention.html')


@app.route('/facts')
def facts():
    return render_template('facts.html')


def isUserExist(username):
    con = sqlite3.connect(DATABASE)
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute('select * from users where username = ?',[username])

    row = cur.fetchall()

    count = len(row)

    cur.close()
    con.close()

    return count > 0


if __name__ == "__main__":
    app.run(debug=True)
