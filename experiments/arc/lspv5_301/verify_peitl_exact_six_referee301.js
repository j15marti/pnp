#!/usr/bin/env node
"use strict";

// Independent no-import verifier for PEITL-EXACT-SIX-REFEREE301.
const fs = require("fs");
const crypto = require("crypto");

const rawPath = process.argv[2];
const outPath = process.argv[3];
if (!rawPath || !outPath) throw new Error("usage: verifier raw.json verify.json");
const raw = JSON.parse(fs.readFileSync(rawPath, "utf8"));
const inputBytes = fs.readFileSync(raw.input.path);

function parseDimacs(text) {
  let n = null, declared = null;
  const clauses = [];
  for (const original of text.split(/\r?\n/)) {
    const line = original.trim();
    if (!line || line.startsWith("c")) continue;
    const p = line.split(/\s+/);
    if (p[0] === "p") {
      if (n !== null || p.length !== 4 || p[1] !== "cnf") throw new Error("bad header");
      n = Number(p[2]); declared = Number(p[3]);
      if (!Number.isInteger(n) || !Number.isInteger(declared) || n < 0 || declared < 0) throw new Error("bad dimensions");
    } else {
      if (n === null || p[p.length - 1] !== "0" || p.filter(x => x === "0").length !== 1) throw new Error("bad clause");
      const c = p.slice(0, -1).map(Number);
      if (new Set(c).size !== c.length || c.some(x => !x || Math.abs(x) > n || c.includes(-x))) throw new Error("bad literal");
      clauses.push(c);
    }
  }
  if (n === null || declared !== clauses.length) throw new Error("count mismatch");
  return {n, clauses};
}

function clauseTable(c, n) {
  let t = 0;
  for (let a = 0; a < (1 << n); a++) {
    if (c.some(l => ((a >> (Math.abs(l) - 1)) & 1) === (l > 0 ? 1 : 0))) t |= (1 << a);
  }
  return t >>> 0;
}

function modelCount(clauses, n) {
  let count = 0;
  for (let a = 0; a < (1 << n); a++) {
    if (clauses.every(c => c.some(l => ((a >> (Math.abs(l) - 1)) & 1) === (l > 0 ? 1 : 0)))) count++;
  }
  return count;
}

function support(t, n) {
  let count = 0;
  for (let i = 0; i < n; i++) {
    let changes = false;
    for (let a = 0; a < (1 << n); a++) {
      if (((t >>> a) & 1) !== ((t >>> (a ^ (1 << i))) & 1)) { changes = true; break; }
    }
    if (changes) count++;
  }
  return count;
}

function affineTable(mask, rhs, n) {
  let t = 0;
  for (let a = 0; a < (1 << n); a++) {
    let x = a & mask, parity = 0;
    while (x) { parity ^= 1; x &= x - 1; }
    if (parity === rhs) t |= 1 << a;
  }
  return t >>> 0;
}

function aliases(n) {
  const clause = new Map();
  const total = 3 ** n;
  for (let code = 0; code < total; code++) {
    let z = code, c = [];
    for (let v = 1; v <= n; v++) {
      const d = z % 3; z = Math.floor(z / 3);
      if (d) c.push(d === 1 ? v : -v);
    }
    clause.set(clauseTable(c, n), c);
  }
  const affine = new Map();
  for (let mask = 0; mask < (1 << n); mask++) for (let rhs = 0; rhs <= 1; rhs++) affine.set(affineTable(mask, rhs, n), [mask, rhs]);
  return {clause, affine};
}

function mixed(a, b, n, names) {
  const out = new Set();
  const conjunction = (a & b) >>> 0;
  if (support(conjunction, n) <= 3) out.add(conjunction);
  if (names.affine.has(a) && names.affine.has(b)) {
    const [ma, ra] = names.affine.get(a), [mb, rb] = names.affine.get(b);
    out.add(affineTable(ma ^ mb, ra ^ rb, n));
  }
  if (names.clause.has(a) && names.clause.has(b)) {
    const ca = names.clause.get(a), cb = names.clause.get(b);
    for (const p of ca) if (cb.includes(-p)) {
      const s = new Set([...ca, ...cb]); s.delete(p); s.delete(-p);
      if (![...s].some(x => s.has(-x))) out.add(clauseTable([...s], n));
    }
  }
  return out;
}

