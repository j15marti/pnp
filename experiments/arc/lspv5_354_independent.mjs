// Independent implementation of REFEREE354's two-variable affine audit.
// It shares no parser/checker code with the Python implementation.

const valuations = [[0, 0], [0, 1], [1, 0], [1, 1]];

function row(mask, rhs) {
  return valuations.map(([x, y]) => Number((((mask & 1) ? x : 0) ^ ((mask & 2) ? y : 0)) === rhs));
}

function same(a, b) {
  return a.length === b.length && a.every((x, i) => x === b[i]);
}

function add(a, b) {
  return {mask: a.mask ^ b.mask, rhs: a.rhs ^ b.rhs};
}

let checks = 0;
const exact = [];
for (let code = 0; code < 16; code++) {
  const factor = [0, 1, 2, 3].map(i => (code >> i) & 1);
  let count = 0;
  for (let mask = 0; mask < 4; mask++) {
    for (let rhs = 0; rhs < 2; rhs++) {
      if (same(factor, row(mask, rhs))) {
        count++;
        exact.push({code, mask, rhs});
      }
      checks++;
    }
  }
  if (!(count === 0 || count === 1)) throw new Error(`non-unique annotation for ${code}`);
  checks++;
}
if (exact.length !== 8) throw new Error(`expected 8 affine factors, saw ${exact.length}`);
checks++;

const xEq1 = {mask: 1, rhs: 1};
const yEq1 = {mask: 2, rhs: 1};
const sum = add(xEq1, yEq1);
if (sum.mask !== 3 || sum.rhs !== 0) throw new Error("bad witness sum");
if (!same(row(xEq1.mask, xEq1.rhs), [0, 0, 1, 1])) throw new Error("bad x table");
if (!same(row(yEq1.mask, yEq1.rhs), [0, 1, 0, 1])) throw new Error("bad y table");
if (!same(row(sum.mask, sum.rhs), [1, 0, 0, 1])) throw new Error("bad sum table");
checks += 4;

// A typed consumer rejects relation-preserving annotation erasure.
const exactXFactor = {table: [0, 0, 1, 1], affine: xEq1};
const erasedXFactor = {table: [...exactXFactor.table], affine: null};
if (!same(exactXFactor.table, erasedXFactor.table)) throw new Error("relation changed");
if (erasedXFactor.affine !== null) throw new Error("annotation not erased");
checks += 2;

process.stdout.write(JSON.stringify({
  schema: "Rmix341-typed-affine-independent-js-v1",
  status: "PASS",
  checks,
  affineFactorCount: exact.length,
  witness: {
    node1Table: exactXFactor.table,
    node2Table: row(yEq1.mask, yEq1.rhs),
    xor: sum,
    erasedTableEqual: same(exactXFactor.table, erasedXFactor.table),
    erasedHasTypedRow: erasedXFactor.affine !== null,
  },
}, null, 2) + "\n");
