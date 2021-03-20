import json

from flask import Flask, render_template


app = Flask(__name__)



@app.route('/restaurant')
def hello():
    return render_template('restaurant.html') # can include name = "name" as well, not sure where it can be used tho

@app.route('/store')
def store():
    return render_template('store.html') # can include name = "name" as well, not sure where it can be used tho

@app.route('/leaderboard')
def leader():
    return render_template('leaderboard.html') # can include name = "name" as well, not sure where it can be used tho


@app.route('/')
@app.route('/intro')
def intro():
    return render_template('intro.html')


@app.route('/customer')
def testing():
    return render_template('customer.html')

if __name__ == '__main__':
    app.run()
