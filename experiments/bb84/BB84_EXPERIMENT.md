# BB84 Quantum Key Distribution Experiment Using SimulaQron Between Two Ubuntu Machines

# Objective

This experiment demonstrates BB84 Quantum Key Distribution (QKD) using SimulaQron over LAN between two Ubuntu machines.

The BB84 protocol is the first and most famous quantum cryptography protocol.

It allows two parties:

* Alice
* Bob

to generate a secure secret cryptographic key using quantum mechanics.

---

# What This Experiment Demonstrates

This setup demonstrates:

* Quantum key distribution
* Quantum superposition
* Quantum measurement
* Random quantum states
* Quantum cryptography
* Secure communication
* Basis mismatch detection
* Quantum no-cloning principle

---

# Experimental Setup

| Machine   | Role                       | IP Address  |
| --------- | -------------------------- | ----------- |
| Machine 1 | Alice + SimulaQron Backend | 10.11.80.93 |
| Machine 2 | Bob                        | 10.11.80.94 |

---

# Architecture

## Machine 1

Runs:

* SimulaQron backend
* Alice BB84 sender

Responsibilities:

* Generate random bits
* Generate random bases
* Encode qubits
* Send qubits to Bob

---

## Machine 2

Runs:

* Bob BB84 receiver

Responsibilities:

* Receive qubits
* Randomly choose measurement basis
* Measure qubits
* Generate shared secret key

---

# Prerequisites

Before performing BB84:

You must already have:

* Ubuntu installed on both systems
* LAN connection working
* SimulaQron installed
* CQC installed
* Two-machine qubit communication working

---

# Required Package Versions

Run on BOTH machines:

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

# Step 1 — Start SimulaQron Backend

On Machine 1:

```bash
simulaqron stop
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

# Step 2 — Verify Active Ports

On Machine 1:

```bash
lsof -iTCP -sTCP:LISTEN
```

Important ports:

| Purpose     | Port |
| ----------- | ---- |
| Alice CQC   | 8016 |
| Alice vnode | 8017 |
| Bob CQC     | 8019 |
| Bob vnode   | 8020 |

---

# Step 3 — Create BB84 Alice Program

On Machine 1:

```bash
nano ~/bb84_alice.py
```

Paste the following complete code:

```python
from cqc.pythonLib import CQCConnection, qubit
import random
import time

N = 10

alice_bits = []
alice_bases = []

with CQCConnection(
    "Alice",
    socket_address=("127.0.0.1", 8016)
) as Alice:

    print("Alice starting BB84")

    for i in range(N):

        bit = random.randint(0, 1)
        basis = random.randint(0, 1)

        alice_bits.append(bit)
        alice_bases.append(basis)

        q = qubit(Alice)

        # Encode bit
        if bit == 1:
            q.X()

        # Encode basis
        if basis == 1:
            q.H()

        print(f"Sending qubit {i}: bit={bit}, basis={basis}")

        Alice.sendQubit(q, "Bob")

        time.sleep(1)

print("\nAlice bits:", alice_bits)
print("Alice bases:", alice_bases)
```

Save:

* CTRL + O
* ENTER
* CTRL + X

---

# Step 4 — Create BB84 Bob Program

On Machine 2:

```bash
nano ~/bb84_bob.py
```

Paste the following complete code:

```python
from cqc.pythonLib import CQCConnection
import random

N = 10

bob_bases = []
bob_results = []

with CQCConnection(
    "Bob",
    socket_address=("10.11.80.93", 8019)
) as Bob:

    print("Bob starting BB84")

    for i in range(N):

        basis = random.randint(0, 1)
        bob_bases.append(basis)

        q = Bob.recvQubit()

        # Measurement basis
        if basis == 1:
            q.H()

        result = q.measure()

        bob_results.append(result)

        print(f"Received qubit {i}: basis={basis}, result={result}")

