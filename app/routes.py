from flask import Blueprint, redirect, render_template, request, url_for

main = Blueprint("main", __name__)


@main.route("/")
def home():
    return render_template("index.html")


@main.route("/contributors")
def contributors():
    return render_template("contributors.html")


@main.route("/terms")
def terms():
    return render_template("terms.html")


@main.route("/privacy")
def privacy():
    return render_template("privacy.html")


@main.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        return redirect(url_for("main.contact"), code=303)

    return render_template("contact.html")


@main.route("/waitlist", methods=["GET", "POST"])
def waitlist():
    if request.method == "POST":
        return redirect(url_for("main.waitlist"), code=303)

    return render_template("waitlist.html")
