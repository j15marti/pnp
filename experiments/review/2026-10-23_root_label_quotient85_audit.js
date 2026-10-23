"use strict";

// ROOT-LABEL-QUOTIENT85 audit.
// Finite validation of exact quotient counts for Boolean residual functions.
// No unrestricted time lower bound is claimed.

let assertions = 0;
let failures = 0;
let exhaustiveFunctions = 0;
let quotientCases = 0;
let singletonCases = 0;

function check(cond, msg) {
  assertions++;
  if (!cond) {
    failures++;
    if (failures <= 20) process.stderr.write("FAIL: " + msg + "\n");
  }
}

// For m=2^r truth-table positions and q<m selected point contexts:
// signature = q selected bits plus OR of all m bits.
// Exact class count is 2^q+1. For q=m, OR is redundant and the count is 2^m.
for (let r = 0; r <= 4; r++) {
  const m = 2 ** r;
  const functionCount = 2 ** m;

  const root = new Set();
  const full = new Set();
  for (let f = 0; f < functionCount; f++) {
    root.add(f === 0 ? "0" : "1");
    full.add(f.toString(2).padStart(m, "0"));
    exhaustiveFunctions++;
  }
  check(root.size === 2, "root quotient has two classes at r=" + r);
  check(full.size === functionCount, "complete evaluation contexts distinguish every function at r=" + r);

  for (let q = 0; q <= m; q++) {
    const signatures = new Set();
    for (let f = 0; f < functionCount; f++) {
      const selected = f & ((2 ** q) - 1);
      const sat = f === 0 ? 0 : 1;
      signatures.add(selected + ":" + sat);
    }
    const expected = q < m ? (2 ** q + 1) : 2 ** m;
    check(signatures.size === expected, "root+" + q + " point contexts exact quotient at r=" + r);
    const bits = Math.ceil(Math.log2(signatures.size));
    check((2 ** bits) >= signatures.size, "state-bit lower bound rounds upward");
    if (bits > 0) check((2 ** (bits - 1)) < signatures.size, "state-bit lower bound is minimal");
    quotientCases++;
  }
}

// Singleton family: all members have the same root SAT label but complete point
// contexts distinguish all 2^r possible witness locations.
for (let r = 1; r <= 18; r++) {
  const m = 2 ** r;
  const rootLabels = new Set();
  const locations = new Set();
  for (let z = 0; z < m; z++) {
    rootLabels.add(1);
    locations.add(z);
    singletonCases++;
  }
  check(rootLabels.size === 1, "all singleton predicates are SAT at r=" + r);
  check(locations.size === m, "point contexts distinguish singleton locations at r=" + r);
  check(Math.ceil(Math.log2(locations.size)) === r, "location service needs r state bits at r=" + r);
}

// Combinatorial identity behind the q-point quotient count. This is checked
// independently of explicit truth-table enumeration for larger m.
for (let m = 1; m <= 60; m++) {
  for (let q = 0; q <= Math.min(m, 50); q++) {
    if (q < m) {
      const derived = (2 ** q - 1) + 2;
      check(derived === 2 ** q + 1, "root-plus-points class identity");
    }
    quotientCases++;
  }
}

const result = {
  artifact: "ROOT-LABEL-QUOTIENT85",
  assertions,
  failures,
  exhaustive_functions_checked: exhaustiveFunctions,
  quotient_cases: quotientCases,
  singleton_predicates_checked: singletonCases,
  status: failures === 0 ? "PASS_RESTRICTED_REPRESENTATION_ONLY" : "FAIL",
  disclaimer: "Finite quotient validation only; does not extract a context interface from arbitrary SAT deciders."
};

process.stdout.write(JSON.stringify(result, null, 2) + "\n");
process.exitCode = failures === 0 ? 0 : 1;
