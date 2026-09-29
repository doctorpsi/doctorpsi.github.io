const UP = [243, 243, 248];
const DOWN = [24, 24, 30];

export default {
  render({ model, el }) {
    el.innerHTML = "";

    const wrap = document.createElement("div");
    wrap.className = "ising-wrap";
    el.appendChild(wrap);

    const bar = document.createElement("div");
    bar.className = "ising-bar";
    wrap.appendChild(bar);

    const play = document.createElement("button");
    play.className = "ising-btn";
    play.textContent = "Pause";
    bar.appendChild(play);

    const speedLabel = document.createElement("span");
    speedLabel.className = "ising-label";
    speedLabel.textContent = "sweeps / frame";
    bar.appendChild(speedLabel);

    const speed = document.createElement("input");
    speed.type = "range";
    speed.className = "ising-speed";
    speed.min = "1";
    speed.max = "40";
    speed.value = "8";
    speed.title = "Sweeps per frame";
    speed.setAttribute("aria-label", "Sweeps per frame");
    bar.appendChild(speed);

    const rand = document.createElement("button");
    rand.className = "ising-btn";
    rand.textContent = "Randomise";
    bar.appendChild(rand);

    const canvas = document.createElement("canvas");
    wrap.appendChild(canvas);
    const ctx = canvas.getContext("2d");

    const readout = document.createElement("div");
    readout.className = "ising-readout";
    wrap.appendChild(readout);

    // Offscreen L x L buffer: one pixel per spin, upscaled on draw.
    const off = document.createElement("canvas");
    const offCtx = off.getContext("2d");
    let side = 0;
    let image = null;
    let playing = true;
    let inflight = false;
    let nextAllowed = 0;

    function sizeCanvas() {
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      const box = Math.max(240, Math.min(wrap.clientWidth || 480, 480));
      canvas.width = Math.round(box * dpr);
      canvas.height = Math.round(box * dpr);
      canvas.style.width = box + "px";
      canvas.style.height = box + "px";
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }

    function rebuild(n) {
      side = n;
      off.width = n;
      off.height = n;
      image = offCtx.createImageData(n, n);
      sizeCanvas();
    }

    function draw() {
      const spins = model.get("spins") || [];
      if (!image || spins.length !== side * side) return;

      const data = image.data;
      for (let n = 0; n < spins.length; n++) {
        // Compare against 0: -1 is truthy in JavaScript, so a plain
        // ternary on the spin would paint every site up.
        const c = spins[n] > 0 ? UP : DOWN;
        const p = 4 * n;
        data[p] = c[0];
        data[p + 1] = c[1];
        data[p + 2] = c[2];
        data[p + 3] = 255;
      }
      offCtx.putImageData(image, 0, 0);

      const box = canvas.clientWidth;
      ctx.fillStyle = "#0b0d10";
      ctx.fillRect(0, 0, box, box);
      ctx.imageSmoothingEnabled = false;
      ctx.drawImage(off, 0, 0, box, box);

      const m = model.get("magnetisation") || 0;
      const T = model.get("temperature") || 0;
      const Tc = model.get("critical_temperature") || 1;
      const total = model.get("sweep_count") || 0;
      readout.textContent =
        "L = " + side +
        "   T = " + T.toFixed(2) + "  (T/T" + String.fromCharCode(0x1d04) + " = " + (T / Tc).toFixed(2) + ")" +
        "   m = " + m.toFixed(3) +
        "   sweeps = " + total;
    }

    play.addEventListener("click", () => {
      playing = !playing;
      play.textContent = playing ? "Pause" : "Play";
    });

    rand.addEventListener("click", () => {
      model.send({ type: "randomise" });
    });

    speed.addEventListener("input", () => {
      model.set("sweeps_per_step", Number(speed.value));
      model.save_changes();
    });

    speed.addEventListener("dblclick", () => {
      speed.value = "8";
      model.set("sweeps_per_step", 8);
      model.save_changes();
    });

    // Ask Python for the next step, one request at a time.
    //
    // The kernel's message queue is shared with UI events, so a hot loop of
    // requests would make slider changes feel laggy. Two guards keep the
    // animation polite:
    //   * one request in flight, so no backlog of stale work can build up;
    //   * a short cooldown after each acknowledgement, which leaves the queue
    //     free for slider and cell traffic.
    const COOLDOWN_MS = 8;

    function pump() {
      const now = performance.now();
      if (playing && !inflight && now >= nextAllowed) {
        inflight = true;
        model.send({ type: "step", sweeps: model.get("sweeps_per_step") || 8 });
      }
      requestAnimationFrame(pump);
    }

    // Ack on step_ack, NOT on change:spins. A sweep can legitimately leave the
    // lattice untouched (a fully aligned state below T_c does this most of the
    // time), and traitlets does not fire a change event when a list is
    // reassigned to equal contents -- so acking on spins would deadlock here.
    model.on("change:step_ack", () => {
      inflight = false;
      nextAllowed = performance.now() + COOLDOWN_MS;
    });

    model.on("change:spins", draw);
    model.on("change:magnetisation", draw);
    model.on("change:temperature", draw);
    model.on("change:sweep_count", draw);
    model.on("change:L", () => {
      rebuild(model.get("L"));
      draw();
    });

    rebuild(model.get("L") || 32);
    window.addEventListener("resize", () => {
      sizeCanvas();
      draw();
    });
    draw();
    requestAnimationFrame(pump);
  },
};
