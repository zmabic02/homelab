import random
import time

from flask import Flask, render_template
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    Counter,
    Gauge,
    Histogram,
    generate_latest,
)

app = Flask(__name__)


REQUESTS = Counter(
    "demo_http_requests_total",
    "Total number of HTTP requests",
    ["method", "route", "status"],
)

ACTIVE_REQUESTS = Gauge(
    "demo_active_requests",
    "Number of HTTP requests currently being processed",
    ["route"],
)

REQUEST_DURATION = Histogram(
    "demo_http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["route"],
)


@app.route("/")
@ACTIVE_REQUESTS.labels(route="/").track_inprogress()
@REQUEST_DURATION.labels(route="/").time()
def index():
    REQUESTS.labels(
        method="GET",
        route="/",
        status="200",
    ).inc()

    return render_template("index.html")


@app.route("/slow")
@ACTIVE_REQUESTS.labels(route="/slow").track_inprogress()
@REQUEST_DURATION.labels(route="/slow").time()
def slow():
    time.sleep(random.uniform(2.0, 5.0))

    REQUESTS.labels(
        method="GET",
        route="/slow",
        status="200",
    ).inc()

    return "Slow response\n"


@app.route("/error")
@ACTIVE_REQUESTS.labels(route="/error").track_inprogress()
@REQUEST_DURATION.labels(route="/error").time()
def error():
    REQUESTS.labels(
        method="GET",
        route="/error",
        status="500",
    ).inc()

    return "Intentional error\n", 500


@app.route("/health")
def health():
    return "OK\n", 200


@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {
        "Content-Type": CONTENT_TYPE_LATEST,
    }


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8080,
    )