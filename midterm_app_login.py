from flask import Flask, request, render_template   #Flask Imports
#import pyotp    #generates one-time passwords
import sqlite3  #database for username/passwords
import hashlib  #secure hashes and message digests
#import uuid     #for creating universally unique identifiers
app = Flask(__name__) 

db_name = 'accounts.db'

@app.route("/")
@app.route("/welcome")
def main():
    return render_template("welcome.html")

@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route('/login', methods=['GET'])
def login(): 
    return render_template("login.html")

@app.route('/login2', methods=['POST'])
def login2():
    output = request.form.to_dict()
    print(output)
    userName = output["user"]
    passWord = output["pass"]
    if request.method == 'POST':
        if verify_hash(userName, passWord):
            logSuc = 'login success'
            return render_template('index.html', logSuc = logSuc)
        else:
            invalCred = 'Invalid username/password'
            return render_template('login.html', invalCred = invalCred)
    else:
        invalMet = 'Invalid Method'
        return render_template('login.html', invalMet = invalMet)

def verify_hash(userName, passWord):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS USER_HASH (USERNAME  TEXT    PRIMARY KEY NOT NULL, HASH      TEXT    NOT NULL);''')
    conn.commit()
    query = "SELECT HASH FROM USER_HASH WHERE USERNAME = '{0}'".format(userName)
    c.execute(query)
    records = c.fetchone()
    conn.close()
    if not records:
        return False
    return records[0] == hashlib.sha256(passWord.encode()).hexdigest()

@app.route('/signup', methods=['GET'])
def signup(): 
    return render_template("signup.html")

@app.route('/signup2', methods=['POST'])
def signup2():
    output = request.form.to_dict()
    print(output)
    userName = output["user"]
    passWord = output["pass"]
    missinguser = bool(userName)
    missingpass = bool(passWord)
    conn = sqlite3.connect(db_name, timeout=10)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS USER_HASH (USERNAME  TEXT    PRIMARY KEY NOT NULL, HASH      TEXT    NOT NULL);''')
    conn.commit()
    if (missinguser == False or missingpass == False):
        missing = "Missing Credentials"
        return render_template("signup.html", missing = missing)
    elif verify_hash(userName, passWord):
        existing = "Username is already used"
        return render_template("signup.html", existing = existing)
    else:
        hash_value = hashlib.sha256(passWord.encode()).hexdigest()
        c.execute("INSERT INTO USER_HASH (USERNAME, HASH) ""VALUES ('{0}', '{1}')".format(userName, hash_value))
        conn.commit()
        integError = "User has been registered."
        signSuc = "signup success"
        return render_template("signup.html", integError = integError, signSuc = signSuc)

@app.route('/update')
def updateDelete(): 
    return render_template("updateDelete.html")

@app.route('/searchUpdate', methods=['POST'])
def searchUpdate():
    output = request.form.to_dict()
    print(output)
    userName = output["user"]
    if(userName == ""):
        missing = "Please Enter Account Name"
        return render_template("updateDelete.html", missing = missing)
    else:
        db_account = 'accounts.db'
        conn = sqlite3.connect(db_account, timeout=10)
        c = conn.cursor()
        c.execute("SELECT * FROM USER_HASH WHERE USERNAME = '%s'"%userName)
        result = c.fetchone()
        try:
            userOut = result[0]
            passOut = result[1]
            return render_template("update.html", userOut = userOut, passOut = passOut)
        except TypeError:
            noUserName = ("Error occurred: No Account Name Existed")
            return render_template("updateDelete.html", noUserName = noUserName)
        

@app.route("/update2", methods=['POST'])
def update2():
    output = request.form.to_dict()
    print(output)
    userName = output["user"]
    passWord = output["pass"]
    db_account = 'accounts.db'
    conn = sqlite3.connect(db_account, timeout=10)
    c = conn.cursor()
    if(userName == "" and passWord == ""):
        missing = "Nothing to Update"
        return render_template("updateDelete.html", missing = missing)
    elif(userName and passWord):
        hash_value = hashlib.sha256(passWord.encode()).hexdigest()
        c.execute("""UPDATE USER_HASH SET HASH=? WHERE USERNAME=?""",(hash_value, userName))
        conn.commit()
        allUpdate = str(userName) + " Password Successfully Updated"
        return render_template("updateDelete.html", allUpdate = allUpdate)
    else:
        Failed = "Error?"
        return render_template("updateDelete.html", Failed = Failed)

@app.route("/delete")
def delete():
    return render_template("updateDelete.html")

@app.route("/delete2", methods=['POST'])
def delete2():
    output = request.form.to_dict()
    print(output)
    userName = output["user"]
    db_account = 'accounts.db'
    conn = sqlite3.connect(db_account, timeout=10)
    c = conn.cursor()
    if(userName == ""):
        missing = "Please Enter Account Name"
        return render_template("updateDelete.html", missing = missing)
    else:
        db_account = 'accounts.db'
        conn = sqlite3.connect(db_account, timeout=10)
        c = conn.cursor()
        c.execute("SELECT * FROM USER_HASH WHERE USERNAME = '%s'"%userName)
        result = c.fetchone()
        try:
            result = result[0]
            c.execute("DELETE FROM USER_HASH WHERE USERNAME = '%s'"%userName)
            conn.commit()
            deleteSuccess = str(userName) + " Account is Deleted"
            return render_template("updateDelete.html", deleteSuccess = deleteSuccess)
        except TypeError:
            noUserName = ("Error occurred: No Account Name Existed")
            return render_template("updateDelete.html", noUserName = noUserName)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)