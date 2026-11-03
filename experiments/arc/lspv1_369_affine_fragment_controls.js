// LSPV-1 BRAUN-AFFINE-FRAGMENT369: deterministic finite signed controls; Node/V8.
"use strict";
function run(){
let checks=0,malformed=0,corrupted=0;
function ok(c,m){checks++;if(!c)throw Error(m)}
function bad(f){let rejected=false;try{f()}catch(e){rejected=true}ok(rejected,"bad input must reject")}
function lit(l,a){let b=(a>>(Math.abs(l)-1))&1;return l>0?b===1:b===0}
function cl(c,a){return c.some(l=>lit(l,a))}
function source(c,n){if(!Array.isArray(c)||!c.length)throw Error("bad source");let s=new Set();for(let l of c){if(!Number.isInteger(l)||!l||Math.abs(l)>n||s.has(l)||s.has(-l))throw Error("bad literal");s.add(l)}}
function sat(F,a){return F.every(c=>cl(c,a))}
function eq(a,mask,b){let z=0;for(let i=0;i<12;i++)if((mask>>i)&1)z^=(a>>i)&1;return z===b}
function imply(P,Q){for(let a=0;a<8;a++)if(P.every(f=>f(a))&&!Q(a))return false;return true}
const odd=[2,4,1,7],bl=odd.map(b=>a=>a!==b);
const p1=a=>!!(a&1)||eq(a,6,0),p2=a=>!(a&1)||eq(a,6,1),Q=a=>eq(a,7,0);
ok(imply([bl[0],bl[1]],p1),"parity local implication first");
ok(imply([bl[2],bl[3]],p2),"parity local implication second");
ok(imply([p1,p2],Q),"parity local implication third");
ok(!imply([bl[0],bl[1]],a=>!!(a&1)||eq(a,6,1)),"bad parity orientation");corrupted++;
const A=a=>eq(a,3,0),B=a=>eq(a,6,1),W=a=>eq(a,5,1)||eq(a,6,0),O=a=>eq(a,5,1);
ok(imply([A],W),"Res-oplus weakening");
ok(imply([W,B],O),"Res-oplus resolution");
for(let a=0;a<8;a++)ok(Q(a)===((((a&1)^((a>>1)&1)^((a>>2)&1)))===0),"parity truth");
let stats=[];
for(let ell of [1,2]){
let n=2**ell,p=n+1,v=p*ell,F=[],meta=[];
function varLit(i,k,h){let id=i*ell+k+1;return (h>>k)&1?-id:id}
for(let i=0;i<p;i++)for(let j=i+1;j<p;j++)for(let h=0;h<n;h++){
let c=[];for(let t=0;t<ell;t++)c.push(varLit(i,t,h));for(let t=0;t<ell;t++)c.push(varLit(j,t,h));
source(c,v);F.push(c);meta.push({i,j,h})
}
ok(F.length===n*p*(p-1)/2,"BPHP number sources");let models=0;
for(let a=0;a<2**v;a++)if(sat(F,a))models++;
ok(models===0,"BPHP UNSAT");
let deletions=0,flips=0;
for(let k=0;k<F.length;k++){
let {i,j,h}=meta[k],bits=0,other=0;
for(let t=0;t<p;t++){
let hole;
if(t===i||t===j)hole=h;
else{while(other===h)other++;hole=other++}
for(let b=0;b<ell;b++)if((hole>>b)&1)bits|=1<<(t*ell+b)
}
ok(!cl(F[k],bits),"target source false");
for(let z=0;z<F.length;z++)if(z!==k)ok(cl(F[z],bits),"deletion witness");
deletions++;
for(let t=0;t<F[k].length;t++){let changed=F[k].slice();changed[t]=-changed[t];ok(cl(changed,bits),"signed repair");flips++}
}
stats.push({ell,holes:n,pigeons:p,variables:v,clauses:F.length,models,deletion_sat_witnesses:deletions,sign_flip_sat_witnesses:flips})
}
const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
function paritySource(charges){let F=[];for(let v=0;v<4;v++){let e=edges.map((z,i)=>z.includes(v)?i+1:0).filter(Boolean);for(let a=0;a<8;a++)if(((a&1)^((a>>1)&1)^((a>>2)&1))!==charges[v])F.push(e.map((id,j)=>((a>>j)&1)?-id:id))}return F}
let oddF=paritySource([1,0,0,0]),evenF=paritySource([0,0,0,0]),oddCount=0,evenCount=0;
for(let c of [...oddF,...evenF])source(c,6);
for(let a=0;a<64;a++){oddCount+=sat(oddF,a)?1:0;evenCount+=sat(evenF,a)?1:0}
ok(oddCount===0&&evenCount===8,"odd/even K4 labels");
for(let f of [[],[0],[7],[1,-1],[1,1],[2.5],null]){bad(()=>source(f,6));malformed++}
ok(!imply([p1,p2],a=>eq(a,7,1)),"bad output rejected");corrupted++;
return {status:"PASS",checks,malformed_rejected:malformed,corrupted_semantic_steps_rejected:corrupted,semantic_local_steps:3,res_oplus_row_sum_steps:2,bit_php:stats,parity_K4:{odd_models:oddCount,even_models:evenCount},limitations:"Only finite syntax/soundness controls. No asymptotic lower-bound proof or general mixed-calculus minimum computation."}
}
if(typeof module!=="undefined"&&require.main===module)process.stdout.write(JSON.stringify(run(),null,2)+"\n");
