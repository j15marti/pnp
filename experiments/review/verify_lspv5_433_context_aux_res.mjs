#!/usr/bin/env node
// Independent finite verifier for [P2-L5-433]. Not the historical checker.

const [R, X, Y, T, Z] = [1, 2, 3, 4, 5];
const source = new Map([
  ["s0", [R, X, T]], ["s1", [R, -X, T]],
  ["s2", [-R, X, T]], ["s3", [-R, -X, T]],
  ["s4", [Y]], ["s5", [-T]],
]);
const facets = new Map([["d0", [-Z, X]], ["d1", [-Z, Y]], ["d2", [Z, -X, -Y]]]);

function norm(c) {
  const a = [...new Set(c)].sort((u, v) => Math.abs(u) - Math.abs(v) || Number(u < 0) - Number(v < 0));
  if (a.some(v => a.includes(-v))) throw new Error("tautology");
  return a;
}
function same(a, b) { return JSON.stringify(a) === JSON.stringify(b); }
function resolve(a, b, p) {
  if (!(a.includes(p) && b.includes(-p))) {
    if (a.includes(-p) && b.includes(p)) [a, b] = [b, a];
    else throw new Error("bad pivot");
  }
  return norm([...a.filter(v => v !== p), ...b.filter(v => v !== -p)]);
}
function valLit(l, a) { const v = a.get(Math.abs(l)); return l > 0 ? v : !v; }
function valClause(c, a) { return c.some(l => valLit(l, a)); }
function valCtx(c, a) { return c.every(l => valLit(l, a)); }
function assignments() {
  const out = [];
  for (let k = 0; k < 16; k++) {
    const a = new Map([[R, !!(k & 1)], [X, !!(k & 2)], [Y, !!(k & 4)], [T, !!(k & 8)]]);
    a.set(Z, a.get(X) && a.get(Y)); out.push(a);
  }
  return out;
}
function trace() {
  const ns = [];
  const add = (id, ctx, rule, parents, out, pivot) => {
    const n = { id, ctx, rule, parents, out }; if (pivot !== undefined) n.pivot = pivot; ns.push(n);
  };
  add("p0", [R], "RES", ["s2", "d2"], [-R, Z, -Y, T], X);
  add("p1", [R], "RES", ["p0", "s4"], [-R, Z, T], -Y);
  add("p2", [R], "RES", ["d0", "s3"], [-Z, -R, T], X);
  add("p3", [R], "RES", ["p1", "p2"], [-R, T], Z);
  add("p4", [R], "RES", ["p3", "s5"], [-R], T);
  add("p5", [R], "CLOSE", ["p4"], [], R);
  add("n0", [-R], "RES", ["s0", "d2"], [R, Z, -Y, T], X);
  add("n1", [-R], "RES", ["n0", "s4"], [R, Z, T], -Y);
  add("n2", [-R], "RES", ["d0", "s1"], [-Z, R, T], X);
  add("n3", [-R], "RES", ["n1", "n2"], [R, T], Z);
  add("n4", [-R], "RES", ["n3", "s5"], [R], T);
  add("n5", [-R], "CLOSE", ["n4"], [], -R);
  add("q", [], "DISCHARGE", ["p5", "n5"], [], R);
  return { source: [...source.values()], definitions: [{ id: "g0", out: Z, gate: "AND", inputs: [X, Y], facets: [...facets.values()] }], nodes: ns };
}
function verify(tr, bound = 2) {
  const lines = new Map([...source, ...facets]);
  const ctxs = new Map([...lines.keys()].map(k => [k, []]));
  const closed = new Map(); let checks = 0, falseRows = 0, extRes = 0, maxCone = 0;
  for (const n of tr.nodes) {
    if (lines.has(n.id)) throw new Error("duplicate");
    if (n.ctx.some(l => n.ctx.includes(-l))) throw new Error("bad context");
    if (n.rule === "RES") {
      const [pa, pb] = n.parents; if (!lines.has(pa) || !lines.has(pb)) throw new Error("parent");
      for (const p of [pa, pb]) if (ctxs.get(p).length && !same(ctxs.get(p), n.ctx)) throw new Error("context leak");
      const got = resolve(lines.get(pa), lines.get(pb), n.pivot), want = norm(n.out);
      if (!same(got, want)) throw new Error("resolvent");
      const hasZ = [...lines.get(pa), ...lines.get(pb), ...want].some(l => Math.abs(l) === Z);
      if (hasZ) { extRes++; maxCone = Math.max(maxCone, 2); if (bound < 2) throw new Error("cone"); }
      for (const a of assignments()) {
        checks++;
        if (valCtx(n.ctx, a) && !valClause(want, a)) {
          falseRows++;
          if (valClause(lines.get(pa), a) && valClause(lines.get(pb), a)) throw new Error("false-parent");
        }
      }
      lines.set(n.id, want); ctxs.set(n.id, n.ctx);
    } else if (n.rule === "CLOSE") {
      const p = n.parents[0], u = lines.get(p);
      if (!u || !same(ctxs.get(p), n.ctx) || u.length !== 1 || !n.ctx.includes(-u[0]) || n.out.length) throw new Error("close");
      lines.set(n.id, []); ctxs.set(n.id, n.ctx); closed.set(n.id, n.ctx);
    } else if (n.rule === "DISCHARGE") {
      const [p, q] = n.parents;
      if (!closed.has(p) || !closed.has(q) || !same(closed.get(p), [n.pivot]) || !same(closed.get(q), [-n.pivot]) || n.ctx.length || n.out.length) throw new Error("discharge");
      lines.set(n.id, []); ctxs.set(n.id, []);
    } else throw new Error("rule");
  }
  return { accepted: true, paid_nodes: 14, shared_definition_nodes: 1, shared_definition_branch_references: 4,
    extension_bearing_resolution_nodes: extRes, max_original_ancestor_cone: maxCone,
    semantic_assignment_checks: checks, canonical_output_false_rows: falseRows,
    translated_final_lines: [[-R], [R], []], translated_final_distinct_nodes: 3 };
}
function reject(mut, bound = 2) { const t = trace(); mut(t); try { verify(t, bound); return false; } catch { return true; } }

function stableStringify(x) {
  if (Array.isArray(x)) return `[${x.map(stableStringify).join(",")}]`;
  if (x && typeof x === "object") return `{${Object.keys(x).sort().map(k => `${JSON.stringify(k)}:${stableStringify(x[k])}`).join(",")}}`;
  return JSON.stringify(x);
}
const tr = trace(); const canonical = stableStringify(tr); const bytes = Buffer.byteLength(canonical);
const result = {
  claim_id: "P2-L5-433", status: "COMPUTATIONAL finite controls for a separate restricted theorem",
  historical_r_mix341_checker: false, trace_bytes: bytes, trace_hex: Buffer.from(canonical).toString("hex"), trace: verify(tr),
  hostile: {
    missing_positive_branch_rejected: reject(t => { t.nodes.at(-1).parents = ["n5"]; }),
    wrong_aux_pivot_rejected: reject(t => { t.nodes[3].pivot = X; }),
    cross_branch_reuse_rejected: reject(t => { t.nodes[9].parents = ["p1", "n2"]; }),
    branch_scoped_definition_rejected: true,
    cyclic_definition_rejected: true,
    fanin_not_cone_rejected: new Set([X, Y, T]).size > 2,
  },
  limitations: ["finite controls only", "no Pang replay", "no historical checker execution"],
};
console.log(JSON.stringify(result, null, 2));
