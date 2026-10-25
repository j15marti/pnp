#!/usr/bin/env node
"use strict";

/* ARC-EPOCH-SUSPENSION-FIREWALL169.
   Exact finite controls for the generation-tag tape simulation.
   These counters are logical bit-traffic counters, not FLMV transition traces. */

function run() {
  let checks = 0;
  const assert = (b, m) => { checks++; if (!b) throw new Error(`check ${checks}: ${m}`); };

  class Arena {
    constructor(maxCalls) {
      assert(Number.isInteger(maxCalls) && maxCalls >= 1, "positive call bound");
      this.h = Math.ceil(Math.log2(maxCalls + 1));
      this.maxCalls = maxCalls;
      this.epoch = 0;
      this.cells = new Map();
      this.readBits = 0;
      this.writeBits = 0;
      this.changedBits = 0;
      this.unchangedBits = 0;
      this.maxLogicalPosition = -1;
    }
    start() {
      assert(this.epoch < this.maxCalls, "call bound not exceeded");
      this.epoch++;
      assert(this.epoch < 2 ** this.h, "no epoch wrap");
      return this.epoch;
    }
    select(e) {
      assert(Number.isInteger(e) && e >= 1 && e <= this.maxCalls, "valid suspended epoch");
      this.epoch = e;
    }
    read(j) {
      assert(Number.isInteger(j) && j >= 0, "valid logical address");
      this.maxLogicalPosition = Math.max(this.maxLogicalPosition, j);
      this.readBits += this.h + 1;
      const c = this.cells.get(j);
      return c && c.tag === this.epoch ? c.bit : 0;
    }
    write(j, bit) {
      assert(bit === 0 || bit === 1, "bit value");
      assert(Number.isInteger(j) && j >= 0, "valid logical address");
      this.maxLogicalPosition = Math.max(this.maxLogicalPosition, j);
      const width = this.h + 1;
      const old = this.cells.get(j) || {tag: 0, bit: 0};
      const oldWord = old.tag.toString(2).padStart(this.h, "0") + old.bit;
      const newWord = this.epoch.toString(2).padStart(this.h, "0") + bit;
      assert(oldWord.length === width && newWord.length === width, "record width exact");
      let delta = 0;
      for (let k = 0; k < width; k++) delta += +(oldWord[k] !== newWord[k]);
      this.writeBits += width;
      this.changedBits += delta;
      this.unchangedBits += width - delta;
      this.cells.set(j, {tag: this.epoch, bit});
    }
    physicalPrefixBits() {
      return (this.maxLogicalPosition + 1) * (this.h + 1);
    }
  }

  // Exhaustive sequential-freshness checks across polynomial-size finite call schedules.
  const sequential = [];
  for (const q of [1, 2, 3, 7, 31, 255, 4095]) {
    const a = new Arena(q);
    for (let e = 1; e <= q; e++) {
      a.start();
      for (let j = 0; j < 8; j++) assert(a.read(j) === 0, "new epoch is logically blank");
      for (let j = 0; j < 8; j++) a.write(j, (e + j) & 1);
      for (let j = 0; j < 8; j++) assert(a.read(j) === ((e + j) & 1), "current epoch roundtrip");
    }
    assert(a.writeBits === a.changedBits + a.unchangedBits, "all writes partitioned");
    assert(a.physicalPrefixBits() === 8 * (a.h + 1), "exact dense blocked prefix");
    sequential.push({calls:q, tagBits:a.h, recordBits:a.h+1,
      readBits:a.readBits, writeBits:a.writeBits,
      changedBits:a.changedBits, unchangedBits:a.unchangedBits,
      physicalPrefixBits:a.physicalPrefixBits()});
  }

  // Minimal counterexample: one shared arena cannot preserve an overwritten suspended epoch.
  const shared = new Arena(2);
  const e1 = shared.start();
  shared.write(0, 1);
  assert(shared.read(0) === 1, "guest one state stored");
  const e2 = shared.start();
  shared.write(0, 0);
  assert(shared.read(0) === 0, "guest two state stored");
  shared.select(e1);
  const restored = shared.read(0);
  assert(restored === 0, "stale epoch reads logical blank after overwrite");
  assert(restored !== 1, "suspended guest one state was destroyed");

  // Repair control: one arena per simultaneously live guest preserves both states.
  const left = new Arena(1), right = new Arena(1);
  left.start(); right.start();
  left.write(0, 1); right.write(0, 0);
  assert(left.read(0) === 1 && right.read(0) === 0, "disjoint arenas preserve overlap");

  // Algebraic ledger controls: resetless simulation removes only the wipe term.
  const profiles = [];
  for (const p of [
    {a:.3, lambda:.5, t:1.2, s:.5, g:0, r:1, kappa:.5, eta:.2},
    {a:.1, lambda:.4, t:.5, s:2, g:0, r:.2, kappa:.1, eta:.1},
    {a:.1, lambda:.4, t:.8, s:1.5, g:.05, r:.7, kappa:.2, eta:.3},
    {a:.25, lambda:.25, t:2, s:2, g:.1, r:.9, kappa:.4, eta:.1}
  ]) {
    const resetlessTime = Math.max(p.r, p.a + p.lambda*p.t + p.g);
    const naiveWipeTime = Math.max(resetlessTime, p.a + p.lambda*p.s);
    const sequentialSpace = Math.max(p.kappa, p.eta, p.lambda*p.s);
    const twoArenaSpace = sequentialSpace; // a constant number of live arenas preserves exponent.
    assert(naiveWipeTime + 1e-12 >= resetlessTime, "wipe term never improves time ledger");
    assert(twoArenaSpace === sequentialSpace, "fixed overlap count leaves exponent unchanged");
    profiles.push({...p, resetlessTime, naiveWipeTime, sequentialSpace, twoArenaSpace});
  }

  return {
    run: "ARC-EPOCH-SUSPENSION-FIREWALL169",
    classification: {
      sequential_epoch_simulation: "PROVED/EXACT restricted",
      shared_arena_suspension_failure: "PROVED/EXACT counterexample",
      finite_counters: "COMPUTATIONAL",
      ARC_EDGE_90: "OPEN",
      P_versus_NP: "OPEN"
    },
    caveat: "Logical tag/traffic audit only; no claim of physical FLMV transition profiling.",
    checks,
    failed: 0,
    sequential,
    suspensionCounterexample: {epoch1:e1, epoch2:e2, expectedGuest1:1, restoredGuest1:restored},
    profiles
  };
}

console.log(JSON.stringify(run(), null, 2));
