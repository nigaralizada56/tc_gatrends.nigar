"""
Author: Furkan Karakutuk
Created for Hype Google Trends Tool.
"""

from flask import Flask, request, send_file, redirect, url_for
from flask import session
from flask import render_template
from trends import get_trends, generate_key
from pathlib import Path


app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = generate_key(12)

home = str(Path.home())


@app.route("/", methods=["GET", "POST"])
def mode_page():
    last_inserted = ""
    if "keywords" not in session:
        session["keywords"] = []

    errors = ""
    if request.method == "POST":

        if request.form["keyword"] == None or request.form["keyword"] == "" and session["keywords"] == []:
            errors += "<p>Please enter the keyword.</p>\n"
        else:
            session["keywords"].append(request.form["keyword"])
            session["s_date"] = request.form["s_date"]
            session["e_date"] = request.form["e_date"]
            session.modified = True
            if request.form["action"] == "Get trends":
                # result = get_trends(session["keywords"], session["s_date"], session["e_date"])
                # panda = result[0].to_html(index_names=False)
                session.modified = True
                return redirect(url_for('result_page', keywords=session["keywords"], start_date=session["s_date"], end_date=session["e_date"]))
                session["keywords"].clear()

    if len(session["keywords"]) == 0:
        last_inserted = ""
    else:
        last_inserted = "Keywords so far: "
        for keyword in session["keywords"]:
            last_inserted += keyword + " "

    app.config["SECRET_KEY"] = generate_key(12)

    return render_template('index.html', last_inserted=last_inserted, errors=errors)


@app.route("/result", methods=['GET'])
def result_page():
    keywords = request.args.getlist("keywords")
    s_date = request.args.get("start_date")
    e_date = request.args.get("end_date")

    result = get_trends(keywords, s_date, e_date)
    panda = result.to_html(index_names=False)

    app.config["SECRET_KEY"] = generate_key(12)

    return render_template('result.html', data3=panda)


@app.route("/download", methods=['GET', 'POST'])
def download_file():
    return send_file(home, attachment_filename='trends_data.csv', as_attachment=True)



