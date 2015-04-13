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


Type `GET / HTTP/1.0` and press enter twice. You should see it respond with 'Hello World':


You just successfully connected to a Webserver via the HTTP-Protocol and requested (`GET`) a resource (`/`) over it. Congrats!


**What just happened?**

HTTP is a simple text-based Client-Server-Request-Response-Protocol. A Server waits for connections by clients, which then send a request and receive a response for it. A request always has the same format `VERB RESOURCE PROTOCOL/VERSION` – in our case `GET` is the verb, `/` the resource and we are using the protocol `HTTP` at Version `1.0`.

The request ends with an empty line, which signals the server it can start responding. A response also always has the same structure: `PROTOCOL/VERSION STATUSCODE STATUSNAME`, in our case respectively `HTTP`, `1.1`, `200` and `OK`. After a line-break, the server send us some headers. A header has a key-word and a value, separated by a colon (`:`). There is one header per line. Then follows another empty line, and the resource content (also called *body*). In our case, the server informed us about the `Content-Length` among others and send us the content `Hello World`.

### We can also send headers






## Other topics to discover

Pick any of the following topics you are interested in understanding. Just follow the instructions to explore them, how they work and what they are used for.

### Virtual Hosts

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

For some of the tests to

###

## License

This work is licensed under the [Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License](http://creativecommons.org/licenses/by-nc-sa/3.0/). To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/ or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.