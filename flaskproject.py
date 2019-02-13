from flask import Flask

app = Flask(__name__)
app.debug = True

@app.route("/")
def greeting():
    return "<h1 style='color:green'>Hello World</h1>"

@app.route('/<c1>/<c2>/<url>')
def show_user_profile(c1, c2, url):
    # show the user profile for that user
    return f'{c1}, {c2}, {url}'

@app.route('/test')
def test():
    urls_to_pics('test')
    return url

if __name__ == "__main__":
    app.run(host='0.0.0.0')
