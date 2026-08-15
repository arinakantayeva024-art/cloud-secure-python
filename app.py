from flask import Flask, request, jsonify
import hashlib
import time

app = Flask(__name__)

# Demo user
USERNAME = "admin"
PASSWORD_HASH = hashlib.sha256("admin123".encode()).hexdigest()

# Security log
security_logs = []


def log_event(event, ip):
    security_logs.append({
        "time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "event": event,
        "ip": ip
    })


@app.route("/")
def home():
    return """
    <h1>Cloud Secure Python</h1>
    <p>Python application is running securely in the cloud!</p>
    <p>Available endpoints:</p>
    <ul>
        <li>/login</li>
        <li>/health</li>
        <li>/logs</li>
    </ul>
    """


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "cloud": "Render",
        "application": "Cloud Secure Python"
    })


@app.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Invalid request"
        }), 400

    username = data.get("username")
    password = data.get("password")

    ip = request.remote_addr

    if username != USERNAME:
        log_event("Invalid username", ip)

        return jsonify({
            "error": "Invalid credentials"
        }), 401

    password_hash = hashlib.sha256(
        password.encode()
    ).hexdigest()

    if password_hash != PASSWORD_HASH:
        log_event("Failed login attempt", ip)

        return jsonify({
            "error": "Invalid credentials"
        }), 401

    log_event("Successful login", ip)

    return jsonify({
        "message": "Login successful"
    })


@app.route("/logs")
def logs():

    return jsonify({
        "security_events": security_logs
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=10000
    )
