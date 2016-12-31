# -*- coding: utf-8 -*- 
import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_mysqldb import MySQL
from werkzeug import secure_filename




app = Flask(__name__)
mysql = MySQL(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'pythontest'

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'static/game_img'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
    filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']



@app.route('/')
def home():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT name, score FROM tableone''')
    res = cur.fetchall()
    res = str(res)
    return   render_template('accueil.html', res=res)


@app.route('/clicking_game')
def clicking_game():
    return render_template('clicking_game.html')

@app.route('/boardgames')
def boardgames():

    cur = mysql.connection.cursor()
    cur.execute('''SELECT name, year, n_players, play_time, age, designer, artist, publisher, filename FROM boardgames''')
    result = cur.fetchall()

    return render_template('boardgames.html' , result = result)

@app.route('/addgame', methods=['POST'])
def addgame():
    name = request.form['name']
    year = request.form['year']
    n_players = request.form['n_players']
    play_time = request.form['play_time']
    age = request.form['age']
    designer = request.form['designer']
    artist = request.form['artist']
    publisher = request.form['publisher']

    # Get the name of the uploaded file
    file = request.files['file']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # Move the file form the temporal folder to
        # the upload folder we setup
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        

    cur = mysql.connection.cursor()
    cur.execute('''INSERT INTO boardgames (name, year, n_players, play_time, age, designer, artist, publisher, filename) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''', (name, year, n_players, play_time, age, designer, artist, publisher, filename))
    mysql.connection.commit()

    return redirect(url_for('boardgames'))

@app.route('/boardgames/page')
def boardgame_page():

    chosenName = "page"

    cur = mysql.connection.cursor()
    cur.execute('''SELECT name, year, n_players, play_time, age, designer, artist, publisher, filename FROM boardgames WHERE name="Splendor"''')
    result = cur.fetchall()

    return render_template('boardgame_page.html', result=result)

@app.route('/codegen')
def codegen():

    return render_template('codegen.html')

@app.route('/codegenAct', methods=['POST'])
def codegenAct():
    numberOfDigits = request.form['numberOfDigits']

    return render_template('codegen.html', numberOfDigits=numberOfDigits)



@app.route('/highscore')
def highscore():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT name, score FROM tableone ORDER BY score DESC''')
    result = cur.fetchall()

    return render_template('highscore.html', result = result)


@app.route('/addscore', methods=['POST'])
def addscore():

    name = request.form['name']
    score = request.form['score']

    cur = mysql.connection.cursor()
    cur.execute('''INSERT INTO tableone (name, score) VALUES (%s, %s)''', (name, score))
    mysql.connection.commit()

    return redirect(url_for('highscore'))

@app.route('/specteropschart')
def specteropschart():
    return render_template('specteropschart.html')

@app.route('/contact')
def contact():

    return render_template('contact.html')

@app.route('/sendmail', methods=['POST'])
def sendmail():
    '''
    email=request.form['email']
    subject=request.form['subject']
    content=request.form['content']

    mailit(email, subject, content)
    '''
    msg = "Mail was sent"
    

    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(port=5000, threaded=True, debug=True)




