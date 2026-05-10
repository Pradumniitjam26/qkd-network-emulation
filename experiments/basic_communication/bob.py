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
