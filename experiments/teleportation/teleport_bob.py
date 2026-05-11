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
