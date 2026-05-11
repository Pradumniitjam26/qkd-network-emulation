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
