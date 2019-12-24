#modules-------------------------
from app import app, db
from models import Restaurants
from models import Reservations
from models import ReSettings
from forms import BookForm

#libraries-----------------------
from flask import render_template, request, flash, redirect, session, url_for
import random
import string
from passlib.hash import sha256_crypt
from functools import wraps

### functions
def randomString(stringLength):
    """Generate a random string with the combination of lowercase and uppercase letters """

    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(stringLength))

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('unauthorized, please login')
            return redirect(url_for('login'))

    return wrap

def get_bool(what_bool):
                if what_bool == "False":
                    return True
                else:
                    return False

"""@app.route("/", methods=["GET", "POST"])
def home():
    reservations = Reservations.query.all()
    if request.method == "POST":
        if 'add' in request.form:
            res_day = Reservations(s_day=request.form.get("s_day"), s_r_id=request.form.get("s_r_id"))
            db.session.add(res_day)
            db.session.commit()
            print(request.form)
        elif 'show' in request.form:
            return render_template("home.html", reservations=reservations, toshow=True)
        elif 'hide' in request.form:
            return render_template("home.html", reservations=reservations, toshow=False)
    return render_template("home.html")"""

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/reservation/<string:id>", methods=["GET", "POST"])
def reservation(id):
    msg = None

    a = Restaurants.query.all()
    counter = 0
    for i in a:
        if id == i.r_key:
            counter += 1

    if counter == 0:
        return render_template("error.html")

    else:
        reservations = Reservations.query.filter(Reservations.s_r_id == id)
        reservations_check = Reservations.query.filter(Reservations.s_r_id == id).first()

        restaurant_id = Restaurants.query.filter_by(r_key = id).first()
        freespot_default = ReSettings.query.filter_by(d_r_id = restaurant_id.id).first()

        print(freespot_default.d_freespot_max)
        for i in reservations:
            print(i.s_r_id)
            
        if request.method == "POST":
            if 'add' in request.form:
                data_day = request.form["sday"]
                n_of_people = request.form["n_of_people"]
                
                try:
                    reservations_check2 = Reservations.query.filter_by(s_r_id = id , s_day = data_day).all()
                    under_zero_res = reservations_check2[-1].s_freespot_total
                    print(reservations_check2[-1].s_freespot_total)
                    app.logger.info("ciao")
                    if under_zero_res - int(n_of_people) < 0:
                        msg = "There are no more spots available"
                        pass

                    else:
                        res_day = Reservations(s_day=request.form.get("sday"), s_freespot = n_of_people, s_freespot_total = under_zero_res - int(n_of_people), s_r_id=id)
                        db.session.add(res_day)
                        db.session.commit()
                except:
                    res_day = Reservations(s_day=request.form.get("sday"), s_freespot = n_of_people, s_freespot_total = freespot_default.d_freespot_max - int(n_of_people), s_r_id=id)
                    db.session.add(res_day)
                    db.session.commit()

            elif 'show' in request.form:
                return render_template("reservation.html", reservations=reservations, toshow=True, id=id)
            elif 'hide' in request.form:
                return render_template("reservation.html", reservations=reservations, toshow=False, id=id)
            elif 'delete' in request.form:
                get_id_to_delete = request.form.getlist("get_id_to_delete")
                to_delete = Reservations.query.filter_by(id = get_id_to_delete[1]).first()
                tot_people_to_add = to_delete.s_freespot
                db.session.delete(to_delete)
                db.session.commit()

                try:
                    reservations_check2 = Reservations.query.filter_by(s_day = get_id_to_delete[0]).all()
                    reservations_check2[-1].s_freespot_total += tot_people_to_add
                    db.session.commit()
                    print(last_res)
                except:
                    pass
                

        return render_template("reservation.html", id=id, msg = msg)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = sha256_crypt.hash(request.form["password"])
        name = request.form["rest_name"]
        address = request.form["rest_address"]
        owner_name = request.form["owner_name"]
        new_key = randomString(15)
        new_user = Restaurants(r_username=username, r_password=password, r_name=name, r_adress=address, r_ownername=owner_name, r_key=new_key)
        db.session.add(new_user)
        #db.session.commit()
        app.logger.info("new user registered")
        ###add basic restaurant settings
        rest_name = Restaurants.query.filter_by(r_username=username).first()
        rest_id = rest_name.id

        for i in range(1,8):
            new_day = ReSettings(d_days = i, d_close = 1, d_open_time = "19:30", d_close_time = "23:30", d_freespot_max = 20, d_r_id = rest_id)
            db.session.add(new_day)
        
        db.session.commit()

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password_candidate = request.form["password"]

        get_user = Restaurants.query.filter_by(r_username=username).first()

        if get_user != None:
            password = get_user.r_password

            if sha256_crypt.verify(password_candidate, password):
                session["logged_in"] = True
                session["username"] = get_user.r_username
                session["id"] = get_user.id
                session["key"] = get_user.r_key

                app.logger.info("logged in!")

                return redirect(url_for("dashboard2"))
            else:
                error = "invalid"
                app.logger.info("PASSWORD WRONG")
                return render_template("login.html", error = error)
        else:
            error = "Invalid"
            app.logger.info("USER NOT FOUND")
            return render_template("login.html", error = error)


    return render_template("login.html")

