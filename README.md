# http-fun

Let's have some fun exploring the HTTP Protocol.

## Preamble

This interactive learning material assumes you are familiar with the command line (Shell/Terminal) and have done some web server programming before. You don't need to be no expert on either of them, but if you hear about them the first time, you will struggle


## Installation Instructions

You will need:

 - Python
 - httpie
 - (recent) Firefox Browser

### Installing Python

You will need Python and PIP. If you don't have Python yet, download and install the latest version from here (pip is included in it):

   http://python.org/download/


*Note*: On Windows, you’ll want to add Python to your path, so it can be found by other programs. To do this, navigate to your installation directory (`C:\Python33\`), open the `Tools`, then `Scripts` folders, and run the `win_add2path.py` file by double clicking on it.


### Installing httpie

We now need to install [httpie](https://pypi.python.org/pypi/httpie/0.9.2) using pip on the commandline by typing:

    pip install --upgrade httpie

And we are ready to go.

### Installing Firefox

Technically this should all also work with Chrome, Chromium and Safari, but all are slightly different in where features are located. This guide will only directly show and explain these features using Firefox. Also, you should just have a browser which is actually free, so ...

   [getfirefox.com](http://www.getfirefox.com)


## Let the fun begin

### First steps with telnet

Open a [terminal/commandline/shell/cmd.exe](http://opentechschool.github.io/python-beginners/en/getting_started.html#opening-a-console-on-mac-os-x) and start telnet

*Note*: If you are [running your own server](#Running your own server), use `localhost:5000` instead of `http-fun.hackership.org`.

    telnet http-fun.hackership.org

You will see it connect and waiting for input.

![](images/waiting-telnet.png?raw=true)


Type `GET / HTTP/1.0` and press enter twice. You should see it respond with 'Hello World':

![](images/hello-world.png?raw=true)

You just successfully connected to a Webserver via the HTTP-Protocol and requested (`GET`) a resource (`/`) over it. Congrats!


**What just happened?**

HTTP is a simple text-based Client-Server-Request-Response-Protocol. A Server waits for connections by clients, which then send a request and receive a response for it. A request always has the same format `VERB RESOURCE PROTOCOL/VERSION` – in our case `GET` is the verb, `/` the resource and we are using the protocol `HTTP` at Version `1.0`.

The request ends with an empty line, which signals the server it can start responding. A response also always has the same structure: `PROTOCOL/VERSION STATUSCODE STATUSNAME`, in our case respectively `HTTP`, `1.1`, `200` and `OK`. After a line-break, the server send us some headers. A header has a key-word and a value, separated by a colon (`:`). There is one header per line. Then follows another empty line, and the resource content (also called *body*). In our case, the server informed us about the `Content-Length` among others and send us the content `Hello World`.

### We can also send headers

Let's reopen telnet and do a GET-Request but this time, instead of doing a double empty line, add another line after the first as follows:

    GET / HTTP/1.0
    User-Agent: Telnet

![](images/with-user-agent.png?raw=true)

You've just successfully send your first header to the server, telling them that you are using the _telnet_ to connect (as the "browser"). As you can see, the format for sending headers is exactly the same as for receiving them, a keyword, a colon (`:`) and the value. Multiple headers separated by a line-break. Let's do it again, this time we identify as 'Terminal' and see what happens.

    GET / HTTP/1.0
    Host: example.org
    User-Agent: Terminal

You will see

![](images/hello-terminal.png?raw=true)


### What just happened?

All headers you specify are send to the server. The server can then decide what to do with them. In this specific case, the server is set up to send you different output when you tell it the User-Agent was "Terminal". If you do, it sends you some awesome ASCII Art.

This is the basic principle of how headers work. When you send them to the server, the server might (or might not) react differently depending on them.

## Moving to httpie

Typing this up every time is kinda dreadfull and mostly an excerise for you to understand what goes on under the hood. In order to make the typing a little easier, we will use the awesome [httpie](https://pypi.python.org/pypi/httpie/0.9.2) command line http-debugger from here on up.

Let's do a simple request with it again, type `http -v http://http-fun.hackership.org/`:

![](images/httpie-hello.png?raw=true)

Httpie formats the output the same we just did (request, headers + body then the response, headers and body), but gives us pretty syntax highlighting and helps us in doing the right headers and formatting of those.

Note: Per default `httpie` doesn't show our request (nor headers). Thus we are running it with `-v` to switch on verbose output.

Let's fake the User-Agent again. We can do that by adding our headers at the end of the command like this:

    http -v http://http-fun.hackership.org/ User-Agent:Terminal

And we are back at seeing our terminal output again.

## hmmm, cookies

Each and every header has its function and implementing HTTP fully means that you have act in a certain way when you encounter certain headers. Of course, as with many specs, not all servers support all features and you might encounter one or the other feature that doesn't work as expected.

One very important feature of HTTP are "cookies". You have probably heard about cookies before, probably in the context of privacy. So let's see what that is all about.

To enable cookies in `httpie`, we need to specify a session for it. We do that by giving it the `--session cookie_test` parameter. Let's see what happens, when we go to the `/cookie/set`-path of our server:

    http -v --session cookie_test http://http-fun.hackership.org/cookie/set?name=test

In your response, you'll find the header:

    Set-Cookie: name=test; Path=/

This tells our client, that the server set a cookie with the name 'name' to the value 'test'. Let's try it again, this time set the parameter 'name' to something else. Go ahead, I'll wait. Don't forget to set the `--session cookie_test` .

### Cookie jar

You might have noticed, that in the second request, our client has added the header `Cookie: name=test` to the request. Wohaa. What just happened?

Whenever the server sends a `Set-Cookie` header our client understand that it should store this key-value pair and whenever we send to a request to this server matching the given `Path` (in this case, everything), send it back out there. Httpie stores this information in the `--session` (you sometimes also find this named a 'Cookie Jar').

HTTP by itself is a stateless protocol. Meaning that we only request on resource and get a resource. The server doesn't know whether that request is part of a bigger range of requests, the context it might be run in or anything else you don't specificly provide. Cookies allow the server to identify a request or set additional information.

A very commonly use case for this is, to keep the login information of a user around. As the client is sending back the information every time, the server can use it to identify you as you. Let's play around with this a little.

Here is a page, that you can only request, once you 'logged in' into the system, try accessing it with httpie:

    http -v --session cookie_test http://http-fun.hackership.org/cookie/secret-room

As you can see, the server told us, we aren't authorized to access this page. Let's try to login:


    http -v --session cookie_test http://http-fun.hackership.org/cookie/login?username=hackership&password=password

The server accepted our request and told us we are authorized.

![](images/authorized.png?raw=true)

We can see in the headers, that it set the cookie "username" to "hackership". Well, let's try to connect to the secrect-room again and see what happens:

    http -v --session cookie_test http://http-fun.hackership.org/cookie/secret-room

Holy kewl, we are part of the club now! The server identifies us just by using the cookie. Don't want to believe me? Run the same command again but without the `--session cookie_test`.

### Secure Cookies

This is all cool, but if you think about it, this also quite easy to hack. Just figure out the username, add it as the set-cookie header and you are imposing as someone else:

    http -v http://http-fun.hackership.org/cookie/secret-room Cookie:username=imposter

![](images/imposter.png?raw=true)

Well. That's not really what we want – or can allow for that matter. This is why most modern web-frameworks have a mechanic called "session"-handeling. The specific implementions differ, but in general there are two approaches:

**Encrypted Cookies**:
Instead of sending plaintext, all session-information is encrypted into one long string, which is being encrypted before it sends it on the line – this is called a 'cyphertext'. When the client sends back the ciphertext, the server is able to decrypt and thus, restore the session.

If someone wants to impose another persons session now (or fiddle with their own), they need the encryption key or the server won't accept the content they send.

**Session IDs**:
Instead of sending the entire session over the line (but encrypted), a lot of platforms store the actual content of the session on a third party storage system (typically a database) and only sends over an identifier to find and look up that session. The benefits to this over the encrypted cookie is that the cookie has a deterministic length independent of the session length and no one can mess with the session unless they connect to the database. The drawback, of course, is that you need a a database.

We have a lightweight server without a database, so it uses the first method to provide secure sessions. Let's check it out. Try to connect to `/session/secret-room` (including your current session):


    http -v --session cookie_test http://http-fun.hackership.org/session/secret-room

Looks, like we have login first. Well, let's do that. This time against the `/session/login`-resource.

    http -v --session cookie_test http://http-fun.hackership.org/cookie/login?username=hackership&password=password

Can you spot the `Set-Cookie`-header in the response? Well, that looks like a bunch of garbage, doesn't it? But we know it is the value of 'session'. Let's see if we can connect now:

    http -v --session cookie_test http://http-fun.hackership.org/session/secret-room

Looks like we can:

![](images/login-time.png?raw=true)

## Cookies and Privacy

But what is this? It knows when I logged in? Well, yes. The server can store anything in the session or the database they want. And with a cookie hidden from you, you don't know what that is. Our server here, just also put in the timestamp, when you logged in, but can literally be anything.


Through cookies, which the browser is sending _with every request_ to the server, the server can identify the request and with that ultimately you. Even when you logged out, you might still have a session lingering around. And as cookies are transparent to the user, you don't know when or for how long a server might request the client to follow you.

This includes all iframe-requests, like for facebook like-buttons. Whenever there is a like-button on a website, the browser connects to facebook and sends over the cookies, they've previously set along-side which site is currently being visited. You don't even need to be logged in for facebook to know that you've just looked at this news article about how the NSA is spying on all of us.

On the other side, cookies are pretty much essential to our way of interacting with the internet today. Turning off cookies, means not being able to participate in the majority of online platforms for discussions, discourse or even be able to comment on youtube videos. That's not a solution either.

## HTTP URL Parameters

We briefly touched the URL and it's parameters but we haven't really talked about this. I also quickly skimmed over the Status-Codes and the HTTP-Verbs, but both of them you can learn more about later down. But before you start looking into that, I want to cover URLs and "request parameters".

When we connected to the server and asked for a Resource we were using this weird `/something?x=1`-notation. This is called the resource-path and is part of the URL (Uniform resource locator). The features and caveats of URL is a tutorial by itself, but what you have to know is that this path is how the server identifies, which "resource" you are trying to access.

It is generally split into two parts, separated by (the first) `?`: the path and parameters. The Path has to start with a a slash (`/`), parameters are optional. While the path dictates which resource to load, the paramter are generally passed to the execution of that resource access. Parameters come in the form of `key=value`-pairs, separated by an ampersand (`&`). Which parameters are given and the effects they have are totally resource-implementation-specific and are not dictated by the HTTP specificiation.

In our examples above, when logging in, we are using url-parameters to tell the `login-`resource what username and password we have.


## Other topics to discover

Pick any of the following topics you are interested in understanding. Just follow the instructions to explore them, how they work and what they are used for.

### HTTP Verbs

We haven't talked much about the `VERB` in the HTTP-Protocol yet. It essentially tells the server the way you want to access a resource. This often means, that for different "verbs", the server executes different parts of the progamme.

HTTP, in its first version, only knows about `GET`, `POST` and `HEAD`, the second version (1.1) added `OPTIONS`, `PUT`, `DELETE`, `TRACE` and `CONNECT`. There are more extensions to the protocol (for example WebDav) but for this document, we will focus on the main foure `GET`, `POST`, `PUT`, `DELETE` and briefly cover `OPTIONS`, `HEAD` and the later added `PATCH` – not all of which are supported by all servers.

On its lowest basis HTTP is implemented under the CRUD-Principles of accessing resources. This essentially means, that everything is a resource and the main ways to connect to them is by either reading it (`GET`), creating a resource (`POST`), writing to the resource (`PUT`) or deleting it (`DELETE`).

#### An example

Let's take our simple `/resource_manager` for example, which lists things I own in various categories. When we try to read its contents, we query it with a `GET` method:


    http -v --session resource_test http://http-fun.hackership.org/resource_manager


I can also query one item specifically:

    http -v --session resource_test http://http-fun.hackership.org/resource_manager/cake

Now, I can add new items, by posting to the resource manager and add a new items using the 'POST' method

    http -v --form --session resource_test http://http-fun.hackership.org/resource_manager dog=jake

As you can see, when we add parameters after a space in the commandline, httpie understands that we want to send a body and automatically switches to the "POST"-method. By setting the `--form`-flag, we tell it to the use "key=value"-form notation. Other notations is `--json` (but our resource manager doesn't understand that).

Now, if we look at the output, we can see, that we created a new resource. We can also overwrite the resource by sending a `PUT` to the newly created resource:

    echo 'jake' | http -v --session resource_test PUT http://http-fun.hackership.org/resource_manager/dog

Or delete the resource:

    http -v --session resource_test DELETE http://http-fun.hackership.org/resource_manager/dog

It is also common practice that a PUT on the outer object resets the entire resource. Our server has that implementation, too:

    http -v --session resource_test PUT http://http-fun.hackership.org/resource_manager/ dog=jake bag=tote

These are the basic ways to interact with http-resources. And although it is rather simple (four main methods), it is an incredibly powerful system and the basis of most [Restful APIs](#restful-api-design)


#### Extra Verbs

We have two more verbs to briefly look into: `HEAD` and `OPTIONS`.

**Options** essentially tells you which verbs are available on this resource. You can find it in the `Allow`-header.

Want to see an example?

    http -v --session resource_test OPTIONS http://http-fun.hackership.org/resource_manager/


**HEAD** on the other hand, executes a `GET`-Request on the resource but instead of returning the entire content, only returns the headers.

Want to see an example?

    http -v --session resource_test HEAD http://http-fun.hackership.org/resource_manager/


### HTTP Status Codes


### HTTP-Redirects

### Basic Authentication

### Content Negotiation

### User Agent Tricks (SEO optimised page serving)

### Caching

### AJAX

### Cross Origin Request (CORS)

### Cross-Site-Scripting (CSRF-Tokens)

### Restful (API) Design

### HTTP Streaming

### Keep-Alive

### Long-Polling/Comet

### Websockets


## Honourable mentions

### Do Not Track

### HTTPS (Certificate nightmare)



## Appendix

### Running your own server

For some of the tests to work properly, you need to host the server yourself. You will need a proper virtualenv (on python 2.7) on your system, then you can get going with this:

    virtualenv .
    ./bin/pip install -r requirements
    ./bin/python server.py

And you can run the tests against your local instance on port 8080:

    ./bin/http -v http://localhost:8080/

###

## License

This work is licensed under the [Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License](http://creativecommons.org/licenses/by-nc-sa/3.0/). To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/ or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.