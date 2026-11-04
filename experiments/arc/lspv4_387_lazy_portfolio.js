'use strict';
// LSPV-4/387, reproducible Node.js finite controls. Run: node lspv4_387_lazy_portfolio.js
const assert = require('assert');
let checks=0, childChecks=0, totalRaw=0, malformedRejected=0;
const cases=[];
function eq(a,b,msg){ checks++; assert.deepStrictEqual(a,b,msg); }
function parent(n,b){
  if(!Number.isInteger(n)||n<1||![0,1].includes(b))throw Error('bad source spec');
  let s='p cnf '+(n+1)+' '+(n+2)+'\n1 0\n'+(b?1:-1)+' 0\n';
  for(let i=2;i<=n+1;i++)s+=i+' 0\n';
  return s;
}
function child(q,d,j,b){
  if(!Number.isInteger(q)||!Number.isInteger(d)||q<1||d<0||j<1||j>q||![0,1].includes(b))throw Error('bad child spec');
  const v=j+1;
  let s='p cnf '+(q+d+2)+' '+(d+2)+'\n'+v+' 0\n'+(b?v:-v)+' 0\n';
  for(let i=1;i<=d;i++)s+=(q+i+2)+' 0\n';
  return s;
}
function parseDimacs(s){
  if(typeof s!=='string')throw Error('non-string');
  const lines=s.trimEnd().split('\n');
  if(!/^p cnf [1-9][0-9]* [0-9]+$/.test(lines[0]))throw Error('header');
  const [, , vars, count]=lines[0].split(' ');
  const v=Number(vars),m=Number(count);
  if(!Number.isSafeInteger(v)||!Number.isSafeInteger(m)||m!==lines.length-1)throw Error('counts');
  const clauses=[];
  for(let i=1;i<lines.length;i++){
    if(!/^-?[1-9][0-9]*(?: -?[1-9][0-9]*)* 0$/.test(lines[i]))throw Error('clause format');
    const a=lines[i].split(' ').slice(0,-1).map(Number);
    if(a.some(x=>!Number.isSafeInteger(x)||Math.abs(x)>v))throw Error('invalid literal');
    clauses.push(a);
  }
  return clauses;
}
function satExhaustive(s){
  const cs=parseDimacs(s), vv=[...new Set(cs.flat().map(x=>Math.abs(x)))];
  if(vv.length>16)throw Error('finite verifier variable cap');
  const index=new Map(vv.map((v,i)=>[v,i]));
  for(let a=0;a<(1<<vv.length);a++)
    if(cs.every(c=>c.some(l=>Boolean(a&(1<<index.get(Math.abs(l))))===(l>0))))return true;
  return false;
}
function lazyBit(s,i){
  if(!Number.isInteger(i)||i<0||i>=s.length)throw Error('index');
  return s.charCodeAt(i);
}
const lambda=.10,zeta=.02;
for(let n=1;n<=12;n++)for(let b=0;b<=1;b++){
  const source=parent(n,b),N=Buffer.byteLength(source,'utf8');
  const q=Math.ceil(N**(1-lambda+zeta));
  const d=Math.max(1,Math.ceil(N**lambda/Math.log2(N+2)));
  eq(satExhaustive(source),b===1,'source label');
  let both=true,either=false,len=0;
  const distinct=new Set();
  for(let j=1;j<=q;j++){
    const g=child(q,d,j,b),sat=satExhaustive(g);
    eq(sat,b===1,'child label');
    both=both&&sat;either=either||sat;
    len+=Buffer.byteLength(g,'utf8'); distinct.add(g);
    for(const i of [0,Math.floor(g.length/2),g.length-1])eq(lazyBit(g,i),g.charCodeAt(i));
    childChecks++;
  }
  eq(both,b===1);eq(either,b===1);eq(distinct.size,q);
  totalRaw+=len;
  cases.push({n,b,parent_bytes:N,Q:q,pad_units:d,raw_child_bytes:len,distinct:q});
}
const malformed=[
'p cnf 1 1\n1 0\n2 0\n','p cnf 1 2\n1 0\n','p cnf 0 1\n1 0\n',
'p cnf 1 1\n2 0\n','p cnf 1 1\n1\n','p cnf 1 1\n0\n',
'p cnf 1 1\n01 0\n','p cnf 1 1\n-0 0\n','p cnf 1 1\n1  0\n','p cnf 1 1\n1 0\n0\n'];
for(const s of malformed){let bad=false;try{parseDimacs(s)}catch(_){bad=true}eq(bad,true);malformedRejected++}
function xorEdge(a,b,odd){return odd?[[a,b],[-a,-b]]:[[a,-b],[-a,b]]}
function triangle(parity){
  let cs=[];for(const [a,b,t] of [[1,2,0],[2,3,0],[3,1,parity]])cs.push(...xorEdge(a,b,t));
  return 'p cnf 3 '+cs.length+'\n'+cs.map(c=>c.join(' ')+' 0\n').join('');
}
eq(satExhaustive(triangle(1)),false);
eq(satExhaustive(triangle(0)),true);
const out={status:'PASS',label:'COMPUTATIONAL only',cases:cases.length,children:childChecks,assertions:checks,malformed_rejected:malformedRejected,total_raw_child_bytes:totalRaw,parameters:{lambda,zeta},case_rows:cases};
console.log(JSON.stringify(out,null,2));
