from flask import Flask, request, make_response, session
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/", subdomain="blog")
def hello_blog():
    return "Welcome to my awesome blog!"


@app.route('/public_cookie')
def set_name():
    name = request.args.get("name")
    resp = make_response("Name accepted")
    resp.set_cookie("name", name)
    return resp

@app.route('/secret_cookie', methods=['POST', 'GET'])
def secret_cookie():
    if request.method == 'POST':
        session['secret'] = request.form['secret']

    return "The serect is '{}'".format(session.get('secret', ''))


if __name__ == "__main__":
    app.secret_key = "complicatedHash"
    app.run(debug=True, host="0.0.0.0", port=8080)
