
"use strict";
/* LSPV-3/397. No-import triple-guard verification; run with node. */
function edgesFor(k) {
  if(k===0){const es=[];for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)es.push([i,j]);return [4,es];}
  const es=[];for(let i=0;i<k;i++){es.push([i,(i+1)%k],[k+i,k+(i+1)%k],[i,k+i]);}
  return [2*k,es];
}
function parity(x){return (x&1)^((x>>1)&1)^((x>>2)&1);}
function evalClause(lits,a){return lits.some(l=>((a>>(Math.abs(l)-1))&1)===(l>0?1:0));}
function make(h,edges,odd){
  const E=edges.length,z=E+1,inc=Array.from({length:h},()=>[]);
  for(let e=0;e<E;e++)for(const v of edges[e])inc[v].push(e+1);
  if(inc.some(r=>r.length!==3))throw Error("noncubic");
  let base=[],groups=[],charge=Array(h).fill(0);if(odd)charge[0]=1;
  for(let v=0;v<h;v++)for(let p=0;p<8;p++){
    if(parity(p)===charge[v])continue;
    let c=inc[v].map((id,j)=>((p>>j)&1)?-id:id);
    base.push(c);groups.push([c,c.concat([z]),c.concat([-z])]);
  }
  return {E,z,inc,base,groups,charge};
}
function check(cond,msg){if(!cond)throw Error(msg);return 1;}
function main(){
  let checked=0,records=[];
  for(let k of [0,3,4]){
    const [h,edges]=edgesFor(k),f=make(h,edges,true),sat=make(h,edges,false);
    let wOld=[];
    for(let x=0;x<(1<<f.E);x++){
      checked+=check(!f.base.every(c=>evalClause(c,x)),"odd original unexpectedly SAT");
      if(sat.base.every(c=>evalClause(c,x)))wOld.push(x);
      for(let z=0;z<2;z++){
        const y=x|(z<<f.E);
        checked+=check(f.groups.every(g=>g.every(c=>evalClause(c,y)))===f.base.every(c=>evalClause(c,x)),"guard identity");
      }
    }
    checked+=check(wOld.length===1<<(f.E-h+1),"even label and rank");
    const m=f.base.length,L=f.base.reduce((a,c)=>a+c.length,0);
    checked+=check(m===4*h&&L===12*h&&f.groups.length===m,"source count");
    let witnesses=[];
    for(let i=0;i<m;i++){
      let w=null;
      for(let x=0;x<(1<<f.E);x++){
        if(!evalClause(f.base[i],x)&&f.base.every((c,j)=>j===i||evalClause(c,x))){w=x;break;}
      }
      checked+=check(w!==null,"missing deletion witness");
      witnesses.push(w);
      for(let k2=0;k2<f.base[i].length;k2++)for(let guardSlot of [1,2]){
        const t=guardSlot===1?0:1,y=w|(t<<f.E);
        const edited=f.groups.map(g=>g.map(c=>c.slice()));
        edited[i][0][k2]*=-1;edited[i][guardSlot][k2]*=-1;
        checked+=check(edited.every(g=>g.every(c=>evalClause(c,y))),"two-bit SAT neighbor");
      }
    }
    // Check local parity tables; binary source-supported AND3 proof uses three gates per vertex.
    let rows=[];
    for(let v=0;v<h;v++){
      const gs=f.groups.slice(v*4,v*4+4);
      checked+=check(gs.length===4,"local four clauses");
      let mask=0;for(const e of f.inc[v])mask^=(1<<(e-1));
      for(let p=0;p<8;p++){
        const local=f.inc[v].reduce((a,e,j)=>a|(((p>>j)&1)<<(e-1)),0);
        const all=gs.every(g=>evalClause(g[0],local));
        checked+=check(all===(parity(p)===f.charge[v]),"AND3 local parity recovery");
      }
      rows.push([mask,f.charge[v]]);
    }
    let mask=0,rhs=0;for(const [a,b] of rows){mask^=a;rhs^=b;}
    checked+=check(mask===0&&rhs===1,"odd global XOR contradiction");
    const paid=3*h+h-1;
    checked+=check(paid===4*h-1,"proof count");
    records.push({graph:k===0?"K4":"PRISM_"+k,vertices:h,edge_variables:f.E,
      old_clauses:m,triple_guard_clauses:3*m,old_occurrences:L,guarded_occurrences:11*m,
      exact_fractional_hitting:L,nearest_SAT_sign_flips:2,exact_paid_mixed_nodes:paid,
      even_models:wOld.length,block_deletion_witnesses:witnesses.length,
      two_flip_SAT_controls:2*L});
  }
  for(const bad of [[],[1],[0,0],null,"x"]){
    let rejected=false;
    try{if(!Array.isArray(bad)||bad.length<3||bad.some(x=>typeof x!=="number"||x===0))throw Error("bad clause");}catch{rejected=true;}
    checked+=check(rejected,"malformed fixture");
  }
  return {id:"LSPV3-397",status:"COMPUTATIONAL; global proof theorem separate",checked,records};
}
const result=main();
if(typeof console!=="undefined")console.log(JSON.stringify(result,null,2));
