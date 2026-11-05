#!/usr/bin/env node
// Independent restricted checker for the REFEREE364 DEF/RES slicing family.

import {writeFileSync} from "node:fs";

const canonical = xs =>
  [...new Set(xs)].sort((a, b) =>
    Math.abs(a) - Math.abs(b) || Number(a < 0) - Number(b < 0));

const facets = (a, b, z, truth) => {
  const out = [];
  for (const av of [0, 1]) for (const bv of [0, 1]) {
    const zv = 1 - truth[av | (bv << 1)];
    out.push(canonical([
      av === 0 ? a : -a,
      bv === 0 ? b : -b,
      zv === 0 ? z : -z,
    ]));
  }
  return out;
};

const key = x => JSON.stringify(x);
const oriented = (a, b, p) => {
  const out = [];
  if (a.includes(p) && b.includes(-p))
    out.push(canonical([...a.filter(x => x !== p), ...b.filter(x => x !== -p)]));
  if (a.includes(-p) && b.includes(p))
    out.push(canonical([...a.filter(x => x !== -p), ...b.filter(x => x !== p)]));
  return out;
};

function check(doc) {
  const views = new Map();
  const n = doc.source.nvars;
  doc.source.clauses.forEach((c, i) => views.set("s:" + i, canonical(c)));
  let next = n + 1;
  const get = (r, before) => {
    if (Object.hasOwn(r, "src")) {
      const v = views.get("s:" + r.src);
      if (!v) throw Error("missing source");
      return v;
    }
    if (!(r.node < before)) throw Error("forward node");
    const k = Object.hasOwn(r, "facet")
      ? "n:" + r.node + ":f:" + r.facet
      : "n:" + r.node;
    const v = views.get(k);
    if (!v) throw Error("missing view");
    return v;
  };
  doc.nodes.forEach((node, i) => {
    if (node.id !== i) throw Error("node id");
    if (node.rule === "DEF") {
      if (node.var !== next++) throw Error("nonfresh DEF");
      if (node.inputs.length !== 2 ||
          node.inputs.some(v => !(v >= 1 && v < node.var)))
        throw Error("bad DEF input");
      facets(node.inputs[0], node.inputs[1], node.var, node.truth)
        .forEach((c, j) => views.set("n:" + i + ":f:" + j, c));
    } else if (node.rule === "RES") {
      const a = get(node.left, i), b = get(node.right, i);
      const candidates = oriented(a, b, node.pivot).map(key);
      if (!candidates.includes(key(canonical(node.clause))))
        throw Error("wrong RES");
      views.set("n:" + i, canonical(node.clause));
    } else {
      throw Error("unsupported");
    }
  });
  const fin = get(doc.final, doc.nodes.length);
  if (fin.length !== 0) throw Error("not contradiction");
  return true;
}

function build(chain, dead = 0, sat = false) {
  const nodes = [
    {id:0, rule:"DEF", var:2, inputs:[1,1], truth:[0,0,0,0]}
  ];
  for (let j = 2; j <= chain; j++)
    nodes.push({
      id:nodes.length, rule:"DEF", var:j+1,
      inputs:[j,1], truth:[0,0,1,1]
    });
  const finalDef = chain - 1, w = chain + 1;
  for (let j = 0; j < dead; j++) {
    const varId = 2 + nodes.filter(x => x.rule === "DEF").length;
    nodes.push({
      id:nodes.length, rule:"DEF", var:varId,
      inputs:[1,1], truth:[0,1,1,0]
    });
  }
  const k = nodes.length;
  nodes.push(
    {id:k,rule:"RES",left:{node:finalDef,facet:1},
     right:{node:finalDef,facet:3},pivot:chain,clause:[-1,w]},
    {id:k+1,rule:"RES",left:{node:k},right:{src:0},pivot:1,clause:[w]},
    {id:k+2,rule:"RES",left:{node:finalDef,facet:0},
     right:{node:finalDef,facet:2},pivot:chain,clause:[1,-w]},
    {id:k+3,rule:"RES",left:{node:k+2},right:{src:1},pivot:1,clause:[-w]},
    {id:k+4,rule:"RES",left:{node:k+1},right:{node:k+3},pivot:w,clause:[]}
  );
  return {
    source:{nvars:1,clauses:[[1],sat?[1]:[-1]]},
    nodes,
    final:{node:nodes.length-1}
  };
}

const refs = n => n.rule === "RES" ? [n.left,n.right] : [];
function explicit(doc) {
  const keep = new Set(), todo = [doc.final.node];
  while (todo.length) {
    const i = todo.pop();
    if (keep.has(i)) continue;
    keep.add(i);
    refs(doc.nodes[i]).forEach(r => {
      if (Object.hasOwn(r,"node")) todo.push(r.node);
    });
  }
  return keep;
}

function closed(doc) {
  const keep = explicit(doc), owner = new Map();
  doc.nodes.forEach(n => {
    if (n.rule === "DEF") owner.set(n.var,n.id);
  });
  let changed = true;
  while (changed) {
    changed = false;
    for (const i of [...keep]) {
      const n = doc.nodes[i];
      const vars = n.rule === "DEF"
        ? [n.var,...n.inputs]
        : [n.pivot,...n.clause.map(Math.abs)];
      for (const v of vars) if (v > doc.source.nvars) {
        if (!owner.has(v)) throw Error("ownerless");
        const o = owner.get(v);
        if (!keep.has(o)) {
          keep.add(o);
          changed = true;
        }
      }
      refs(n).forEach(r => {
        if (Object.hasOwn(r,"node") && !keep.has(r.node)) {
          keep.add(r.node);
          changed = true;
        }
      });
    }
  }
  return keep;
}

let checks = 0;
const rows = [];
for (const chain of [2,3,10,50]) for (const dead of [0,1,7]) {
  const doc = build(chain,dead,false);
  if (!check(doc)) throw Error("original");
  checks++;
  const e = explicit(doc), c = closed(doc);
  if (e.size !== 6 || c.size !== chain+5) throw Error("closure counts");
  checks += 2;
  rows.push({
    chain,dead,original:doc.nodes.length,
    explicit:e.size,closed:c.size
  });
}
try {
  check(build(3,0,true));
  throw Error("SAT accepted");
} catch (e) {
  if (e.message === "SAT accepted") throw e;
  checks++;
}

const malformed = build(2);
malformed.nodes[0].var = 3;
try {
  check(malformed);
  throw Error("bad fresh accepted");
} catch (e) {
  if (e.message === "bad fresh accepted") throw e;
  checks++;
}

const result = {
  format:"LSPV5-DEPENDENCY-SLICE-INDEPENDENT-REFEREE364-1",
  checks,
  rows,
  conclusion:
    "explicit proof-reference ancestry misses numeric auxiliary-owner edges; dependency closure restores them",
  status:"PASS"
};
const encoded = JSON.stringify(result,null,2) + "\n";
writeFileSync(
  "results/raw/arc/2026-11-05_0748_LSPV5_REFEREE364_independent.json",
  encoded
);
console.log(encoded.trimEnd());
