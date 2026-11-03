"use strict";
// LSPV-4 SOURCE-REREAD-INDEX-ACCOUNT357. Node >=18, stdlib only.
// The raw input/proof is read-only in the declared abstract model.
// This executable measures bit-index writes and finite SAT controls.
// It does NOT pretend Node's heap is native TM workspace.
const assert=require("node:assert/strict"),fs=require("node:fs");
function pop(n){let z=0;while(n){z++;n&=n-1;}return z}
function indexWrites(seq){let prev=0,s=0;for(const i of seq){s+=pop(prev^i);prev=i}return s}
function cnf(x){let f=x.map((b,i)=>[b?i+1:-(i+1)]);f.push(x.map((b,i)=>b?-(i+1):i+1));return f}
function sat(n,F){for(let mask=0;mask<(1<<n);mask++){let yes=true;for(const C of F){let hit=false;for(const l of C){if((mask>>(Math.abs(l)-1)&1)===(l>0?1:0)){hit=true;break}}if(!hit){yes=false;break}}if(yes)return mask}return null}
function strict(X,i,b){if(typeof X!=="string"||!/^[01]+$/.test(X))throw Error("malformed source");if(!Number.isInteger(i)||i<0||i>=X.length||(b!==0&&b!==1))throw Error("malformed query");return Number(X[i])===b}
function k4(ch){const edges=[];for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)edges.push([i,j]);let F=[];for(let v=0;v<4;v++){const es=edges.map((e,i)=>e.includes(v)?i+1:null).filter(x=>x!==null);for(let a=0;a<8;a++){const bits=[0,1,2].map(k=>(a>>k)&1);if((bits[0]^bits[1]^bits[2])!==ch[v])F.push(es.map((e,k)=>bits[k]?-e:e))}}return F}
// Deliberately rescans the read-only sign field source for every named
// original-clause occurrence (j,t), including restart address writes.
// The physical source bytes live OUTSIDE the modeled writable work space.
function rereadClaims(X,claims){
 if(typeof X!=="string"||!/^[01]+$/.test(X))throw Error("bad source");
 let a=0,probes=0,indexChanges=0,valid=true,L=X.length;
 function read(i){indexChanges+=pop(a^i);a=i;probes++;return Number(X[i])}
 for(const [j,t,b] of claims){
   if(!Number.isInteger(j)||!Number.isInteger(t)||(b!==0&&b!==1)||j<0||j>L||t<0||t>=L||(j<L&&t!==0))throw Error("bad occurrence");
   let observed=-1;const seek=(j===L?t:j);
   for(let i=0;i<L;i++){const v=read(i);if(i===seek)observed=j===L?1-v:v}
   if(observed!==b)valid=false;
 }
 return {valid,probes,indexChanges,registerBits:Math.max(1,Math.ceil(Math.log2(L)))};
}
function run(){
 let checks=0,unsat=0,deletion=0,flip=0,rejected=0,authentication=0,table=[],replayRuns=0,replaySourceProbes=0,replayIndexWrites=0;
 for(let L=1;L<=9;L++)for(let v=0;v<(1<<L);v++){
    const x=Array.from({length:L},(_,i)=>((v>>i)&1)),F=cnf(x);
    assert.equal(sat(L,F),null);checks++;unsat++;
    const X=x.join(""),claims=F.flatMap((C,j)=>C.map((l,t)=>[j,t,l>0?1:0]));
    const good=rereadClaims(X,claims);
    assert.equal(good.valid,true);assert.equal(good.probes,2*L*L);
    const forged=claims.map(z=>z.slice());forged[forged.length-1][2]^=1;
    assert.equal(rereadClaims(X,forged).valid,false);
    checks+=3;replayRuns+=2;replaySourceProbes+=good.probes*2;replayIndexWrites+=good.indexChanges*2;
    for(let j=0;j<F.length;j++){
       assert.notEqual(sat(L,F.filter((_,i)=>i!==j)),null);checks++;deletion++;
       for(let t=0;t<F[j].length;t++){const G=F.map(c=>c.slice());G[j][t]=-G[j][t];assert.notEqual(sat(L,G),null);checks++;flip++}
    }
 }
 const malformed=[null,undefined,"",{},-1,2**60,[],[2],[-1],[0],["bad"]];
 for(const i of malformed){assert.throws(()=>strict("0101",i,1));rejected++}
 const badSources=["","0102","2","0 1","01a","00\\n1",null,42,[],{},undefined];
 for(const x of badSources){assert.throws(()=>strict(x,0,1));rejected++}
 for(let L=1;L<=32;L++){const s="01".repeat(32).slice(0,L);for(let i=0;i<L;i++){assert.equal(strict(s,i,Number(s[i])),true);assert.equal(strict(s,i,1-Number(s[i])),false);checks+=2;authentication+=2}}
 for(let w=2;w<=12;w++){
    const N=2**w,ids=Array.from({length:N},(_,i)=>i);
    const row={w,N,binary_ascending:indexWrites(ids),gray_permutation:indexWrites(ids.map(i=>i^(i>>1))),alternating:indexWrites(ids.map((_,i)=>i%2?N-1:0)),repeated_zero:indexWrites(ids.map(_=>0))};
    assert.equal(row.binary_ascending,2*N-w-2);
    assert.equal(row.gray_permutation,N-1);
    assert.equal(row.alternating,w*(N-1));
    assert.equal(row.repeated_zero,0);checks+=4;table.push(row);
 }
 const odd=sat(6,k4([1,0,0,0])),even=[];for(let i=0;i<64;i++){const F=k4([0,0,0,0]);if(F.every(C=>C.some(l=>((i>>(Math.abs(l)-1)&1)===(l>0?1:0)))))even.push(i)}
 assert.equal(odd,null);assert.equal(even.length,8);checks+=2;
 return {status:"PASS", checks, unsat_sources:unsat,deletion_sat_witnesses:deletion,single_sign_flip_sat_witnesses:flip,malformed_queries_rejected:rejected,source_bit_authentication_controls:authentication,replay_test_runs:replayRuns,replay_source_bit_reads:replaySourceProbes,replay_index_bit_writes:replayIndexWrites,odd_K4_models:0,even_K4_models:8,index_sequences:table,
       model:"fixed binary-address register, one bit change per index-tape cell write; bit counts are not native machine time",
       scope:"Rmix341 unchanged; source authentication only; B1/B2/B3 OPEN; P versus NP OPEN"};
}
const result=run();if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(result,null,2)+"\n");console.log(JSON.stringify({status:result.status,checks:result.checks,UNSAT:result.unsat_sources,deletion:result.deletion_sat_witnesses,signflip:result.single_sign_flip_sat_witnesses,malformed:result.malformed_queries_rejected,oddK4:result.odd_K4_models,evenK4:result.even_K4_models},null,2));
