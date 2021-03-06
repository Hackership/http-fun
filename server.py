from gevent.wsgi import WSGIServer
from flask import Flask, request, make_response, session, abort, redirect, Response
app = Flask(__name__)

from datetime import datetime, timedelta

from gevent import monkey
monkey.patch_time()

import json
import os
import time


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


@app.route('/resource_manager', methods=['GET', 'POST', 'PUT'])
def resource_manager():
    if "resources" not in session:
        session["resources"] = {"car": "mustang",
                                "cake": "cheesecake",
                                "drink": "zombie"}
    method = request.method
    if request.method == 'PUT':
        session['resources'] = request.form

    elif request.method == 'POST':
        for key, value in request.form.iteritems():
            session['resources'][key] = value

    return "Your current resources:\n   {}".format(
                "\n   ".join(map(lambda x: ": ".join(x),
                    session["resources"].items())))


@app.route('/resource_manager/<item>', methods=['POST', 'PUT', 'GET', 'DELETE'])
def resource_item_manager(item):
    if "resources" not in session:
        session["resources"] = {}

    if request.method == 'DELETE':
        del session['resources'][item]
    elif request.method == "PUT":
        session['resources'][item] = request.data
    return session['resources'].get(item, "")

# Status code lol cats
@app.route('/status/<int:code>')
def status_codes(code):
    resp = make_response('<img src="http://httpcats.herokuapp.com/{}" />'.format(code), code)
    if code in [301, 302, 307]:
        resp.location = "http://www.hackership.org/"
    return resp


# Redirects
# Status code lol cats
@app.route('/redirect/simple')
def redirect_simple():
    return redirect("/")


@app.route('/redirect/bounce')
def redirect_bounce():
    return redirect('/redirect/back')


@app.route('/redirect/back')
def redirect_back():
    return redirect('/redirect/bounce')


@app.route('/redirect/permanent')
def redirect_permanent():
    return redirect('/', 301)


@app.route('/redirect/old/<path:path>')
@app.route('/redirect/old')
def redirect_old(path=''):
    return redirect('http://www.hackership.org/' + path, 301)


@app.route('/redirect/restricted')
def redirect_restricted():
    if not request.args.get("accepted"):
        return redirect('/redirect/login', 303)
    return "Access granted!"


@app.route('/redirect/login', methods=["POST", "GET"])
def redirect_login():
    if request.method == "POST":
        return redirect('/redirect/restricted?accepted=1', 303)
    return "You need to POST 'username=test' to this page to login"

# HTTP Auth

from functools import wraps
import authdigest
import flask

