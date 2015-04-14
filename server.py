from flask import Flask, request, make_response, session, abort
app = Flask(__name__)

from datetime import datetime


ASCII_HELLO = """
.................##...##..######..##.......####....####...##...##..######..........######...####..................
.................##...##..##......##......##..##..##..##..###.###..##................##....##..##.................
.................##.#.##..####....##......##......##..##..##.#.##..####..............##....##..##.................
.................#######..##......##......##..##..##..##..##...##..##................##....##..##.................
..................##.##...######..######...####....####...##...##..######............##.....####..................
..................................................................................................................
.........##..##...####....####...##..##..######..#####....####...##..##..######..#####.....##.....####..........  
.........##..##..##..##..##..##..##.##...##......##..##..##......##..##....##....##..##....##....##.............  
.........######..######..##......####....####....#####....####...######....##....#####......#.....####..........  
.........##..##..##..##..##..##..##.##...##......##..##......##..##..##....##....##..................##.........  
.........##..##..##..##...####...##..##..######..##..##...####...##..##..######..##...............####..........  
................................................................................................................  
.................##..##..######..######..#####...........######..##..##..##..##.................................  
.................##..##....##......##....##..##..........##......##..##..###.##.................................  
.................######....##......##....#####...........####....##..##..##.###.................................  
.................##..##....##......##....##..............##......##..##..##..##.................................  
.................##..##....##......##....##..............##.......####...##..##.................................  
................................................................................................................  
"""

### Hello world, Chapter 1

@app.route("/")
def hello():
    if request.headers.get("User-Agent") == "Terminal":
        return ASCII_HELLO

    return "Hello World!"


### Playing with cookies
### In order of appereance

@app.route('/cookie/set')
def cookies_set():
    name = request.args.get("name", "Test")
    resp = make_response("Name accepted")
    resp.set_cookie("name", name)
    return resp


@app.route('/cookie/secret-room')
def cookies_secret_room():
    name = request.cookies.get("username", False)

    if not name:
        abort(401)

    resp = make_response("Hello {}".format(name))
    return resp


@app.route('/cookie/login')
def cookies_login():
    name = request.args.get("username", False)
    password = request.args.get("password", False)
    print name, password
    if not password == "password" or not name:
        abort(401)

    resp = make_response("You are now authorized")
    resp.set_cookie("username", name)
    return resp

### Sessions

@app.route("/session/secret-room")
def session_secret():
    name = session.get("username", False)
    if not name:
        abort(401)

    resp = make_response("""Hello {},
You logged in at {}
""".format(name, session.get("login-time")))
    return resp


@app.route('/session/login')
def session_login():
    name = request.args.get("username", False)
    password = request.args.get("password", False)
    print name, password
    if not password == "password" or not name:
        abort(401)

    resp = make_response("You are now authorized")
    session['username'] = name
    session['login-time'] = datetime.now()
    return resp


if __name__ == "__main__":
    app.secret_key = "complicatedHash"
    app.run(debug=True, host="0.0.0.0", port=8080)
