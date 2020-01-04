#modules-------------------------
from app import app, db
from models import *
from forms import *

#libraries-----------------------
from flask import render_template, request, flash, redirect, session, url_for, logging
import random
import string
from passlib.hash import sha256_crypt
from functools import wraps
import datetime

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
@is_logged_in
def reservation(id):

    a = Restaurants.query.all()
    counter = 0
    for i in a:
        if id == i.r_key:
            counter += 1

    if counter == 0:
        return render_template("error.html")

    else:
        #reservations_check = Reservations.query.filter(Reservations.s_r_id == id).first()
        restaurant_id = Restaurants.query.filter_by(r_key = id).first()

            
        if request.method == "POST":
            
            if 'show' in request.form:
                data_day = request.form["sday"]
                reservations = Reservations.query.filter_by(s_r_id=id, s_day=data_day)
                reservations = reservations.order_by(Reservations.s_time)
                freespot_default = AvailableSpot.query.filter_by(t_restaurant=id, t_date_id=data_day)
                freespot_default = freespot_default.order_by(AvailableSpot.t_time_id)
                return render_template("reservation.html", reservations=reservations, freespot = freespot_default, toshow=True, id=id)
            elif 'hide' in request.form:
                return render_template("reservation.html", reservations=reservations, toshow=False, id=id)
            elif 'delete' in request.form:
                delete_id = request.form.getlist("get_res_to_delete")
                compare_form_timerange = Time_range.query.filter_by(t_time = delete_id[1]).first().id
    
                #select available spot to upgrade(canceled reservation)
                update_availablespot_frst = AvailableSpot.query.filter_by(t_restaurant=id, t_time_id=compare_form_timerange, t_date_id=delete_id[2]).first()
                update_availablespot_scnd = AvailableSpot.query.filter_by(t_restaurant=id, t_time_id=compare_form_timerange + 1, t_date_id=delete_id[2]).first()
                update_availablespot_frst.t_freespot = update_availablespot_frst.t_freespot + int(delete_id[0])
                update_availablespot_scnd.t_freespot = update_availablespot_scnd.t_freespot + int(delete_id[0])

                #delete_reservation
                delete_reservation = Reservations.query.filter_by(id = delete_id[3]).first()
                db.session.delete(delete_reservation)
                db.session.commit()                
                

        return render_template("reservation.html", id=id)

"""
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
"""


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


@app.route("/register", methods = ["GET", "POST"])
def register():

    form = RegisterForm()

    if request.method == "POST" and form.validate_on_submit():
        username = form.username.data
        restaurant_address = form.restaurant_address.data
        restaurant_name = form.restaurant_name.data
        owner_fname = form.owner_fname.data
        owner_lname = form.owner_lname.data
        website = form.website.data
        email = form.email.data
        telephone_number = form.telephone_number.data
        country = form.country.data
        pwd = sha256_crypt.hash(form.pwd.data)
        new_key = randomString(15)

        print(username, restaurant_name, restaurant_address, owner_lname, owner_fname, website, email, telephone_number, country, pwd, new_key)

        new_user = Restaurants(r_username=username, r_password=pwd, r_name=restaurant_name,
                                r_adress=restaurant_address, r_ownername=owner_fname, r_ownerlastname=owner_lname,
                                r_country=country, r_website=website, r_telephone=telephone_number,
                                r_email=email, r_key=new_key)
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
    print(form.errors)

    
    return render_template("provalog.html", form = form)


@app.route("/main_cont")
@is_logged_in
def main_cont():

    dataload = ReSettings.query.filter_by(d_r_id = session["id"])
    dataload = dataload.order_by(ReSettings.id)
    print(dataload)

    return render_template("main_cont.html", dataload=dataload)


@app.route("/login2", methods=["GET", "POST"])
def login2():
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        username = form.username.data
        password_candidate = form.pwd.data

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
                return render_template("login2.html", error = error, form=form)
        else:
            error = "Invalid"
            app.logger.info("USER NOT FOUND")
            return render_template("login2.html", error = error, form=form)

    return render_template("login2.html", form=form)


@app.route("/reservations/<string:id>/", methods=["GET", "POST"])
def reservations(id):
    msg = None
    freespot = None

    a = Restaurants.query.all()
    counter = 0
    for i in a:
        if id == i.r_key:
            counter += 1

    if counter == 0:
        return render_template("error.html")

    else:
        reservations = Reservations.query.filter(Reservations.s_r_id == id)
        #reservations_check = Reservations.query.filter(Reservations.s_r_id == id).first()

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
                        msg = "There are no more spots available, spots available: "
                        reservations_check2 = Reservations.query.filter_by(s_r_id=id, s_day=data_day).all()
                        freespot = reservations_check2[-1].s_freespot_total
                        pass

                    else:
                        res_day = Reservations(s_day=request.form.get("sday"), s_freespot = n_of_people, s_freespot_total = under_zero_res - int(n_of_people), s_r_id=id)
                        db.session.add(res_day)
                        db.session.commit()
                        reservations_check2 = Reservations.query.filter_by(s_r_id=id, s_day=data_day).all()
                        freespot = reservations_check2[-1].s_freespot_total
        

                except:
                    if 20 - int(n_of_people) < 0:
                        msg = "There are no more spots available, spots available: "
                        freespot = freespot_default.d_freespot_max
                        pass
                    else:
                        res_day = Reservations(s_day=request.form.get("sday"), s_freespot = n_of_people, s_freespot_total = freespot_default.d_freespot_max - int(n_of_people), s_r_id=id)
                        db.session.add(res_day)
                        db.session.commit()
                

        return render_template("reservation2.html", id=id, msg = msg, freespot = freespot)



