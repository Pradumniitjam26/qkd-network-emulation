# bb84_receiver.py
# QUANTUM LAYER - BOB (RECEIVER)

from cqc.pythonLib import CQCConnection
from cqc.pythonLib.util import CQCTimeoutError

import random
import time

N = 50


class BB84Receiver:

    def __init__(self):

        self.bob_bases = []
        self.bob_results = []

        self.received_qubits = 0

    # =====================================================
    # RESET SESSION
    # =====================================================

    def reset(self):

        self.bob_bases.clear()
        self.bob_results.clear()

        self.received_qubits = 0

    # =====================================================
    # RANDOM BASIS
    # =====================================================

    def random_basis(self):

        return random.randint(0, 1)

    # =====================================================
    # MEASURE QUBIT
    # =====================================================

    def measure_qubit(self, q, basis):

        if basis == 1:
            q.H()

        return q.measure()

    # =====================================================
    # RECEIVE SINGLE QUBIT
    # =====================================================

    def receive_qubit(self, connection, index):

        while True:

            try:

                q = connection.recvQubit()

                return q

            except CQCTimeoutError:

                print(
                    f"[BOB] Waiting for qubit {index}..."
                )

                time.sleep(1)

            except Exception as e:

                print(
                    f"[BOB] Receive error: {e}"
                )

                time.sleep(1)

    # =====================================================
    # RUN RECEIVER
    # =====================================================

    def run(self):

        self.reset()

        print("\n" + "=" * 60)
        print(" BB84 RECEIVER (BOB)")
        print("=" * 60)

        with CQCConnection(
            "Bob",
            socket_address=("10.11.80.93", 8005)
        ) as Bob:

            for i in range(N):

                basis = self.random_basis()

                self.bob_bases.append(basis)

                q = self.receive_qubit(
                    Bob,
                    i
                )

                result = self.measure_qubit(
                    q,
                    basis
                )

                self.bob_results.append(result)

                self.received_qubits += 1

                print(
                    f"[BOB] Qubit {i} | "
                    f"basis={basis} "
                    f"result={result}"
                )

                time.sleep(0.05)

        print("\nReception Complete")
        print(f"Received Qubits: {self.received_qubits}")

        return {
            "bases": self.bob_bases,
            "results": self.bob_results,
            "count": self.received_qubits
        }


# =========================================================
# STANDALONE EXECUTION
# =========================================================

if __name__ == "__main__":

    receiver = BB84Receiver()

    results = receiver.run()

    print("\nRaw Receiver Key:")
    print(receiver.bob_results)
