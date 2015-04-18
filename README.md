# http-fun

Let's have some fun exploring the HTTP Protocol. HTTP stands for Hypertext Transport Protocol and is the way browsers talk to server, fetch websites, images and everything they need. It is further more often use as the base protocol between public APIs (like twitter or Facebooks) and to serve for mobile clients.

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

```console
pip install --upgrade httpie
```

And we are ready to go.

### Installing Firefox

Technically this should all also work with Chrome, Chromium and Safari, but all are slightly different in where features are located. This guide will only directly show and explain these features using Firefox. Also, you should just have a browser which is actually free, so ... [getfirefox.com](http://www.getfirefox.com)


## Let the fun begin

### First steps with telnet

Open a [terminal/commandline/shell/cmd.exe](http://opentechschool.github.io/python-beginners/en/getting_started.html#opening-a-console-on-mac-os-x) and start telnet

```console
telnet http-fun.hackership.org
```

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

```HTTP
GET / HTTP/1.0
User-Agent: Telnet
```

![](images/with-user-agent.png?raw=true)

You've just successfully send your first header to the server, telling them that you are using the _telnet_ to connect (as the "browser"). As you can see, the format for sending headers is exactly the same as for receiving them, a keyword, a colon (`:`) and the value. Multiple headers separated by a line-break. Let's do it again, this time we identify as 'Terminal' and see what happens.

```HTTP
GET / HTTP/1.0
Host: example.org
User-Agent: Terminal
```

You will see

![](images/hello-terminal.png?raw=true)


### What just happened?

All headers you specify are send to the server. The server can then decide what to do with them. In this specific case, the server is set up to send you different output when you tell it the User-Agent was "Terminal". If you do, it sends you some awesome ASCII Art.

This is the basic principle of how headers work. When you send them to the server, the server might (or might not) react differently depending on them.

## Moving to httpie

Typing this up every time is kinda dreadful and mostly an exercise for you to understand what goes on under the hood. In order to make the typing a little easier, we will use the awesome [httpie](https://pypi.python.org/pypi/httpie/0.9.2) command line http-debugger from here on up.

Let's do a simple request with it again, type `http -v http://http-fun.hackership.org/`:

![](images/httpie-hello.png?raw=true)

Httpie formats the output the same we just did (request, headers + body then the response, headers and body), but gives us pretty syntax highlighting and helps us in doing the right headers and formatting of those.

Note: Per default `httpie` doesn't show our request (nor headers). Thus we are running it with `-v` to switch on verbose output.

Let's fake the User-Agent again. We can do that by adding our headers at the end of the command like this:

```console
http -v http://http-fun.hackership.org/ User-Agent:Terminal
```

And we are back at seeing our terminal output again.

## hmmm, cookies

Each and every header has its function and implementing HTTP fully means that you have act in a certain way when you encounter certain headers. Of course, as with many specs, not all servers support all features and you might encounter one or the other feature that doesn't work as expected.

One very important feature of HTTP are "cookies". You have probably heard about cookies before, probably in the context of privacy. So let's see what that is all about.

To enable cookies in `httpie`, we need to specify a session for it. We do that by giving it the `--session cookie_test` parameter. Let's see what happens, when we go to the `/cookie/set`-path of our server:

```console
http -v --session cookie_test http://http-fun.hackership.org/cookie/set?name=test
```

In your response, you'll find the header:

```HTTP
Set-Cookie: name=test; Path=/
```

This tells our client, that the server set a cookie with the name 'name' to the value 'test'. Let's try it again, this time set the parameter 'name' to something else. Go ahead, I'll wait. Don't forget to set the `--session cookie_test` .

### Cookie jar

You might have noticed, that in the second request, our client has added the header `Cookie: name=test` to the request. Wohaa. What just happened?

Whenever the server sends a `Set-Cookie` header our client understand that it should store this key-value pair and whenever we send to a request to this server matching the given `Path` (in this case, everything), send it back out there. Httpie stores this information in the `--session` (you sometimes also find this named a 'Cookie Jar').

HTTP by itself is a stateless protocol. Meaning that we only request on resource and get a resource. The server doesn't know whether that request is part of a bigger range of requests, the context it might be run in or anything else you don't explicitly provide. Cookies allow the server to identify a request or set additional information.

A very commonly use case for this is, to keep the login information of a user around. As the client is sending back the information every time, the server can use it to identify you as you. Let's play around with this a little.

Here is a page, that you can only request, once you 'logged in' into the system, try accessing it with httpie:

```console
http -v --session cookie_test http://http-fun.hackership.org/cookie/secret-room
```

As you can see, the server told us, we aren't authorized to access this page. Let's try to login:


```console
http -v --session cookie_test http://http-fun.hackership.org/cookie/login?username=hackership&password=password
```

The server accepted our request and told us we are authorized.

![](images/authorized.png?raw=true)

We can see in the headers, that it set the cookie "username" to "hackership". Well, let's try to connect to the secrect-room again and see what happens:

```console
http -v --session cookie_test http://http-fun.hackership.org/cookie/secret-room
```

Holy cow, we are part of the club now! The server identifies us just by using the cookie. Don't want to believe me? Run the same command again but without the `--session cookie_test`.

### Secure Cookies

This is all cool, but if you think about it, this also quite easy to hack. Just figure out the username, add it as the set-cookie header and you are imposing as someone else:

```console
http -v http://http-fun.hackership.org/cookie/secret-room Cookie:username=imposter
```

![](images/imposter.png?raw=true)

Well. That's not really what we want – or can allow for that matter. This is why most modern web-frameworks have a mechanic called "session"-handling. The specific implementations differ, but in general there are two approaches:

**Encrypted Cookies**:
Instead of sending plaintext, all session-information is encrypted into one long string, which is being encrypted before it sends it on the line – this is called a 'ciphertext'. When the client sends back the ciphertext, the server is able to decrypt and thus, restore the session.

If someone wants to impose another persons session now (or fiddle with their own), they need the encryption key or the server won't accept the content they send.

**Session IDs**:
Instead of sending the entire session over the line (but encrypted), a lot of platforms store the actual content of the session on a third party storage system (typically a database) and only sends over an identifier to find and look up that session. The benefits to this over the encrypted cookie is that the cookie has a deterministic length independent of the session length and no one can mess with the session unless they connect to the database. The drawback, of course, is that you need a a database.

We have a lightweight server without a database, so it uses the first method to provide secure sessions. Let's check it out. Try to connect to `/session/secret-room` (including your current session):


```console
http -v --session cookie_test http://http-fun.hackership.org/session/secret-room
```

Looks, like we have login first. Well, let's do that. This time against the `/session/login`-resource.

```console
http -v --session cookie_test http://http-fun.hackership.org/cookie/login?username=hackership&password=password
```

Can you spot the `Set-Cookie`-header in the response? Well, that looks like a bunch of garbage, doesn't it? But we know it is the value of 'session'. Let's see if we can connect now:

```console
http -v --session cookie_test http://http-fun.hackership.org/session/secret-room
```

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

It is generally split into two parts, separated by (the first) `?`: the path and parameters. The Path has to start with a a slash (`/`), parameters are optional. While the path dictates which resource to load, the parameter are generally passed to the execution of that resource access. Parameters come in the form of `key=value`-pairs, separated by an ampersand (`&`). Which parameters are given and the effects they have are totally resource-implementation-specific and are not dictated by the HTTP specification.

In our examples above, when logging in, we are using url-parameters to tell the `login-`resource what username and password we have.


## Other topics to discover

Pick any of the following topics you are interested in understanding. Just follow the instructions to explore them, how they work and what they are used for.

### HTTP Verbs

We haven't talked much about the `VERB` in the HTTP-Protocol yet. It essentially tells the server the way you want to access a resource. This often means, that for different "verbs", the server executes different parts of the progamme.

HTTP, in its first version, only knows about `GET`, `POST` and `HEAD`, the second version (1.1) added `OPTIONS`, `PUT`, `DELETE`, `TRACE` and `CONNECT`. There are more extensions to the protocol (for example WebDav) but for this document, we will focus on the main foure `GET`, `POST`, `PUT`, `DELETE` and briefly cover `OPTIONS`, `HEAD` and the later added `PATCH` – not all of which are supported by all servers.

On its lowest basis HTTP is implemented under the CRUD-Principles of accessing resources. This essentially means, that everything is a resource and the main ways to connect to them is by either reading it (`GET`), creating a resource (`POST`), writing to the resource (`PUT`) or deleting it (`DELETE`).

#### An example

Let's take our simple `/resource_manager` for example, which lists things I own in various categories. When we try to read its contents, we query it with a `GET` method:


```console
http -v --session resource_test http://http-fun.hackership.org/resource_manager
```


I can also query one item specifically:

```console
http -v --session resource_test http://http-fun.hackership.org/resource_manager/cake
```

Now, I can add new items, by posting to the resource manager and add a new items using the 'POST' method

```console
http -v --form --session resource_test http://http-fun.hackership.org/resource_manager dog=jake
```

As you can see, when we add parameters after a space in the commandline, httpie understands that we want to send a body and automatically switches to the "POST"-method. By setting the `--form`-flag, we tell it to the use "key=value"-form notation. Other notations is `--json` (but our resource manager doesn't understand that).

Now, if we look at the output, we can see, that we created a new resource. We can also overwrite the resource by sending a `PUT` to the newly created resource:

```console
echo 'jake' | http -v --session resource_test PUT http://http-fun.hackership.org/resource_manager/dog
```

Or delete the resource:

```console
http -v --session resource_test DELETE http://http-fun.hackership.org/resource_manager/dog
```

It is also common practice that a PUT on the outer object resets the entire resource. Our server has that implementation, too:

```console
http -v --session resource_test PUT http://http-fun.hackership.org/resource_manager/ dog=jake bag=tote
```

These are the basic ways to interact with http-resources. And although it is rather simple (four main methods), it is an incredibly powerful system and the basis of most [Restful APIs](#restful-api-design)


#### Extra Verbs

We have two more verbs to briefly look into: `HEAD` and `OPTIONS`.

**Options** essentially tells you which verbs are available on this resource. You can find it in the `Allow`-header.

Want to see an example?

```console
http -v --session resource_test OPTIONS http://http-fun.hackership.org/resource_manager/
```


**HEAD** on the other hand, executes a `GET`-Request on the resource but instead of returning the entire content, only returns the headers.

Want to see an example?

```console
http -v --session resource_test HEAD http://http-fun.hackership.org/resource_manager/
```


### HTTP Status Codes

Another aspect we've just quietly ignored until know are the "Status Codes" the server responds with. These are three character long number indicating whether our access worked of it didn't and provides more context about them. Each of these numbers is followed with the descriptive text for the code as the standard requires.

The most prominently known is probably the response code `404 Not Found`. But in general the number as part of one of these three categories:

#### Success 2xx

Starting with a 2 indicates a success of the request. The most common being the `200 OK` status code, indicating that everything went fine and you can find the resource representation in the body of the response.

#### Error 4xx, 5xx

Error Codes starting with 4 and 5 indicate that something went wrong. Where 4xx indicates the error is on the client side while 5xx are server side errors.

Among those the most widely known are the `404 Not Found` indicating the resource can't be found or read, `401 Unauthorized` and `403 Forbidden` indicating the client doesn't have the authorization to access this resource.

On the server side the most commonly found is the general `500 Internal Server Error` and `502 Bad Gateway`. Bad Gateway is often thrown from in-between parties, when they are unable to read from the remote.

#### Redirects 3xx

This class of status codes indicates that the resource exists but additional action is required to access them. `301 Moved Permanently` and `307 Temporary Redirect` for example return a header "Location" telling the client where to look for the request instead.

One other important status code in this category is `304 Not modified`, which is used to learn about the cache is valid.

In most cases, there is no body attached to these responses as they require further action anyways. However, you still can provide a body.

### Full List

These are just a few, picked response codes. We will explore more when we go into specific topics (below) to see how these help us implement certain behaviours. 

If you are interested to read a full list, including vendor specific additions, please [see this great wikipedia article](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes).

For, we just want to redirect our browser to the awesome website on our server, to watch some lolcats:

```console
http://http-fun.hackership.org/status/200
```

Where does it redirect us to?

Bonus challenge: Can you find the teapot?


### HTTP-Redirects

As previously mentioned, there are certain status codes, which we can use to _redirect_ the browser/client somewhere else.

Here we want to focus on these error codes, learn there differences and see how they are being used.

If we try to access `/redirect/simple` on our server with http:

```console
http -v http://http-fun.hackership.org/redirect/simple
```

We'll see the most simple version of a redirect:

![](images/302-found.png?raw=true)

The server responds with the status code "302 Found" and through the "Location"-header tells the client where the resource is to be found now. In our case it just redirects us back to the main page at `/` .

#### Let's loop

By the way, if you were to switch on the `--follow` flag when running http, you'll only see the end-resulting request. As request are independent from each other a second request could still return you a redirect, the client should follow first.

Which leads to a problematic potential, as we will see next, when we try to connect to `/redirect/bounce` with the `--follow` flag:


```console
http --follow --verbose http://http-fun.hackership.org/redirect/bounce
```

It'll come back with a `TooManyRedirects: Exceeded 30 redirects.` .

What just happened? Removing the follow flag, we see that `/redirect/bounce` takes us to `/redirect/back`:

```HTTP
Location: http://http-fun.hackership.org/redirect/back
```

Doing the same on `/redirect/back`, we see it points us to 

```HTTP
Location: http://http-fun.hackership.org/redirect/bounce
```

Darn. We are an endless-redirection loop, as bounce will tell us to check again with `/redirect/back`. In order to not get stuck in these loops, clients keep track of the amount of redirects they've followed and usually break on a hard-limit to avoid going on forever. In this case, it appears that `httpie` takes up to 30 redirects. Browser often show a simimlar error message, when they get stuck in such a loop.

#### Permanent redirects

But back to the more common cases. So, in the previous, we had a reponse (to `/redirect/simple`) that told us to `/` with a status code `302 Found`. 

As you remember from before, there is a `301 Moved permanently`, therefor this must mean it is _temporary_ right? Well, it was, in the first edition for the standard (HTTP/1.0) and it still does serve under this use case. But because industry found other use cases and put them under this status code for a while, in version 1.1 it was renamed to the broader "Found" and more specific status codes `303` to `307` were added.

These specific cases you can read up on on wikipedia if you like, but for our purpose we will only look at `303 See other` and `307 Temprorary Redirect` of HTTP/1.1 standard (although our server respones with version 1.0 as we speak).

Let's get back to our previous example where we received a 302. Assuming this means it is a temporary code, the client shall forward to the other but not keep this information cached. With `301` on the other hand, the client is allowed to assume that this move is permanent and if they were to request the same URL again, they could just skip ahead and go to the end result.

For the server, this is just a question of difference in status codes. But it is an important feature, if you were to move, for example the server, domain or just an entire folder.

See this simple permanent move:

```console
http -v http://http-fun.hackership.org/redirect/permanent
```

Now, let's assume we were to move an entire folder and all siblings but want old URLs to still react and tell them we have moved to a different server. For this, our server matches the URL and redirect the entire path. Try fetching:

```console
http -v http://http-fun.hackership.org/redirect/old/
```

**Excercise**: Where did our path `/redirect/old/about` go? Try to argu first what you expect to happen, then make a request and see if you were right?

#### Redirects in Authentication

Another very common usage of sending the moved-temprorary code, is to point the client towards a login-page because they requested a page they can't access. This, as well as redirecting the User back after they successfully logged in, is the primary use case for the `303 See Other`-use case (although you might still see `302 Found` in practice).

**Excerise**: See, what happens if you try to access `/redirect/restricted`.


### Basic Authentication

Although nowadays most systems use a Cookie-Based System for authentication as they allow full control to the backend on how to authorize you in the beginning – shall be via Twitter, Facebook, Google or Username + Password – HTTP actually contains a simple authentication system.

In this system the client adds the `Authorization`-header to the request and server accepts or denies access depending on the value of that header. In its most basic form, this uses a mechanism called "Basic Authenication" in which the client sends a non-encrypted username-password pair. As this means, we are sending the password as plaintext over the page, which everyone can read, this isn't considered a very secure mechanism. But beause of its easy configuration, it is still widely in use, primarely to secure to site from bots and random scanners.

So let's play with it first. At `/auth/basic` we have a resource, you can only access if you provide user-name and password, otherwise we will receive a 401. If we send a normal request, we are blocked from seeing the content:


```console
http -v http://http-fun.hackership.org/auth/basic
```

We can instruct `httpie` to add username and password as follows:

```console
http -v http://username:password@http-fun.hackership.org/auth/basic
```

In this request, you can find the "Authorization"-Header:

```HTTP
Authorization: Basic YmVuOnRlc3Q=
```

Although this looks cryptic, basic authentication really is just "username:password" in a base64encoding. Anyone can recover this information easily.

This is why the HTTP protocol contains a second authentication mechanism by default, called "digest". Let's try to get going with this one on the `/auth/digest` URL. Accessing this one with our 'basic auth', yields a very interesting result. Among others we find a

```HTTP
WWW-Authenticate: Digest nonce="cfc82b49f2bd8201", realm="Example Auth", qop="auth"
```

header. This tells us, that the server requires a digest-authentication. We won't get far with our bad basic-plain-text here. Let's switch on digest auth on httpie:


```console
http -v --auth-type digest http://user:password@localhost:8080/auth/digest
```

You'll see in the header that we send out a much more complex "Authorize" string with many parameters and values. And although this overall looks much more complex, it isn't that much more secure. Not only does it use the broken MD5 and SHA algorithms, in order to make it more secure every request is signed individually (as you can see in the parameters) increasing the calculation overhead a lot.

If you want to learn more on how this is calculated, I recommend this really good Wikipedia article about [digest auth](https://en.wikipedia.org/wiki/Digest_access_authentication).


### Content Negotiation

As HTTP only sends "a representation" of its resource, the server and client need a way to discuss, what the format of that representation should be. This process called _content negotiation_ and – as so many other things – happens through the usage of specific, standardised header fields. This header is the `Accept:`-header you might have noticed before (as `httpie` sends it by default).

In general there are three main ways, in which this negotiation can happens:

 1. the client sends the specific headers of what it supports and the server figures out, which one to pick (server-driven negotiation)
 2. the server might respond with a `300 Multiple Choice` or `406 Not Acceptable` to alert the client, they have to choose a different content type (agent-driven negotiation)
 3. a cache does this in between (transparent negotiation)

Let's start by looking at the most commonly used version: the client sending the header and the server figures out an appropriate response.

Please send a normal request to the endpoint `/content/simple`:

```console
http -v http://http-fun.hackership.org/content/simple
```

You should see a text-formatted response as follows:

```HTTP
HTTP/1.0 200 OK
Content-Length: 23
Content-Type: text/html; charset=utf-8
Date: Fri, 17 Apr 2015 20:04:24 GMT
Server: Werkzeug/0.10.4 Python/2.7.5

peter: cat
hello: world
```

In the content header you can see the result of the "negotiation", the `Content-Type` the server choose in the end is `text/html` in the `utf-8` encoding.

This server chose this as the preferred response, beause the client – you – send an i-accept-anything-`*/*`-`Accept` header. We can also overwrite any header `httpie` sends by adding it to the end of the request. For example, let's tell the server we only accept 'application/json' format:

```console
http -v http://http-fun.hackership.org/content/simple Accept:'application/json'
```

Voila

```HTTP
HTTP/1.0 200 OK
Content-Length: 34
Content-Type: application/json
Date: Fri, 17 Apr 2015 20:07:23 GMT
Server: Werkzeug/0.10.4 Python/2.7.5

{
    "hello": "world",
    "peter": "cat"
}
```

The server responded with the same data, but formatted in `JSON` as we requested and the responding `Content-Type` tells us.

We can also give multiple formats, the client supports and let the server decide which one to pick. We do that by giving multiple values delimited with a comma (`,`) as follows:

```console
http -v http://http-fun.hackership.org/content/simple Accept:'text/plain, application/json'
```

**Exercise**: Can you argue, which format the server response will be? What if you change the order of the entries? Try it.

#### Quality for choosing

Right now, if the server finds multiple formats applicable it will just pick the first in line. Althought that might be fine for the client, the client might actually prefer some formats over others. In order to let the server know about that, we can give each mimetype a quality-value `;q=` to order them by. The default quality is `1.0`. So if we wanted to discourage the usage of `text/plan` from our previous example, no matter the order, we could request:

```console
http -v http://http-fun.hackership.org/content/simple Accept:'text/plain; q=0.9, application/json'
```

Nice, eh?

#### Agent and transparent Negotiation

Are very uncommon in practice. Primarily because they are very cumbersome and scale rather bad. As the client doesn't know the formats they can ask for when they receive an `300 Multiple Choices`, the have to potentially ask for a lot before it eventually fails. More commonly you'll find `406 Not Acceptable` as it might be used in conjunction with your client asking an API to deliver in a format (like `xml`) that is not, or no longer, supported. In which case you probably want to upgrade your code ;) .

You can learn more about content negotiation and how browsers handle it on this great [Mozilla Developer Network site](https://developer.mozilla.org/en-US/docs/Web/HTTP/Content_negotiation).

#### Compressed Content

One other really important header for content negotiation is the `Accept-Encoding`-header. As so much of the content, which is send over HTTP is text-driven, there is a clear opportunity for compression to lower the bandwidth used.

During the content negotiation, the client can also inform the server any compression they are able to accept. Allowing the server to compress the content before sending it over.

Note: In Web-Development the compression is typically handeled by a load-balancing instance in between the app and the server, for example _Apache httpd_ or _nginx_. They are usually faster and handle this header transparently to the webapp and the client. For the purpose of education, we've implemented zipped content into our app, but that is rather odd to see in production...

Let's redirect our attention to a resource that has gzip-encoding enabled: `/content/compressed`. Aside from sending the body gzip-encoded, it behaves exactly the same as `/content/simple` did before. So you can compare requests to both and the results, you'll get back. Now run:

```console
http -v http://http-fun.hackership.org/content/compressed
```

**Note**: If `httpie` finds the appropriate `Content-Encoding`-Header send by the server, it will automatically decode the content before showing. So, you can only see the difference by looking at the headers send back.


**Exercise**: Do you notice any difference to the same call to `/content/simple`? Does `httpie` send any `Accept-Encoding`-Header? If so, what is it set to? What happens if we overwrite the header by adding a specific `Accept-Encoding:'deflate'` to the httpie command?


You might have noticed that the content size with gzip is larger than the content of the raw text. This is a caused by gzip adding overhead to the content. This, in addition to the extra performance impact this has, is why in production content that is smaller than 500bytes usually is not compressed by the server even if the client supports it.

If you want to learn more about content negotiation, [MDN has an excellent article about it](https://developer.mozilla.org/en-US/docs/Web/HTTP/Content_negotiation), including the various ways in which browsers implement it and their behaviour differs. This article also covers the `Accept-Language`-header we skipped here for the sake of keeping it focussed.


### User Agent Tricks (SEO and mobile optimised page serving)

Although you could considered it part of content negotiation, serving different pages depending on the user agent, hasn't initially been the focus of the `User-Agent`-header. [As MDN clearly states](https://developer.mozilla.org/en-US/docs/Web/HTTP/Content_negotiation#The_User-Agent.3A_header): "_though there are legitimate uses of this header for selecting content, it is considered bad practice to rely on it to define what features are supported by the user agent_".

In here, we want to focus on the clearly legitimate cases only: **to know whether a search bot is crawling our website or if someone is accessing the page from a mobile device**. In both of these cases it is very legit to serve different content than to a normal user. For the first because a crawling-optimised site should be faster and more brief to load, for the second a stripped down version as the bandwidth and CPU of mobile devices is more limited.

In a way this feature works very similar to the previously discussed `Accept-Content`-header as the server will match the given `User-Agent`-String and send us different content depending on what it finds there. Remember the `User-Agent: Terminal` trick from the beginning? This was essentially it: serving different content based on the browser.

One problem with this approach is that browser are notourisly bad at giving a good description: in order to be served sites compatible with other products they have been adding more and more strings – leading to a huge mess and making browser and platform detection a science by itself. Just the various forms of [Mozilla-Products](https://developer.mozilla.org/en-US/docs/Web/HTTP/Gecko_user_agent_string_reference) have a list of over 20 different strings, excluding the various version numbers they could have.

Fortunately, this practice has declined recently. With the emergence of use cases like mobile, more browser are inclined to make it easy to detect them. In our use cases we will detect a any mobile device by learning if they have `mobi` in their User Agent.

Go ahead, try it out – this is a fake user agent, which should be detected as mobile:

```console
http http://http-fun.hackership.org/useragent User-Agent:' Mobile/5G77 Safari/525.20'
```

Go, try it out with a few more User Agent string:

 - Safari on hungarian iPhone: `Mozilla/5.0 (Mozilla/5.0 (iPhone; U; CPU iPhone OS 2_0_1 like Mac OS X; hu-hu) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5G77 Safari/525.20 `
 - Internet Explorer 10.6: `Mozilla/5.0 (compatible; MSIE 10.6; Windows NT 6.1; Trident/5.0; InfoPath.2; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 2.0.50727) 3gpp-gba UNTRUSTED/1.0`

 - Firefox 31: `Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20130401 Firefox/31.0`

You can find plenty more on [useragentstring.com/pages/useragentstring.php](http://useragentstring.com/pages/useragentstring.php) (as well as an analyse tool).

You see, these strings became increasingly complex, which is why pattern matching them is in general discouraged and should be used with **a lot of caution**.

#### Matching the crawlers

What is relatively safe though, is serving different search-engine optimised content to search engines. Search-Engines use web-browser-like tools – called crawlers – to scan and index websites for them. All major search engines have been very vocal about what the User String for each is to encourage web hosters to allow them to get through.

Google for example uses the term ["Googlebot"](http://useragentstring.com/Googlebot2.1_id_71.php), while Bing identifies as ["bingbot"](http://useragentstring.com/pages/Bingbot/). It is relatively safe to match for these terms and serve different content based on that. It is in their interest to not come with a different User Agent, as that might be blocked or wrongly accounted to website usage stats.

Here are some search engine strings our server is able to detect:

 - Googlebot: `Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)`
 - Bing: `Mozilla/5.0 (compatible; bingbot/2.0 +http://www.bing.com/bingbot.htm)`
 - Yandex:  `Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)`


With the same detection any server can serve different content to mobile or crawlers, or deny access at all (although that is discouraged). But if you want to make sure the Googlebot never indexes your site, this is a way to do it.

### Caching

We've discussed one optimisation in the HTTP Protocol before, the compression of content. As HTTP is a request-response-protocol it means there are only so many things we can request at the same time and we have to often wait for them to get back. Even if they are compressed, if the content didn't change since the last time we fetched, we still send the entire content over the wire and have to figure that it is the same. Or, do we?

In order to help with this common problem and improve performance HTTP has certain caching features, which can be enable – you guessed it – through the usage of specific headers. Although the responsibility for an implementation is totally on the side of the client, it is the server, who controls what and for how long to cache it. Throughout all the headers we will look at next, this is the underlying mechanic.

But caching can also be handled by an intermediate instance. In nowadays world with CDNs (Content Delivery Networks) that is even more common. So, if you are serving your content through any of these systems (like cloudflare), you should take extra care about the caching they do on your behalf based on the http headers you serve.

#### Cache-Control

The main entry point to look at caching is the `Cache-Control`-header. Unlike some other fields we come to later, these **must be passed through as well as be obeyed by intermediates**. Which makes it a highly important field for controlling intermediate caches and how they act.

Cache control has various extensions, and the specification even allows for third party vendor extensions, which are separated by a comma. If the client doesn't understand an extension, it should simply ignore it, as long as it implements the ones in the standard. Let's take a look at a simple example:

```console
http -v http://http-fun.hackership.org/cache/simple
```

In our output we find the `Cache-Control`-header:

```HTTP
HTTP/1.0 200 OK
Cache-Control: public, max-age=20
Content-Length: 24
Content-Type: text/html; charset=utf-8
Date: Sat, 18 Apr 2015 00:54:19 GMT
Server: Werkzeug/0.10.4 Python/2.7.5

Simple Cache-able Response
```


In this case the server informs us, the caching features `public` and `max-age` (set to 20) are activated. These two in combination are the most common example. So, let's take a look at the various extensions for Cache-Control and what they do:

- `public` | `private`: to be stated first, are mutually exclusive. Where `public` means, anyone is allowed to cache, and `private` that only the end-user is allowed (as it is their content).
- `no-cache` :  as you guessed means no instance should cache this ever. However, if you specified a field after no cache, like `no-cache=Cookies`, the response may be cached after this header field has been stripped. This can be very useful, but you shouldn't rely on it solely as some don't actually implement that behaviour.
- `max-age` defines a maximum amount of time, in seconds, the cache is allowed to hold the content without any revalidation. Meaning that unless the time elapsed the client doesn't even ask the server before serving stale content. This already makes requests significantly faster.
- `s-maxage` acts the same as `max-age` but is only used for "shared-caches" (hence the prefixed `s-`). Meaning this is only for the CDN/Proxy but end-client will ignore it.
- `must-revalidate` means that the client has to check back with the server before serving a stale instance. This is typically used in conjunction with the later explained 'Etag'-field.
- `no-transform` some proxies do transformation on behalf of the end-users, for example convert images into lower resolutions or concatenate Javascript-files for mobile usage. You can enforce them to not do anything by using this flag.

As these are just fields the server can send, most of which are for intermediates and we – as the client implementation – don't really have much caching enabled, there is little do with these at the moment. Aside from knowing about them.

What is more interesting is the two different approaches caching can work in general. Expiry vs. etag.

#### Expires

So, the expires header essentially states until when (as in timestamp) the client (or any intermediate) is allowed to keep a stale version around without _asking the server again_.

Usage of this header field reduced the amount of hits on your server BY A LOT and will improve load time tremendously. But it comes with a few things to keep in mind.

But first let's look at an example:

```console
http http://http-fun.hackership.org/cache/expire
```

As you can see it serves you both the Cache-Control and the Expires headers. Both dating to 364 days into the future from when the server was started. We are using both as Cache-Control isn't understood by all HTTP/1.0 clients and caches. So as a best practice always set both.

But here you can already see one caveat of this approach. Even if we were to update the server now and set different content and a different expiry time, a client who received this response before **will not know about this** as they will be caching the stale version until it is invalidated.

Setting expire, especially for long into the future, therefore must be used with a lot of caution. To not cause troubles later. As a general rule of thumb, only use it for content that is changing almost never and/or set the value to small amounts. Or use Etags

#### Etag

Unlike expires, which allows the client to cache the content, the entity tag (short `etag`) requires revalidation of the content but can be used to omit the content if it doesn't differ.

Here is a simple example on how this works. Let's take the following resource at `/cache/etag`:

```console
http -v http://http-fun.hackership.org/cache/etag
```

It comes back with a `Cache-Control` header allowing anyone to cache, but more interesting for us, it delivers us an `Etag` for the content. Now when we want to access the entity again later, our cache tells us we need to revalidate it and we can do so by supplying that etag using the `If-None-Match`-header:

```console
http -v http://http-fun.hackership.org/cache/etag If-None-Match:'1234567-etd'
```

```HTTP
HTTP/1.0 304 NOT MODIFIED
Connection: close
Date: Sat, 18 Apr 2015 01:34:16 GMT
Server: Werkzeug/0.10.4 Python/2.7.5

```

And voila, instead of the entire response, the server informed us that the resource was `304 Not Modified`. Which means we can just load the content from our cache and be happy with it. Thus increasing download time significantly.

We can also ask with a stale etag, in which case we receive a full response again – including an updated etag:

```console
http -v http://http-fun.hackership.org/cache/etag If-None-Match:'1234567'
```


#### Vary-Header

One header, I'd like to add to this chapter about Caching is the `vary`-header. This really cool field signals a client that although they might not be allowed to cache the result as is, they might be if they supply a different value to the field specified here. One classic example for that is, telling the Google Bot through `Vary: User-Agent`, that there is a different version for them than for others. Thus triggering the Google Bot to try to connect to your page and cache a mobile version of your website, too.


#### There's much more

There are plenty more things you can set, but these are the most common ones to know about. There is a good article explaining many of these more in depth on [the mobify blog](https://www.mobify.com/blog/beginners-guide-to-http-cache-headers/) and the [specification is actually quite readable](www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.9), too.If you want to learn more about any of these fields.


### AJAX Request

AJAX stands for Asynchronous JavaScript and XML and describes a group of web development techniques used in client side web-application. A client-side web application uses Javascript to execute code in the browser outside of the context of the server. This allows for more fluid updates and a generally a better and more instant response as not every action first requires to be confirmed from the web server.

One very important aspect of these websites is to allow content-changes without refreshing the entire website. A good example for that is a chat app. You don't want to refresh the entire site, just because one message has been added.

In this case we will first emulate the Javascript client using our lovely `httpie` tool before moving over and introspect a working javascript-based implementation. For the later you need some basic understanding of HTML and be able to briefly parse Javascript (although we'll explain the major part of it).

Let's image a very simple chat API with the endpoint `/chat/messages`. If we send a post-message to that endpoint a new message is created and stored, when we send a get, we receive the latest 10 messages.

Now image you are the website, and you poll the `/chat/messages/` endpoint once a second by doing:

```console
http -v http://http-fun.hackership.org/chat/messages
```

Do that once a second (rougly), while on the other shell now post a message to it. On the website that could happen through a form for example:

```console
http -v --form http://http-fun.hackership.org/chat/messages message="Hello"
```

*Note*: this server implementation is rather dumb, if many people do that at the same time, you might don't even see your message pop up ;) .

Alright. We now have a rough but simple enough working chat emulator. We can read messages (by polling once a second) and we can post messages. What else do we need? A UI? Why? Aren't you capable of using the Terminal? You think it's not pretty? PFFFFFFF... well ok.

Redirect your browser to `http://http-fun.hackership.org/chat/` then...

TADA! The exact same functionality. And if you open your Developer Tools, you'll find that it does exactly what we have just been doing. Here a tiny part of the code:

```javascript
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
```

Even without super awesome Javascript Skill you will probably be able to understand the basics: In line 1 we connect to the `form` encapsulating the input-item and the button and whenever that is `submit`ed, our code is triggered. We then read the content of the input field (line 3) and if some is given (line 4) we trigger the same post request as we just did from the command line before (line 5). In either case we clear the input-field after (line 8).

The second function (line 12ff) does the second part of what we did before: once a second (line 14) we reload the content of the html-element `#messages` with the content from the server.

Sending data to the server, receiving data from it without reloading the page, all possible through using Javascript in teh browser. This is the basic principle of AJAX.


### Cross Origin Request Security (CORS)

**Note**: As this is a very specific topic within AJAX, I assume you are familiar with at least that (otherwise read up in the chapter before). I also believe you've encountered that primarily through the usage of jQuery or a similar web-frontend library. So I assume you are familiar with the basics of Javascript and jQuery to illustrate this chapter.

In the example before, we were loading chat messages from  `http-fun.hackership.org/chat/messages`. Let's assume, we want to do that from the Javascript of a different server. For the simplicity of this case, just head over to [www.hackership.org](http://www.hackership.org) and [open the developer console](#opening-the-developer-console) there.

Now, in the console type in the following and press enter:

```Javascript
$.get("http://http-fun.hackership.org/chat/messages").then(function(data) {alert(data);});
```

From the code you'd expect an alert message with the content of the response. But instead what you'll see is this ugly error message:

![CORS](images/cors-error.png?raw=true)

#### Some Background

In the early times of the web, when Javascript was still a new thing, people abused it to send faulty data and try to impersonate other people online. Remember the Cookie-Request thing from before? If they are send _at every request_ if you were to make – let's say – a request that would post something on the facebook wall with the javascript from within the browser from a different website, you can impersonate them and their account. Posting content in their name is still the more harmless thing you could do.

In order to prevent that, Javascript is generally sandboxed into its own domain. A script that comes from `www.hackership.org` is not allowed to access content from `http-fun.hackership.org` as that is a different server. That is called 'the origin' and trying to make a request across origins is disallowed by the browser. Hence the "Cross-Origin Request Blocked" error message. This behaviour is generally implemented in all browser, which have a decent cookie and Javascript support enabled. And it is a sane and good default.

### Back to the issue

But in this case, we actually want to allow the client to read that content. There have been various ways to hack around this in the past, until eventually HTTP introduced the `Access-Control-Allow-Origin`-header. Through this header the server can specify other domains, which are allowed to access this content.

Take a look at this resource:

```console
http -v http://http-fun.hackership.org/chat/allowed-messages Origin:'http://www.hackership.org'
```

You can see, that one has the `Access-Control-Allow-Origin` header set to allow "http://www.hackership.org". But you will also see, that trying to "POST" to it is denied by the server:

```console
http -v POST http://http-fun.hackership.org/chat/allowed-messages Origin:'http://www.hackership.org'
```

This way, the server can allow third-party sites to load the content but disallow the imposting of others. Another way to enforce this behaviour by also setting the `Access-Control-Allow-Method` header.

In order to not rely on the browser implementing and enforcing the security rule, many APIs which generally allow CORS will only do so, when the request contains a specific `Origin`-Header (which is automatically supplied when doing AJAX requests). If you remove the `Origin`-header in our `httpie`-request, you will see that the server denies access:

```console
http -v http://http-fun.hackership.org/chat/allowed-messages
```


Let's get back to the browser and try again with the `/chat/allowed` url...:


```Javascript
$.get("http://http-fun.hackership.org/chat/allowed-messages").then(function(data) {alert(data);});
```

Allowing access across origin is called "Cross Origin Resource Sharing", or CORS for short. As so often, this is just a brief overview of the key principle and the main parameters and there are plenty more to discover. I recommend [the MDN article](https://developer.mozilla.org/en-US/docs/Web/HTTP/Access_control_CORS) and the [CORS-specification](http://www.w3.org/TR/access-control/) for further reading.

### Cross-Site-Scripting

### Cross Site Request Forgery (& Token)


### Restful (API) Design




### HTTP Streaming


### Keep-Alive and Pipelining



## Coming up next/ ToDo

### Reverse Proxies

### Do Not Track

### HTTPS

### Long-Polling/Comet/Streaming

### Websockets

### HTTP/2.0


## Appendix

### Running your own server

For some of the tests to work properly, you need to host the server yourself. You will need a proper virtualenv (on python 2.7) on your system, then you can get going with this:

```console
virtualenv .
./bin/pip install -r requirements
./bin/python server.py
```

And you can run the tests against your local instance on port 8080:

```console
./bin/http -v http://localhost:8080/
```

### Opening the Developer Console

In Firefox navigate to `Tools->Web Developer->Web Console` and click it.

![Webconsole](images/webconsole.png?raw=true)

Unless you configured it differently before a big panel should pop up from the bottom like this:

![console-open](images/console-open.png?raw=true)

This panel is the "developer console". Head back to the chapter you were looking at :D .


## License

This work is licensed under the [Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License](http://creativecommons.org/licenses/by-nc-sa/3.0/). To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/ or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.