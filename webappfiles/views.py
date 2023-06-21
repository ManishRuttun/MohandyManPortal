from turtle import title
from flask import Blueprint, render_template, request, session, redirect, flash

import mysql.connector
from webappfiles import dbconnect

from datetime import datetime
import os

views = Blueprint('views', __name__)
cur, con = dbconnect.get_connection()
# referring to the default page via the “/” route


@views.route("/home/")
def home():
    return render_template("index.html")


@views.route("/loginho/")
def login_ho():
    return render_template("loginho.html")


@views.route("/loginhk/")
def login_hk():
    return render_template("loginhk.html")


@views.route("/registerhk/")
def register_hk():
    return render_template("registerhk.html")


@views.route("/registerho/")
def register_ho():
    return render_template("registerho.html")


@views.route("/addjob/")
def addjob():
    cur.execute("SELECT * FROM tblhouseowner")
    rows = cur.fetchall()
    cur.execute("SELECT * FROM tblhousekeeper")
    rows = cur.fetchall()
    return render_template("addjob.html", rows=rows)


@views.route("/savedetails", methods=["POST"])
def saveDetails():
    msg = "msg"
    if request.method == "POST":
        try:
            # add codes to retrieve the form values
            job_title = request.form["txtjtitle"]
            job_reference = request.form["txtjref"]
            job_description = request.form["txtjdes"]
            salary = request.form["txtsalary"]
            closing_date = request.form["txtjclose"]
            sql = "INSERT into tbljob (title, reference, description, salary, close_date) values (%s,%s,%s,%s,%s)"
            # add the form variables for each column
            val = (job_title, job_reference,
                   job_description, salary, closing_date,)
            cur.execute(sql, val)
            con.commit()
            msg = str(cur.rowcount) + " Job added"

        except Exception as e:
            con.rollback()
            msg = "Job cannot be added " + str(e)
        finally:
            # pass the msg variable to the return statement
            return render_template("addjob.html", msg=msg, title=job_title)
            con.close()


@views.route("/viewjob/")
def viewjob():
    cur.execute("SELECT * FROM tbljob")
    rows = cur.fetchall()
    return render_template("viewjob.html", rows=rows)


@views.route("/viewjob1/")
def viewjob1():
    cur.execute("SELECT * FROM tbljob")
    rows = cur.fetchall()
    return render_template("viewjob1.html", rows=rows)


@views.route("/profile/")
def profile():
    if 'houseowner_id' in session:
        cur, con = dbconnect.get_connection()
        sql = "SELECT * FROM tblhouseowner where houseowner_id = %s"
        val = (session.get('houseowner_id'),)
        cur.execute(sql, val)
        rows = cur.fetchall()
        return render_template("profile.html", rows=rows)
    else:
        return redirect('/home/')


@views.route("/updateprofile/", methods=["GET", "POST"])
def update_profile():
    if request.method == "POST":
        email = request.form['txtemail']
        first_name = request.form['txtfn']
        last_name = request.form['txtln']
        postal_address = request.form['txtadd']

        try:
            cur, con = dbconnect.get_connection()
            sql = "UPDATE tblhouseowner SET email = %s, firstname = %s, lastname = %s, postal_address = %s where houseowner_id = %s"
            val = (email, first_name, last_name,
                   postal_address, session['houseowner_id'])
            cur.execute(sql, val)
            con.commit()
            msg = str(cur.rowcount) + " record successfully updated"
            flash(msg, category='success')
        except:
            msg = "Cannot be updated"
            flash(msg, category='error')
        finally:
            return redirect('/profile/')

    else:
        return redirect('/login/')


@views.route("/profile1/")
def profile1():
    if 'housekeeper_id' in session:
        cur, con = dbconnect.get_connection()
        sql = "SELECT * FROM tblhousekeeper where housekeeper_id = %s"
        val = (session.get('housekeeper_id'),)
        cur.execute(sql, val)
        rows = cur.fetchall()
        return render_template("profile1.html", rows=rows)
    else:
        return redirect('/home/')


