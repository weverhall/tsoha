from app import app
from flask import render_template, request, redirect
import rides
import users


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("login.html", message="Error: Wrong username or password.")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"]
        if len(username) < 3 or len(username) > 30:
            return render_template("register.html",
                message="Error: Username length must be between 3 and 30 characters.")

        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if len(password1) < 3 or len(password1) > 30:
            return render_template("register.html",
                message="Error: Password length must be between 3 and 30 characters.")
        if password1 != password2:
            return render_template("register.html", message="Error: Passwords do not match.")

        role = request.form["role"]
        if role not in ("1", "2"):
            return render_template("register.html", message="Error: Unknown role.")
        if not users.register(username, password1, role):
            return render_template("register.html",
                message="Error: Registering new account failed.")
        return redirect("/")

@app.route("/all", methods=["GET", "POST"])
def show_all():
    return render_template("all.html", rides=rides.fetch_rides())

@app.route("/new", methods=["GET", "POST"])
def new_ride():
    users.require_role(2)
    if request.method == "GET":
        return render_template("new.html")

    if request.method == "POST":
        users.check_csrf()
        name = request.form["name"]
        if len(name) < 1 or len(name) > 30:
            return render_template("new.html",
                message="Error: Name length must be between 1 and 30 characters.")

        description = request.form["description"]
        if len(description) > 1000:
            return render_template("new.html",
                message="Error: Description length must be under 1000 characters.")

        location_id = request.form["location_id"]
        material_id = request.form["material_id"]
        drop_id = request.form["drop_id"]

        ride_id = rides.new_ride(name, description, location_id, material_id, drop_id)

        return redirect("/ride/"+str(ride_id))

@app.route("/ride/<int:ride_id>")
def show_ride(ride_id):
    data = rides.fetch_ride_data(ride_id)

    return render_template("ride.html", id=ride_id, name=data[0], description=data[1],\
                            location=data[2], material=data[3], drop=data[4])
