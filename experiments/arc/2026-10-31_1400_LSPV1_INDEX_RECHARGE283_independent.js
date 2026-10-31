// Independent ARC-INDEX-RECHARGE283 controls, standard Node.js.
"use strict";
function assert(x,msg){if(!x)throw Error(msg);}
function countBits(x){let n=0;for(;x;x>>=1)n+=x&1;return n;}
function verify(raw,fixture){
 const d=typeof raw==="string"?JSON.parse(raw):raw;
 let tests=0;
 const check=(x,m)=>{tests++;assert(x,m);};
 check(d.claim==="ARC-INDEX-RECHARGE283","wrong claim");
 let visited=0;
 // A second enumeration uses direct bit-vector snapshots and a separate ledger.
 for(const spec of d.machine.checked_enumerations){
   let count=0,nonempty=0;
   function go(w,i,k,up,er,delta){
     check(er<=up,"prior index writes too small");
     check(delta<=2*k,"full-run amortization failed");
     if(k===spec.depth){count++;return;}
     for(let j=0;j<spec.width;j++){
       for(let v=0;v<=1;v++){
         const old=i&(1<<j),newIndex=v?(i|(1<<j)):(i&~(1<<j));
         const dx=countBits(i^newIndex);
         go(w,newIndex,k+1,up+(v&&!old?1:0),er,delta+dx);
       }
     }
     if(i)nonempty++;
     go(w,0,k+1,up,er+countBits(i),delta+countBits(i));
     go(w^1,i,k+1,up,er,delta+1);
     go(w,i,k+1,up,er,delta);
   }
   go(0,0,0,0,0,0);
   check(count===spec.leaves,"enum leaf mismatch");
   check(nonempty===spec.nonempty_index_resets,"reset event count mismatch");
   visited+=count;
 }
 const ex=d.machine.reset16;
 check(ex.cumulative_full_XOR===32,"reset total");
 check(ex.total_preparation_plus_reset_steps===17,"charged reset steps");
 check(ex.index_bulk_erased_bits===16,"erased index bits");
 check(ex.ordinary_0_to_1_writes===16,"initial recharge");
 check(ex.cumulative_full_XOR>ex.total_preparation_plus_reset_steps,"naive same-cell per-step bound should fail");
 const Y=[[1,2,3],[1,4,5],[2,4,6],[3,5,6],[-1,-2,-4],[-1,-3,-6],[-2,-3,-5],[-4,-5,-6]];
 const evals=(F,a)=>F.map(c=>c.reduce((s,x)=>s+Number(a[Math.abs(x)]===(x>0?1:0)),0));
 const signCounts=(F)=>{const z=new Map();for(const c of F)for(const x of c)z.set(x,(z.get(x)||0)+1);return z;};
 function checkSource(F,record){
   const n=F.reduce((u,c)=>Math.max(u,...c.map(x=>Math.abs(x))),0),m=F.length;
   check(record.n===n&&record.m===m,"source counts");
   const occ=signCounts(F);
   for(let i=1;i<=n;i++){check(occ.get(i)===2,"positive quota");check(occ.get(-i)===2,"negative quota");}
   check(record.local_extremes.length===m,"all original clause S/U targets");
   const a=new Array(n+1).fill(0);
   for(let j=0;j<m;j++){
     const orig=F[j],e=record.local_extremes[j];
     check(orig.join(",")===e.source_literals.join(","),"source clause provenance");
     for(let t=0;t<3;t++){
       check(e.S_all_literals_true[t][0]===Math.abs(orig[t]),"S source identifier");
       check(e.U_all_literals_false[t][1]===1-e.S_all_literals_true[t][1],"inverse polarity");
     }
   }
   let masks="";
   for(let j=0;j<m;j++)for(let k=j+1;k<m;k++){
      let s=false,o=false;
      const aj=new Map(F[j].map(x=>[Math.abs(x),Math.sign(x)]));
      for(const l of F[k])if(aj.has(Math.abs(l))){
         if(aj.get(Math.abs(l))===Math.sign(l))s=true;else o=true;
      }
      masks+=((o?0:9)|(s?0:6)).toString(16);
   }
   check(record.extreme_pair_compatibility.masks_hex===masks,"independent SS/SU/US/UU pair matrix");
   let before=evals(F,a),bin=0,gray=0,recordChanges=0;
   for(let i=1;i<=n;i++){
      a[i]=1;let after=evals(F,a);
      for(let j=0;j<m;j++)if(before[j]!==after[j]){
       check(Math.abs(before[j]-after[j])===1,"original clause count nonunit");
       bin+=countBits(before[j]^after[j]);
       const gg=x=>x^(x>>1);
       gray+=countBits(gg(before[j])^gg(after[j]));
       recordChanges++;
      }
      before=after;
   }
   check(record.logical_sweep.logical_status_binary_XOR===bin,"binary XOR");
   check(record.logical_sweep.logical_status_gray_XOR===gray,"Gray XOR");
   check(record.logical_sweep.record_changes===recordChanges,"record count");
   check(bin===4*m&&gray===3*m&&recordChanges===4*n,"strict22 XOR quota");
 }
 checkSource(Y,d.sources.Y6);
 let models=0;
 for(let a=0;a<64;a++){const vals=new Array(7).fill(0);for(let i=1;i<=6;i++)vals[i]=(a>>(i-1))&1;
    if(evals(Y,vals).every(t=>t>0))models++;
 }
 check(models===20&&d.sources.Y6.independent_exhaustive.model_count===20,"Y6 independent exhaustive");
 if(fixture){
   const U=JSON.parse(fixture.slice(fixture.indexOf("[[")));
   const V=U.map(c=>c.slice());
   [V[2][2],V[44][2]]=[V[44][2],V[2][2]];
   checkSource(U,d.sources.U198);checkSource(V,d.sources.V198);
   const witness="001110010011110001010001110100111110011011000101000101001010100001011010"+
       "101011000100000111001010110101001110001001101000110001100010100101101110"+
       "010101011001001100000110111001001101001101101001010101";
   check(witness.length===198,"witness length");
   const a=[0,...witness.split("").map(Number)];
   const h=[0,0,0,0],uh=[0,0,0,0];
   for(const t of evals(V,a))h[t]++;
   for(const t of evals(U,a))uh[t]++;
   check(h.join(",")==="0,158,80,26","V198 genuine checked witness");
   check(uh[0]>=1,"U198 is not satisfied by V witness (NOT an UNSAT proof)");
 }
 return {verification_status:"PASS",independent_assertions:tests,enumerated_machine_leaves:visited,
   V198_witness_replayed:!!fixture,U198_UNSAT_certificate:"CITED_PREVIOUS_INDEPENDENT_MODULE_PROOF_NOT_REDERIVED",
   theorem_scope:"INDEX_TAPE_BIT_VECTOR_WITH_ATOMIC_BULK_ERASE",P_vs_NP:"OPEN"};
}
if(typeof module!=="undefined"&&module.exports)module.exports={verify};
if(typeof require!=="undefined"&&require.main===module){
 const fs=require("fs"),path=require("path");
 const root=path.resolve(__dirname,"../..");
 const raw=fs.readFileSync(path.resolve(root,"results/raw/arc/2026-10-31_1400_LSPV1_INDEX_RECHARGE283.json"),"utf8");
 const fp=path.resolve(root,"research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt");
 console.log(JSON.stringify(verify(raw,fs.readFileSync(fp,"utf8")),null,2));
}
// END_OF_INDEPENDENT_VERIFIER::ARC-INDEX-RECHARGE283