@views.route("/updateprofile1/", methods=["GET", "POST"])
def update_profile1():
    if request.method == "POST":
        email = request.form['txtemail']
        first_name = request.form['txtfn']
        last_name = request.form['txtln']
        contact = request.form['txtnum']
        skill = request.form['txtskill']

        try:
            cur, con = dbconnect.get_connection()
            sql = "UPDATE tblhousekeeper SET email_address = %s, firstname = %s, lastname = %s, number = %s, skill = %s where housekeeper_id = %s"
            val = (email, first_name, last_name, contact,
                   skill, session['housekeeper_id'])
            cur.execute(sql, val)
            con.commit()
            msg = str(cur.rowcount) + " record successfully updated"
            flash(msg, category='success')
        except:
            msg = "Cannot be updated"
            flash(msg, category='error')
        finally:
            return redirect('/profile1/')

# To Check


@views.route("/searchjob/", methods=["GET"])
def searchjob():
    # retrieve the querystring txtlang from the URL
    skill = request.args.get("txtskill")
    try:
        sql = "select * from tblhousekeeper  WHERE skill = %s "
        val = (skill,)
        cur.execute(sql, val)
        rows = cur.fetchall()
        msg = str(cur.rowcount) + " record found!"
    except:
        msg = "There was an issue while searching!"
    finally:
        return render_template("searchjob.html", rows=rows, msg=msg, title=skill)


@views.route("/searchjob1/", methods=["GET"])
def searchjob1():
    # retrieve the querystring txtlang from the URL
    title = request.args.get("txtjtitle")
    try:
        sql = "select * from tbljob  WHERE title = %s "
        val = (title,)
        cur.execute(sql, val)
        rows = cur.fetchall()
        msg = str(cur.rowcount) + " record found!"
    except:
        msg = "There was an issue while searching!"
    finally:
        return render_template("searchjob1.html", rows=rows, msg=msg, title=title)


@views.route("/updatejob/")
def updatejob():
    return render_template("updatejob.html")


@views.route("/updaterecord/", methods=["POST"])
def updaterecord():
    # retrieve the form values
    ref = request.form["txtref"]
    des = request.form["txtdes"]
    sal = request.form["txtsal"]
    date = request.form["txtdate"]
    try:
        sql = "UPDATE tbljob SET description = %s, close_date = %s, salary = %s where reference= %s"
        val = (des, date, sal, ref)
        cur.execute(sql, val)
        con.commit()
        msg = str(cur.rowcount) + " record successfully updated"
    except:
        msg = "Cannot be updated"
    finally:
        return render_template("updatejob.html", msg=msg)


@views.route("/deletejob/")
def deletejob():
    return render_template("deletejob.html")


@views.route("/deleterecord/", methods=["POST"])
def deleterecord():
    # retrieve the form value
    reference = request.form["txtref"]
    try:
        sql = "DELETE FROM tbljob WHERE reference = %s"
        val = (reference,)
        cur.execute(sql, val)
        con.commit()
        msg = str(cur.rowcount) + " record successfully deleted"
    except:
        msg = "Cannot be deleted"
    finally:
        return render_template("deletejob.html", msg=msg)


@views.route("/joblisting/")
def job_listing():
    cur, con = dbconnect.get_connection()
    cur.execute("SELECT * FROM tbljob")
    rows = cur.fetchall()
    return render_template('joblisting.html', rows=rows)


@views.route("/applyjob/")
def applyjob():
    cur.execute(
        "SELECT * FROM tbljob jb INNER JOIN tblhouseowner ho on (jb.houseowner_id=ho.houseowner_id)")
    rows1 = cur.fetchall()
    return render_template("applyjob.html", rows1=rows1)


@views.route("/submition", methods=['GET', 'POST'])
def submition():
    if request.method == 'POST':
        title = request.form['txtjtitle']
        ref = request.form['txtref']
        date = request.form['txtdate']
        sql = "INSERT into tblapplication (date_of_application, housekeeper_id, job_id) values (%s,%s,%s)"
        val = (title, ref, date, session.get('housekeeper_id'))
        cur.execute(sql, val)
        con.commit()
    return render_template("applyjob.html")
