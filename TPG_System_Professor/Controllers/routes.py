from flask import render_template, request, redirect, url_for, flash
import urllib
import json
from werkzeug.security import generate_password_hash,check_password_hash
from markupsafe import Markup

def init_app(app):
    @app.route('/')
    def home():
        return render_template('index.html')
    
    @app.route('/login', methods=['GET','POST'])
    def login():
        if request.method == 'POST':
            return redirect(url_for('home'))
        return render_template('login.html')
    
    @app.route('/cadastro', methods=['GET', 'POST'])
    def caduser():
        if request.method == 'POST':
            name = request.form.get('name')
            eMail = request.form.get('eMail')
            password = request.form.get('password')

            teacher_data = json.dumps({
                'name': name,
                'eMail': eMail,
                'password': password
            })

            req = urllib.request.Request(
                url='http://127.0.0.1:5000/teachers',
                data=teacher_data.encode('utf-8'),
                headers={'Content-Type': 'application/json'},
                method='POST'
            )

            try:
                with urllib.request.urlopen(req) as resp:
                    if resp.status == 201:
                        return redirect(url_for('login'))
            except Exception as e:
                print('Erro ao cadastrar o professor:', e)

            return redirect(url_for('caduser'))

        return render_template('cadUser.html')
    @app.route('/graphics')
    def graphics():
        return render_template('graphic.html')
    @app.route('/cadStudent')
    def cadstudent():
        return render_template('cadStudent.html')
    @app.route('/cadClass')
    def cadclass():
        return render_template('cadClass.html')
    @app.route('/cadQuest')
    def cadquest():
        return render_template('cadQuest.html')
    @app.route('/Student')
    def student():
        return render_template('Student.html')
    @app.route('/Class')
    def cclass():
        return render_template('Class.html')
    @app.route('/Quest')
    def quest():
        return render_template('Quest.html')