import os
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    env = os.getenv("SERVER_ENV", "development")
    
    is_prod = env.lower() == "production"

    debug = False if is_prod else True
    host = "0.0.0.0" if is_prod else "127.0.0.1"

    app.run(host=host, port=8080, debug=debug)
