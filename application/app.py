from flask import Flask, jsonify, Response, request
import time
import logging

from prometheus_client import (
    Counter,
    Histogram,
    generate_latest,
    CONTENT_TYPE_LATEST
)

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

REQUEST_COUNT = Counter(
    "banking_app_requests_total",
    "Total number of HTTP requests",
    ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "banking_app_request_latency_seconds",
    "HTTP request processing time",
    ["endpoint"]
)

@app.before_request
def start_timer():
    request.start_time = time.time()

@app.after_request
def record_metrics(response):
    if request.path != "/metrics":
        REQUEST_COUNT.labels(
            request.method,
            request.path,
            str(response.status_code)
        ).inc()

        REQUEST_LATENCY.labels(
            request.path
        ).observe(time.time() - request.start_time)

    return response

@app.route("/")
def home():
    logging.info("Banking application homepage accessed")
    return jsonify({
        "application": "Banking Application",
        "status": "running"
    })

@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200

@app.route("/transactions")
def transactions():
    logging.info("Transaction API accessed")
    return jsonify({
        "transactions": [
            {"id": 101, "amount": 5000},
            {"id": 102, "amount": 2500}
        ]
    })

@app.route("/slow")
def slow():
    time.sleep(5)
    logging.warning("Slow API response detected")
    return jsonify({"message": "Slow response simulated"})

@app.route("/simulate-error")
def simulate_error():
    logging.error("Simulated application failure detected")
    return jsonify({
        "error": "Simulated internal server error"
    }), 500


@app.route("/metrics")
def metrics():
    return Response(
        generate_latest(),
        content_type=CONTENT_TYPE_LATEST
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
