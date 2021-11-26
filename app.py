from flask import *  
import sqlite3

      
app = Flask(__name__) 

@app.route("/",methods = ["POST","GET"])  
def index():
    con = sqlite3.connect('/opt/TrainApp/trainpower.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
 
    if request.method == "POST":
        if request.form['mode'] == 'start':
            cur.execute("UPDATE trains SET mode='run',running=0 WHERE id=%s" % (request.form['trainid']))
            con.commit()
        elif request.form['mode'] == 'stop':
            cur.execute("UPDATE trains SET mode='stop',running=1 WHERE id=%s" % (request.form['trainid']))
            con.commit()
        elif request.form['mode'] == 'home':
            cur.execute("UPDATE trains SET mode='home' WHERE id=%s" % (request.form['trainid']))
            con.commit()
    
    activeprofiles = {}
    cur.execute("select * from activeprofile")
    aprows = cur.fetchall()
    profilereset = 0
    for aprow in aprows:
        try:
            cur.execute("SELECT * FROM trains WHERE id = %s" % aprow['trainid'])
            train = cur.fetchone()
            if train['mode'] == 'stop' and train['running'] == 0:
                mode = 'Stopped'
            elif train['mode'] == 'stop' and train['running'] == 1:
                mode = 'Stopping'
            elif train['mode'] == 'run' and train['running'] == 0:
                mode = 'Starting'
            elif train['mode'] == 'run' and train['running'] == 1:
                mode = 'Running'
            elif train['mode'] == 'home':
                mode ='Going Home'
            activeprofiles["Track " + str(aprow['tracknum'])] = train['trainname'],mode,train['id']
            if profilereset == 1:
                msg="Looks like a active train profile has been deleted, All active train profiles have been reset."
            else:
                msg=0
            
        except:
            con = sqlite3.connect("/opt/TrainApp/trainpower.db")
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("SELECT * from activeprofile")
            tracks = cur.fetchall()
            cur.execute("SELECT * from trains")
            train = cur.fetchone()
            for track in tracks:
                cur.execute("UPDATE activeprofile SET trainID = '%s' WHERE tracknum = '%s'" %(train['id'], track['id']))
                con.commit()
            cur.execute("SELECT * FROM trains WHERE id = %s" % train['id'])
            train = cur.fetchone()
            if train['mode'] == 'stop' and train['running'] == 0:
                mode = 'Stopped'
            elif train['mode'] == 'stop' and train['running'] == 1:
                mode = 'Stopping'
            elif train['mode'] == 'run' and train['running'] == 0:
                mode = 'Starting'
            elif train['mode'] == 'run' and train['running'] == 1:
                mode = 'Running'
            elif train['mode'] == 'home':
                mode ='Going Home'
            activeprofiles["Track " + str(aprow['tracknum'])] = train['trainname'],mode,train['id']
            profilereset = 1
            msg="Looks like a active train profile has been deleted, All active train profile have been reset."
    con.close()
    return render_template("index.html", activeprofiles = activeprofiles, the_title="Train Power", msg=msg)

    
    
    


@app.route("/addprofile")  
def add():  

    return render_template("addprofile.html",the_title="Added Profile")  

@app.route("/saveprofile",methods = ["POST","GET"])  
def saveprofile():  
    msg = "msg"  
    if request.method == "POST":  
        trainname = request.form["trainname"]  
        speed = request.form["speed"]  
        slowtime = request.form["slowtime"]  
        lowtrackvoltage = request.form["lowtrackvoltage"]  
        slowspeed = request.form["slowspeed"]
        mode = 'stop'  
        running = '0'

        #form validation
        if (int(speed) >= 0 and int(speed) <= 100 and int(slowtime) >= 0 and int(slowtime) <= 100 and int(lowtrackvoltage) >=0 and int(lowtrackvoltage) <=100 and  int(slowspeed) >= 0 and int(slowspeed) <= 100):
            
            try:  
                with sqlite3.connect("/opt/TrainApp/trainpower.db") as con:  
                    con.row_factory = sqlite3.Row
                    cur = con.cursor()  
                    cur.execute("INSERT into trains (trainname, speed, mode, running, slowtime, lowtrackvoltage, slowspeed) values (?,?,?,?,?,?,?)",(trainname,speed,mode,running,slowtime,lowtrackvoltage,slowspeed))  
                    con.commit()  
                    msg = "Profile added successfully"  
                    cur = con.cursor()  
                    cur.execute("select * from trains")  
                    rows = cur.fetchall()
                    con.close()    
                    return render_template("viewprofiles.html",rows = rows, the_title="View Profiles",msg=msg)
                    
            except:  
                con.rollback()  
                msg = "Something happened"  
            finally:  
                con.close()
                return render_template("viewprofiles.html",rows = rows, the_title="View Profiles",msg=msg)  
                
        else:
            msg = "Please Check your Values, all numeric values need to be between 0-100"
            return render_template("addprofile.html",msg = msg, train = request.form) 

@app.route("/viewprofiles")  
def viewprofiles():
    con = sqlite3.connect("/opt/TrainApp/trainpower.db")  
    con.row_factory = sqlite3.Row  
    cur = con.cursor()  
    cur.execute("select * from trains")  
    rows = cur.fetchall()
    con.close()    
    return render_template("viewprofiles.html",rows = rows, the_title="View Profiles")
    

@app.route("/editprofile", methods = ["POST","GET"])
def editprofile():
    if request.method == "GET":
        con = sqlite3.connect("/opt/TrainApp/trainpower.db")  
        con.row_factory = sqlite3.Row  
        cur = con.cursor()  
        cur.execute("select * from trains")  
        rows = cur.fetchall() 
        con.close()    
        return render_template("editprofileview.html", rows = rows, the_title='Edit Profile')
    elif request.method == "POST":
        if request.form['action'] == 'edit':
            trainid  =  request.form["trainid"]
            con = sqlite3.connect("/opt/TrainApp/trainpower.db")
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("SELECT * from trains WHERE id = %s" % (trainid))
            train = cur.fetchone()
            con.close()    
            return render_template("editprofile.html", train = train, the_title='Edit Profile')
        elif request.form['action'] ==  'delete':
            con = sqlite3.connect("/opt/TrainApp/trainpower.db")
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute('DELETE FROM trains WHERE id = %s' % (request.form['trainid']))
            con.commit()
            cur.execute("select * from trains")  
            rows = cur.fetchall()
            con.close()    
            return render_template("viewprofiles.html",rows = rows, the_title="View Profiles")
            

@app.route("/updateprofile", methods = ["POST","GET"])
def updateprofile():
    if request.method == "POST":
        con = sqlite3.connect("/opt/TrainApp/trainpower.db")  
        cur = con.cursor()
        cur.execute("""UPDATE trains SET trainname = '%s', speed = '%s', slowtime = '%s', lowtrackvoltage = '%s', slowspeed = '%s' WHERE id = '%s'""" % (request.form['trainname'],request.form['speed'],request.form['slowtime'],request.form['lowtrackvoltage'],request.form['slowspeed'],request.form['id']))
        con.commit()
        con.close()
        return render_template("updateprofile.html", the_profile="Update Profile")
    
@app.route("/editactiveprofiles", methods = ["POST", "GET"])
def editactiveprofiles():
    if request.method == "GET":
        con = sqlite3.connect("/opt/TrainApp/trainpower.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * from activeprofile")
        tracks = cur.fetchall()
        cur.execute("SELECT * from trains")
        trains = cur.fetchall()
        return render_template("editactiveprofiles.html", trains=trains, tracks=tracks, the_title="Edit Active Profiles")
    elif request.method == "POST":

        con = sqlite3.connect("/opt/TrainApp/trainpower.db")
        cur = con.cursor()
        cur.execute("""UPDATE activeprofile SET trainID = '%s' WHERE tracknum = '%s'""" %(request.form['train'],request.form['track']))
        con.commit()
        con.close()
        return render_template("updateactiveprofile.html",the_title="Update Active Profiles")





if __name__ == "__main__":  
    app.run(debug=True,host="0.0.0.0",port=80)  
