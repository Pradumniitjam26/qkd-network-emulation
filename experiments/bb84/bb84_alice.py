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
