
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_multivector
from IPython.display import display

combinations = [
    (0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1),
    (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1)
]

for q0_input, q1_input, q2_input in combinations:
    print(f"\n--- Input state |{q0_input}{q1_input}{q2_input}> ---")

    # Create a 3-qubit quantum circuit
    qc = QuantumCircuit(3)

    # Prepare the input state
    if q0_input == 1:
        qc.x(0)
    if q1_input == 1:
        qc.x(1)
    if q2_input == 1:
        qc.x(2)

    # Apply Toffoli (CCNOT) gate (controls: q0, q1, target: q2)
    qc.ccx(0, 1, 2)

    print(qc.draw())

    state = Statevector(qc)
    print("Statevector:")
    print(state)

    # Plot Bloch spheres for all three qubits
    fig = plot_bloch_multivector(state)
    display(fig)
