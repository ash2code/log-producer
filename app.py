import logging
import time
import random
import sys
import os

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("log-producer")

# Simulated services and events
SERVICES = ["auth-service", "payment-service", "user-service", "inventory-service", "notification-service"]
USERS = ["user_1042", "user_2891", "user_3374", "user_5512", "user_7723"]
ENDPOINTS = ["/api/login", "/api/checkout", "/api/profile", "/api/cart", "/api/order"]

INFO_MESSAGES = [
    lambda: f"Request received: GET {random.choice(ENDPOINTS)} from {random.choice(USERS)}",
    lambda: f"Service {random.choice(SERVICES)} responded in {random.randint(10, 300)}ms",
    lambda: f"Cache hit for key: session_{random.randint(1000,9999)}",
    lambda: f"Database query executed in {random.randint(5, 150)}ms, rows returned: {random.randint(1,100)}",
    lambda: f"User {random.choice(USERS)} successfully authenticated",
    lambda: f"Health check passed for {random.choice(SERVICES)}",
    lambda: f"Processed {random.randint(1,50)} messages from queue",
    lambda: f"Config reloaded: {random.randint(5,20)} keys updated",
]

WARNING_MESSAGES = [
    lambda: f"High latency detected on {random.choice(SERVICES)}: {random.randint(500, 2000)}ms",
    lambda: f"Retry attempt {random.randint(1,3)}/3 for {random.choice(ENDPOINTS)}",
    lambda: f"Memory usage at {random.randint(70,89)}% of limit",
    lambda: f"Rate limit approaching for {random.choice(USERS)}: {random.randint(80,99)}% used",
    lambda: f"Deprecated API version called by {random.choice(SERVICES)}",
    lambda: f"Slow query detected ({random.randint(1000,5000)}ms): SELECT * FROM orders",
]

ERROR_MESSAGES = [
    lambda: f"Connection timeout to {random.choice(SERVICES)} after {random.randint(3000,5000)}ms",
    lambda: f"Failed to process payment for {random.choice(USERS)}: insufficient funds",
    lambda: f"NullPointerException in {random.choice(SERVICES)} at line {random.randint(100,500)}",
    lambda: f"Database connection pool exhausted: {random.randint(50,100)}/100 connections in use",
    lambda: f"HTTP 500 returned for {random.choice(ENDPOINTS)}: internal server error",
]

DEBUG_MESSAGES = [
    lambda: f"Entering function: validate_token(user_id={random.randint(1000,9999)})",
    lambda: f"Raw SQL: SELECT id, name FROM users WHERE active=1 LIMIT {random.randint(10,100)}",
    lambda: f"Cache miss for key: product_{random.randint(1,500)}, fetching from DB",
    lambda: f"Token expiry: {random.randint(1,24)}h remaining for {random.choice(USERS)}",
]

def emit_log():
    roll = random.random()
    if roll < 0.55:
        logger.info(random.choice(INFO_MESSAGES)())
    elif roll < 0.75:
        logger.debug(random.choice(DEBUG_MESSAGES)())
    elif roll < 0.90:
        logger.warning(random.choice(WARNING_MESSAGES)())
    else:
        logger.error(random.choice(ERROR_MESSAGES)())

def main():
    interval = float(os.environ.get("LOG_INTERVAL", "1.0"))
    logger.info(f"Log producer started. Emitting logs every {interval}s")
    logger.info(f"Pod: {os.environ.get('POD_NAME', 'unknown')} | Namespace: {os.environ.get('POD_NAMESPACE', 'unknown')}")

    count = 0
    while True:
        emit_log()
        count += 1
        if count % 50 == 0:
            logger.info(f"--- Milestone: {count} logs emitted ---")
        time.sleep(interval)

if __name__ == "__main__":
    main()
