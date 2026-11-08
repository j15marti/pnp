'use strict';
// LSPV-1/505. Independently implemented finite checker for the one-layer
// common-isotropic affine-guard theorem. Distinct model, NOT historical R_mix341.
// Run: node experiments/arc/lspv1_505_quotient_rank_guards.cjs
let assertions=0, rejected=0;
function ok(v,msg){assertions++;if(!v)throw Error(msg||'test failed')}
function bit(a,b){let v=a&b,p=0;while(v){v&=v-1;p^=1}return p}
function aff(a,x){return bit(a[0],x)^a[1]}
function val(g,x){return (g[2]>>((aff(g[0],x)<<1)+aff(g[1],x)))&1}
function polar(g,u,v){let a=g[0][0],b=g[1][0],p=0;
 for(let k=0;k<4;k++)p^=(g[2]>>k)&1;
 return p&((bit(a,u)&bit(b,v))^(bit(a,v)&bit(b,u)))}
function subspaces(n){let res=[[0]],seen=new Set(['0']);
 for(let z=0;z<res.length;z++){let U=res[z],set=new Set(U);
 for(let x=1;x<(1<<n);x++){if(set.has(x))continue;
 let V=U.concat(U.map(y=>y^x)).sort((a,b)=>a-b),key=V.join(',');
 if(!seen.has(key)){seen.add(key);res.push(V)}}}
 return res}
function iso(U,G){for(let g of G)for(let x of U)for(let y of U)
 if(polar(g,x,y))return false;return true}
function brute(U,G,n){for(let g of G)for(let x=0;x<(1<<n);x++)
 for(let u of U)for(let v of U)
 if(val(g,x)^val(g,x^u)^val(g,x^v)^val(g,x^u^v))return false;
 return true}
function rank(rows,n){let basis=Array(n).fill(0),r=0;
 for(let v of rows)while(v){let p=31-Math.clz32(v);
 if(basis[p])v^=basis[p];else{basis[p]=v;r++;break}}
 return r}
function anchors(G,n){let H=G.filter(g=>[0,1,2,3].reduce((p,j)=>p^((g[2]>>j)&1),0));
 let best=n;for(let m=0;m<(1<<H.length);m++)
 best=Math.min(best,rank(H.map((g,j)=>g[(m>>j)&1][0]),n));return best}
function rho(G,n,spaces){let best=n;for(let U of spaces)
 if(iso(U,G))best=Math.min(best,n-Math.log2(U.length));return best}
function malformed(n,G){if(!Number.isInteger(n)||n<1||n>9)throw Error('n');
 for(let [a,b,tt] of G){if(!Number.isInteger(tt)||tt<0||tt>15)throw Error('tt');
 for(let [mask,c] of [a,b])
 if(mask<0||mask>=(1<<n)||(c!==0&&c!==1))throw Error('mask')}}
const start=Date.now(),counts={},ex={};
for(let n=1;n<=5;n++)counts[n]=subspaces(n).length;
ok(JSON.stringify(counts)===JSON.stringify({1:2,2:5,3:16,4:67,5:374}),'subspaces');
for(let g=2;g<=4;g++){let n=g+1,t=1<<g,G=Array.from({length:g},
 (_,i)=>[[1<<i,0],[(1<<i)^t,0],8]);
 let x=rho(G,n,subspaces(n)),y=anchors(G,n);
 ok(x===1&&y===g,'twisted rank gap');ex['twisted_'+g]={rho:x,anchor_rank:y}}
for(let g=1;g<=2;g++){let n=g*2,G=Array.from({length:g},
 (_,i)=>[[1<<(2*i),0],[1<<(2*i+1),0],8]);
 ok(rho(G,n,subspaces(n))===g,'independent gates')}
let seed=5052026;function rnd(n){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;
 return(seed>>>0)%n}
let cases=0,subspaceComparisons=0;
for(let n=2;n<=4;n++){let spaces=subspaces(n);
 for(let iter=0;iter<20;iter++){let G=Array.from({length:1+rnd(5)},
 ()=>[[rnd(1<<n),rnd(2)],[rnd(1<<n),rnd(2)],rnd(16)]);
 ok(rho(G,n,spaces)<=anchors(G,n),'guard <= anchor rank');
 for(let U of spaces){ok(iso(U,G)===brute(U,G,n),'isotropy iff affine');
 subspaceComparisons++}cases++}}
for(let bad of [()=>malformed(0,[]),()=>malformed(3,[[[9,0],[1,0],8]]),
 ()=>malformed(3,[[[1,0],[1,0],16]])]){
 try{bad()}catch(e){rejected++;continue}throw Error('bad grammar accepted')}
ok(rejected===3,'hostile controls');
let twisted=[[[1,0],[5,0],8],[[2,0],[6,0],8]];
ok(!iso([0,1,4,5],twisted),'missing shared guard');
let clauses=Array.from({length:8},(_,a)=>Array.from({length:3},
 (_,i)=>((a>>i)&1)?-(i+1):i+1));
let sat=(c,x)=>c.some(l=>(((x>>(Math.abs(l)-1))&1)===1)===(l>0));
ok(!Array.from({length:8},(_,x)=>x).some(x=>clauses.every(c=>sat(c,x))),
 'original proper 3CNF UNSAT');
for(let j=0;j<8;j++){let witness=[];
 for(let x=0;x<8;x++)if(clauses.every((c,k)=>k===j||sat(c,x)))witness.push(x);
 ok(witness.length===1&&witness[0]===j,'source clause deletion')}
console.log(JSON.stringify({id:'LSPV1-505',status:'COMPUTATIONAL in distinct gate model',
 assertions,hostileRejected:rejected,subspace_counts:counts,examples:ex,
 random_cases:cases,full_subspace_equivalences:subspaceComparisons,
 seed_initial:5052026,elapsed_ms:Date.now()-start},null,2));
