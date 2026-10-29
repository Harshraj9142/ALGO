
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_multivector
from IPython.display import display


def swap(qc: QuantumCircuit):
    # SWAP built from three CNOT gates
    qc.cx(0, 1)
    qc.cx(1, 0)
    qc.cx(0, 1)


# Input labels are written as q0 q1 (Qiskit prints states as q1 q0)
inputs = ["00", "01", "10", "11"]

for bits in inputs:
    print(f"\n--- Input state |{bits}> ---")

    qc = QuantumCircuit(2)

    # Prepare the input state
    if bits[0] == "1":
        qc.x(0)
    if bits[1] == "1":
        qc.x(1)

    # Same input, swapped with the three-CNOT decomposition
    qc_cx = qc.copy()
    swap(qc_cx)

    # Apply built-in SWAP gate
    qc.swap(0, 1)

    print("Built-in SWAP:")
    print(qc.draw())
    print("SWAP from three CNOTs:")
    print(qc_cx.draw())

    state = Statevector(qc)
    print("Statevector:")
    print(state)
    print("Three-CNOT SWAP matches built-in:", state.equiv(Statevector(qc_cx)))

    # Plot Bloch spheres for both qubits
    fig = plot_bloch_multivector(state)
    display(fig)