print("\nBob bases:", bob_bases)
print("Bob results:", bob_results)
```

Save:

* CTRL + O
* ENTER
* CTRL + X

---

# Step 5 — Test LAN Port Connectivity

From Machine 2:

```bash
nc -zv 10.11.80.93 8019
```

Expected:

```text
Connection succeeded
```

---

# Step 6 — Run BB84 Experiment

## Machine 2 FIRST

Run Bob:

```bash
python ~/bb84_bob.py
```

Expected:

```text
Bob starting BB84
```

Keep terminal open.

---

## Machine 1 SECOND

Run Alice:

```bash
python ~/bb84_alice.py
```

---

# Expected Alice Output

Example:

```text
Alice starting BB84
Sending qubit 0: bit=1, basis=1
Sending qubit 1: bit=0, basis=0
Sending qubit 2: bit=1, basis=0
...
```

Final output:

```text
Alice bits: [1, 0, 1, 1, 0, 1, 0, 1, 0, 0]
Alice bases: [1, 0, 0, 0, 1, 0, 1, 0, 1, 1]
```

---

# Expected Bob Output

Example:

```text
Bob starting BB84
Received qubit 0: basis=1, result=1
Received qubit 1: basis=0, result=0
Received qubit 2: basis=1, result=1
...
```

Final output:

```text
Bob bases: [1, 0, 1, 1, 0, 0, 1, 0, 1, 0]
Bob results: [1, 0, 1, 0, 0, 1, 0, 1, 1, 0]
```

---

# Understanding BB84 Bases

| Basis Value | Meaning     |
| ----------- | ----------- |
| 0           | Z Basis (+) |
| 1           | X Basis (×) |

---

# Quantum Encoding Process

## Bit Encoding

| Bit | Operation    |
| --- | ------------ |
| 0   | No operation |
| 1   | X gate       |

---

## Basis Encoding

| Basis | Operation           |
| ----- | ------------------- |
| 0     | Computational basis |
| 1     | Hadamard basis      |

---

# Quantum States Used in BB84

| Bit | Basis | Quantum State |    |
| --- | ----- | ------------- | -- |
| 0   | Z     |               | 0⟩ |
| 1   | Z     |               | 1⟩ |
| 0   | X     |               | +⟩ |
| 1   | X     |               | -⟩ |

---

# How Secret Key Is Generated

After transmission:

* Alice and Bob compare ONLY bases
* They do NOT reveal actual bits

If bases match:

* Keep bit

If bases differ:

* Discard bit

Remaining bits become the secret key.

---

# Example Key Extraction

## Alice

```text
bits   = [1,0,1,1]
bases  = [0,1,1,0]
```

## Bob

```text
bases  = [0,0,1,1]
results= [1,1,1,0]
```

---

# Basis Comparison

| Position | Alice Basis | Bob Basis | Keep? |
| -------- | ----------- | --------- | ----- |
| 0        | 0           | 0         | Yes   |
| 1        | 1           | 0         | No    |
| 2        | 1           | 1         | Yes   |
| 3        | 0           | 1         | No    |

---

# Final Secret Key

```text
1 1
```

---

# Why BB84 Is Secure

If an eavesdropper (Eve) measures qubits:

* Quantum states collapse
* Measurement changes qubits
* Alice and Bob detect errors

This provides:

* Eavesdropping detection
* Quantum security
* Information-theoretic security

---

# Important Quantum Concepts Demonstrated

This experiment demonstrates:

* Quantum superposition
* Quantum measurement collapse
* No-cloning theorem
* Random quantum states
* Quantum cryptography
* Secure key distribution
* Quantum communication

---

# Common Problems and Solutions

# Problem 1 — Connection Refused

## Error

```text
Connection refused
```

## Cause

SimulaQron backend not listening.

## Solution

Restart backend:

```bash
simulaqron stop
simulaqron start
```

---

# Problem 2 — CQCTimeoutError

## Error

```text
CQCTimeoutError
```

## Cause

Bob started after Alice finished.

## Solution

Always:

1. Start Bob first
2. Start Alice second

---

# Problem 3 — Host Name Not In Network

## Error

```text
Host name 'Bob' is not in the cqc network
```

## Cause

Broken network configuration.

## Solution

Fix:

```bash
~/.simulaqron/simulaqron_network.json
```

---

# Problem 4 — No Module Named cqc

## Error

```text
ModuleNotFoundError: No module named 'cqc'
```

## Solution

Install correct version:

```bash
pip install cqc==3.2.3
```

---

# Problem 5 — Python 3.12 Errors

## Cause

SimulaQron incompatibility with Python 3.12.

## Solution

Use Python 3.10.

---

# Important Commands

## Activate Environment

```bash
source simulaqron_env/bin/activate
```

---

## Check Ports

```bash
lsof -iTCP -sTCP:LISTEN
```

---

## Check Connectivity

```bash
nc -zv IP PORT
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

# Future Improvements

You can extend this experiment with:

* Eve eavesdropper simulation
* Error rate calculation
* Automatic key extraction
* Privacy amplification
* Authentication channel
* Entanglement-based QKD
* E91 protocol

---

# Conclusion

A fully working BB84 Quantum Key Distribution experiment was successfully implemented between two Ubuntu machines using SimulaQron over LAN.

The setup demonstrates:

* Distributed quantum communication
* Quantum cryptography
* Secure key generation
* Quantum networking
* Practical quantum internet concepts

This experiment forms the foundation for advanced quantum communication and quantum cybersecurity research.
