// LSPV-2/432. Self-contained exact finite 3CNF/footprint-sharing control.
// Executed by: node lspv2_432_compact_replay.mjs
const assert=(b,m)=>{if(!b)throw Error(m);checks++};let checks=0;
const bits=(n,k)=>n.toString(2).padStart(k,'0');
function clauses(h,edges,odd){let inc=Array.from({length:h},()=>[]);edges.forEach(([u,v],j)=>{inc[u].push(j+1);inc[v].push(j+1)});let out=[];
  for(let v=0;v<h;v++)for(let a=0;a<8;a++){let z=[a&1,(a>>1)&1,(a>>2)&1];if((z[0]^z[1]^z[2])!==(odd&&v===0?1:0))out.push(inc[v].map((x,k)=>z[k]?-x:x))}return out}
function enc(n,F){return '11001010'+bits(n,8)+bits(F.length,8)+F.map(c=>c.map(x=>(x<0?'1':'0')+bits(Math.abs(x),4)).join('')+'0').join('')}
function run(s){let seen=new Set();function read(p){seen.add(p);return s[p]};function u(p,k){return parseInt(Array.from({length:k},(_,j)=>read(p+j)).join(''),2)}let label='MALFORMED';
  if(s.length>=24&&u(0,8)===202){let n=u(8,8),m=u(16,8);if(n>=1&&n<=12&&s.length===24+16*m){let F=[],valid=true;
    for(let j=0;j<m;j++){let c=[];for(let k=0;k<3;k++){let p=24+16*j+5*k,sign=read(p),v=u(p+1,4);if(v<1||v>n){valid=false;break}c.push(sign==='1'?-v:v)}if(!valid||new Set(c.map(Math.abs)).size!==3){valid=false;break}F.push(c)}
    if(valid){label='UNSAT';for(let a=0;a<2**n;a++)if(F.every(c=>c.some(z=>Boolean((a>>(Math.abs(z)-1))&1)===(z>0)))){label='SAT';break}}}}
  return {label,seen:[...seen].sort((a,b)=>a-b)}}
function flip(s,k){return s.slice(0,k)+(s[k]==='0'?'1':'0')+s.slice(k+1)}
const families=[['K4',4,[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]]],['cube',8,Array.from({length:8},(_,v)=>[v^1,v^2,v^4].filter(w=>v<w).map(w=>[v,w])).flat()]];
let cases=0,reused=0;
for(const [name,h,edges] of families){let base=enc(edges.length,clauses(h,edges,true)),sat=enc(edges.length,clauses(h,edges,false)),m=4*h;
  assert(run(base).label==='UNSAT',name+' odd');assert(run(sat).label==='SAT',name+' even');let anchor=base,first=run(base);for(let j=0;j<m;j++){
    let pad=flip(base,24+16*j+15);assert(first.seen.every(p=>pad[p]===anchor[p]),'padding footprint');assert(run(pad).label===first.label,'cached UNSAT');cases++;reused++}
  for(let j=0;j<m;j++)for(let k=0;k<3;k++){let x=flip(base,24+16*j+5*k);assert(run(x).label==='SAT','critical source sign');assert(first.seen.some(p=>x[p]!==base[p]),'opposite label must differ in read footprint');cases++}
  for(let j=0;j<4;j++){let malformed=[base.slice(0,1)+'0'+base.slice(2),base.slice(0,-1),base+'0',base.slice(0,24)+'11111'+base.slice(29)][j];assert(run(malformed).label==='MALFORMED','malformed code');cases++}}
console.log(JSON.stringify({checks,cases,reused,model:'finite n<=12 exact checker; no FLMV machine claim'}));
