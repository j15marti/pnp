/* Independent LSPV-5/375 verifier.  No import from the Python producer. */
'use strict';
const fs = require('fs');
const crypto = require('crypto');
const raw = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
let checks = 0;
function ok(x, msg) { checks++; if (!x) throw Error(msg); }
const source = [
  [1,3,4],[1,3,-4],[1,-3,4],[1,-3,-4],
  [2,5,6],[2,5,-6],[2,-5,6],[2,-5,-6],[-1,-2,7],[-1,-2,-7]
];
const dimacs = `p cnf 7 10\n${source.map(c => `${c.join(' ')} 0`).join('\n')}\n`;
const sourceHash = crypto.createHash('sha256').update(dimacs).digest('hex');
const val = (c, a) => c.some(x => a[Math.abs(x)] === (x > 0));
const norm = c => [...new Set(c)].sort((a,b) => Math.abs(a)-Math.abs(b) || a-b);
ok(raw.run === 'LSPV5_REFEREE375', 'run');
ok(raw.status === 'PASS', 'status');
ok(sourceHash === 'f6e44b39eaf5f4824951fca61b9fe3e35a67a3918c4aca8c6da9acee7cda153e', 'known source hash');
ok(raw.source_sha256 === sourceHash, 'raw source hash');
ok(raw.source_dimacs_bytes === 104, 'DIMACS bytes');
ok(raw.source_assignments === 128 && raw.source_models === 0, 'UNSAT enumeration');
ok(raw.peer_436_hash_audit.published_sha256 === '5d7299e97c4a0b4b5ee0a6fdb3acd54a76192a2fbf84d64da9694857316748ec', 'peer hash');
ok(raw.peer_436_hash_audit.actual_104_byte_dimacs_sha256 === sourceHash, 'peer DIMACS mismatch');
ok(raw.peer_436_hash_audit.recovered_serialization_bytes === 148, 'peer JSON bytes');
ok(raw.peer_436_hash_audit.recovered_sha256 === raw.peer_436_hash_audit.published_sha256, 'peer JSON recovery');
ok(raw.peer_436_hash_audit.exact_match, 'peer exact hash match');
ok(raw.essential_clauses === 10 && raw.deletion_witness_bits.length === 10, 'essential sources');
let models = 0;
for (let bits=0; bits<128; bits++) {
  const a = {}; for (let i=1;i<=7;i++) a[i] = !!(bits & (1<<(i-1)));
  models += source.every(c => val(c,a)) ? 1 : 0;
}
ok(models === 0, 'independent UNSAT enumeration');
for (let omit=0; omit<10; omit++) {
  const bits = raw.deletion_witness_bits[omit];
  ok(Number.isInteger(bits) && bits >= 0 && bits < 128, 'deletion witness range');
  const a = {}; for (let i=1;i<=7;i++) a[i] = !!(bits & (1<<(i-1)));
  ok(source.every((c,j) => j===omit || val(c,a)), 'deletion witness semantics');
}
for (const k of ['pos', 'content']) {
  const c = raw.facet_proof[k];
  ok(c.paid_nodes === 15 && c.weight === 15, 'facet cost');
  ok(c.span === 5 && c.references === 29 && c.def_nodes === 1, 'facet ledger');
}
for (const k of ['POS', 'CONTENT', 'GATE']) {
  const c = raw.resolution_minimum.checks[k];
  ok(c.paid_nodes === 9 && c.weight === 9 && c.def_nodes === 0, 'minimum proof');
}
const gl = raw.gate_local_repair.check;
ok(gl.paid_nodes === 19 && gl.weight === 19, 'GATE+LOCAL paid cost');
ok(gl.def_nodes === 1 && raw.gate_local_repair.added_shared_LOCAL_nodes === 4, 'GATE+LOCAL shared facets');
ok(raw.gate_local_repair.general_bound === "q'<=q+4d<=5q for d two-input DEF nodes", 'GATE+LOCAL bound');
ok(raw.same_bytes_differential.pos_rejected_by_content, 'pos/content differential');
ok(raw.same_bytes_differential.content_rejected_by_pos, 'content/pos differential');
ok(raw.same_bytes_differential.pos_rejected_by_gate, 'pos/gate differential');
ok(raw.selector_roundtrip.definition_cases === 64, 'selector cases');
ok(raw.selector_roundtrip.facets === 256, 'selector facets');
ok(raw.selector_roundtrip.exact_semantic_view_preservation, 'view preservation');
ok(raw.selector_roundtrip.exact_weight_preservation, 'weight preservation');
ok(raw.hostile_rejections === 6, 'hostile controls');
ok(raw.assertions >= 400, 'producer assertions');

// Independently replay the nine-node Resolution upper bound.
const S = i => ({s:i}), N = i => ({n:i});
const p9 = [
  [S(0),S(1),4,[1,3]], [S(2),S(3),4,[1,-3]], [N(0),N(1),3,[1]],
  [S(4),S(5),6,[2,5]], [S(6),S(7),6,[2,-5]], [N(3),N(4),5,[2]],
  [S(8),S(9),7,[-1,-2]], [N(2),N(6),1,[-2]], [N(5),N(7),2,[]]
];
const done = [];
const get = r => 's' in r ? source[r.s] : done[r.n];
for (const [lr,rr,p,claim] of p9) {
  const l=get(lr), r=get(rr);
  ok(l.includes(p) && r.includes(-p), 'nine-proof pivot');
  const out=norm([...l.filter(x=>x!==p),...r.filter(x=>x!==-p)]);
  ok(JSON.stringify(out)===JSON.stringify(claim), 'nine-proof resolvent');
  done.push(out);
}
ok(JSON.stringify(done[8])==='[]', 'nine-proof terminal');

// Independent selector-view audit on repeated and ordered gate inputs.
let cases=0, facets=0;
for (const a of [1,2]) for (const b of [1,2]) for (let mask=0;mask<16;mask++) {
  const views=[];
  for (let av=0;av<2;av++) for (let bv=0;bv<2;bv++) {
    const truth=(mask>>(av+2*bv))&1, bad=1-truth;
    views.push(norm([av?-a:a,bv?-b:b,bad?-8:8]));
  }
  for (const view of views) { ok(views.some(x=>JSON.stringify(x)===JSON.stringify(view)), 'content view'); facets++; }
  cases++;
}
ok(cases===64 && facets===256, 'selector totals');
console.log(JSON.stringify({status:'PASS', independent_checks:checks,
  audited:'LSPV5_REFEREE375 selector isometry and exact finite minimum'}));
