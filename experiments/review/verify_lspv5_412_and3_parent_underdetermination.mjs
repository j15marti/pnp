#!/usr/bin/env node
// Independent LSPV-5/412 replay.  This is an audit grammar, not the native
// historical R_mix341 checker.
import assert from 'node:assert/strict';
import crypto from 'node:crypto';

let checks = 0;
const ck = (x, m='check') => { checks++; assert.ok(x, m); };
class Reject extends Error {}
const key = x => `${Math.abs(x)}:${x<0?1:0}`;
const canonical = xs => [...xs].sort((a,b)=>key(a).localeCompare(key(b),undefined,{numeric:true}));
const proper = xs => Array.isArray(xs) && xs.length===new Set(xs).size && xs.every(x=>Number.isSafeInteger(x)&&x!==0&&!xs.includes(-x)) && JSON.stringify(xs)===JSON.stringify(canonical(xs));
const stable = x => JSON.stringify(x, Object.keys(x).sort());
const deepSort = x => Array.isArray(x) ? x.map(deepSort) : (x && typeof x==='object' ? Object.fromEntries(Object.keys(x).sort().map(k=>[k,deepSort(x[k])])) : x);
const bytes = x => Buffer.from(JSON.stringify(deepSort(x)));
const hash = x => crypto.createHash('sha256').update(bytes(x)).digest('hex');
const px = bs => bs.reduce((a,b)=>a^b,0);
const lval = (l,e) => l>0 ? e.get(l) : 1-e.get(-l);
const support = r => r.k==='c' ? [...new Set(r.c.map(Math.abs))].sort((a,b)=>a-b) : [...(r.s??r.m)];
const val = (r,e) => r.k==='c' ? +r.c.some(l=>lval(l,e)) : r.k==='f' ? r.t.reduce((ans,b,i)=>ans || (b && i===r.s.reduce((z,v,j)=>z+(e.get(v)<<j),0)),false)+0 : +(px(r.m.map(v=>e.get(v)))===r.r);
function factor(a,b){
  const s=[...new Set([...support(a),...support(b)])].sort((x,y)=>x-y);
  if(s.length>3) throw new Reject('support');
  const t=[]; for(let z=0;z<(1<<s.length);z++){const e=new Map(s.map((v,i)=>[v,(z>>i)&1]));t.push(val(a,e)&val(b,e));}
  return {k:'f',s,t};
}
const xor = (a,b) => ({k:'a',m:[...new Set([...a.m,...b.m])].filter(v=>a.m.includes(v)!==b.m.includes(v)).sort((x,y)=>x-y),r:a.r^b.r});
function resolvents(a,b,p){
  const out=[];
  for(const [u,v] of [[p,-p],[-p,p]]) if(a.includes(u)&&b.includes(v)){
    const c=canonical([...new Set([...a.filter(x=>x!==u),...b.filter(x=>x!==v)])]);
    if(!c.some(x=>c.includes(-x))) out.push(c);
  }
  return out;
}
class Checker{
  constructor(mode){this.mode=mode;this.rows=0;}
  run(d, terminal=true){
    if(d.schema!=='LSPV5-412-AUDIT-GRAMMAR'||!Array.isArray(d.source)||d.source.some(c=>!proper(c))||d.source_sha256!==hash(d.source))throw new Reject('source');
    const R=new Map(), O=new Map();
    d.source.forEach((c,i)=>{R.set(`s:${i}:clause`,{k:'c',c});O.set(`s:${i}:clause`,'SOURCE');});
    const ref=(x,now)=>{
      if(!x||!['source','node'].includes(x.kind)||!Number.isSafeInteger(x.id)||typeof x.view!=='string')throw new Reject('ref');
      if(x.kind==='node'&&x.id>=now)throw new Reject('forward');
      const k=`${x.kind==='source'?'s':'n'}:${x.id}:${x.view}`; if(!R.has(k))throw new Reject('missing'); return [R.get(k),O.get(k)];
    };
    d.nodes.forEach((n,i)=>{
      if(n.id!==i||!Number.isSafeInteger(n.id))throw new Reject('id');
      if(n.rule==='RES'){
        const [a]=ref(n.left,i),[b]=ref(n.right,i); if(a.k!=='c'||b.k!=='c'||!proper(n.clause))throw new Reject('res type');
        if(!resolvents(a.c,b.c,n.pivot).some(c=>JSON.stringify(c)===JSON.stringify(n.clause)))throw new Reject('res');
        R.set(`n:${i}:clause`,{k:'c',c:n.clause});O.set(`n:${i}:clause`,'RES');
      } else if(n.rule==='AND3'){
        const [a,ao]=ref(n.left,i),[b,bo]=ref(n.right,i); if(!['c','f'].includes(a.k)||!['c','f'].includes(b.k))throw new Reject('and type');
        if(this.mode==='TAGGED'&&![ao,bo].every(o=>['SOURCE','AND3'].includes(o)))throw new Reject('TAGGED AND3 parent');
        const f=factor(a,b); if(JSON.stringify(n.factor)!==JSON.stringify({support:f.s,truth:f.t}))throw new Reject('factor'); this.rows+=1<<f.s.length;
        R.set(`n:${i}:factor`,f);O.set(`n:${i}:factor`,'AND3');
        if(n.affine){const q={k:'a',m:n.affine.mask,r:n.affine.rhs};for(let z=0;z<(1<<f.s.length);z++){const e=new Map(f.s.map((v,j)=>[v,(z>>j)&1]));if(val(f,e)!==val(q,e))throw new Reject('affine');this.rows++;}R.set(`n:${i}:affine`,q);O.set(`n:${i}:affine`,'AND3');}
      } else if(n.rule==='GF2'){
        const [a]=ref(n.left,i),[b]=ref(n.right,i);if(a.k!=='a'||b.k!=='a')throw new Reject('gf2 type');const q=xor(a,b);
        if(JSON.stringify(n.affine)!==JSON.stringify({mask:q.m,rhs:q.r}))throw new Reject('gf2');R.set(`n:${i}:affine`,q);O.set(`n:${i}:affine`,'GF2');
      } else throw new Reject('rule');
    });
    if(terminal){const q=R.get(`n:${d.nodes.length-1}:affine`);if(!q||q.m.length||q.r!==1)throw new Reject('not contradiction');}
    return {paid:d.nodes.length,rows:this.rows};
  }
}
const sr=i=>({kind:'source',id:i,view:'clause'}), nr=(i,v)=>({kind:'node',id:i,view:v});
function source(ch){
  const es=[[1,2],[1,3],[1,4],[2,3],[2,4],[3,4]], inc=[[],[],[],[],[]];es.forEach((e,i)=>e.forEach(v=>inc[v].push(i+1)));
  const s=[],pack=[];for(let v=1;v<=4;v++){const ids=[];for(let z=0;z<8;z++){const bs=[z&1,(z>>1)&1,(z>>2)&1];if(px(bs)!==ch[v-1]){ids.push(s.length);s.push(canonical(inc[v].map((x,i)=>bs[i]?-x:x)));}}pack.push([ids,[...inc[v]].sort((a,b)=>a-b),ch[v-1]]);}return [s,pack];
}
class Build{
  constructor(s){this.s=s;this.n=[];this.r=new Map(s.map((c,i)=>[`s:${i}:clause`,{k:'c',c}]));}
  get(x){return this.r.get(`${x.kind==='source'?'s':'n'}:${x.id}:${x.view}`);}
  res(l,r,p,c){const i=this.n.length;this.n.push({id:i,rule:'RES',left:l,right:r,pivot:p,clause:c});this.r.set(`n:${i}:clause`,{k:'c',c});return nr(i,'clause');}
  and(l,r,q=null){const i=this.n.length,f=factor(this.get(l),this.get(r)),x={id:i,rule:'AND3',left:l,right:r,factor:{support:f.s,truth:f.t}};if(q)x.affine={mask:q[0],rhs:q[1]};this.n.push(x);this.r.set(`n:${i}:factor`,f);if(q)this.r.set(`n:${i}:affine`,{k:'a',m:q[0],r:q[1]});return [nr(i,'factor'),q?nr(i,'affine'):null];}
  gf(l,r){const i=this.n.length,q=xor(this.get(l),this.get(r));this.n.push({id:i,rule:'GF2',left:l,right:r,affine:{mask:q.m,rhs:q.r}});this.r.set(`n:${i}:affine`,q);return nr(i,'affine');}
  doc(){return {schema:'LSPV5-412-AUDIT-GRAMMAR',source:this.s,source_sha256:hash(this.s),nodes:this.n};}
}
function packets(b,refs,p){let rows=[];refs.forEach((rr,i)=>{const [a]=b.and(rr[0],rr[1]);const [c]=b.and(rr[2],rr[3]);const [,q]=b.and(a,c,[p[i][1],p[i][2]]);rows.push(q);});let q=rows[0];for(let i=1;i<rows.length;i++)q=b.gf(q,rows[i]);}
function base(ch){const [s,p]=source(ch),b=new Build(s);packets(b,p.map(x=>x[0].map(sr)),p);return b.doc();}
function split(ch){const [s,p]=source(ch),ss=[],pairs=[];s.forEach((c,i)=>{const a=7+i,p0=canonical([c[0],c[1],a]),q0=canonical([c[0],c[2],-a]);pairs.push([ss.length,ss.length+1,a,c]);ss.push(p0,q0);});const b=new Build(ss),r=pairs.map(x=>b.res(sr(x[0]),sr(x[1]),x[2],x[3]));packets(b,p.map(x=>x[0].map(i=>r[i])),p);return b.doc();}
function models(s){const n=Math.max(...s.flat().map(Math.abs));let c=0;for(let z=0;z<(1<<n);z++){const e=new Map(Array.from({length:n},(_,i)=>[i+1,(z>>i)&1]));if(s.every(cl=>cl.some(l=>lval(l,e))))c++;}return c;}
const odd=base([1,0,0,0]),even=base([0,0,0,0]),sp=split([1,0,0,0]);
ck(models(odd.source)===0);ck(models(even.source)===8);ck(odd.nodes.length===15);ck(sp.nodes.length===31);
ck(new Checker('EXTENSIONAL').run(odd).paid===15);ck(new Checker('TAGGED').run(odd).paid===15);ck(new Checker('EXTENSIONAL').run(sp).paid===31);
try{new Checker('TAGGED').run(sp);assert.fail();}catch(e){ck(e.message==='TAGGED AND3 parent');}
try{new Checker('EXTENSIONAL').run(even);assert.fail();}catch(e){ck(e.message==='not contradiction');}
const muts=[
 d=>d.source_sha256='0'.repeat(64), d=>d.nodes[0].pivot=1, d=>d.nodes[16].left.id=999,
 d=>d.nodes[0].id=Number.MAX_SAFE_INTEGER+1, d=>d.nodes[16].factor.truth[0]^=1,
 d=>d.nodes[18].affine.rhs^=1, d=>d.nodes.at(-1).affine.rhs=0, d=>d.nodes[0].rule='ORACLE'
];
for(const f of muts){const d=structuredClone(sp);f(d);try{new Checker('EXTENSIONAL').run(d);assert.fail();}catch{ck(true);}}
const c={k:'c',c:odd.source[0]},f=factor(c,c);for(let z=0;z<(1<<f.s.length);z++){const e=new Map(f.s.map((v,i)=>[v,(z>>i)&1]));ck(val(c,e)===val(f,e));}
console.log(JSON.stringify({schema:'LSPV5/412-independent-node',status:'PASS',checks,base_paid:15,split_paid:31,base_both_grammars:true,split_extensional:true,split_tagged:false,split_tagged_reason:'TAGGED AND3 parent',odd_models:0,even_models:8,mutations_rejected:muts.length,base_sha256:hash(odd),split_sha256:hash(sp)},null,2));