function sourceTrees(clauses, n, names) {
  const m = clauses.length, bank = Array.from({length: 1 << m}, () => new Set());
  clauses.forEach((c, i) => bank[1 << i].add(clauseTable(c, n)));
  let tests = 0;
  for (let size = 2; size <= m; size++) for (let whole = 1; whole < (1 << m); whole++) {
    if (popcount(whole) !== size) continue;
    const least = whole & -whole;
    for (let left = (whole - 1) & whole; left; left = (left - 1) & whole) {
      const right = whole ^ left;
      if (!(left & least) || !right) continue;
      for (const a of bank[left]) for (const b of bank[right]) {
        tests++;
        for (const t of mixed(a, b, n, names)) bank[whole].add(t);
      }
    }
  }
  return {bank, tests};
}

function popcount(x) { let c = 0; while (x) { c++; x &= x - 1; } return c; }

function unicycle(clauses, n) {
  const m = clauses.length, full = (1 << m) - 1, names = aliases(n);
  const trees = sourceTrees(clauses, n, names);
  const sourceTables = clauses.map(c => clauseTable(c, n));
  const cache = new Map();
  function extend(shared, mask) {
    const key = shared + ":" + mask;
    if (cache.has(key)) return cache.get(key);
    const atoms = [shared];
    for (let i = 0; i < m; i++) if ((mask >> i) & 1) atoms.push(sourceTables[i]);
    const bank = Array.from({length: 1 << atoms.length}, () => new Set());
    atoms.forEach((t, i) => bank[1 << i].add(t));
    for (let size = 2; size <= atoms.length; size++) for (let whole = 1; whole < (1 << atoms.length); whole++) {
      if (popcount(whole) !== size) continue;
      const least = whole & -whole;
      for (let left = (whole - 1) & whole; left; left = (left - 1) & whole) {
        const right = whole ^ left;
        if (!(left & least) || !right) continue;
        for (const a of bank[left]) for (const b of bank[right]) for (const t of mixed(a, b, n, names)) bank[whole].add(t);
      }
    }
    cache.set(key, bank[bank.length - 1]);
    return bank[bank.length - 1];
  }
  let rootTests = 0;
  for (let sharedMask = 1; sharedMask <= full; sharedMask++) {
    const rest = full ^ sharedMask;
    for (let tail = rest;; tail = (tail - 1) & rest) {
      const cycleRest = rest ^ tail;
      for (let left = cycleRest;; left = (left - 1) & cycleRest) {
        const right = cycleRest ^ left;
        if (left <= right) for (const shared of trees.bank[sharedMask]) {
          for (const a of extend(shared, left)) for (const b of extend(shared, right)) {
            rootTests++;
            for (const cycle of mixed(a, b, n, names)) if (extend(cycle, tail).has(0)) return {found: true, rootTests, cacheSize: cache.size};
          }
        }
        if (left === 0) break;
      }
      if (tail === 0) break;
    }
  }
  return {found: false, rootTests, cacheSize: cache.size, treeTests: trees.tests, terminal: trees.bank[full].size, floorFalse: trees.bank[full].has(0)};
}