class FlaskRealmDigestDB(authdigest.RealmDigestDb):
    def requires_auth(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            request = flask.request
            if not self.isAuthenticated(request):
                return self.challenge()

            return f(*args, **kwargs)

        return decorated


authDB = FlaskRealmDigestDB('Example Auth')
authDB.addUser('user', 'password')


@app.route('/auth/basic')
def auth_restricted():
    if not request.headers.get("Authorization"):
        abort(401)
    return "Access Granted"


@app.route("/auth/digest")
@authDB.requires_auth
def auth_digest():
    return "Yay, you are {}".format(request.authorization.username)


# Content negotiation

@app.route("/content/simple")
def content_simple():
    result = dict(hello="world", peter='cat')
    mtype = request.accept_mimetypes.best
    if mtype.endswith("json"):
        resp = make_response(json.dumps(result))
        resp.content_type = "application/json"
    else:
        resp = make_response("\n".join([": ".join(x) for x in result.iteritems()]))
    return resp


import cStringIO, gzip

@app.route("/content/compressed")
def content_compressed():
    response = content_simple()
    if response.status_code != 200 or 'Content-Encoding' in response.headers\
        or "gzip" not in request.headers.get('Accept-Encoding', '').lower():
        return response

    gzip_buffer = cStringIO.StringIO()
    gzip_file = gzip.GzipFile(mode='wb', compresslevel=6, fileobj=gzip_buffer)
    gzip_file.write(response.data)
    gzip_file.close()
    response.data = gzip_buffer.getvalue()
    if not request.args.get("disableContentHeader"):
        response.headers['Content-Encoding'] = 'gzip'
    response.headers['Content-Length'] = str(len(response.data))
    return response

# User Agent detection

@app.route("/useragent")
def useragent():
    agent = request.headers.get("User-Agent", "").lower()
    for ua in ["googlebot", "yandexbot", "bingbot"]:
        if ua in agent:
            return "Hello {} crawler. Nice to detect you".format(ua)

    if 'mobil' in agent:
        return "Mobile optimised website"

    return "Normal website"


# Cache behaviour
@app.route("/cache/simple")
def cache_simple():
    resp = make_response("Simple Cache-able Response")
    resp.headers["Cache-Control"] = "public, max-age=20"
    return resp

STARTTIME = datetime.now()
EXPIRES = STARTTIME + timedelta(days=364)


@app.route("/cache/expire")
def cache_expire():
    resp = make_response("Simple expering Response")
    resp.headers["Cache-Control"] = "public, max-age={}".format( (EXPIRES - datetime.now()).seconds )
    resp.headers["Expires"] = EXPIRES.strftime("%a, %d-%b-%Y %H:%M:%S GMT")
    return resp


@app.route('/cache/etag')
def cache_etag():
    if request.headers.get("If-None-Match") == '1234567-etd':
        return make_response("", 304)
    resp = make_response("Simple tagged Response")
    resp.headers["Cache-Control"] = "public"
    resp.headers["Etag"] = "1234567-etd"
    return resp

CHAT = []

@app.route('/chat/messages', methods=["GET"])
def chat_messages_get():
    global CHAT
    return "- " + "<br>\n- ".join(CHAT[-10:])


@app.route('/chat/messages', methods=["POST"])
def chat_messages_post():
    global CHAT
    if not request.form.get("message"):
        abort(400, "Please provide a message")
    CHAT.append(request.form.get("message"))
    if len(CHAT) > 10:
        CHAT[:] = CHAT[-10:]
    return ""

@app.route('/chat')
def chat():
    return """<html><head><title>Minimal ajax example</title><head>
<body>
<div id="messages">Loading ...</div>
<div>
<form id="form"><input type="text" id="input"/>
     <button type="submit">Send</button>
</form>
</div>
<script src="http://code.jquery.com/jquery-2.1.3.min.js"></script>
<script type="text/javascript">
$(function(){
    $("#form").submit(function(evt){
        evt.preventDefault();
        var content = $("#input").val().trim();
        if (content.length){
            $.post("/chat/messages", {message: content});
        }

        $("#input").val("");
    });

    setInterval(function(){
        $("#messages").load("/chat/messages");
    }, 1000);
});
</script>
</body>
</html>
"""

# CORS enabled messages

@app.route('/chat/allowed-messages', methods=["GET"])
def chat_messages_cors():
    if not request.headers.get("Origin", False) == "http://www.hackership.org":
        abort(401)
    response = make_response(chat_messages_get())
    response.headers['Access-Control-Allow-Origin'] = "http://www.hackership.org"
    return response


# Streaming

@app.route("/stream/time", methods=["GET"])
def stream_time():
    def events():
        for x in xrange(10):
            yield "{}\n".format(datetime.now().isoformat())
            time.sleep(1)  # an artificial delay
    return Response(events(), content_type='text/event-stream')


@app.route("/stream/chat", methods=["GET"])
def stream_chat():
    def events():
        global CHAT
        chat = CHAT[:]
        updates = 0
        yield "{}\n".format(json.dumps(CHAT))
        while updates < 5:
            if chat != CHAT:
                yield "{}\n".format(json.dumps(CHAT))
                chat = CHAT[:]
                updates += 1
            time.sleep(1)  # an artificial delay
    return Response(events(), content_type='text/event-stream')



## General Configuration, needed for cookies

app.secret_key = "complicatedHash"

if __name__ == "__main__":
    config = dict(port=8080, debug=True)
    if os.getenv('production'):
        config = dict(host="0.0.0.0", port=5000)

    # app.run(**config)
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()

