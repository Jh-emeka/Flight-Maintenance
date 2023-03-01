from flask import Flask, render_template, request, url_for, redirect, g
from User import User
from gevent.pywsgi import WSGIServer
import os
import bcrypt as bcrypt
import sqlite3 as sqlite
from flask_login import LoginManager, login_user, login_required, logout_user

app = Flask(__name__, template_folder="Templates")
app.debug = True

app.config['SECRET_KEY'] = os.urandom(12).hex()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.session_protection = "strong"

SESSION_COOKIE_HTTPONLY = True,
REMEMBER_COOKIE_HTTPONLY = True,
SESSION_COOKIE_SAMESITE = "Strict"


@login_manager.user_loader
def load_user(user_id):
    con = sqlite.connect("ABCAIR.db")
    curs = con.cursor()
    curs.execute("SELECT * FROM Admins WHERE Admin_Id = ?", [user_id])
    row = curs.fetchone()
    g.user = row[1]
    if row is None:
        return None
    else:
        return User(int(row[0]), row[1], row[2])


@app.route('/logout')
@login_required
def logout():
    logout_user()
    msg = "Admin logged out"
    return render_template('Login.html', msg=msg)


@app.route('/')
def index():
    return render_template('Login.html')


@app.route('/home')
@login_required
def home_page():
    msg = f"Welcome {g.user}"
    return render_template('Homepage.html', msg=msg)


@app.route('/newAdmin')
@login_required
def add_admin():
    return render_template('New_Admin.html')


@app.route('/manageAirframes')
@login_required
def airframes():
    con = sqlite.connect("ABCAIR.db")
    print("Database opened successfully")
    cur = con.cursor()
    cur.execute("SELECT * FROM Air_Frame")
    rows = cur.fetchall()
    return render_template('Manage_Airframes.html', rows=rows)


@app.route('/manageMaintenance')
@login_required
def maintenance():
    con = sqlite.connect("ABCAIR.db")
    print("Database opened successfully")
    cur = con.cursor()
    cur.execute("SELECT * FROM Maintenance")
    rows = cur.fetchall()
    return render_template('Manage_Maintenance.html', rows=rows)


@app.route('/manageEngineers')
@login_required
def engineers():
    con = sqlite.connect("ABCAIR.db")
    print("Database opened successfully")
    cur = con.cursor()
    cur.execute("SELECT * FROM Engineers")
    rows = cur.fetchall()
    return render_template('Manage_Engineers.html', rows=rows)


@app.route('/newAirframe')
@login_required
def new_airframe():
    return render_template('Add_Airframe.html')


@app.route('/updateAirframe')
@login_required
def upd_airframe():
    return render_template('Update_Airframe.html')


@app.route('/deleteAirframe')
@login_required
def del_airframe():
    return render_template('Delete_Airframe.html')


@app.route('/newMaintenance')
@login_required
def new_maintenance():
    con = sqlite.connect("ABCAIR.db")
    print("Database opened successfully")
    cur = con.cursor()
    cur.execute("SELECT Name FROM Engineers")
    rows = cur.fetchall()
    print(rows)
    return render_template('Add_Maintenance.html', rows=rows)


@app.route('/updateMaintenance')
@login_required
def upd_maintenance():
    return render_template('Update_Maintenance.html')


@app.route('/deleteMaintenance')
@login_required
def del_maintenance():
    return render_template('Delete_Maintenance.html')


@app.route('/newEngineer')
@login_required
def new_engineer():
    return render_template('Add_Engineer.html')


@app.route('/updateEngineer')
@login_required
def upd_engineer():
    return render_template('Update_Engineer.html')


@app.route('/deleteEngineer')
@login_required
def del_engineer():
    return render_template('Delete_Engineer.html')


