from flask import Flask, render_template, url_for, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")


#POST METHOD FORM

@app.route("/add-book", methods = ['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        return f"""
            Title: {request.form['title']} 
            Author: {request.form['author']} 
            Fiction or Not: {request.form['fiction-or-not']} 
            To Read or Read: {request.form['to-read-or-read']} 
        """

    return render_template("add-book.html")


if __name__ == "__main__":
    app.run(debug=True)
