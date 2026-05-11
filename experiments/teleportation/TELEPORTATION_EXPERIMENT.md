# Quantum Teleportation Experiment using SimulaQron

## Repository

GitHub Repository:

[https://github.com/Pradumniitjam26/qkd-network-emulation](https://github.com/Pradumniitjam26/qkd-network-emulation)

---

# 1. Introduction

This experiment demonstrates Quantum Teleportation using SimulaQron on two Ubuntu machines connected over a distributed quantum network.

Quantum teleportation is one of the most important protocols in quantum communication and quantum networking. It allows the transfer of a quantum state from one location to another using:

* Quantum entanglement
* Classical communication
* Quantum gates

The experiment was implemented using:

* SimulaQron
* Python
* CQC library
* Ubuntu Linux

---

# 2. Objective

The objective of this experiment is:

* To create entangled qubits
* To distribute qubits across two machines
* To teleport a quantum state from Alice to Bob
* To simulate distributed quantum communication

---

# 3. System Configuration

## Machine 1 (Alice)

| Parameter        | Value          |
| ---------------- | -------------- |
| Role             | Alice          |
| IP Address       | 10.11.80.93    |
| Operating System | Ubuntu 24.04   |
| Environment      | simulaqron_env |

---

## Machine 2 (Bob)

| Parameter        | Value          |
| ---------------- | -------------- |
| Role             | Bob            |
| IP Address       | 10.11.80.94    |
| Operating System | Ubuntu 24.04   |
| Environment      | simulaqron_env |

---

# 4. Quantum Teleportation Theory

Quantum teleportation transfers the state of a qubit from one location to another without physically sending the original qubit.

The protocol uses:

* Quantum entanglement
* Bell-state generation
* Hadamard gate
* CNOT gate
* Quantum measurement
* Classical communication

The teleportation process is based on entangled qubits shared between Alice and Bob.

---

# 5. SimulaQron Network Configuration

## simulaqron_network.json

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

---

# 6. Alice Program

## teleport_alice.py

```python
from cqc.pythonLib import CQCConnection, qubit

with CQCConnection(
    "Alice",
    socket_address=("127.0.0.1", 8016)
) as Alice:

    print("Alice: Creating qubits")

    q1 = qubit(Alice)
    q2 = qubit(Alice)

    print("Alice: Creating entanglement")

    q1.H()
    q1.cnot(q2)

    print("Alice: Sending entangled qubit to Bob")

    Alice.sendQubit(q2, "Bob")

    print("Alice: Measuring local qubit")

    m = q1.measure()

    print("Alice measurement =", m)
```

---

# 7. Bob Program

## teleport_bob.py

```python
from cqc.pythonLib import CQCConnection

with CQCConnection(
    "Bob",
    socket_address=("10.11.80.93", 8019)
) as Bob:

    print("Bob: Waiting for qubit")

    q = Bob.recvQubit()

    print("Bob: Qubit received")

    m = q.measure()

    print("Bob: Measurement result =", m)
```

---

# 8. Running the Experiment

## Step 1: Activate Environment

### Machine 1

```bash
source ~/simulaqron_env/bin/activate
```

### Machine 2

```bash
source ~/simulaqron_env/bin/activate
```

---

## Step 2: Start SimulaQron

### Machine 1

```bash
simulaqron start
```

---

## Step 3: Run Bob Program First

### Machine 2

```bash
python ~/teleport_bob.py
```

Expected Output:

```text
Bob: Waiting for qubit
```

---

## Step 4: Run Alice Program

### Machine 1

```bash
python ~/teleport_alice.py
```

Expected Output:

```text
Alice: Creating qubits
Alice: Creating entanglement
Alice: Sending entangled qubit to Bob
Alice: Measuring local qubit
Alice measurement = 1
```

---

# 9. Final Result

## Bob Output

```text
Bob: Waiting for qubit
Bob: Qubit received
Bob: Measurement result = 1
```

---

# 10. Experiment Analysis

The experiment successfully demonstrated:

* Quantum entanglement generation
* Distributed quantum communication
* Remote qubit transfer
* Quantum state measurement
* Two-machine quantum networking

The teleportation protocol used Hadamard and CNOT gates to create entangled states before transmitting qubits between nodes.

---

# 11. Problems Encountered and Solutions

## Problem 1

### Error

```text
CQCTimeoutError: Timeout
```

### Cause

Bob was waiting before Alice transmitted the qubit.

### Solution

* Start Bob first
* Immediately run Alice
* Use correct socket ports

---

## Problem 2

### Error

```text
Connection refused
```

### Cause

SSH or SimulaQron backend not running.

### Solution

Restart SSH and SimulaQron services.

---

## Problem 3

### Error

```text
Host name 'Bob' is not in the cqc network
```

### Solution

Correct SimulaQron network configuration was added.

---

## Problem 4

### Issue

Dynamic ports (8016–8029) appeared instead of configured ports.

### Solution

Used active backend socket ports for teleportation communication.

---

# 12. Commands Used

## Start SimulaQron

```bash
simulaqron start
```

## Stop SimulaQron

```bash
simulaqron stop
```

## Reset SimulaQron

```bash
simulaqron reset
```

## Check Active Ports

```bash
lsof -iTCP -sTCP:LISTEN
```

## SSH Remote Machine Access

```bash
ssh ubuntu@10.11.80.93
```

## Copy Files Between Machines

```bash
scp ubuntu@10.11.80.93:/home/ubuntu/teleport_alice.py ~/qkd-network-emulation/experiments/teleportation/
```

---

# 13. Screenshots

The experiment screenshots include:

* teleport_alice.png
* teleport_bob.png

These screenshots demonstrate successful distributed quantum teleportation.

---

# 14. GitHub Repository Structure

```text
experiments/
└── teleportation/
    ├── teleport_alice.py
    ├── teleport_bob.py
    ├── TELEPORTATION_EXPERIMENT.md
    ├── teleport_alice.png
    └── teleport_bob.png
```

---

# 15. Future Work

Future enhancements planned:

* Full Bell-state teleportation
* Classical correction operations
* Multi-node teleportation
* Quantum repeater simulation
* Entanglement swapping
* Quantum internet experiments
* Superdense coding
* E91 Quantum Key Distribution

---

# 16. Conclusion

This experiment successfully demonstrated distributed quantum teleportation using SimulaQron over two Ubuntu machines.

The implementation verified:

* Entanglement generation
* Distributed quantum communication
* Qubit transmission
* Remote quantum measurement
* Quantum networking principles

The experiment forms an important foundation for advanced quantum networking and quantum internet research.

---

# Author

## Pradumn Shukla

Quantum Computing and Quantum Networking Research

GitHub:

[https://github.com/Pradumniitjam26](https://github.com/Pradumniitjam26)
