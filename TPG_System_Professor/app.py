from flask import Flask, render_template
from Controllers import routes
app = Flask(__name__, template_folder='Views')

routes.init_app(app)

if __name__ == '__main__':
    app.run(host='localhost', port=4000, debug=True)