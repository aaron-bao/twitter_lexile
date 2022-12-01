from flask import Flask
from flask import request, render_template

from lexile import get_lexile_score

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def welcome():
    if request.method == 'GET':
        return(render_template('welcome.html'))

@app.route("/find_lexile", methods=['GET', 'POST'])
def find_lexile():
    if request.method == 'POST':
        username = request.form.get('username', None)
        lexscore = str(get_lexile_score(username))
        display_string = username + "\'s most recent tweets are at a " + lexscore + "th Grade Reading Level!!!! "
        #display_string = "Your username is: " + username
        return(render_template('welcome.html', result_text=display_string))
    if request.method == 'GET':
        return(render_template('welcome.html', result_text="You sent a GET request to get here"))
    """
    username = request.form.get('username')
    return(render_template('welcome.html'))
    """

if __name__ == '__main__':
    app.debug = True
    app.run()
