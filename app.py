from flask import Flask, render_template, request, redirect, url_for
import json
import os.path
#from werkzeug import secure_filename


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/your-url", methods=["GET", "POST"])
def your_url():
    if request.method == "POST":
        urls = {}
        
          
        if os.path.exists("urls.json"):
            with open("urls.json") as urls_file:
                urls = json.load(urls_file)

        if request.form["code"] in urls.keys():
            #flash("That short name has already been taken. Please select another name.")
            return redirect(url_for("home"))


        urls[request.form["code"]] = {"url":request.form["url"]}
        with open("urls.json","w") as url_file:
            json.dump(urls, url_file)
        return render_template("your_url.html", code=request.form["code"])
    else:
        return redirect(url_for("home"))
