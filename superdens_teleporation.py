
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import matplotlib.pyplot as plt

inputs = ["00", "01", "10", "11"]

for bits in inputs:
    print("\nInput:", bits)

    qc = QuantumCircuit(2)

    # Create shared Bell pair
    qc.h(0)
    qc.cx(0, 1)

    # Alice encodes the input
    if bits == "00":
        pass
    elif bits == "01":
        qc.x(0)
    elif bits == "10":
        qc.z(0)
    elif bits == "11":
        qc.x(0)
        qc.z(0)

    print("\nAlice's encoded circuit:")
    print(qc.draw())

    state = Statevector(qc)
    print("\nEncoded state:")
    print(state.draw("latex_source"))

    # Bob decodes the input
    qc.cx(0, 1)
    qc.h(0)

    print("\nBob's decoding circuit:")
    print(qc.draw())

    state = Statevector(qc)
    print("\nDecoded state:")
    print(state.draw("latex_source"))

    # Save Q-sphere plot
    fig = state.draw("qsphere")
    fig.savefig(
        f"superdense_input_{bits}_qsphere.png",
        bbox_inches="tight",
        dpi=150
    )
    plt.close(fig)

print("\nAll Q-sphere plots saved as PNG files in the current folder.")
