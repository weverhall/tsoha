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
            return render_template("login.html", message="Error: Invalid credentials.")

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
            return render_template("register.html", 
                    message="Error: Passwords do not match.")

        role = request.form["role"]
        if role not in ("1", "2"):
            return render_template("register.html", message="Error: Unknown role.")
        if not users.register(username, password1, role):
            return render_template("register.html", message="Error: Username already exists.")
        return redirect("/")

@app.route("/all", methods=["GET", "POST"])
def show_all():
    if request.method == "GET":
        all = rides.fetch_all_rides()      
        return render_template("all.html", rides=all)

    if request.method == "POST":
        users.require_role(2)
        users.check_csrf()

        if "ride" in request.form:
            ride = request.form["ride"]
            rides.remove_ride(ride)

        return redirect("/all")

@app.route("/new", methods=["GET", "POST"])
def new_ride():
    users.require_role(2)
    if request.method == "GET":
        return render_template("new.html")

    if request.method == "POST":
        users.check_csrf()
        name = request.form["name"].strip()
        if len(name) < 1 or len(name) > 30:
            return render_template("new.html",
                    message="Error: Name length must be between 1 and 30 characters.")

        description = request.form["description"].strip()
        if len(description) > 1000:
            return render_template("new.html",
                    message="Error: Description length must be under 1000 characters.")

        location_id = request.form["location_id"]
        material_id = request.form["material_id"]
        drop_id = request.form["drop_id"]

        if rides.check_ride_name(name) is not None or rides.check_ride_name(name.lower()) is not None\
            or rides.check_ride_name(name.upper()) is not None or rides.check_ride_name(name.title()) is not None:
                return render_template("new.html", message="Error: Ride with that name already exists.")

        ride_id = rides.new_ride(name, description, location_id, material_id, drop_id)

        return redirect("/ride/"+str(ride_id))

@app.route("/ride/<int:ride_id>")
def show_ride(ride_id):
    data = rides.fetch_ride_data(ride_id)
    reviews = rides.fetch_ride_reviews(ride_id)
    average = rides.fetch_average_rating(ride_id)

    return render_template("ride.html", id=ride_id, name=data[0], description=data[1],\
            location=data[2], material=data[3], drop=data[4], reviews=reviews, average=average)

@app.route("/result", methods=["GET"])
def result():
    query = request.args["query"].strip()
    results = rides.search(query)

    return render_template("result.html", results=results, query=query)

@app.route("/review", methods=["POST"])
def review():
    users.require_role(1)
    users.check_csrf()

    stars = int(request.form["stars"])
    if stars < 1 or stars > 5:
        return render_template("index.html", 
                message="Error: Choose a rating between 1 and 5 stars.")

    content = request.form["content"].strip()
    if len(content) > 500:
        return render_template("index.html",
                message="Error: Review length must be under 500 characters.")
    if content == "":
        content = "I'm only leaving a rating."
    
    ride_id = request.form["ride_id"]

    rides.new_review(content, stars, users.user_id(), ride_id)

    return redirect("/ride/"+str(ride_id))

@app.route("/top", methods=["GET"])
def show_top():
    top = rides.fetch_top_averages()      
    return render_template("top.html", top=top)

@app.route("/reviews", methods=["GET", "POST"])
def show_reviews():
    if request.method == "GET":
        reviews = rides.fetch_all_reviews()      
        return render_template("reviews.html", reviews=reviews)

    if request.method == "POST":
        users.require_role(2)
        users.check_csrf()

        if "review" in request.form:
            review = request.form["review"]
            rides.remove_review(review)

        return redirect("/reviews")
