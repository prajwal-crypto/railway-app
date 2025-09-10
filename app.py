import requests
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "rail_secret"

USER = {"username": "admin", "password": "rail123"}

API_KEY = "YOUR_API_KEY"
API_URL = "https://api.railradar.in/trains-between"  # example

routes = {
    "mysuru": "MYS",
    "mangaluru": "MAQ",
    "hassan": "HAS",
    "coimbatore": "CBE",
    "tumkur": "TK"
}

@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        if (request.form["username"], request.form["password"]) == (USER["username"], USER["password"]):
            session["user"] = USER["username"]
            return redirect(url_for("search"))
        error = "Invalid credentials!"
    return render_template("login.html", error=error)

@app.route("/search", methods=["GET", "POST"])
def search():
    if "user" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        frm = request.form["from"].lower()
        to = request.form["to"].lower()
        src = routes.get(frm)
        dst = routes.get(to)
        if not src or not dst:
            return render_template("search.html", error="Unsupported route", routes=routes.keys())
        resp = requests.get(API_URL, params={"from": src, "to": dst, "apikey": API_KEY})
        trains = resp.json().get("trains", [])
        session["trains"] = trains
        return render_template("results.html", trains=trains)
    return render_template("search.html", routes=routes.keys())

@app.route("/select/<int:train_index>")
def select(train_index):
    trains = session.get("trains", [])
    if not trains or train_index >= len(trains):
        return redirect(url_for("search"))
    session["selected"] = trains[train_index]
    return render_template("select.html", train=trains[train_index])

@app.route("/ticket")
def ticket():
    if "selected" not in session:
        return redirect(url_for("search"))
    return render_template("ticket.html", train=session["selected"])

if __name__ == "__main__":
    app.run(debug=True)

