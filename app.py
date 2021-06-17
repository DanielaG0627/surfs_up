## Import flask instance
from flask import Flask

## Create a New Flask App Instance
app = Flask(__name__)

## Creatre Flask Routes
@app.route('/')
def hello_world():
    return 'Hello world'
