from flask import Flask
import socket

app = Flask(__name__)

@app.route("/")
def home():
    return f"Production Kubernetes App Running on {socket.gethostname()}"

@app.route("/health")
def health():
    return {"status": "healthy"}, 200

@app.route("/metrics")
def metrics():
    return "app_requests_total 1"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)