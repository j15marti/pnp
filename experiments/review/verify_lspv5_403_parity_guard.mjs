import fs from 'node:fs';

const path = process.argv[2];
if (!path) throw new Error('usage: node verify_lspv5_403_parity_guard.mjs result.json');
const data = JSON.parse(fs.readFileSync(path, 'utf8'));
let checks = 0;
const assert = (v, m) => { if (!v) throw new Error(m); checks++; };
assert(data.status === 'PASS', 'status');
assert(data.rows.length === 16, 'row count');
for (const row of data.rows) {
  const k = row.bits;
  assert(row.state_nodes === 1 + 2 * k, `states k=${k}`);
  assert(row.state_edges === 4 * k - 2, `edges k=${k}`);
  assert(row.context_leaves === 2 ** k, `leaves k=${k}`);
  assert(row.even_contexts === 2 ** (k - 1), `even contexts k=${k}`);
  assert(row.odd_contexts === 2 ** (k - 1), `odd contexts k=${k}`);
  assert(row.char_not_2_normal_form_monomials === 2 ** k, `odd char k=${k}`);
  assert(row.char_2_normal_form_monomials === k + 1, `char2 k=${k}`);
  assert(row.explicit_pcr_even_leaf_guards === 2 ** (k - 1), `PCR leaves k=${k}`);
  for (const p of ['3', '5', '7', '11'])
    assert(row.odd_prime_nonzero_counts[p] === 2 ** k, `p=${p}, k=${k}`);
}
for (const [name, value] of Object.entries(data.corruptions_rejected))
  assert(value === true, `corruption ${name}`);
assert(data.disclaimer.includes('not an authoritative checker'), 'disclaimer');
console.log(JSON.stringify({status: 'PASS', checks, k_max: 16}));
