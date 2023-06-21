from flask import Blueprint, render_template, request, flash, redirect, url_for, session
import mysql.connector
from webappfiles import dbconnect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
from . import mail
auth = Blueprint('auth', __name__)


@auth.route('/registerho/', methods=['GET', 'POST'])
def register_ho():
    if request.method == 'POST':
        first_name = request.form['txtfn']
        last_name = request.form['txtln']
        email = request.form['txtemail']
        password1 = request.form['txtpwd']
        password2 = request.form['txtcpwd']
        Postal_Address = request.form['txtdistrict']
        cur, con = dbconnect.get_connection()
        sql = "select email from tblhouseowner where email= %s"
        val = (email,)
        cur.execute(sql, val)
        rows = cur.fetchall()
        count = cur.rowcount

        if (count > 0):
            flash('User already exists.', category='error')
        elif (len(email) < 5):
            flash('Email must be greater than 4 characters.', category='error')
        elif (len(first_name) < 3):
            flash('First name must be greater than 2 characters.', category='error')
        elif (password1 != password2):
            flash('Passwords don\'t match.', category='error')
        elif (len(password1) < 3):
            flash('Password must be at least 3 characters.', category='error')
        else:
            password1 = generate_password_hash(password1, method='sha256')
            sql2 = "INSERT into tblhouseowner (firstname, lastname, email, password, postal_address) values (%s,%s,%s,%s,%s)"
            val2 = (first_name, last_name, email,
                    password1, Postal_Address)
            cur.execute(sql2, val2)
            con.commit()
            msg = str(cur.rowcount) + " record added, "
            msg1 = Message('Job Portal',
                           sender='kruttun47@gmail.com', recipients=[email])
            msg1.body = "Welcome to Job Portal " + first_name + "\r\n"
            msg1.body += "You are now a member and may access the website \r\n "
            msg1.body += "@ http://localhost:5000/"
            mail.send(msg1)
            flash(msg + ' account created!', category='success')
        return redirect(url_for('auth.login_ho'))
    return render_template("registerho.html")


@auth.route('/registerhk/', methods=['GET', 'POST'])
def register_hk():
    if request.method == 'POST':
        title = request.form['txttitle']
        first_name = request.form['txtfn']
        last_name = request.form['txtln']
        email = request.form['txtemail']
        password1 = request.form['txtpwd']
        password2 = request.form['txtcpwd']
        Postal_Address = request.form['txtpadd']
        contact = request.form['txtcontact']
        Date_of_birth = request.form['txtdob']
        H_Qualification = request.form['txthqa']
        f = request.form['txtfilecv']
        skill = request.form['txtskills']
        cur, con = dbconnect.get_connection()
        sql = "select email_address from tblhousekeeper where email_address= %s"
        val = (email,)
        cur.execute(sql, val)
        rows = cur.fetchall()
        count = cur.rowcount

        if (count > 0):
            flash('User already exists.', category='error')
        elif (len(email) < 5):
            flash('Email must be greater than 4 characters.', category='error')
        elif (len(first_name) < 3):
            flash('First name must be greater than 2 characters.', category='error')
        elif (password1 != password2):
            flash('Passwords don\'t match.', category='error')
        elif (len(password1) < 3):
            flash('Password must be at least 3 characters.', category='error')
        else:
            password1 = generate_password_hash(password1, method='sha256')
            sql2 = "INSERT into tblhousekeeper (title, firstname, lastname, email_address, password, postal_address, number, date_of_birth, highest_qualification, cv_upload, skill) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val2 = (title, first_name, last_name, email,
                    password1, Postal_Address, contact, Date_of_birth, H_Qualification, f, skill)
            cur.execute(sql2, val2)
            con.commit()
            msg = str(cur.rowcount) + " record added, "
            msg1 = Message('Job Portal',
                           sender='kruttun47@gmail.com', recipients=[email])
            msg1.body = "Welcome to Job Portal " + first_name + "\r\n"
            msg1.body += "You are now a member and may access the website \r\n "
            msg1.body += "@ http://localhost:5000/"
            mail.send(msg1)
            flash(msg + ' account created!', category='success')
        return redirect(url_for('auth.login_hk'))
    return render_template("registerhk.html")


# Houseowner Login

@auth.route("/loginho/", methods=['GET', 'POST'])
def login_ho():
    if request.method == 'POST':
        email = request.form['txtemail']
        pwd = request.form['txtpwd']
        cur, con = dbconnect.get_connection()
        sql = "select password, email, houseowner_id, firstname from tblhouseowner where email= %s"
        val = (email,)
        cur.execute(sql, val)
        rows = cur.fetchall()
        count = cur.rowcount
        for row in rows:
            passw = row[0]
        if (count > 0):
            if check_password_hash(passw, pwd):
                session['houseowner_id'] = rows[0][2]
                session['firstname'] = rows[0][3]
                flash('Logged in successfully!', category='success')
                return redirect(url_for('views.profile'))
            else:
                flash('Incorrect password, pls try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
        return render_template("loginho.html")


@auth.route('/logout/')
def logout():
    session.pop('houseowner_id')
    return redirect('/home/')

# Housekeeper Login


@auth.route("/loginhk/", methods=['GET', 'POST'])
def login_hk():
    if request.method == 'POST':
        email = request.form['txtemail']
        pwd = request.form['txtpwd']

        cur, con = dbconnect.get_connection()
        sql = "select password, email_address, housekeeper_id, firstname from tblhousekeeper where email_address= %s"
        val = (email,)
        cur.execute(sql, val)
        rows = cur.fetchall()
        count = cur.rowcount
        for row in rows:
            passw = row[0]
        if (count > 0):
            if check_password_hash(passw, pwd):
                session['housekeeper_id'] = rows[0][2]
                session['firstname'] = rows[0][3]
                flash('Logged in successfully!', category='success')
                return redirect(url_for('views.profile1'))
            else:
                flash('Incorrect password, pls try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
        return render_template("loginhk.html")


@auth.route('/logout1/')
def logout1():
    session.pop('housekeeper_id')
    return redirect('/home/')
