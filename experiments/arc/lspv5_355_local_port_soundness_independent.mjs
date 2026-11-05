// Independent REFEREE355 two-variable port-soundness enumeration.

function bits(code) {
  return [0, 1, 2, 3].map(i => (code >> i) & 1);
}

function not(a) {
  return a.map(x => x ^ 1);
}

function or(a, b) {
  return a.map((x, i) => x | b[i]);
}

function entails(a, b) {
  return a.every((x, i) => !x || b[i]);
}

function same(a, b) {
  return a.length === b.length && a.every((x, i) => x === b[i]);
}

let checks = 0;
let factors = 0;
let pairs = 0;
let unsound = 0;
let entailed = 0;

for (let fcode = 1; fcode < 16; fcode++) {
  const factor = bits(fcode);
  factors++;
  for (let gcode = 0; gcode < 16; gcode++) {
    const gate = bits(gcode);
    const root = or(gate, not(gate));
    pairs++;
    if (!same(root, [1, 1, 1, 1])) throw new Error("non-tautological root");
    if (!entails(factor, root)) throw new Error("factor does not entail root");
    checks += 2;
    if (entails(factor, gate)) {
      entailed++;
    } else {
      unsound++;
      if (!factor.some((x, i) => x && !gate[i])) throw new Error("missing countermodel");
      checks++;
    }
  }
}

if (factors !== 15 || pairs !== 240 || unsound !== 175 || entailed !== 65) {
  throw new Error(JSON.stringify({factors, pairs, unsound, entailed}));
}
checks += 4;

const x = [0, 0, 1, 1];
const notX = not(x);
const root = or(x, notX);
if (!entails(x, root)) throw new Error("LOCAL root invalid");
if (entails(x, notX)) throw new Error("internal NOT x was entailed");
if (!same(root, [1, 1, 1, 1])) throw new Error("bad witness root");
checks += 3;

// The root relation has zero delta; changing one declared port-kind bit changes
// whether the internal term may be used as an assertion.
const nativeTag = 0;
const permissiveTag = 1;
const dLogicRoot = root.reduce((s, bit, i) => s + (bit ^ root[i]), 0);
const dPhysicalTag = nativeTag ^ permissiveTag;
if (dLogicRoot !== 0 || dPhysicalTag !== 1) throw new Error("bad delta control");
checks += 2;

process.stdout.write(JSON.stringify({
  schema: "Rmix341-local-port-soundness-independent-js-v1",
  status: "PASS",
  checks,
  catalog: {factors, pairs, unsoundAssertedExports: unsound, entailedExports: entailed},
  witness: {
    factor: x,
    internalNotX: notX,
    root,
    factorEntailsRoot: entails(x, root),
    factorEntailsInternal: entails(x, notX),
    dLogicRoot,
    dPhysicalTag,
  },
}, null, 2) + "\n");