@app.route("/reservations3/<string:id>/", methods=["GET", "POST"])
def reservations3(id):

    msg = None

    #check if route exists--------------
    a = Restaurants.query.all()

    counter = 0
    for i in a:
        if id == i.r_key:
            counter += 1

    if counter == 0:
        return render_template("error.html")

    #if exists render else:-------------

    else:
            
        if request.method == "POST":
            if 'set_reservation' in request.form:
                data_day = request.form["sday"]
                n_of_people = int(request.form["n_of_people"])
                booking_time = request.form["booking_time"]

                day_in_numbers = datetime.datetime.strptime(data_day, "%Y-%m-%d").weekday()

                #find id in time_range from actual time "19:00" is equal to 1, "19:30" to 2 ecc...
                find_time_range_id = Time_range.query.filter_by(t_time = booking_time).first()
                time_range_id = find_time_range_id.id

                #retrieve freespot total_for given day using day_in_numbers
                freespot_total_day = Restaurants.query.filter_by(r_key=id).first()
                freespot_total_day = freespot_total_day.id
                freespot_total_day = ReSettings.query.filter_by(d_r_id=freespot_total_day).all()
                freespot_total_day = freespot_total_day[day_in_numbers].d_freespot_max

                print(time_range_id)

                find_spot_hour_frst = AvailableSpot.query.filter_by(t_time_id = time_range_id, t_date_id = data_day, t_restaurant=id).first()
                try:
                    find_spot_hour_scnd = AvailableSpot.query.filter_by(t_time_id = time_range_id + 1, t_date_id = data_day, t_restaurant=id).first()
                except:
                    print("index out of range, not considered")

                if not find_spot_hour_frst and not find_spot_hour_scnd:
                    if freespot_total_day - n_of_people < 0:
                        app.logger.info("max reached")
                        msg = 2
                        pass
                    else:
                        #make new reservation if both "ranges" return none
                        new_reservation = Reservations(s_day=data_day, s_npeople=n_of_people, s_time=booking_time, s_r_id=id)
                        db.session.add(new_reservation)
                        #add n_of_people to both ranges(1 hour per table) by taking original settings(both none is a new reservation for that range)
                        new_spot_frst = AvailableSpot(t_restaurant=id, t_time_id=time_range_id, t_date_id=data_day, t_freespot = freespot_total_day - n_of_people)
                        new_spot_scnd = AvailableSpot(t_restaurant=id, t_time_id=time_range_id + 1, t_date_id=data_day, t_freespot = freespot_total_day - n_of_people)
                        db.session.add(new_spot_frst)
                        db.session.add(new_spot_scnd)

                elif find_spot_hour_frst and find_spot_hour_scnd:
                    #get freespot from both ranges
                    get_available_frst = AvailableSpot.query.filter_by(t_time_id = time_range_id, t_date_id = data_day, t_restaurant=id).first()
                    get_available_scnd = AvailableSpot.query.filter_by(t_time_id = time_range_id + 1, t_date_id = data_day, t_restaurant=id).first()
                    if get_available_frst.t_freespot - n_of_people < 0 or get_available_scnd.t_freespot - n_of_people < 0:
                        app.logger.info("max reached")
                        pass
                    else:
                        new_reservation = Reservations(s_day=data_day, s_npeople=n_of_people, s_time=booking_time, s_r_id=id)
                        db.session.add(new_reservation)
                        #add n_of_people to both ranges(1 hour per table) by taking original settings(both none is a new reservation for that range)
                        get_available_frst.t_freespot = get_available_frst.t_freespot - n_of_people
                        get_available_scnd.t_freespot = get_available_scnd.t_freespot - n_of_people

                elif find_spot_hour_frst and not find_spot_hour_scnd:
                    get_available_frst = AvailableSpot.query.filter_by(t_time_id = time_range_id, t_date_id = data_day, t_restaurant=id).first()
                    if get_available_frst.t_freespot - n_of_people < 0:
                        app.logger.info("max reached")
                        pass
                    else:
                        new_reservation = Reservations(s_day=data_day, s_npeople=n_of_people, s_time=booking_time, s_r_id=id)
                        db.session.add(new_reservation)
                        #add n_of_people to both ranges(1 hour per table) by taking original settings(both none is a new reservation for that range)
                        get_available_frst.t_freespot = get_available_frst.t_freespot - n_of_people
                        new_spot_scnd = AvailableSpot(t_restaurant=id, t_time_id=time_range_id + 1, t_date_id=data_day, t_freespot = freespot_total_day - n_of_people)
                        db.session.add(new_spot_scnd)

                elif not find_spot_hour_frst and find_spot_hour_scnd:
                    get_available_scnd = AvailableSpot.query.filter_by(t_time_id = time_range_id + 1, t_date_id = data_day, t_restaurant=id).first()
                    if get_available_scnd.t_freespot - n_of_people < 0:
                        app.logger.info("max reached")
                        pass
                    else:
                        new_reservation = Reservations(s_day=data_day, s_npeople=n_of_people, s_time=booking_time, s_r_id=id)
                        db.session.add(new_reservation)
                        #add n_of_people to both ranges(1 hour per table) by taking original settings(both none is a new reservation for that range)
                        get_available_scnd.t_freespot = get_available_scnd.t_freespot - n_of_people
                        new_spot_frst = AvailableSpot(t_restaurant=id, t_time_id=time_range_id, t_date_id=data_day, t_freespot = freespot_total_day - n_of_people)
                        db.session.add(new_spot_frst)
            
                db.session.commit()

                #print(data_day, n_of_people, booking_time)
                

        return render_template("reservation3.html", id=id, msg = msg)


