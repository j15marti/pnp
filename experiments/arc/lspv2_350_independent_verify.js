/* Independent no-import Node proof/DIMACS verifier for LSPV-2 350.
   Usage: node thisfile.js results/raw/arc/2026-11-02_2112_LSPV2_GUARD_EXCESS_CAP350.json */
'use strict';
const fs=require('fs');const file=process.argv[2];if(!file)throw Error('supply raw JSON');
const x=JSON.parse(fs.readFileSync(file,'utf8'));let checks=0;
function insist(ok,msg){checks++;if(!ok)throw Error(msg);}
function normalize(clause){const s=new Set(clause);const a=[...s].sort((u,v)=>Math.abs(u)-Math.abs(v)||u-v);if(a.some(v=>s.has(-v)))throw Error('tautology');return a;}
function verifySource(cs,n){if(!Number.isInteger(n)||!Array.isArray(cs))throw Error('invalid source');
for(const c of cs){if(!Array.isArray(c)||!c.length)throw Error('bad clause');
const t=new Set();for(const l of c){if(!Number.isInteger(l)||!l||Math.abs(l)>n||t.has(l)||t.has(-l))throw Error('bad signed occurrence');t.add(l);}}}
function pivot(a,b,p){if(!Number.isInteger(p)||p<1)throw Error('pivot');
if(a.includes(p)&&b.includes(-p))return normalize([...a.filter(v=>v!==p),...b.filter(v=>v!==-p)]);
if(a.includes(-p)&&b.includes(p))return normalize([...a.filter(v=>v!==-p),...b.filter(v=>v!==p)]);
throw Error('not complementary');}
function replay(source,steps){const all=source.map(normalize);for(const step of steps){const [u,v]=step.parents||[];
if(!Number.isInteger(u)||!Number.isInteger(v)||u<0||v<0||u>=all.length||v>=all.length)throw Error('parent index');
const next=pivot(all[u],all[v],step.pivot);if(JSON.stringify(next)!==JSON.stringify(step.clause))throw Error('resolvent');all.push(next);}
if(JSON.stringify(all.at(-1))!=='[]')throw Error('not contradictory');return all;}
function models(cs,n){let count=0;for(let mask=0;mask<(1<<n);mask++){let good=true;
for(const c of cs)if(!c.some(v=>Boolean(mask & (1<<(Math.abs(v)-1)))===(v>0))){good=false;break;}
if(good)count++;}return count;}
const original=[[-1,2],[-2,3],[-3,4],[-4,5],[1,-5],[1,2,3,4,5],[-1,-2,-3,-4,-5]];
insist(x.cases.length===4,'four cases');
let dels=0,signs=0;
for(const c of x.cases){const {t,variables,sources,proof}=c,m=7,k=1<<t;
verifySource(sources,variables);insist(sources.length===m*k,'source count');
for(let e=0;e<k;e++)for(let i=0;i<m;i++){
 const want=[...original[i],...Array.from({length:t},(_,j)=>e&(1<<j)?-(6+j):(6+j))];
 insist(JSON.stringify(normalize(want))===JSON.stringify(normalize(sources[e*m+i])),'authentic signed copy');}
const all=replay(sources,proof);
insist(proof.length===9+m*(k-1),'all rule nodes');insist(c.constructed_upper===proof.length,'declared upper');
for(let i=0;i<m;i++)if(t){const idx=sources.length+i*(k-1)+k-2;
 insist(JSON.stringify(all[idx])===JSON.stringify(normalize(original[i])),'eliminated copy');}
insist(models(sources,variables)===0,'UNSAT');
for(let i=0;i<sources.length;i++){const v=models(sources.filter((_,j)=>i!==j),variables);
 insist(v===c.deletion_counts[i]&&v>0,'deletion SAT');dels++;}
let j=0;for(let i=0;i<sources.length;i++)for(let p=0;p<sources[i].length;p++){
const edited=sources.map(a=>a.slice());edited[i][p]*=-1;const v=models(edited,variables);
insist(v===c.sign_flip_counts[j]&&v>0,'one sign flip SAT');signs++;j++;}
}
insist(models([[1,2],[-1,2]],2)===2,'positive SAT fixture');
insist(models([[1],[-1]],1)===0,'negative UNSAT fixture');
let malformed=0;for(const f of [{n:2,c:[[0]]},{n:2,c:[[3]]},{n:2,c:[[]]},{n:2,c:[[1,-1]]},{n:2,c:[[1,1]]},{n:0,c:[[1]]},{n:1,c:[null]},{n:1,c:[[1.5]]}])try{verifySource(f.c,f.n);}catch(e){malformed++;}
insist(malformed===8,'all malformed rejected');
let corruptions=0;for(let z=0;z<4;z++){const c=x.cases[1],bad=JSON.parse(JSON.stringify(c.proof));
if(z===0)bad[0].pivot=999;if(z===1)bad[0].parents=[-1,1];if(z===2)bad[0].clause=[999];if(z===3)bad.pop();
try{replay(c.sources,bad);}catch(e){corruptions++;}}
insist(corruptions===4,'all corruptions rejected');
insist(dels===x.total_deletion_checks&&signs===x.total_sign_checks,'control totals');
console.log(JSON.stringify({status:'PASS',assertions:checks,source_deletions:dels,sign_inversions:signs,malformed_rejected:malformed,corrupt_proofs_rejected:corruptions},null,2));
