# Complete Guide: SimulaQron Communication Between Two Ubuntu Machines Over LAN

## Objective

This guide explains how to configure two Ubuntu systems connected through the same LAN network and establish quantum communication using SimulaQron.

The setup enables:

* Quantum qubit transmission
* Distributed quantum network simulation
* Remote CQC communication
* Quantum networking experiments

The final result allows one machine (Alice) to create and send a qubit, while another machine (Bob) receives and measures it.

---

# System Architecture

## Machines Used

| Machine   | Role                       | IP Address  |
| --------- | -------------------------- | ----------- |
| Machine 1 | SimulaQron Backend + Alice | 10.11.80.93 |
| Machine 2 | Remote Bob Client          | 10.11.80.94 |

---

# Important Notes

## Why Python 3.10 Was Required

SimulaQron and CQC libraries are not fully compatible with Python 3.12.

Using Python 3.12 caused:

* Twisted installation failures
* CQC import errors
* Backend startup failures
* SimulaQron incompatibility

Therefore Python 3.10 was installed and used.

---

# Step 1 — Verify LAN Connectivity

Both systems must be connected to the same LAN network.

## Test Ping

From Machine 1:

```bash
ping 10.11.80.94
```

Expected:

```text
64 bytes from 10.11.80.94
```

From Machine 2:

```bash
ping 10.11.80.93
```

---

# Step 2 — Install Python 3.10

Run on BOTH machines.

```bash
sudo apt update
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install python3.10 python3.10-venv python3.10-dev -y
```

---

# Step 3 — Create Virtual Environment

Run on BOTH machines.

```bash
python3.10 -m venv simulaqron_env
```

Activate environment:

```bash
source simulaqron_env/bin/activate
```

Expected prompt:

```text
(simulaqron_env)
```

---

# Step 4 — Install Compatible SimulaQron Versions

Run on BOTH machines.

## Remove Old Packages

```bash
pip uninstall -y cqc simulaqron twisted
```

## Install Compatible Versions

```bash
pip install twisted==20.3.0
pip install cqc==3.2.3
pip install simulaqron==3.0.16
```

---

# Step 5 — Verify Installation

Run:

```bash
pip list | grep -E "simulaqron|cqc|Twisted"
```

Expected:

```text
cqc               3.2.3
simulaqron        3.0.16
Twisted           20.3.0
```

---

# Step 6 — Reset SimulaQron

Run on BOTH machines.

```bash
simulaqron reset
```

Type:

```text
yes
```

---

# Step 7 — Start SimulaQron Backend

## Important Final Working Configuration

The stable working setup used:

* SimulaQron backend running on Machine 1
* Machine 2 acting as remote Bob client

This avoids distributed daemon startup issues.

---

# Step 7A — Configure SimulaQron Network JSON File

The network JSON file defines:

* Node names
* IP addresses
* CQC ports
* Virtual node ports
* QNodeOS ports

This file is essential for communication between Alice and Bob.

---

## Configure Network File on BOTH Machines

Open:

```bash
nano ~/.simulaqron/simulaqron_network.json
```

Delete existing contents and paste:

```json
[
    {
        "name": "default",
        "nodes": [
            {
                "Alice": {
                    "app_socket": [
                        "10.11.80.93",
                        8000
                    ],
                    "cqc_socket": [
                        "10.11.80.93",
                        8001
                    ],
                    "vnode_socket": [
                        "10.11.80.93",
                        8002
                    ],
                    "qnodeos_socket": [
                        "10.11.80.93",
                        8003
                    ]
                }
            },
            {
                "Bob": {
                    "app_socket": [
                        "10.11.80.94",
                        8004
                    ],
                    "cqc_socket": [
                        "10.11.80.94",
                        8005
                    ],
                    "vnode_socket": [
                        "10.11.80.94",
                        8006
                    ],
                    "qnodeos_socket": [
                        "10.11.80.94",
                        8007
                    ]
                }
            }
        ],
        "topology": null
    }
]
```

Save:

* CTRL + O
* ENTER
* CTRL + X

---

## Verify Network File

Run:

```bash
cat ~/.simulaqron/simulaqron_network.json
```

Ensure:

* Alice IP = `10.11.80.93`
* Bob IP = `10.11.80.94`
* JSON ends with:

```json
]
```

---

## Why This File Is Important

This configuration tells SimulaQron:

* where Alice is located
* where Bob is located
* which ports to use
* how quantum communication should route between nodes

Without this file:

* nodes cannot discover each other
* `Host name 'Bob' is not in the cqc network` errors occur
* remote qubit transmission fails

---

# Step 8 — Start SimulaQron on Machine 1

Machine 1 IP:

```text
10.11.80.93
```

Run:

```bash
simulaqron start
```

If prompted:

```text
Do you want to add/replace the network...
```

Type:

```text
yes
```

