from cqc.pythonLib import CQCConnection, qubit

with CQCConnection("Alice") as Alice:
    print("Alice: Creating qubit")

    q = qubit(Alice)
    q.H()

    print("Alice: Sending qubit to Bob")
    Alice.sendQubit(q, "Bob")

    print("Alice: Done")
