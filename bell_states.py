
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from IPython.display import display

# Input (q0, q1) -> Bell state produced by H on q0 followed by CNOT(0, 1)
bell_states = {
    (0, 0): "Phi+",
    (0, 1): "Psi+",
    (1, 0): "Phi-",
    (1, 1): "Psi-",
}

for (q0_input, q1_input), name in bell_states.items():
    print(f"\n--- {name}: input q0={q0_input}, q1={q1_input} ---")

    qc = QuantumCircuit(2)

    # Prepare the input state
    if q0_input == 1:
        qc.x(0)
    if q1_input == 1:
        qc.x(1)
    input_state = Statevector(qc)

    # Generate the Bell state
    qc.h(0)
    qc.cx(0, 1)

    state = Statevector(qc)
    display(state.draw('latex'))
    display(qc.draw())
    display(state.draw('qsphere'))

    # Verify: CNOT then H undoes the entangling circuit and recovers the input
    qc.cx(0, 1)
    qc.h(0)

    display(qc.draw())
    print("Input recovered:", Statevector(qc).equiv(input_state))
