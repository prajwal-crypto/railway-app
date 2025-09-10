from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "secret123"

# Dummy login credentials
USER_CREDENTIALS = {"username": "admin", "password": "1234"}

# Dummy train data
TRAINS = {
    ("Bengaluru", "Mysuru"): [
        {"no": "56264", "name": "Bangalore City - Mysore Night Queen Passenger", "dep": "21:00", "arr": "23:55", "status": "On Time", "pf": "3"},
        {"no": "16021", "name": "Kaveri Express", "dep": "22:30", "arr": "01:15", "status": "On Time", "pf": "4"},
    ],
    ("Bengaluru", "Mangaluru"): [
        {"no": "16511", "name": "KSR Bengaluru - Kannur Express", "dep": "21:45", "arr": "06:50", "status": "On Time", "pf": "3"},
        {"no": "16585", "name": "SMVT Bengaluru - Murdeshwar Express", "dep": "20:02", "arr": "08:13", "status": "On Time", "pf": "1"},
    ],
    ("Bengaluru", "Hassan"): [
        {"no": "16511", "name": "KSR Bengaluru - Kannur Express", "dep": "21:45", "arr": "00:30", "status": "On Time", "pf": "3"},
        {"no": "16585", "name": "SMVT Bengaluru - Murdeshwar Express", "dep": "20:02", "arr": "01:55", "status": "On Time", "pf": "1"},
        {"no": "11311", "name": "Solapur - Hassan Express", "dep": "05:58", "arr": "10:56", "status": "Delayed 7m", "pf": "4"},
    ],
    ("Bengaluru", "Tumkur"): [
        {"no": "12613", "name": "SBC - Tumkur Passenger", "dep": "06:30", "arr": "07:45", "status": "On Time", "pf": "2"},
        {"no": "17325", "name": "Vishwamanava Express", "dep": "14:00", "arr": "15:10", "status": "On Time", "pf": "5"},
    ],
    ("Bengaluru", "Coimbatore"): [
        {"no": "12677", "name": "KSR Bengaluru - Coimbatore Intercity Express", "dep": "07:15", "arr": "13:10", "status": "On Time", "pf": "6"},
        {"no": "11013", "name": "Coimbatore Express", "dep": "22:00", "arr": "06:15", "status": "On Time", "pf": "1"},
    ]
}

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == USER_CREDENTIALS["username"] and password == USER_CREDENTIALS["password"]:
            session["user"] = username
            return redirect(url_for("search"))
        else:
            return render_template("login.html", error="Invalid credentials!")
    return render_template("login.html", error=None)

@app.route("/search", methods=["GET", "POST"])
def search():
    if "user" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        from_station = request.form["from_station"]
        to_station = request.form["to_station"]
        session["from_station"] = from_station
        session["to_station"] = to_station
        return redirect(url_for("result"))
    return render_template("search.html")

@app.route("/result")
def result():
    from_station = session.get("from_station")
    to_station = session.get("to_station")
    trains = TRAINS.get((from_station, to_station), [])
    return render_template("result.html", trains=trains, from_station=from_station, to_station=to_station)

@app.route("/select/<train_no>")
def select(train_no):
    from_station = session.get("from_station")
    to_station = session.get("to_station")
    trains = TRAINS.get((from_station, to_station), [])
    train = next((t for t in trains if t["no"] == train_no), None)
    session["selected_train"] = train
    return render_template("select.html", train=train)

@app.route("/ticket", methods=["POST"])
def ticket():
    passenger = request.form["passenger"]
    train = session.get("selected_train")
    from_station = session.get("from_station")
    to_station = session.get("to_station")
    return render_template("ticket.html", passenger=passenger, train=train, from_station=from_station, to_station=to_station)

if __name__ == "__main__":
    app.run(debug=True)
