from flask import Flask, request, jsonify, render_template_string
import hashlib
import time
import base64
from io import BytesIO

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    ConfusionMatrixDisplay
)

import matplotlib

# Required for running Matplotlib on Render/cloud server
matplotlib.use("Agg")

import matplotlib.pyplot as plt


app = Flask(__name__)


# ============================================================
# CLOUD SECURITY
# ============================================================

USERNAME = "admin"

PASSWORD_HASH = hashlib.sha256(
    "admin123".encode()
).hexdigest()

security_logs = []


def log_event(event, ip):

    security_logs.append({
        "time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "event": event,
        "ip": ip
    })


# ============================================================
# RESEARCH METRICS
# ============================================================

def create_metrics():

    # --------------------------------------------------------
    # EXAMPLE EXPERIMENTAL DATA
    # Replace these with your real research results
    # --------------------------------------------------------

    y_true = [
        0, 0, 0, 0, 0,
        1, 1, 1, 1, 1,
        0, 0, 1, 1, 0
    ]

    y_pred = [
        0, 0, 0, 1, 0,
        1, 1, 1, 0, 1,
        0, 1, 1, 1, 0
    ]

    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

    accuracy = accuracy_score(
        y_true,
        y_pred
    )

    precision = precision_score(
        y_true,
        y_pred,
        zero_division=0
    )

    recall = recall_score(
        y_true,
        y_pred,
        zero_division=0
    )

    f1 = f1_score(
        y_true,
        y_pred,
        zero_division=0
    )

    # --------------------------------------------------------
    # CONFUSION MATRIX
    # --------------------------------------------------------

    cm = confusion_matrix(
        y_true,
        y_pred
    )

    fig, ax = plt.subplots(
        figsize=(6, 5)
    )

    disp = ConfusionMatrixDisplay(
        confusion_matrix=cm,
        display_labels=[
            "Normal",
            "Attack"
        ]
    )

    disp.plot(
        ax=ax
    )

    ax.set_title(
        "Confusion Matrix"
    )

    plt.tight_layout()

    # --------------------------------------------------------
    # CONVERT GRAPH TO PNG
    # --------------------------------------------------------

    buffer = BytesIO()

    plt.savefig(
        buffer,
        format="png",
        dpi=200,
        bbox_inches="tight"
    )

    plt.close()

    buffer.seek(0)

    graph = base64.b64encode(
        buffer.getvalue()
    ).decode("utf-8")

    return (
        accuracy,
        precision,
        recall,
        f1,
        graph
    )


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def home():

    return """
    <h1>Cloud Secure Python</h1>

    <p>
        Python application is running securely in the cloud!
    </p>

    <h2>Available endpoints</h2>

    <ul>
        <li>
            <a href="/health">
                Health
            </a>
        </li>

        <li>
            <a href="/research">
                Research Metrics
            </a>
        </li>

        <li>
            <a href="/logs">
                Security Logs
            </a>
        </li>
    </ul>

    <h3>Login API</h3>

    <p>
        POST /login
    </p>
    """


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route("/health")
def health():

    return jsonify({
        "status": "healthy",
        "cloud": "Render",
        "application": "Cloud Secure Python"
    })


# ============================================================
# LOGIN
# ============================================================

@app.route(
    "/login",
    methods=["POST"]
)
def login():

    data = request.get_json()

    if not data:

        return jsonify({
            "error": "Invalid request"
        }), 400

    username = data.get(
        "username"
    )

    password = data.get(
        "password"
    )

    ip = request.remote_addr

    if username != USERNAME:

        log_event(
            "Invalid username",
            ip
        )

        return jsonify({
            "error": "Invalid credentials"
        }), 401

    password_hash = hashlib.sha256(
        password.encode()
    ).hexdigest()

    if password_hash != PASSWORD_HASH:

        log_event(
            "Failed login attempt",
            ip
        )

        return jsonify({
            "error": "Invalid credentials"
        }), 401

    log_event(
        "Successful login",
        ip
    )

    return jsonify({
        "message": "Login successful"
    })


# ============================================================
# SECURITY LOGS
# ============================================================

@app.route("/logs")
def logs():

    return jsonify({
        "security_events": security_logs
    })


# ============================================================
# RESEARCH DASHBOARD
# ============================================================

@app.route("/research")
def research():

    (
        accuracy,
        precision,
        recall,
        f1,
        graph
    ) = create_metrics()

    return render_template_string("""

    <!DOCTYPE html>

    <html>

    <head>

        <title>
            Cloud Security Research
        </title>

        <style>

            body {

                font-family:
                    Arial,
                    sans-serif;

                max-width: 1100px;

                margin: auto;

                padding: 40px;

                background:
                    #f5f7fa;

            }

            h1 {

                text-align: center;

            }

            .metrics {

                display: flex;

                gap: 20px;

                margin-top: 30px;

                margin-bottom: 40px;

            }

            .card {

                background: white;

                padding: 25px;

                border-radius: 12px;

                box-shadow:
                    0 2px 8px
                    rgba(0,0,0,0.1);

                text-align: center;

                flex: 1;

            }

            .card h3 {

                margin-bottom: 15px;

            }

            .value {

                font-size: 30px;

                font-weight: bold;

            }

            .graph {

                background: white;

                padding: 25px;

                border-radius: 12px;

                text-align: center;

                box-shadow:
                    0 2px 8px
                    rgba(0,0,0,0.1);

            }

            img {

                max-width: 600px;

                width: 100%;

            }

        </style>

    </head>


    <body>

        <h1>
            Cloud Security Research Dashboard
        </h1>


        <div class="metrics">


            <div class="card">

                <h3>
                    Accuracy
                </h3>

                <div class="value">

                    {{ accuracy }}

                </div>

            </div>


            <div class="card">

                <h3>
                    Precision
                </h3>

                <div class="value">

                    {{ precision }}

                </div>

            </div>


            <div class="card">

                <h3>
                    Recall
                </h3>

                <div class="value">

                    {{ recall }}

                </div>

            </div>


            <div class="card">

                <h3>
                    F1-score
                </h3>

                <div class="value">

                    {{ f1 }}

                </div>

            </div>


        </div>


        <div class="graph">

            <h2>
                Confusion Matrix
            </h2>

            <img
                src="data:image/png;base64,{{ graph }}"
            >

        </div>


    </body>

    </html>

    """,

    accuracy=f"{accuracy:.4f}",

    precision=f"{precision:.4f}",

    recall=f"{recall:.4f}",

    f1=f"{f1:.4f}",

    graph=graph

    )


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=10000
    )
