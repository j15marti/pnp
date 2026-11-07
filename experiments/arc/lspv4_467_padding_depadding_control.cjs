'use strict';
// LSPV-4/467 source-preserving padding control. Abstract encoded-bit model, NOT native FLMV.
function main(){
const r={run:'LSPV-4/467',status:'COMPUTATIONAL',checks:0,cases:[],seed:null,failures:0};
const ok=(v,s)=>{r.checks++;if(!v){r.failures++;throw Error(s)}};
function graph(name){let V=name==='K4'?4:name==='cube'?8:10,E=[];
if(name==='K4')for(let a=0;a<V;a++)for(let b=a+1;b<V;b++)E.push([a,b]);
if(name==='cube')for(let a=0;a<V;a++)for(let k=0;k<3;k++){const b=a^(1<<k);if(a<b)E.push([a,b])}
if(name==='Petersen')for(let a=0;a<5;a++){E.push([a,(a+1)%5],[5+a,5+(a+2)%5],[a,5+a])}
return {name,V,E}}
function make(G,odd){const inc=Array.from({length:G.V},()=>[]);G.E.forEach(([a,b],k)=>{inc[a].push(k+1);inc[b].push(k+1)});
ok(inc.every(a=>a.length===3),'cubic');
let F=[];for(let v=0;v<G.V;v++)for(let p=0;p<8;p++){const bits=[p&1,(p>>1)&1,(p>>2)&1];if((bits[0]^bits[1]^bits[2])!==(odd&&v===0?1:0))F.push(inc[v].map((id,j)=>bits[j]?-id:id))}return F}
const valid=F=>Array.isArray(F)&&F.every(c=>Array.isArray(c)&&c.length===3&&c.every(x=>Number.isSafeInteger(x)&&x!==0)&&new Set(c.map(Math.abs)).size===3);
const gamma=n=>2*Math.floor(Math.log2(n))+1;
const cnfbits=F=>F.reduce((a,c)=>a+1+c.reduce((b,x)=>b+2+2*Math.floor(Math.log2(Math.abs(x))),0),0);
function pad(F){const m=F.length,h=m+1,blocks=[F];let id=Math.max(...F.flat().map(Math.abs))+1;for(let b=1;b<h;b++){let d=[];for(let j=0;j<m;j++)d.push([id++,id++,id++]);blocks.push(d)}let sizes=blocks.map(cnfbits),N=gamma(h)+sizes.reduce((a,b)=>a+b+gamma(b),0);return {N,h,blocks,sizes,m}}
function models(F,e){let count=0;for(let mask=0;mask<2**e;mask++)if(F.every(c=>c.some(x=>(((mask>>(Math.abs(x)-1))&1)===1)===(x>0))))count++;return count}
for(const name of ['K4','cube','Petersen'])for(const odd of [false,true]){
const G=graph(name),F=make(G,odd),P=pad(F),n=P.sizes[0],N=P.N,num=models(F,G.E.length);
ok(valid(F),'valid original');ok(num===(odd?0:2**(G.E.length-G.V+1)),'Tseitin labels');
ok(P.blocks.every(valid),'valid padded');ok(P.blocks[0]===F,'unaltered root');
ok(P.blocks.slice(1).every(b=>b.every(c=>c.every(x=>x>0))),'dummy SAT');
let seen=new Set();for(let b of P.blocks){for(let x of new Set(b.flat().map(Math.abs))){ok(!seen.has(x),'cross-block variable');seen.add(x)}}
ok(P.h===F.length+1,'block count');ok(N>n,'expanded input');
r.cases.push({graph:name,charge:odd?'odd UNSAT':'even SAT',vertices:G.V,edgeVariables:G.E.length,originalClauses:F.length,models:num,blocks:P.h,totalClauses:P.m*P.h,sourceBits:n,paddedBits:N,largestBlockBits:Math.max(...P.sizes),interfaceWidth:0,logRatio:Number((Math.log(N)/Math.log(n)).toFixed(6)),rootGuestBits:n,paidAuthenticationProbes:N})}
r.exponentAudit=[1,1.2,1.5,2,4,8].map(t=>{let c=Math.max(1,t/2),d=2*c;ok(d>=t&&d>=2,'depadding bound');return {t,idealPaddedExponent:c,composedOriginalExponent:d}});
for(const F of [[[1,2,0]],[[1,2,1.25]],[[1,2,-1]],[[1,2,NaN]],[[1,2]],[[1,1,3]]])ok(!valid(F),'malformed rejection');
ok(valid([[1,2,3]]),'positive grammar');
r.paddingExponentAsymptotic=2;
r.model='Tree of h=m+1 isolated original strict-3CNF blocks; root is original source and other nodes contain m independent positive strict-3CNF clauses. N=Theta(m^2 log m), n=Theta(m log m) on cubic dense-ID Tseitin, so N=n^(2+o(1)). Paid whole-parent authentication costs Omega(N).';
return r}
if(typeof module!=='undefined'){module.exports={main};if(require.main===module)console.log(JSON.stringify(main(),null,2))}