@login_manager.unauthorized_handler
def unauthorised():
    # raise Unauthorized

    msg = "Please log in to access this page"
    return render_template('Login.html', msg=msg)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':

        username = request.form['username']
        user_input = request.form['password'].encode("utf-8")

        with sqlite.connect("ABCAIR.db") as con:

            print("Database opened successfully")
            cur = con.cursor()
            statement = f"SELECT * FROM Admins WHERE Username = '{username}' "
            cur.execute(statement)
            rows = cur.fetchone()
            con.commit()

        try:

            if not rows:
                msg = "Invalid details"
                return render_template("Login.html", msg=msg)

            password = rows[2]
            if bcrypt.checkpw(user_input, password):

                user = User(rows[0], rows[1], password)
                login_user(user)
                user.authenticated = True

                msg = "Login Successful"
                print(msg)

                return redirect(url_for('home_page'))





            else:
                logout_user()
                msg = "Login failed, Incorrect username or password"
                return render_template("Login.html", msg=msg)


        except TypeError:
            msg = "Invalid details"
            return render_template("Login.html", msg=msg)


@app.route('/addAdmin', methods=['POST', 'GET'])
def new_admin():
    if request.method == 'POST':

        admin_username = request.form['username']
        admin_password = request.form['Pwd']  # encode("utf-8")
        confirm_password = request.form['Pwd2']

        if not admin_password == confirm_password:
            msg = "Passwords do not match"
            return render_template("New_Admin.html", msg=msg)

        elif not admin_username or not admin_password or not confirm_password:
            msg = "Please fill in all text boxes"
            return render_template("New_Admin.html", msg=msg)

        hashed = bcrypt.hashpw(admin_password.encode("utf-8"), bcrypt.gensalt())

        with sqlite.connect("ABCAIR.db") as con:

            print("Database opened successfully")
            cur = con.cursor()

            cur.execute(f"SELECT * FROM Admins WHERE Username LIKE '{admin_username}'")
            rows = cur.fetchall()

            if rows:
                msg = "username already exists, please choose a different username"
                return render_template("New_Admin.html", msg=msg)

            else:
                cur.execute("INSERT INTO Admins(Username, Password) VALUES(?,?)", (admin_username, hashed))
                con.commit()
                print("Admin added successfully")
                msg = "Admin added successfully"

                return render_template("Login.html", msg=msg)


@app.route('/getAirframes', methods=['POST', 'GET'])
def get_airframes():
    if request.method == 'POST':
        aircraft_id = request.form['Id']

        with sqlite.connect("ABCAIR.db") as con:
            print("Database opened successfully")
            cur = con.cursor()
            if not aircraft_id:
                cur.execute("SELECT * FROM Air_Frame")

            else:
                cur.execute("SELECT * FROM Air_Frame WHERE Aircraft_Id = ?", [aircraft_id])

            con.commit()
            rows = cur.fetchall()

            if not rows:
                msg = "No matching records"

            else:
                print("Airframe fetched successfully")
                msg = "Airframe fetched successfully"

        return render_template("Manage_Airframes.html", msg=msg, rows=rows)


@app.route('/getMaintenance', methods=['POST', 'GET'])
def get_maintenance():
    if request.method == 'POST':
        maintenance_id = request.form['Id']

        with sqlite.connect("ABCAIR.db") as con:
            print("Database opened successfully")
            cur = con.cursor()
            if not maintenance_id:
                cur.execute("SELECT * FROM Maintenance")

            else:
                cur.execute("SELECT * FROM Maintenance WHERE Maintenance_Id = ?", [maintenance_id])

            con.commit()
            rows = cur.fetchall()

            if not rows:
                msg = "No matching records"

            else:
                print("Maintenance fetched successfully")
                msg = "Maintenance fetched successfully"

        return render_template("Manage_Maintenance.html", msg=msg, rows=rows)


@app.route('/getEngineers', methods=['POST', 'GET'])
def get_engineers():
    if request.method == 'POST':
        name = request.form['name']

        with sqlite.connect("ABCAIR.db") as con:
            print("Database opened successfully")
            cur = con.cursor()
            if not name:
                statement = "SELECT * FROM Engineers"
                cur.execute(statement)

            else:
                statement = f"SELECT * FROM Engineers WHERE Name Like '{name}' "
                cur.execute(statement)

            con.commit()
            rows = cur.fetchall()

            if not rows:
                msg = "No matching records"

            else:
                print("Engineers fetched successfully")
                msg = "Engineers fetched successfully"

        return render_template("Manage_Engineers.html", msg=msg, rows=rows)


