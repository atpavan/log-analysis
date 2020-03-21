from flask import Flask, render_template
from newsdb import most_popular_articles, most_popular_authors, request_errors


app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
    return render_template("links.html")

@app.route("/top-articles", methods=["GET"])
def top_articles():
    
    return render_template("list.html", items=most_popular_articles())

@app.route("/top-authors", methods=["GET"])
def top_authors():
    
    return render_template("list.html", items=most_popular_authors())

@app.route("/failed-reqs", methods=["GET"])
def failed_reqs():

    return render_template("failed_reqs.html", items=request_errors())

if __name__ == "__main__":
    app.run(port=8000)
    
