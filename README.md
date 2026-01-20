# Simulated HPC Job Queue (Async API + Robot Framework)

A demonstration of testing an asynchronous microservices architecture using **FastAPI**, **Redis**, and a **Hybrid Robot Framework** strategy.

## 🚀 Overview

This project simulates a High-Performance Computing (HPC) environment where users submit complex matrix calculation jobs. Because the jobs are computationally expensive, the system is designed asynchronously:

1.  **API:** Accepts the job and immediately returns a Job ID (FastAPI).
2.  **Broker:** Queues the task (Redis).
3.  **Worker:** Processes the matrix multiplication in the background (Python/Numpy).

**The Challenge:** Testing this end-to-end is difficult because standard HTTP tests fail on race conditions (the job is not done when the HTTP request returns).

**The Solution:** A custom Robot Framework architecture that utilizes a Python-based **Keyword Library** to handle polling, timeouts, and business logic validation.

## 🏗️ Architecture

- **Backend:** FastAPI (Python 3.12)
- **Queue:** Redis (Alpine)
- **Worker:** Python + Numpy for matrix operations
- **Infrastructure:** Docker Compose

## 🧪 The "Hybrid" Testing Strategy

Instead of writing fragile logic inside `.robot` files, this project uses the **Keyword-Driven Testing** pattern extended with real Python code.

- **`test_hpc.robot`**: Handles the high-level test scenarios (readability).
- **`JobLibrary.py`**: A custom Python library that extends Robot Framework. It handles:
  - **Smart Polling:** Retries the status endpoint until completion or timeout.
  - **Data Validation:** Verifies complex mathematical outputs (Matrix Size calculations) that are hard to do in pure Robot syntax.

## 📂 Project Structure

```text
.
├── main.py             # FastAPI entry point
├── worker.py           # Background worker (consumes Redis queue)
├── JobLibrary.py       # [KEY] Custom Robot Framework Python Library
├── test_hpc.robot      # Integration Test Suite
├── docker-compose.yml  # Container orchestration
└── Dockerfile          # Unified build for API and Worker

```

## 🛠️ How to Run

### Prerequisites

- Docker & Docker Compose
- Python 3.x (for running Robot Framework locally)

### 1. Start the Environment

Launch the API, Redis, and Worker containers:

```bash
docker-compose up --build
```

_Wait until you see `[_] Worker Node Started` in the logs.\*

### 2. Install Test Dependencies

Open a new terminal window:

```bash
pip install robotframework robotframework-requests requests
```

### 3. Run the Test Suite

Execute the integration tests:

```bash
robot test_hpc.robot
```

## ✅ Test Scenarios Covered

1. **Valid Job Flow:** Submits a job -> Polls for 'completed' status -> Verifies matrix calculation accuracy.
2. **Error Handling:** Submits a job with excessive complexity -> Verifies that the Worker correctly identifies and fails the job -> Verifies the API reports the failure message.

![Test Results](./test_results.png)