@app.route('/add_airframe', methods=['POST', 'GET'])
def add_airframe():
    if request.method == 'POST':
        aircraft_model = request.form['AircraftModel']
        flight_hours = request.form['FlightHours']
        scheduled_maintenance = request.form['ScheduledMaintenance']

        if not aircraft_model or not flight_hours or not scheduled_maintenance:
            msg = "Please fill in all details"
            return render_template('Add_Airframe.html', msg=msg)

        else:

            with sqlite.connect("ABCAIR.db") as con:
                print("Database opened successfully")
                cur = con.cursor()
                cur.execute("INSERT INTO Air_Frame(Aircraft_Model, Flight_Hours, Scheduled_Maintenance) VALUES(?,?,?)",
                            (aircraft_model, flight_hours, scheduled_maintenance))
                con.commit()
                print("Airframe added successfully")
                msg = "Airframe added successfully"

                return redirect(url_for('airframes', msg=msg))


@app.route('/update_airframe', methods=['POST', 'GET'])
def update_airframe():
    if request.method == 'POST':
        aircraft_id = request.form['Id']
        scheduled_maintenance = request.form['ScheduledMaintenance']

        with sqlite.connect("ABCAIR.db") as con:
            print("Database opened successfully")
            cur = con.cursor()

            check = record_checker('Air_Frame', 'Aircraft_Id', aircraft_id)

            if check == 'Record does not exist':
                msg = check
                return render_template('Update_Airframe.html', msg=msg)

            else:

                cur.execute(f"UPDATE Air_Frame SET Scheduled_Maintenance = '{scheduled_maintenance}' WHERE "
                            f"Aircraft_Id = '{aircraft_id}'")

                con.commit()
                print("Airframe updated successfully")
                msg = "Airframe updated successfully"
                return redirect(url_for('airframes', msg=msg))


@app.route('/delete_airframe', methods=['POST', 'GET'])
def delete_airframe():
    if request.method == 'POST':
        aircraft_id = request.form['Id']

        with sqlite.connect("ABCAIR.db") as con:
            print("Database opened successfully")
            cur = con.cursor()

            check = record_checker('Air_Frame', 'Aircraft_Id', aircraft_id)

            if check == 'Record does not exist':
                msg = check
                return render_template('Delete_Airframe.html', msg=msg)

            else:

                cur.execute("DELETE FROM Air_Frame WHERE Aircraft_Id = ?", [aircraft_id])
                con.commit()
                print("Airframe deleted successfully")
                msg = "Airframe deleted successfully"

                return redirect(url_for('airframes', msg=msg))


@app.route('/add_maintenance', methods=['POST', 'GET'])
def add_maintenance():
    if request.method == 'POST':
        aircraft_id = request.form['Id']
        start_date = request.form['Date']
        duration = request.form['Duration']
        status = request.form['Status']
        engineer = request.form['Engineer']

        if not aircraft_id or not start_date or not duration or not status or not engineer:
            msg = "Please fill in all details"
            return render_template('Add_Maintenance.html', msg=msg)

        else:
            with sqlite.connect("ABCAIR.db") as con:
                print("Database opened successfully")
                cur = con.cursor()
                cur.execute("INSERT INTO Maintenance(Aircraft_Id, Start_Date, Duration, Maintenance_Status, "
                            "Assigned_Engineer) VALUES(?,?,?,?,?)",
                            (aircraft_id, start_date, duration, status, engineer))
                con.commit()
                print("Maintenance added successfully")
                msg = "Maintenance added successfully"

                return redirect(url_for('maintenance', msg=msg))


