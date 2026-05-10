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
