
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_multivector
from IPython.display import display

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

    # Apply CNOT gate (control: q0, target: q1)
    qc.cx(0, 1)

    print(qc.draw())

    state = Statevector(qc)
    print("Statevector:")
    print(state)

    # Plot Bloch spheres for both qubits
    fig = plot_bloch_multivector(state)
    display(fig)
