from flask import render_template, request, redirect, url_for, flash, abort, session, jsonify, Blueprint
import json
import os.path
from werkzeug.utils import secure_filename


bp = Blueprint("urlabridge",__name__)


@bp.route("/")
def home():
    return render_template("home.html", codes=session.keys())

@bp.route("/your-url", methods=["GET","POST"])
def your_url():
    if request.method == "POST":
        urls = {}

        if os.path.exists("urls.json"):
            with open("urls.json") as urls_file:
                urls = json.load(urls_file)

        if request.form["code"] in urls.keys():
            flash("That abridge name has already been taken. Please select another name.")
            return redirect(url_for("urlabridge"))

        if "url" in request.form.keys():
            urls[request.form["code"]] = {"url":request.form["url"]}
        else:
            f = request.files["file"]
            full_name = request.form["code"] + secure_filename(f.filename)
            f.save("/home/pablo/Dev/py/url_abridge/urlabridge/static/user_data/" + full_name)
            urls[request.form["code"]] = {"file":full_name}


        with open("urls.json","w") as url_file:
            json.dump(urls, url_file)
            session[request.form["code"]] = True
        return render_template("your_url.html", code=request.form["code"])
    else:
        return redirect(url_for("urlabridge"))


@bp.route("/<string:code>")
def redirect_to_url(code):
    if os.path.exists("urls.json"):
        with open("urls.json") as urls_file:
            urls = json.load(urls_file)
            if code in urls.keys():
                if "url" in urls[code].keys():
                    return redirect(urls[code]["url"])
                else:
                    return redirect(url_for("static", filename="user_data/" + urls[code]["file"]))
    return abort(404)


@bp.errorhandler(404)
def page_not_found(error):
    return render_template("page_not_found.html"), 404


@bp.route('/api')
def session_api():
    return jsonify(list(session.keys()))

