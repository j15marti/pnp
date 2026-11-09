#!/usr/bin/env node
// LSPV-2/526 independent original-source RAT^- and RUP verifier.
import {createHash} from 'node:crypto';
import {readFileSync} from 'node:fs';
const py = JSON.parse(readFileSync(process.argv[2],'utf8'));
let assertions=0, failures=0, tested=0, malformed=0;
const ensure = (test,msg) => {assertions++; if(!test) {failures++;throw Error(msg)}};
function make(k){
  let cs=[];
  for(let i=0;i<k;i++){ const u=2+i*2,v=u+1;cs.push([1,u,v],[-1,u,v]);}
  return {clauses:cs,variables:2*k+1};
}
function originalBytes(clauses,v){return 'p cnf '+v+' '+clauses.length+'\n'+clauses.map(c=>c.join(' ')+' 0\n').join('');}
function parse(raw){
  const l=raw.split('\n');if(l[l.length-1]==='')l.pop();
  if(!l.length) throw Error('empty');
  const h=l[0].split(' ');
  if(h.length!==4||h[0]!=='p'||h[1]!=='cnf') throw Error('header');
  const n=+h[2],m=+h[3];
  if(!Number.isSafeInteger(n)||!Number.isSafeInteger(m)||n<1||m<0||l.length!==m+1)throw Error('dimensions');
  const cs=[];
  for(const row of l.slice(1)){
    const a=row.split(' ').map(Number);
    if(a.length!==4||a[3]!==0||a.slice(0,3).some(x=>x===0||Math.abs(x)>n||!Number.isInteger(x))||new Set(a.slice(0,3).map(Math.abs)).size!==3)throw Error('clause');
    cs.push(a.slice(0,3));
  }
  return {clauses:cs,variables:n};
}
function propagate(cnf,ass){
  const tr=new Map();
  for(const l of ass){if(tr.has(Math.abs(l))&&tr.get(Math.abs(l))!==(l>0))return true;tr.set(Math.abs(l),l>0)}
  let changed=true;
  while(changed){
    changed=false;
    for(const clause of cnf){
      let sat=false,un=[];
      for(const lit of clause){const x=tr.get(Math.abs(lit));if(x===undefined)un.push(lit);else if(x===(lit>0)){sat=true;break}}
      if(sat)continue;
      if(un.length===0)return true;
      if(un.length===1){let lit=un[0],id=Math.abs(lit);
        if(!tr.has(id)){tr.set(id,lit>0);changed=true}
        else if(tr.get(id)!==(lit>0))return true;
      }
    }
  }
  return false;
}
const rup=(cnf,C)=>propagate(cnf,C.map(x=>-x));
function rat(cnf,C,pivot){
  if(!C.includes(pivot))return [false,0];
  let tests=0;
  for(const D of cnf){if(!D.includes(-pivot))continue;
    tests++;
    const R=[...new Set([...C.filter(x=>x!==pivot),...D.filter(x=>x!==-pivot)])];
    if(R.some(x=>R.includes(-x)))continue;
    if(!rup(cnf,R))return [false,tests];
  }
  return [true,tests];
}
function satisfies(cnf,model){return cnf.every(C=>C.some(l=>model.get(Math.abs(l))===(l>0)))}
for(const r of py.runs){
  const {k,variables,original_clauses,sha256}=r, f=make(k), s=originalBytes(f.clauses,f.variables);
  ensure(f.variables===variables,'variables');ensure(f.clauses.length===original_clauses,'size');
  ensure(createHash('sha256').update(s).digest('hex')===sha256,'hash');
  ensure(JSON.stringify(parse(s))===JSON.stringify(f),'source parser');
  ensure(rup(f.clauses,[1])===false,'not RUP');
  const [valid,checks]=rat(f.clauses,[1],1);ensure(valid,'RAT');ensure(checks===k,'RAT checks');
  const yes=new Map(),no=new Map();for(let i=1;i<=f.variables;i++){yes.set(i,true);no.set(i,i===1?false:true)}
  ensure(satisfies(f.clauses,yes)&&satisfies(f.clauses,no),'both models');
  ensure(satisfies([...f.clauses,[1]],yes)&&!satisfies([...f.clauses,[1]],no),'model changes');
  ensure(!rat(f.clauses.filter((_,i)=>i!==0),[1],1)[0],'corrupt source');
  ensure(!rat([...f.clauses,[1]],[-1],-1)[0],'opposite RAT cannot follow');
  if(k<=5){let c=0;for(let mask=0;mask<(1<<variables);mask++){
    let a=new Map();for(let i=1;i<=variables;i++)a.set(i,!!(mask&(1<<(i-1))));if(satisfies(f.clauses,a))c++;
  }ensure(c===2*3**k,'exhaustive SAT counts')}
  tested++;
}
function xor3(triple,charge){
  const clauses=[];
  for(let b=0;b<8;b++){
    const vals=[!!(b&4),!!(b&2),!!(b&1)];
    const sum=vals.filter(Boolean).length%2;
    if(sum!==charge)clauses.push(triple.map((x,i)=>vals[i]?-x:x));
  }
  return clauses;
}
function rpar(n,permutation){
  const clauses=[];
  for(let q=0;q<2;q++){
    const order=q===0?Array.from({length:n},(_,i)=>i+1):permutation;
    const aux=Array.from({length:n-3},(_,i)=>n+q*(n-3)+i+1);
    const triples=[[order[0],order[1],aux[0]]];
    for(let i=0;i<n-4;i++)triples.push([aux[i],order[i+2],aux[i+1]]);
    triples.push([aux.at(-1),order.at(-2),order.at(-1)]);
    for(let i=0;i<triples.length;i++)clauses.push(...xor3(triples[i],q===1&&i===triples.length-1?1:0));
  }
  return {clauses,variables:3*n-6};
}
for(const r of py.rpar_controls){
  const f=rpar(r.n,r.permutation);
  ensure(f.variables===r.variables&&f.clauses.length===r.clauses,'rPar shape');
  ensure(createHash('sha256').update(originalBytes(f.clauses,f.variables)).digest('hex')===r.sha256,'rPar hash');
  let satCount=0;
  for(let mask=0;mask<(1<<f.variables);mask++){
    const ass=new Map();for(let i=1;i<=f.variables;i++)ass.set(i,!!(mask&(1<<(i-1))));
    if(satisfies(f.clauses,ass))satCount++;
  }
  ensure(satCount===0,'rPar UNSAT');
}
const rejects=['','p cnf 1 1\n1 2 3 0\n','p cnf 3 1\n1 1 2 0\n','p cnf 3 1\n1 2 3\n','p cnf 3 1\n1 2 3 0\n1 2 3 0\n','p cnf X 1\n1 2 3 0\n','p cnf 3 1\n1 2 3 0\nÿ'];
for(let b of rejects){try{parse(b);throw Error('accepted a malformed source')}catch(e){if(e.message==='accepted a malformed source')throw e;malformed++}}
ensure(malformed===7,'malformed count');
console.log(JSON.stringify({experiment:'LSPV2_526_INDEPENDENT_NODE_VERIFIER',assertions,failures,tested_original_sources:tested,malformed_rejections:malformed,largest_k:py.runs.at(-1).k,rpar_sources:py.rpar_controls.length,sha_first:py.runs[0].sha256,sha_last:py.runs.at(-1).sha256},null,2));
