from flask import Flask
import os

app = Flask(__name__, template_folder="Templates")
app.debug = True

app.config['SECRET_KEY'] = os.urandom(12).hex()