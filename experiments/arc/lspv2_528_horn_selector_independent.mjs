#!/usr/bin/env node
// LSPV-2/528: independent original-source Horn-selector RUP verifier.
// Uses Node.js standard library only; no historical R_mix341 claim.
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
function proper(n,h){
  if(!Number.isInteger(n)||n<3||!Array.isArray(h)||!h.length)throw Error('bad 3-CNF');
  for(const c of h)if(!Array.isArray(c)||c.length!==3||
    c.some(l=>!Number.isInteger(l)||l===0||Math.abs(l)>n)||
    new Set(c.map(Math.abs)).size!==3)throw Error('bad proper clause');
  return h;
}
function dimacs(n,h){return 'p cnf '+n+' '+h.length+'\n'+h.map(c=>c.join(' ')+' 0\n').join('');}
function parse(t){
  if(typeof t!=='string'||!/^p cnf [0-9]+ [0-9]+\n/.test(t))throw Error('bad header');
  const l=t.trimEnd().split('\n'),p=l[0].split(' '),n=Number(p[2]),m=Number(p[3]);
  if(l.length!==m+1||!Number.isSafeInteger(n)||!Number.isSafeInteger(m))throw Error('bad size');
  const cs=l.slice(1).map(x=>{
    if(!/^(-?[0-9]+ )+0$/.test(x))throw Error('bad clause line');
    const c=x.split(' ').slice(0,-1).map(Number);
    if(c.some(v=>!Number.isSafeInteger(v)||!v||Math.abs(v)>n))throw Error('bad literal');
    return c;
  });
  return {n,cs};
}
function build(n,h){
  proper(n,h);const m=h.length,z=j=>2*n+j,w=j=>2*n+m+j-1,fixed=[];
  h.forEach((c,j)=>c.forEach(l=>fixed.push([-(l>0?l:n-l),z(j+1)])));
  if(m===1)fixed.push([-z(1)]);
  else {
    fixed.push([-z(1),-z(2),w(2)]);
    for(let j=3;j<=m;j++)fixed.push([-w(j-1),-z(j),w(j)]);
    fixed.push([-w(m)]);
  }
  const units=Array.from({length:2*n},(_,i)=>[i+1]);
  return {vars:2*n+2*m-1,fixed,units,full:[...fixed,...units]};
}
function rupEmpty(clauses){
  const a=new Map();let scans=0,assigns=0;
  for(;;){
    let change=false;
    for(const c of clauses){
      scans++;let trueClause=false,remaining=[];
      for(const l of c){
        const x=a.get(Math.abs(l));
        if(x===undefined)remaining.push(l);
        else if(x===(l>0)){trueClause=true;break;}
      }
      if(trueClause)continue;
      if(!remaining.length)return {ok:true,scans,assigns};
      if(remaining.length===1){
        const l=remaining[0],id=Math.abs(l),val=l>0;
        if(a.has(id) && a.get(id)!==val)return {ok:true,scans,assigns};
        if(!a.has(id)){a.set(id,val);assigns++;change=true;}
      }
    }
    if(!change)return {ok:false,scans,assigns};
  }
}
function checkpoint(n,fixed,s){return [...fixed,...s.map((v,i)=>[v?i+1:n+i+1])];}
function satisfies(h,s){return h.every(c=>c.some(l=>s[Math.abs(l)-1]===(l>0)));}
function k4(d){
  const E=[[1,2,3],[1,4,5],[2,4,6],[3,5,6]],h=[];
  E.forEach((edges,j)=>{for(let t=0;t<8;t++){
    const bits=[(t>>2)&1,(t>>1)&1,t&1];
    if((bits.reduce((a,b)=>a+b,0)%2)===d[j])continue;
    h.push(edges.map((e,i)=>bits[i]?-e:e));
  }});return h;
}
const cases=[];
cases.push(['all_signed8',3,Array.from({length:8},(_,s)=>[1,2,3].map((v,i)=>(s>>i)&1?-v:v))]);
[[0,0,0,0],[1,0,0,0],[1,1,0,0]].forEach(d=>cases.push(['k4_'+d.join(','),6,k4(d)]));
let seed=0x528;function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n;}
for(let n=3;n<=7;n++)for(let trial=0;trial<5;trial++){
  const h=[],m=1+rnd(10);
  for(let j=0;j<m;j++){
    const ids=Array.from({length:n},(_,i)=>i+1);
    for(let q=n-1;q>0;q--){const p=rnd(q+1);[ids[p],ids[q]]=[ids[q],ids[p]];}
    h.push(ids.slice(0,3).map(v=>rnd(2)?-v:v));
  }
  cases.push(['random_'+n+'_'+trial,n,h]);
}
let checks=0,states=0,sat=0,unsat=0,spurious=0,scans=0,assigns=0;
const results=[];
for(const [tag,n,h] of cases){
  proper(n,h);const source=dimacs(n,h);assert.deepEqual(parse(source).cs,h);checks++;
  const b=build(n,h),tmpl=dimacs(b.vars,b.full);
  assert.deepEqual(parse(tmpl).cs,b.full);checks++;
  assert(b.fixed.every(c=>c.filter(l=>l>0).length<=1));checks++;
  assert(rupEmpty(b.full).ok);checks++;
  let accepting=0;
  for(let mask=0;mask<2**n;mask++){
    const s=Array.from({length:n},(_,i)=>Boolean(mask&(1<<i)));
    const run=rupEmpty(checkpoint(n,b.fixed,s));
    assert.equal(run.ok,satisfies(h,s),tag+':'+mask);
    checks++;states++;scans+=run.scans;assigns+=run.assigns;
    accepting+=Number(run.ok);
  }
  if(accepting)sat++;else{unsat++;spurious++;}
  results.push({id:tag,n,m:h.length,original_sha256:createHash('sha256').update(source).digest('hex'),
    template_sha256:createHash('sha256').update(tmpl).digest('hex'),
    choices:2**n,legal_terminal_rup_states:accepting,coarse_may_rup:true});
}
for(const x of ['', 'p cnf 3 1\n1 2 3\n', 'p cnf 3 2\n1 2 3 0\n',
 'p cnf 3 1\n4 2 3 0\n','p cnf 3 1\na b c 0\n','p cnf 3 1\n1 2 0 3\n']){
  assert.throws(()=>parse(x));checks++;
}
for(const [n,h] of [[3,[[1,1,2]]],[3,[[1,2,4]]],[3,[[0,2,3]]],[2,[[1,2,3]]]]){
  assert.throws(()=>proper(n,h));checks++;
}
process.stdout.write(JSON.stringify({status:'PROVED/RESTRICTED + COMPUTATIONAL',tests:cases.length,
  checkpoint_databases:states,sat_sources:sat,unsat_sources:unsat,spurious_joins:spurious,
  assertions:checks,up_clause_scans:scans,up_assignments:assigns,malformed_rejections:10,
  controls:results},null,2)+'\n');
