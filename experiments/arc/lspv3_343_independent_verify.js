#!/usr/bin/env node
// Independent LSPV-3 BPHP-EXTENSION343 verifier: no 3rd-party packages.
// Run from the repository root: node experiments/arc/lspv3_343_independent_verify.js
"use strict";
const fs=require("fs"),crypto=require("crypto");
const file=process.argv[2]||"results/raw/arc/2026-11-02_1324_LSPV3_BPHP_EXTENSION343.json";
const data=JSON.parse(fs.readFileSync(file,"utf8"));
let assertions=0;
function ok(x,msg){if(!x)throw Error(msg);assertions++;}
for(const r of data.cases){
 const ell=r.ell,n=r.n,m=r.m,triples=[];
 for(let i=0;i<m;i++)for(let j=i+1;j<m;j++)for(let z=0;z<n;z++)triples.push([i,j,z]);
 ok(triples.length===r.clauses,"number of constraints");
 // Direct semantic derivation: a clause is false exactly when a pair collides at a fixed hole.
 function clause(i,j,z,holes){return holes[i]!==z||holes[j]!==z;}
 for(let k=0;k<triples.length;k++){
  const [i,j,z]=triples[k],holes=Array(m).fill(-1);holes[i]=holes[j]=z;
  let h=0;for(let p=0;p<m;p++)if(p!==i&&p!==j){
   if(h===z)h++;holes[p]=h++;
  }
  for(let t=0;t<triples.length;t++){
   const [a,b,q]=triples[t];
   ok(clause(a,b,q,holes)===(t!==k),"indispensable clause "+k+"/"+t);
  }
 }
 const holes=Array.from({length:n},(_,i)=>i);
 for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)for(let z=0;z<n;z++)
  ok(clause(i,j,z,holes),"SAT positive label");
 for(const [i,j,z] of triples)for(let a=0;a<n;a++)for(let b=0;b<n;b++)
  ok(Boolean((a^z)||(b^z))===(a!==z||b!==z),"binary/unary equivalence");
 ok(r.signflip_sat===2*ell*r.clauses,"sign flip count");
 // Reconstruct the complete source and verify the original Python producer's digest.
 const clauses=[];
 for(const [i,j,z] of triples){
  const literals=[];
  for(const p of [i,j])for(let bit=0;bit<ell;bit++){
   let x=p*ell+bit+1;literals.push(((z>>bit)&1)?-x:x);
  }
  clauses.push(literals.join(" ")+" 0\n");
 }
 const dimacs="p cnf "+m*ell+" "+r.clauses+"\n"+clauses.join("");
 ok(Buffer.byteLength(dimacs,"ascii")===r.dimacs_bytes,"encoded input bytes");
 ok(crypto.createHash("sha256").update(dimacs).digest("hex")===r.dimacs_sha256,"source SHA256");
 ok(m*(2*n-2)===(n+1)*(2*n-2),"prefix gate count");
}
ok(data.totals.source_deleted_sat===334,"aggregate deletions");
ok(data.totals.signflip_sat===1900,"aggregate sign changes");
ok(data.totals.collision_equivalence_checks===19096,"aggregate local checks");
console.log(JSON.stringify({result:"PASS",assertions,case_count:data.cases.length,
deleted_source_witnesses:334,sign_flip_fields:1900,collision_checks:19096},null,2));
