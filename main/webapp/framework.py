from flask import Flask
app = Flask(__name__)
 
@app.route('/')
def hello():
    hello = "Hello world"
    return hello
 
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
