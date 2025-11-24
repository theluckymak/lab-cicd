from flask import Flask
import datetime

app = Flask(name)

@app.route('/')
def hello():
    return {"message": "Hello from CI/CD!", "time": str(datetime.datetime.now())}

if name == 'main':
    app.run(host='0.0.0.0', port=5000)