"""@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    #loading all restaurant data with id of the session
    dataload = ReSettings.query.filter_by(d_r_id = session['id']).all()
    msg = None
    if request.method == "POST":
        #manage POST from hours form and from days form
        #hours form
        if "settings" in request.form:
            open_time = request.form["open-time"]
            close_time = request.form["close-time"]
            if open_time < close_time:
                print("ok")
                msg = "opening and closing time set!"
            else:
                print("not ok")
                msg = "opening time must be smaller then closing time"

        #days form
        else:
            for i in range (1,8):
                try:
                    a = request.form[str(i)]
                    old_close = ReSettings.query.filter_by(d_close = a, d_days = int(i), d_r_id = session["id"]).first()
                    if old_close.d_close == 0:
                        old_close.d_close = 1
                        db.session.commit()
                    else:
                        old_close.d_close = 0
                        db.session.commit()
                except:
                    pass
    return render_template("dashboard.html", dataload=dataload, msg=msg)"""

#Logout
@app.route('/logout')
def logout():
    session.clear()
    app.logger.info("LOGGED OUT")
    return redirect(url_for("login"))


@app.route("/dashboard2", methods =["GET","POST"])
@is_logged_in
def dashboard2():
        dataload = ReSettings.query.filter_by(d_r_id = session["id"])
        dataload = dataload.order_by(ReSettings.id)
        msg = None
        
        if request.method=="POST":

            if "settings_hours" in request.form:
    
                open_time = request.form["open_time"]
                close_time = request.form["close_time"]
                day_hours = request.form["day_hours"]
                if open_time < close_time:
                    old_time = ReSettings.query.filter_by(d_days = day_hours, d_r_id = session["id"]).first()
                    old_time.d_open_time = open_time
                    old_time.d_close_time = close_time
                    

                    print("ok")
                    msg = "opening and closing time set!"
                else:
                    print("not ok")
                    msg = "opening time must be smaller then closing time"

            else:
                get_status = request.form.getlist("day")
                bool_value_for_db_query = get_bool(get_status[1])
                print(bool_value_for_db_query)
                old_close_status = ReSettings.query.filter_by(d_days = int(get_status[0]), d_close = bool_value_for_db_query, d_r_id = session["id"]).first()
                old_close_status.d_close = not bool_value_for_db_query
                print(not bool_value_for_db_query)
                
                print(get_status)
            db.session.commit()
        return render_template("dashboard2.html", dataload = dataload, msg = msg)



@app.route("/dashboard3", methods =["GET","POST"])
@is_logged_in
def dashboard3():
        dataload = ReSettings.query.filter_by(d_r_id = 1).first()
        msg = None
        print(dataload)
        days = ["Monday", "Tuesdasy", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        if request.method == "POST":
            status_change = request.form.get("status_change")
            plinio = request.form.get("plinio")
            print(status_change)

            """if status == "False":
                status = True
            else:
                status = False

           print(status_change)
            

            old_status = ReSettings.query.filter_by(d_days = day, d_close = status, d_r_id = session["id"]).first()

            print(old_status.d_close)
            a = not status

            old_status.d_close = a

            db.session.commit()"""

        
        """if request.method=="POST":

            if "settings_hours" in request.form:
    
                open_time = request.form["open_time"]
                close_time = request.form["close_time"]
                day_hours = request.form["day_hours"]
                if open_time < close_time:
                    old_time = ReSettings.query.filter_by(d_days = day_hours, d_r_id = session["id"]).first()
                    old_time.d_open_time = open_time
                    old_time.d_close_time = close_time
                    db.session.commit()

                    print("ok")
                    msg = "opening and closing time set!"
                else:
                    print("not ok")
                    msg = "opening time must be smaller then closing time"

            else:
                get_status = request.form.getlist("day")
                bool_value_for_db_query = get_bool(get_status[1])
                print(bool_value_for_db_query)
                old_close_status = ReSettings.query.filter_by(d_days = int(get_status[0]), d_close = bool_value_for_db_query, d_r_id = session["id"]).first()
                old_close_status.d_close = not bool_value_for_db_query
                print(not bool_value_for_db_query)
                db.session.commit()
                print(get_status)"""

        return render_template("dashboard3.html", dataload = dataload, msg = msg, days = days)







