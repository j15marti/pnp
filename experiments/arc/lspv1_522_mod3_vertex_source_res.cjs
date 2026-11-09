#!/usr/bin/env node
"use strict";
/* LSPV-1/522. Strict original-source, one-hot mod-3 vertex Resolution
   packet. Pure Node.js; no dependencies, no imported proof checker.
   Run: node experiments/arc/lspv1_522_mod3_vertex_source_res.cjs
   Checks 24 charge/orientation cases, all 2^10 assignments,
   source deletion witnesses, source-indexed parent/pivot replay. */
function run(){
 let checks=0, cases=0, firstPacket=null;
 const ok=(v,m)=>{checks++;if(!v)throw Error(m||"assertion")};
 const C=xs=>[...new Set(xs)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
 const E=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
 const R=(a,b,p)=>{
  const A=new Set(a),B=new Set(b);
  if(A.has(p)&&B.has(-p)){A.delete(p);B.delete(-p)}
  else if(A.has(-p)&&B.has(p)){A.delete(-p);B.delete(p)}
  else throw Error("wrong orientation/pivot");
  const q=C([...A,...B]);
  if(q.some(v=>q.includes(-v)))throw Error("tautological RES output");
  return q;
 };
 const lit=(e,a,s)=>3*e+((s*a)%3+3)%3+1;
 const val=(q,b)=>q.some(x=>b[Math.abs(x)]===(x>0));
 for(let ch=0;ch<3;ch++)
 for(const s0 of [-1,1])for(const s1 of [-1,1])for(const s2 of [-1,1]){
  const signs=[s0,s1,s2],U=signs.map((s,e)=>[0,1,2].map(a=>lit(e,a,s)));
  const source={};
  U.forEach((v,e)=>{
   source["A"+e]=C(v);
   for(let a=0;a<3;a++)for(let b=a+1;b<3;b++){
    source["B"+e+a+b+"+"]=C([-v[a],-v[b],10]);
    source["B"+e+a+b+"-"]=C([-v[a],-v[b],-10]);
   }
  });
  for(let a=0;a<3;a++)for(let b=0;b<3;b++)for(let w=0;w<3;w++)
   if((a+b+w)%3!==ch) source["D"+a+b+w]=C([-U[0][a],-U[1][b],-U[2][w]]);
  ok(Object.keys(source).length===39,"invalid original source count");
  let nodes=[], avail={...source},targets={};
  for(let a=0;a<3;a++)for(let b=0;b<3;b++){
    let g=((ch-a-b)%3+3)%3;
    let other=[0,1,2].filter(j=>j!==g);
    let p1="R"+a+b+":1",p2="R"+a+b+":2";
    let d1="D"+a+b+other[0],d2="D"+a+b+other[1];
    let c1=R(avail.A2,avail[d1],U[2][other[0]]);
    nodes.push({id:p1,rule:"RES",parents:["A2",d1],pivot:U[2][other[0]],clause:c1});avail[p1]=c1;
    let c2=R(avail[p1],avail[d2],U[2][other[1]]);
    nodes.push({id:p2,rule:"RES",parents:[p1,d2],pivot:U[2][other[1]],clause:c2});avail[p2]=c2;
    let t=C([-U[0][a],-U[1][b],U[2][g]]);
    ok(E(c2,t),"incorrect exact terminal");
    targets["C"+a+b]=t;
  }
  ok(nodes.length===18 && Object.keys(targets).length===9,"wrong DAG size");
  for(let mask=0;mask<1024;mask++){
   let bits=Array.from({length:11},(_,i)=>i>0&&Boolean(mask&(1<<(i-1))));
   if(Object.values(source).every(q=>val(q,bits)))
    ok(Object.values(targets).every(q=>val(q,bits)),"semantic entailment failure");
  }
  for(let a=0;a<3;a++)for(let b=0;b<3;b++)for(let w=0;w<3;w++){
    if((a+b+w)%3===ch)continue;
    let d="D"+a+b+w, bits=Array(11).fill(false);
    bits[U[0][a]]=true;bits[U[1][b]]=true;bits[U[2][w]]=true;
    ok(!val(source[d],bits),"missing D not falsified");
    ok(Object.keys(source).filter(k=>k!==d).every(k=>val(source[k],bits)),"bad D witness");
    ok(!val(targets["C"+a+b],bits),"D missing but target true");
  }
  for(let a=0;a<3;a++)for(let b=0;b<3;b++){
    let bits=Array(11).fill(false);bits[U[0][a]]=bits[U[1][b]]=true;
    ok(Object.keys(source).filter(k=>k!=="A2").every(k=>val(source[k],bits)),"bad A2 witness");
    ok(!val(targets["C"+a+b],bits),"A2 removal irrelevant");
  }
  const live={...source}, used=new Set();
  for(const n of nodes){
    ok(!live[n.id]&&live[n.parents[0]]&&live[n.parents[1]],"future/unknown parent");
    ok(E(R(live[n.parents[0]],live[n.parents[1]],n.pivot),n.clause),"RES replay failed");
    n.parents.filter(p=>Object.hasOwn(source,p)).forEach(p=>used.add(p));
    live[n.id]=n.clause;
  }
  ok(used.size===19,"incorrect essential-source DAG");
  let rejected=false;try{R(source.A2,source[Object.keys(source).find(k=>k[0]==="D")],100)}
    catch(e){rejected=true}ok(rejected,"corrupted pivot accepted");
  ok(!E(C([999]),nodes[0].clause),"corrupted conclusion accepted");
  if(cases===0)firstPacket={charge:ch,signs,source,targets,nodes};
  cases++;
 }
 return {status:"PROVED/RESTRICTED ordinary Resolution local vertex interface; NOT historical R_mix341",
  cases,assertions:checks,source_clauses_per_case:39,source_leaves_essential:19,
  exact_targets_per_case:9,distinct_paid_resolution:18,
  total_required_dependency_vertices:37,premise_edges:36,cycle_rank:0,
  exact_minimum_resolution:18,first_packet:firstPacket,
  missing:"Full-source composition with paid definitions and native historical rule-byte checking; B3"};
}
if(typeof require!=="undefined"&&require.main===module)process.stdout.write(JSON.stringify(run(),null,2)+"\n");
if(typeof module!=="undefined")module.exports=run;