@app.route('/update_maintenance', methods=['POST', 'GET'])
def update_maintenance():
    if request.method == 'POST':
        maintenance_id = request.form['Id']
        status = request.form['Status']

        with sqlite.connect("ABCAIR.db") as con:
            print("Database opened successfully")
            cur = con.cursor()

            check = record_checker('Maintenance', 'Maintenance_Id', maintenance_id)

            if check == 'Record does not exist':
                msg = check
                return render_template('Update_Maintenance.html', msg=msg)

            else:

                cur.execute(f"UPDATE Maintenance SET Maintenance_Status = '{status}'"
                            f" WHERE Maintenance_Id = '{maintenance_id}'")

                con.commit()
                print("Maintenance updated successfully")
                msg = "Maintenance updated successfully"

                return redirect(url_for('maintenance', msg=msg))


@app.route('/delete_maintenance', methods=['POST', 'GET'])
def delete_maintenance():
    if request.method == 'POST':
        maintenance_id = request.form['Id']

        with sqlite.connect("ABCAIR.db") as con:
            print("Database opened successfully")
            cur = con.cursor()

            check = record_checker('Maintenance', 'Maintenance_Id', maintenance_id)

            if check == 'Record does not exist':
                msg = check
                return render_template('Delete_Maintenance.html', msg=msg)

            else:

                cur.execute("DELETE FROM Maintenance WHERE Maintenance_Id = ?", [maintenance_id])
                con.commit()
                print("Maintenance deleted successfully")
                msg = "Maintenance deleted successfully"
                return redirect(url_for('maintenance', msg=msg))


@app.route('/add_engineer', methods=['POST', 'GET'])
def add_engineer():
    if request.method == 'POST':
        name = request.form['Name']
        dob = request.form['DOB']
        date = request.form['Date']
        employment_type = request.form['Type']
        rate = request.form['Rate']

        if not name or not dob or not date or not employment_type or not rate:
            msg = "Please fill in all details"
            return render_template('Add_Engineer.html', msg=msg)

        else:

            with sqlite.connect("ABCAIR.db") as con:
                print("Database opened successfully")
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO Engineers(Name, DOB, Employment_Date, Employment_Type, Hourly_Rate) VALUES(?,?,"
                    "?,?,?)",
                    (name, dob, date, employment_type, rate))
                con.commit()
                print("Engineer added successfully")
                msg = "Engineer added successfully"

                return redirect(url_for('engineers', msg=msg))


@app.route('/update_engineer', methods=['POST', 'GET'])
def update_engineer():
    if request.method == 'POST':
        name = request.form['Name']
        employment_type = request.form['Type']
        rate = request.form['Rate']

        with sqlite.connect("ABCAIR.db") as con:
            print("Database opened successfully")
            cur = con.cursor()

            check = record_checker('Engineers', 'Name', name)

            if check == 'Record does not exist':
                msg = check
                return render_template('Update_Engineer.html', msg=msg)

            else:

                cur.execute(f"UPDATE Engineers SET Employment_Type = ?, Hourly_Rate = ?  WHERE Name = '{name}' ",
                            (employment_type, rate))
                con.commit()
                print("Engineer updated successfully")
                msg = "Engineer updated successfully"

                return redirect(url_for('engineers', msg=msg))


@app.route('/delete_engineer', methods=['POST', 'GET'])
def delete_engineer():
    if request.method == 'POST':
        name = request.form['Name']

        with sqlite.connect("ABCAIR.db") as con:
            print("Database opened successfully")
            cur = con.cursor()

            check = record_checker('Engineers', 'Name', name)

            if check == 'Record does not exist':
                msg = check
                return render_template('Delete_Engineer.html', msg=msg)

            else:
                cur.execute(f"DELETE FROM Engineers WHERE Name = '{name}'")
                con.commit()
                print("Engineer deleted successfully")
                msg = "Engineer deleted successfully"

                return redirect(url_for('engineers', msg=msg))


def record_checker(table, uid, value):
    with sqlite.connect("ABCAIR.db") as con:
        print("check in progress......")
        cur = con.cursor()
        statement = f"SELECT * FROM {table} WHERE {uid} = '{value}'"
        print(table, uid, value)
        cur.execute(statement)
        rows = cur.fetchone()
        if not rows:
            msg = "Record does not exist"
            return msg


if __name__ == "__main__":
    http_server = WSGIServer(('127.0.0.1', 3000), app)
    http_server.serve_forever()
