# return redirect(url_for("user", name="Admin!")) - user is the function name
# so url_for se you redirect to a function

# render_template redirects to an html page


from flask import Flask, redirect, url_for, render_template, request, session, flash # include the flask library
from flaskext.mysql import MySQL
from werkzeug.utils import secure_filename

import os
app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Annefrank911'
app.config['MYSQL_DATABASE_DB'] = 'MyDB'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
conn = mysql.connect()
cursor =conn.cursor()

UPLOAD_FOLDER = "/Users/ishita/Desktop/flask_app"

def getmonth(x):
    if x=="01":
        return "JAN"
    elif x=="02":
        return "FEB"
    elif x=="03":
        return "MAR"
    elif x=="04":
        return "APR"
    elif x=="05":
        return "MAY"
    elif x=="06":
        return "JUN"
    elif x=="07":
        return "JUL"
    elif x=="08":
        return "AUG"
    elif x=="09":
        return "SEP"
    elif x=="10":
        return "OCT"
    elif x=="11":
        return "NOV"
    elif x=="12":
        return "DEC"


def gethour(x):
    if int(x[0:2])>12:
        y=int(x[0:2])-12
        y=str(y)+x[2:]
        y=y+" pm"
        #print("yinside=",y)
        return y
    else:
        if x[0:2]=='00':
            x[0:2]='12'
        x=x+" am"
        return x




@app.route("/<text>")
def success(text):
    if text=="success":
        return render_template("givefeedback.html")
    return f"{text}"

@app.route("/",methods=["POST","GET"])
def login():
    cursor = mysql.get_db().cursor()


    if request.method=="POST":
        input_id=request.form["id"]
        input_password=request.form["password"]


        if input_id=="" or input_password=="":
            return render_template("login.html")


        cursor.execute("select username,password from loginDB where username=%s",[input_id])
        result = cursor.fetchall()
        if result:

            if input_password==result[0][1]:
                return render_template('givefeedback.html')

            else:
                return redirect(url_for("success",text="pass incorrect"))
        else:
            return redirect(url_for("success",text="username don't exist"))

    else:
        return render_template("login.html")


@app.route("/givefeedback",methods=["POST","GET"])
def givefeedback():
    cursor = mysql.get_db().cursor()

    if request.method=="POST":
        cursor.execute("select count(*) from feedbackDB")
        res = cursor.fetchall()

        if res[0][0]==0:
            input_feedbackid="F1"
        else:
            cursor.execute("select max(feedbackid) from feedbackDB")
            res = cursor.fetchall()
            maxid=(res[0][0])[1:]
            maxid=int(maxid)
            input_feedbackid=maxid+1
            input_feedbackid="F"+str(input_feedbackid)

        import datetime
        from datetime import date
        today=date.today()
        date=today.strftime("%Y-%m-%d")
        #print("DMATE IS", date)
        #print("SQQL",date)

        now = datetime.datetime.now()
        now=str(now)
        #print("now=",now)
        now = date+" "+gethour(now[11:19])
        date,time,mer=now.split(" ")
        #print("WAQT",time)

        id=request.form["fname"]
        input_feedback=request.form["feedback"]


        cursor.execute("insert into feedbackDB (feedbackid,username,feedback,date,time) values (%s,%s,%s,%s,%s)",[input_feedbackid,id,input_feedback,date,time])
        cursor.execute("commit")

        return render_template("givefeedback.html")
    else:
        # flash("Please login first")
        return redirect(url_for('login'))




@app.route("/viewbooks",methods=["POST","GET"])
def viewbooks():
    cursor = mysql.get_db().cursor()

    if request.method=="POST":

        querytabs=[None,"all",'bro','swear','ehh']
        info=[]

        try:#query
            title=request.form["title"]
            author=request.form["author"]
            author=request.form["genre"]
            author=request.form["status"]
            cursor.execute("create or return view temp as SELECT ISBN, Title, Author, Genre, status from bookDB")
            cursor.execute("commit")
            print(title,author)

            if title:
                cursor.execute("select * from temp where title like '%%s%'",[title])
                cursor.execute("commit")



        except: print('MLAPO')
        return render_template("login.html",querytabs=result, info=info)
    else:
        querytabs=[None,"all",'bro','swear']
        info=[]
        return render_template("seefeedback.html",querytabs=result, info=info)


@app.route("/addbook",methods=["POST","GET"])
def addbook():
    cursor = mysql.get_db().cursor()

    if request.method=="POST":
        cursor.execute("select count(*) from bookDB")
        res = cursor.fetchall()
        #print(res)

        title=request.form["title"]
        author=request.form["author"]
        genre=request.form["genre"]
        status=request.form["type"]
        ISBN = request.form['ISBN']
        print("WOO",title,author,genre,status,ISBN)

        if status=="futu":
            status="future"
        elif status=="curr":
            status="current"
        else:
            status="complete"


        #print("check1")
        cursor.execute("insert into bookDB (ISBN,title,author,genre,status) values (%s,%s,%s,%s,%s)",[ISBN,title,author,genre,status])
        #print("check2")
        cursor.execute("commit")

        return redirect(url_for('success',text="DONE"))
    else:
        # flash("Please login first")
        return render_template("addbook.html")

        # cursor.execute("""select name from employee_phone_visforce where emp_id=:x1""",[emp_id])
        # result = cursor.fetchall()
        # user=[emp_id,result[0][0]]
    return redirect(url_for('success',text="end"))


if __name__ == '__main__':
   app.run(debug=True)
