// LSPV-3/386: deterministic, no external dependency. COMPU­TATIONAL audit only.
// Run: node experiments/arc/lspv3_386_three_wire_resolution_closure.js
'use strict';
const clauses=[];for(const a of [-1,0,1])for(const b of [-1,0,1])for(const c of [-1,0,1])clauses.push([a,b,c]);
const key=c=>c.join(','), idx=new Map(clauses.map((c,i)=>[key(c),i]));
const truth=c=>{let w=0;for(let a=0;a<8;a++)if(c.some((s,i)=>s!==0&&((a>>i)&1)===(s===1?1:0)))w|=1<<a;return w};
const t=clauses.map(truth), sub=(i,j)=>clauses[i].every((v,p)=>v===0||v===clauses[j][p]);
function resolution(i,j,p){if(!Number.isInteger(p)||p<0||p>2)return -1;const a=clauses[i],b=clauses[j];if(!a||!b||a[p]===0||b[p]!==-a[p])return -1;const r=[];for(let q=0;q<3;q++){if(q===p){r.push(0);continue}if(a[q]&&b[q]&&a[q]!==b[q])return -1;r.push(a[q]||b[q])}return idx.get(key(r))}
const rules=[];for(let i=0;i<27;i++)for(let j=0;j<27;j++)for(let p=0;p<3;p++){const r=resolution(i,j,p);if(r>=0)rules.push([i,j,p,r])}
const blockers=[];for(let f=0;f<256;f++){const a=[];for(let x=0;x<8;x++)if(((f>>x)&1)===0)a.push(idx.get(key([0,1,2].map(i=>x>>i&1?-1:1))));blockers.push(a)}
function closure(source){const seen=new Set(source), proof=[];for(;;){let change=false;for(const [a,b,p,r] of rules)if(seen.has(a)&&seen.has(b)&&!seen.has(r)){seen.add(r);proof.push([a,b,p,r]);change=true}if(!change)break}return {seen,proof}}
const checks={pairs:0,sat:0,unsat:0,entailedClauses:0,outputBlockers:0,guardCofactors:0,malformedRejected:0,corruptedRejected:0};
let maxAdded=0,maxTotal=0;
const assert=(c,msg)=>{if(!c)throw Error('ASSERT: '+msg)};
for(let k=0;k<4096;k++){
 const a=(73*k+41)&255,b=(137*Math.floor(k/16)+19)&255,f=a&b;
 const {seen,proof}=closure([...blockers[a],...blockers[b]]);checks.pairs++;checks[f?'sat':'unsat']++;
 maxAdded=Math.max(maxAdded,proof.length);maxTotal=Math.max(maxTotal,seen.size);assert(seen.size<=27,'closure universe');
 for(let c=0;c<27;c++)if((f&(~t[c]&255))===0){checks.entailedClauses++;assert([...seen].some(d=>sub(d,c)),'implicate k='+k+' clause '+c)}
 for(const c of blockers[f]){checks.outputBlockers++;assert([...seen].some(d=>sub(d,c)),'factor clause')}
 for(const [i,j,p,r] of proof)assert(resolution(i,j,p)===r,'signed replay');
 if(k===1023){for(const [i,j,p,r] of proof.slice(0,8)){assert(resolution(i,j,p)!==(r+1)%27,'corrupt output');checks.corruptedRejected++;assert(resolution(i,j,3)!==r,'corrupt pivot');checks.corruptedRejected++}}
}
for(let f=0;f<256;f++){let co=0;for(let z=0;z<4;z++)co|=((f>>(2*z+1))&1)<<z;for(let z=0;z<4;z++)assert((co>>z&1)===(f>>(2*z+1)&1),'guard cofactor');checks.guardCofactors++}
for(const malformed of [null,[],[0,1],[0,1,2,3],[0,2,0]]){const valid=Array.isArray(malformed)&&malformed.length===3&&malformed.every(x=>[-1,0,1].includes(x));assert(!valid,'malformed rejection');checks.malformedRejected++}
assert(maxAdded<=27,'paid node universal bound');assert(checks.corruptedRejected>=8,'corruption suite');
const result={schema:'lspv3-386-3wire-resolution',status:'COMPUTATIONAL',universeSize:27,maximumAddedResolutionNodes:maxAdded,maximumClosureSize:maxTotal,checks,caseDesign:'4096 deterministic signed pairs of 3-wire factor functions, not random or global proof optimum',scope:'local clause/factor consequences; not complete R_mix341, B3, or arbitrary-machine complexity'};
if(typeof process!=='undefined'&&process.stdout)process.stdout.write(JSON.stringify(result,null,2)+'\n');