function canon(c) { return [...new Set(c)].sort((a,b) => Math.abs(a)-Math.abs(b) || Number(a<0)-Number(b<0)); }
function resolve(left, right, pivot) {
  if (!left.includes(pivot) || !right.includes(-pivot)) throw new Error("pivot");
  const s = new Set([...left, ...right]); s.delete(pivot); s.delete(-pivot);
  if ([...s].some(x => s.has(-x))) throw new Error("tautology");
  return canon([...s]);
}
function same(a,b) { return JSON.stringify(a) === JSON.stringify(b); }
function replayResolution(clauses, certificate) {
  const lines = clauses.map(canon);
  for (const s of certificate) {
    const l = s.left_line - 1, r = s.right_line - 1;
    if (l < 0 || r < 0 || l >= lines.length || r >= lines.length) return false;
    let got; try { got = resolve(lines[l], lines[r], s.pivot); } catch { return false; }
    if (!same(got, canon(s.clause))) return false;
    lines.push(got);
  }
  return lines.length > 0 && lines[lines.length - 1].length === 0;
}

function parityK4(charges) {
  const edges = [[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]], clauses = [];
  for (let v = 0; v < 4; v++) {
    const inc = edges.map((e,i) => e.includes(v) ? i+1 : 0).filter(Boolean);
    for (let bits = 0; bits < 8; bits++) {
      if ((popcount(bits) & 1) === charges[v]) continue;
      clauses.push(inc.map((x,i) => ((bits >> i) & 1) ? -x : x));
    }
  }
  return clauses;
}

let checks = 0;
const parsed = parseDimacs(inputBytes.toString("utf8")); checks++;
if (crypto.createHash("sha256").update(inputBytes).digest("hex") !== raw.input.sha256) throw new Error("sha"); checks++;
if (modelCount(parsed.clauses, parsed.n) !== 0) throw new Error("label"); checks++;
const deletion = parsed.clauses.map((_,i) => modelCount(parsed.clauses.filter((_,j) => i !== j), parsed.n));
if (!same(deletion, raw.input.deletion_model_counts) || deletion.some(x => !x)) throw new Error("deletion"); checks += deletion.length;
const flips = [];
for (let i=0;i<parsed.clauses.length;i++) for(let j=0;j<parsed.clauses[i].length;j++) {
  const copy=parsed.clauses.map(c=>[...c]); copy[i][j]*=-1; flips.push(modelCount(copy,parsed.n));
}
if(!same(flips,raw.input.sign_flip_model_counts)||flips.some(x=>!x)) throw new Error("flip"); checks+=flips.length;
const search=unicycle(parsed.clauses,parsed.n);
if(search.found||search.rootTests!==7212||search.terminal!==82||search.floorFalse) throw new Error("search "+JSON.stringify(search)); checks+=4;
if(!replayResolution(parsed.clauses,raw.resolution_upper_certificate)) throw new Error("proof"); checks+=7;
const badProof=raw.resolution_upper_certificate.slice(0,-1);
if(replayResolution(parsed.clauses,badProof)) throw new Error("corrupt proof"); checks++;
const malformed={
 missing_header:"1 0\n",bad_keyword:"p sat 1 1\n1 0\n",count_mismatch:"p cnf 1 2\n1 0\n",
 out_of_range_variable:"p cnf 1 1\n2 0\n",missing_terminator:"p cnf 1 1\n1\n",
 duplicate_literal:"p cnf 1 1\n1 1 0\n",tautological_clause:"p cnf 1 1\n1 -1 0\n",negative_dimensions:"p cnf -1 0\n"
};
for(const text of Object.values(malformed)){let rejected=false;try{parseDimacs(text);}catch{rejected=true;}if(!rejected)throw new Error("malformed");checks++;}
if(modelCount(parityK4([1,0,0,0]),6)!==0||modelCount(parityK4([0,0,0,0]),6)!==8)throw new Error("parity");checks+=2;
if(raw.exact_mixed_cost!==7||!Object.values(raw.assertions).every(Boolean))throw new Error("raw assertions");checks+=2;

const result={verified:true,checks,exact_mixed_cost:7,search,raw_sha256:crypto.createHash("sha256").update(fs.readFileSync(rawPath)).digest("hex"),node:process.version,peak_rss_kib:process.resourceUsage().maxRSS};
fs.writeFileSync(outPath,JSON.stringify(result,null,2)+"\n");
console.log(JSON.stringify(result,null,2));
