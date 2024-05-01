from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to Ricardo C. Johnson's LinkedIn Assistant API"