---

# Step 9 — Verify Active Ports

On Machine 1:

```bash
lsof -iTCP -sTCP:LISTEN
```

Example working output:

```text
*:8016
*:8017
*:8019
*:8020
```

Important ports:

| Purpose     | Port |
| ----------- | ---- |
| Alice CQC   | 8016 |
| Alice vnode | 8017 |
| Bob CQC     | 8019 |
| Bob vnode   | 8020 |

---

# Step 10 — Create Alice Program

On Machine 1:

```bash
nano ~/alice.py
```

Paste:

```python
from cqc.pythonLib import CQCConnection, qubit

with CQCConnection(
    "Alice",
    socket_address=("127.0.0.1", 8016)
) as Alice:

    print("Alice: Creating qubit")

    q = qubit(Alice)

    q.H()

    print("Alice: Sending qubit")

    Alice.sendQubit(q, "Bob")

    print("Alice: Done")
```

Save:

* CTRL + O
* ENTER
* CTRL + X

---

# Step 11 — Create Bob Program

On Machine 2:

```bash
nano ~/bob.py
```

Paste:

```python
from cqc.pythonLib import CQCConnection

with CQCConnection(
    "Bob",
    socket_address=("10.11.80.93", 8019)
) as Bob:

    print("Bob waiting")

    q = Bob.recvQubit()

    print("Received")

    m = q.measure()

    print("Measurement =", m)
```

Save:

* CTRL + O
* ENTER
* CTRL + X

---

# Step 12 — Test LAN Port Connectivity

From Machine 2:

```bash
nc -zv 10.11.80.93 8019
```

Expected:

```text
Connection succeeded
```

---

# Step 13 — Run Quantum Communication

## Step A — Start Bob First

On Machine 2:

```bash
python ~/bob.py
```

Expected:

```text
Bob waiting
```

Keep terminal open.

---

## Step B — Run Alice

On Machine 1:

```bash
python ~/alice.py
```

Expected:

```text
Alice: Creating qubit
Alice: Sending qubit
Alice: Done
```

---

# Step 14 — Verify Successful Quantum Communication

Machine 2 output:

```text
Bob waiting
Received
Measurement = 0
```

or:

```text
Measurement = 1
```

---

# Why Measurement Changes Between 0 and 1

The command:

```python
q.H()
```

applies a Hadamard gate.

This creates a quantum superposition:

```math
|+> = (|0> + |1>) / sqrt(2)
```

Therefore measurement randomly collapses to:

* 0
* or 1

with equal probability.

---

# Final Working Architecture

## Machine 1

* Runs SimulaQron backend
* Runs Alice
* Hosts CQC ports
* Simulates quantum network

## Machine 2

* Runs Bob client
* Connects remotely through LAN
* Receives qubits
* Measures qubits

---

# Important Problems Encountered and Solutions

## Problem 1 — Python 3.12 Incompatibility

### Error

```text
Twisted build failed
```

### Solution

Installed Python 3.10.

---

## Problem 2 — Missing cqc Module

### Error

```text
ModuleNotFoundError: No module named 'cqc'
```

### Solution

Installed:

```bash
pip install cqc==3.2.3
```

---

## Problem 3 — SimulaQron Version Mismatch

### Error

```text
need simulaqron>=3.0.0 installed
```

### Solution

Installed compatible versions:

```bash
simulaqron==3.0.16
cqc==3.2.3
Twisted==20.3.0
```

---

## Problem 4 — Port Connection Refused

### Error

```text
Connection refused
```

### Cause

SimulaQron backend not listening on required CQC port.

### Solution

Used actual active generated ports from backend.

---

## Problem 5 — Bob Timeout

### Error

```text
CQCTimeoutError
```

### Cause

Alice failed to send qubit correctly.

### Solution

Fixed active CQC port mapping.

---

# Commands Frequently Used

## Check Listening Ports

```bash
lsof -iTCP -sTCP:LISTEN
```

---

## Test Port Connectivity

```bash
nc -zv IP_ADDRESS PORT
```

---

## Stop SimulaQron

```bash
simulaqron stop
```

---

## Start SimulaQron

```bash
simulaqron start
```

---

## Reset SimulaQron

```bash
simulaqron reset
```

---

# Future Experiments Possible

This setup can now be used for:

* Quantum teleportation
* BB84 quantum key distribution
* E91 quantum cryptography
* Entanglement distribution
* Quantum repeaters
* Multi-node quantum internet simulation
* Quantum routing protocols
* Quantum networking research

---

# Conclusion

A fully working distributed SimulaQron quantum communication setup was successfully created between two Ubuntu machines connected over LAN.

The system now supports:

* Remote quantum communication
* Distributed qubit transmission
* Quantum measurement experiments
* Quantum networking protocol development

This setup provides a practical foundation for advanced quantum internet and quantum communication research.
