function quotientAudit(){
const assert=(b,m)=>{if(!b)throw Error(m)};
function graph(n){let seed=12345+n;const rand=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed};const E=Array.from({length:n},(_,i)=>new Set([i]));for(let k=0;k<3;k++){const p=Array.from({length:n},(_,i)=>i);for(let i=n-1;i>0;i--){const j=rand()%(i+1);[p[i],p[j]]=[p[j],p[i]]}for(let i=0;i<n;i++)E[i].add(p[i])}return E.map(s=>[...s].sort((a,b)=>a-b))}
function make(G,mode,guards){let rows=[],edges=[],index=[],free=0;const id=(i,j)=>index[i][G[i].indexOf(j)];for(let i=0;i<G.length;i++){index[i]=G[i].map(j=>{edges.push([i,j]);return edges.length-1})}
const forms=edges.map(()=>null);for(const I of index){for(const q of I.slice(1))forms[q]=[0,[free++]];forms[I[0]]=[1,I.slice(1).map(q=>forms[q][1][0])];rows.push(I.map(q=>[q,1]));for(let a=0;a<I.length;a++)for(let b=a+1;b<I.length;b++)rows.push([[I[a],0],[I[b],0]])}
for(let j=0;j<G.length;j++){const I=G.flatMap((r,i)=>r.includes(j)?[id(i,j)]:[]);for(let a=0;a<I.length;a++)for(let b=a+1;b<I.length;b++)rows.push([[I[a],0],[I[b],0]]);if(!mode&&j===G.length-1)for(const q of I)rows.push([[q,0]])}
for(const [i,j,b] of guards)rows.push([[id(i,j),b]]);
const Q=rows.map(r=>r.map(([q,b])=>[forms[q][0]^b,forms[q][1]]));return {edges,index,forms,rows,Q,free}}
const parity=(I,z)=>I.reduce((a,i)=>a^z[i],0);
const valid=(r,z)=>r.some(([b,I])=>parity(I,z)===b);
function enumerate(F){let sat=0,checks=0;for(let mask=0;mask<2**F.free;mask++){const z=Array.from({length:F.free},(_,i)=>(mask>>i)&1),x=F.forms.map(([b,I])=>b^parity(I,z));const raw=F.rows.every(r=>r.some(([i,b])=>x[i]===b)),q=F.Q.every(r=>valid(r,z));assert(raw===q,"quotient exact");if(q){assert(F.index.every(I=>I.reduce((a,i)=>a+x[i],0)===1),"functionality");sat++}checks++}return {sat,checks}}
function brute(G,mode,guards){let count=0;const M=[],used=new Set();function go(i){if(i===G.length){count++;return}for(const j of G[i]){if(!mode&&j===G.length-1||used.has(j)||guards.some(([u,v,b])=>u===i&&+(v===j)!==b))continue;M[i]=j;used.add(j);go(i+1);used.delete(j)}}go(0);return count}
const out={jobs:[],checks:0,localChecks:0,parameterChecks:0};
for(const h of [4,6])for(const mode of [0,1]){const G=graph(h),gs=[[],[[0,0,0]],[[0,0,1]],[[0,0,1],[1,1,0]]];for(const guards of gs){const F=make(G,mode,guards),r=enumerate(F),b=brute(G,mode,guards);assert(r.sat===b,"independent count");out.checks+=r.checks;out.jobs.push({h,mode,guards,e:F.edges.length,free:F.free,...r,brute:b})}}
for(let h of [8,16,32,64,128])for(const mode of [0,1]){const G=graph(h),F=make(G,mode,[]);for(let j=0;j<F.rows.length;j++){const r=F.rows[j],q=F.Q[j],I=[...new Set(q.flatMap(p=>p[1]))];for(let mask=0;mask<2**I.length;mask++){const z=Array(F.free).fill(0);I.forEach((i,k)=>z[i]=mask>>k&1);assert(valid(q,z)===r.some(([i,b])=>(F.forms[i][0]^parity(F.forms[i][1],z))===b),"local equality");out.localChecks++}}}
for(let h=4;h<=256;h++)for(let a=1;a<=h;a++)for(let k=1;k<=h;k++){const B=k*(Math.max(2*a+4,4*a+1)+1),r=a*(k+1)+1;if(B<h){assert(r<=h,"rank tariff");out.parameterChecks++}}
return out
}
console.log(JSON.stringify(quotientAudit(),null,2));
