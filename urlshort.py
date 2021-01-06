from flask import Flask, render_template, request, redirect, url_for, flash
from flask import abort, session, jsonify
import json
import os

app = Flask(__name__)
app.secret_key = 'what the hell is ccc'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        return render_template('index.html', codes=session.keys())
    else:
        # clear the session
        if os.path.exists('urls.json'):
            os.remove("urls.json")
        session.clear()
        # return render_template('index.html')
        return render_template('index.html', codes=session.keys())

@app.route('/about')
def about():
    return '<h1>This is a URL shorter</h1>'

@app.route('/your-url', methods=['GET', 'POST'])
def your_url():
    # where request.args has two keys, one is the "url" of <input name="url"...>
    # the other is "code" of <input name="code"...>
    # in index.html, the form by default is using GET, so the info of GET is visible in the request
    # see <form action="your-url">

    # when we change it to <form action="your-url" METHOD="post">
    # it will say 'this method is now allowed'
    # we need to change @app.route(..., methods=...) with POST
    # then don't use request.args['code'] since now it has no args
    # but using request.form['code']
    # and request also has request.form['url'] since we have two inputs, one is labeled with 'url', one is 'code'
    
    # debug note: I mistakenly set methods to ['GE', 'POST']
    # then this function can't go to GET branch
    # even I put something before here, such as print("-"*50)
    # it won't show up
    if request.method == 'POST':
        urls = {}
        if os.path.exists('urls.json'):
            with open('urls.json', 'r') as urls_file:
                urls = json.load(urls_file)

        print("urls = {}".format(urls))

        if urls and request.form['code'] in urls.keys():
            # flash the message
            # need secret_key, see line 6
            # here set the flash message
            flash('The short name has already been taken.')
            # then flash message will be sent to index.html
            # see index.html, get_flashed_messages
            return redirect(url_for('index')) 

        urls[request.form['code']] = {'url':request.form['url']}
        with open('urls.json', 'w') as url_file:
            json.dump(urls, url_file)
            session[request.form['code']] = True
        return render_template('your_url.html', code=request.form['code']) 
    else:
        # url_for accepts the name of the function as its first argument
        return redirect(url_for('index')) 

@app.route('/<string:code>')
def redirect_to_url(code):
    # the arg 'code' is from /<string:code>
    if os.path.exists('urls.json'):
        with open('urls.json', 'r') as urls_file:
            urls = json.load(urls_file)
            print(urls)
            if code in urls.keys():
                return redirect(urls[code]['url'])
    
    return abort(404)

@app.errorhandler(404)
def page_not_found(error):
    # error = 404 Not Found: The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.
    return render_template('page_not_found.html'), 404

@app.route('/api')
def session_api():
    return jsonify(list(session.keys()))
if __name__ == '__main__':
    app.run()


