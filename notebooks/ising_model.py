# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "numpy",
#     "anywidget==0.11.0",
#     "traitlets==5.16.1",
# ]
# ///

import marimo

__generated_with = "0.25.0"
app = marimo.App(width="medium")


@app.cell
def _(mo):
    mo.md(r"""
    # 2D Ising Model

    Nearest-neighbour square lattice, $J = k_B = 1$:

    $$
    H = -J \sum_{\langle ij \rangle} s_i s_j, \qquad s_i = \pm 1
    $$

    The exact critical point is

    $$
    T_c = \frac{2}{\ln\!\left(1 + \sqrt{2}\right)} \approx 2.269
    $$

    Python runs every Metropolis sweep; the widget only draws. Press **Play** to
    start, drag the slider to change speed.
    """)
    return


@app.cell
def _():
    from pathlib import Path

    import anywidget
    import marimo as mo
    import numpy as np
    import traitlets

    T_C = 2.0 / np.log(1.0 + np.sqrt(2.0))
    return Path, T_C, anywidget, mo, np, traitlets


@app.cell
def _(np):
    def random_lattice(L, rng):
        return rng.choice(np.array([-1, 1], dtype=np.int8), size=(L, L))

    def magnetisation(spins):
        return float(spins.mean())

    def sweep(spins, T, rng):
        """One checkerboard Metropolis sweep, vectorised over each sublattice.

        Sites on a checkerboard never share a neighbour, so the two sublattices can
        be updated in sequence with no interaction within a pass.
        """
        L = spins.shape[0]
        rows = np.arange(L)
        parity = (rows[:, None] + rows[None, :]) % 2
        for phase in (0, 1):
            chosen = parity == phase
            neighbours = (
                np.roll(spins, 1, axis=0)
                + np.roll(spins, -1, axis=0)
                + np.roll(spins, 1, axis=1)
                + np.roll(spins, -1, axis=1)
            )
            dE = 2 * spins * neighbours
            accept_p = np.exp(-np.maximum(dE, 0) / max(T, 1e-6))
            flip = chosen & ((dE <= 0) | (rng.random(spins.shape) < accept_p))
            spins = np.where(flip, -spins, spins).astype(np.int8)
        return spins

    return random_lattice, sweep


@app.cell
def _(Path, T_C, anywidget, np, random_lattice, sweep, traitlets):
    class IsingWidget(anywidget.AnyWidget):
        """Draws the lattice. All physics stays in this Python kernel.

        The front end owns the play/pause clock and asks for work; ``on_msg`` runs
        the sweeps in Python and pushes the new lattice back as a synced trait.
        """

        _esm = Path(__file__).parent / "ising_viewer.js"
        _css = Path(__file__).parent / "ising_viewer.css"

        L = traitlets.Int(32).tag(sync=True)
        spins = traitlets.List().tag(sync=True)
        magnetisation = traitlets.Float(0.0).tag(sync=True)
        temperature = traitlets.Float(T_C).tag(sync=True)
        critical_temperature = traitlets.Float(T_C).tag(sync=True)
        sweep_count = traitlets.Int(0).tag(sync=True)
        sweeps_per_step = traitlets.Int(8).tag(sync=True)
        step_ack = traitlets.Int(0).tag(sync=True)

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self._rng = np.random.default_rng(0)
            self.lattice = np.zeros((0, 0), dtype=np.int8)
            self.sweeps_done = 0
            self.on_msg(
                lambda _widget, content, _buffers: self.on_message(content)
            )
            self.reseed(0)

        @property
        def side(self):
            return int(self.lattice.shape[0])

        @property
        def temperature_value(self):
            T = self.temperature
            return T_C if T is None else float(T)

        def on_message(self, content):
            kind = content.get("type")
            if kind == "step":
                self.advance(int(content.get("sweeps", 1)))
            elif kind == "randomise":
                self.reseed()

        def advance(self, count):
            T = self.temperature_value
            for _ in range(max(int(count), 0)):
                self.lattice = sweep(self.lattice, T, self._rng)
                self.sweeps_done += 1
            self.publish()

        def reseed(self, seed=None):
            size = self.L if self.side == 0 else self.side
            self._rng = np.random.default_rng(seed)
            self.lattice = random_lattice(int(size), self._rng)
            self.sweeps_done = 0
            self.publish()

        def resize(self, L):
            L = int(L)
            if L == self.side:
                return
            self.L = L
            self._rng = np.random.default_rng(0)
            self.lattice = random_lattice(L, self._rng)
            self.sweeps_done = 0
            self.publish()

        def publish(self):
            self.spins = [int(v) for v in self.lattice.ravel()]
            self.magnetisation = magnetisation(self.lattice)
            self.sweep_count = self.sweeps_done
            # A sweep can legitimately change nothing (e.g. a fully aligned
            # lattice below T_c), and traitlets skips the change event when a list
            # is reassigned to equal contents. The front end acks on this counter
            # so it can never deadlock waiting for a spins change.
            self.step_ack = self.sweeps_done

    return (IsingWidget,)


@app.cell
def _(T_C, mo):
    temperature = mo.ui.slider(0.5, 4.0, 0.01, T_C, label="Temperature $T$")
    size = mo.ui.slider(16, 96, 8, 32, label="Lattice size $L$")
    mo.hstack([temperature, size], justify="start", widths="equal")
    return size, temperature


@app.cell
def _(IsingWidget, mo):
    board = IsingWidget()
    mo.ui.anywidget(board)
    return (board,)


@app.cell
def _(board, size, temperature):
    board.temperature = temperature.value
    if size.value != board.side:
        board.resize(size.value)
    return


@app.cell
def _(mo):
    mo.md(r"""
    A spin flips when $\Delta E = 2 s_i \sum_{j} s_j$ is negative, and otherwise
    with probability $e^{-\Delta E / T}$. Below $T_c$ domains form and coarsen;
    above it the lattice never settles.
    """)
    return


if __name__ == "__main__":
    app.run()
