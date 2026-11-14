'use strict';
// TMR-1/021 exact hosted-V8-executed functions, no external packages. Finite research control.
function sr(x,j){return j===0?"<":j===x.length+1?">":j>=1&&j<=x.length?x[j-1]:"_";}

function wr(t,j){return t.has(j)?t.get(j):"_";}

function qr(p,j){const b=p.toString(2);return j===0?"<":j===b.length+1?">":j>=1&&j<=b.length?b[j-1]:"_";}

function dt(a,b,t){const d=b-a;return Math.abs(d)<=2*t?d:(d>0?"F+":"F-");}

function prep(x,mode){
 const L=x.length,v=parseInt(x,2),wt=new Map([...x].map((z,i)=>[i+1,z]));let ss,ws,q=0;
 if(mode==="near"){ss=[1,2];ws=[1,2];}
 else if(mode==="separate"){ss=[0,L+1];ws=[0,L+1];}
 else if(mode==="overlap"){ss=[2,2];ws=[Math.floor(L/2),Math.floor(L/2)];}
 else if(mode==="far"){ss=[-4*L-v,-4*L-v+1];ws=[3*L+v,3*L+v+1];}
 else if(mode==="far_split"){ss=[-4*L-v,4*L+v];ws=[3*L+v,-3*L-v];}
 else {ss=[2+v%3,3+v%3];ws=[Math.floor(L/2)+v%2,Math.floor(L/2)+v%2+1];q=[...x].reduce((s,z)=>s+ +z,0)%2;}
 return {ss,ws,wt,q};
}

function fp(x,m,t,geom=true){
 const src=m.ss.map(h=>Array.from({length:2*t+1},(_,i)=>sr(x,h+i-t)).join(""));
 const work=m.ws.map(h=>Array.from({length:2*t+1},(_,i)=>wr(m.wt,h+i-t)).join(""));
 return JSON.stringify([m.q,src,work,geom?[dt(...m.ss,t),dt(...m.ws,t)]:[]]);
}

function probe(x,m,p,t){
 let ss=[...m.ss],ws=[...m.ws],wt=new Map(m.wt),q=m.q,qp=0,trace=[];
 for(let step=0;step<t;step++){
  const a=ss.map(h=>sr(x,h)),b=ws.map(h=>wr(wt,h)),c=qr(p,qp),equal=[ss[0]===ss[1],ws[0]===ws[1]];
  const seed=11*q+a.reduce((s,z,i)=>s+(i+1)*z.charCodeAt(0),0)+3*b.reduce((s,z,i)=>s+(i+3)*z.charCodeAt(0),0)+c.charCodeAt(0)+7*+equal[0]+13*+equal[1];
  const sd=[seed%3-1,Math.floor(seed/3)%3-1],wd=[Math.floor(seed/9)%3-1,Math.floor(seed/27)%3-1],qd=Math.floor(seed/81)%3-1;
  const write=["0","1","_"][Math.floor(seed/243)%3],qnext=(3*q+seed)%17,halt=seed%29===0;
  trace.push(JSON.stringify([q,a,b,c,equal,sd,wd,qd,write,qnext,halt?seed%2?"SAT":"UNSAT":null]));
  if(halt)break;
  for(const h of ws)wt.set(h,write);
  ss=ss.map((h,i)=>h+sd[i]);ws=ws.map((h,i)=>h+wd[i]);qp+=qd;q=qnext;
 }
 return trace;
}

function run(){
 const counts={cases:0,collision_pairs:0,paired_index_queries:0,compared_transitions:0,far_head_pairs:0,overlap_pairs:0,shared_head_collisions:0,naive_geometry_counterexamples:0,assertion_failures:0},examples=[];
 for(let L=5;L<=9;L++){
  const xs=Array.from({length:1<<L},(_,i)=>i.toString(2).padStart(L,"0"));
  for(const mode of ["near","separate","overlap","far","far_split","variable"])for(const t of [0,1,2,3]){
   counts.cases++;const buckets=new Map();
   for(const x of xs){const st=prep(x,mode),key=fp(x,st,t);if(!buckets.has(key))buckets.set(key,[]);if(buckets.get(key).length<2)buckets.get(key).push({x,st});}
   for(const members of buckets.values()){
    if(members.length<2)continue;
    const [a,b]=members;
    if(a.x===b.x||fp(a.x,a.st,t)!==fp(b.x,b.st,t))throw Error("bad collision");
    const p=[...a.x].findIndex((z,i)=>z!==b.x[i])+1;
    if(!p)throw Error("missing opposite bit");
    counts.collision_pairs++;
    if(mode==="far"||mode==="far_split")counts.far_head_pairs++;
    if(mode==="overlap")counts.overlap_pairs++;
    if(a.st.ws[0]===a.st.ws[1])counts.shared_head_collisions++;
    for(const idx of new Set([1,L,p,Math.floor((L+1)/2)])){
     const ta=probe(a.x,a.st,idx,t),tb=probe(b.x,b.st,idx,t);
     if(JSON.stringify(ta)!==JSON.stringify(tb))throw Error(`local replay failed L=${L}, mode=${mode}, t=${t}`);
     counts.paired_index_queries++;counts.compared_transitions+=ta.length;
    }
    if(examples.length<12)examples.push({L,mode,t,x:a.x,y:b.x,distinguishing_query:p});
   }
  }
 }
 const x="00000",a={ss:[-20,-19],ws:[0,0],wt:new Map(),q:0},b={ss:[-20,-19],ws:[0,1],wt:new Map(),q:0};
 if(fp(x,a,1,false)!==fp(x,b,1,false)||fp(x,a,1)===fp(x,b,1)||a.ws[0]!==a.ws[1]||b.ws[0]===b.ws[1])throw Error("counterexample failure");
 counts.naive_geometry_counterexamples++;
 return {role:"TMR-1/021",timestamp:"2026-11-14 07:07 PST",status:"COMPUTATIONAL",model:"two sensing source heads sharing one original-input tape; two sensing work heads sharing one writable tape",counts,
  counterexample:{same_one_step_local_windows:true,work_heads_a:[0,0],work_heads_b:[0,1],collision_a:true,collision_b:false,repair:"pairwise clipped relative displacement"},examples};
}

console.log(JSON.stringify(run(),null,2));
