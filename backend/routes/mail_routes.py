from flask import Flask, request, jsonify
from ..mail import add_subscriber

app = Flask(__name__)

@app.route("/subscribe", methods=["POST"])
def subscribe():
    data = request.json
    email = data.get("email")
    first_name = data.get("first_name", "")
    last_name = data.get("last_name", "")

    result = add_subscriber(email, first_name, last_name)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
