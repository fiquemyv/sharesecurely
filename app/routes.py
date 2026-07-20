from flask import Blueprint, render_template

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


@main.route("/contact")
def contact():
    return render_template("contact.html")


@main.route("/waitlist")
def waitlist():
    return render_template("waitlist.html")