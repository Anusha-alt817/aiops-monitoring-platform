# Banking API Troubleshooting Runbook

## 1. Purpose
Troubleshoot HTTP 5xx errors, application failures, and slow API responses
in the Dockerized banking application.

## 2. Application Environment
- Application: Flask banking application
- Docker container: banking-container
- Docker image: banking-app:v3
- Application port: 5000
- Health endpoint: /health
- Metrics endpoint: /metrics
- Monitoring: Prometheus and Grafana

## 3. Symptoms
- HTTP 500 or other HTTP 5xx responses
- Application ERROR messages
- Slow API response warnings
- Health endpoint failures
- Increased API response latency

## 4. Investigation Steps

### Step 1: Check container status
Command:
docker ps -a --filter name=banking-container

Expected:
Container should be running.

### Step 2: Inspect application logs
Command:
docker logs --since 30m --timestamps banking-container

Look for:
- ERROR messages
- Python exceptions
- Stack traces
- Dependency failures

### Step 3: Check container resource usage
Command:
docker stats banking-container --no-stream

Review:
- CPU usage
- Memory usage
- Memory limits

### Step 4: Check application health
Command:
curl -i http://127.0.0.1:5000/health

Expected:
HTTP 200 response when the application is healthy.

### Step 5: Check application metrics
Command:
curl -s http://127.0.0.1:5000/metrics

Review:
- Request counters
- HTTP status codes
- Request latency metrics

### Step 6: Investigate HTTP 5xx errors
Command:
docker logs banking-container 2>&1 | grep -i -E 'error|exception|traceback'

Review the error message and surrounding stack trace.

### Step 7: Investigate slow API responses
Check application logs and Prometheus latency metrics.
Compare average and P95 latency over the incident window.

## 5. Possible Root Causes
- Application code exceptions
- Dependency service failures
- Database connectivity problems
- Slow external API calls
- Resource constraints
- Application configuration errors

These are hypotheses and must be verified using evidence.

## 6. Recommended Actions
- Identify the failing endpoint.
- Review application stack traces.
- Verify dependency health.
- Check CPU and memory utilization.
- Compare API latency before and during the incident.
- Validate the proposed fix before deployment.

## 7. Prevention
- Configure HTTP 5xx alerts.
- Monitor P95 API latency.
- Centralize application logs.
- Add health checks.
- Maintain incident history.
- Review recurring application failures.

## 8. Safety
Do not restart containers, change infrastructure,
or deploy fixes without human approval.
