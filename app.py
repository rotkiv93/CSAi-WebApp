#!/usr/bin/python2.7

from flask import Flask, render_template, json, request, session, redirect
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
import hashlib

mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'db'
app.config['MYSQL_DATABASE_PASSWORD'] = 'dbpass'
app.config['MYSQL_DATABASE_DB'] = 'csai'
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
mysql.init_app(app)

app.secret_key = '"g@d94p2vFfE2Gd@jK#8k$pL`VLY6LM]aj+"k@/F*:wRPH-Gy/7<>$/T`}gP{w<5SG`ZLg=c#[FD7LV^AG%+9ug`ug~CvU`C.U*)7w[^~J#gV&V@Z9D8G~W-C/d,[>'


@app.route('/')
def main():
    return render_template('index.html')

@app.route('/showSignIn')
def showSignIn():
    return render_template('signin.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/products')
def showProducts():
    if session.get('user'):
        return render_template('products.html')
    else:
        return render_template('error.html', error = 'Acceso no permitido')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

@app.route('/signIn',methods=['POST','GET'])
def signIn():
    try:
        _username = request.form['signinUsername']
        _password = request.form['signinPassword']
        _hashed_password = hashlib.sha256(_password)

        if _username and _password:

            db = mysql.connect()
            cursor = db.cursor()

            query = "SELECT password FROM usuario WHERE username = %s"
            cursor.execute(query, (_username,))

            (data,) = cursor.fetchone()

            if (data.lower() == _hashed_password.hexdigest().lower()):
                session['user'] = data
                return json.dumps({'html':'<span>Password correcta</span>'})
            else:
                return json.dumps({'html':'<span>Password incorrecta</span>'})

        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'}) 

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close()
        db.close()

@app.route('/signUp',methods=['POST','GET'])
def signUp():
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validate the received values
        if _name and _email and _password:

            # All Good, let's call MySQL

            conn = mysql.connect()
            cursor = conn.cursor()
            _hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message':'User created successfully !'})
            else:
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close() 
        conn.close()

if __name__ == "__main__":
    app.run(port=5002)
