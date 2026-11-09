"use strict";
/* LSPV-3/530: source-authenticated ternary boundary flat-CNF controls.
   Standalone: node experiments/arc/lspv3_530_ternary_flat_boundary.js
   Proof is symbolic in the paired role-owned report; finite checks are controls. */
function assert(p,m){if(!p)throw Error(m||"assertion failed");}
function decode(x,b){let a=Array(b);for(let i=b-1;i>=0;i--){a[i]=x%3;x=Math.floor(x/3);}return a;}
function mod3(x){return ((x%3)+3)%3;}
function valid(t,eps,c){let z=0;for(let i=0;i<t.length;i++)z+=eps[i]*t[i];return mod3(z)===c;}
function code(i,v){return 3*i+v+1;}
function litval(l,t){let n=Math.abs(l)-1;let value=t[Math.floor(n/3)]===(n%3);return l>0?value:!value;}
function sat(cl,t){return cl.some(l=>litval(l,t));}
function canon(a){return [...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);}
function res(A,B,p){assert(A.includes(-p)&&B.includes(p),"oriented Resolution pivot");
 const out=canon([...A.filter(x=>x!==-p),...B.filter(x=>x!==p)]);
 assert(!out.some(x=>out.includes(-x)),"tautological Resolution");
 return out;
}
function main(){
 let cases=0,tupleChecks=0,origRes=0,fullScan=0,tamperChecks=0,rectangles=0,allowedRects=0,maxRect=0;
 const table=[];
 for(let b=2;b<=7;b++){
   for(let mask=0;mask<2**b;mask++){
     let eps=Array.from({length:b},(_,i)=>(mask&(1<<i))?-1:1);
     for(let c=0;c<3;c++){
       let n=3**(b-1),clauses=[];
       let alo=[code(b-1,0),code(b-1,1),code(b-1,2)];
       for(let idx=0;idx<n;idx++){
         let prefix=decode(idx,b-1);
         let target=[0,1,2].find(v=>valid([...prefix,v],eps,c));
         assert(target!==undefined,"unique completion");
         let stem=prefix.map((v,i)=>-code(i,v));
         let C=canon([...stem,code(b-1,target)]);
         clauses.push(C);
         let wrong=[0,1,2].filter(v=>v!==target);
         let d1=canon([...stem,-code(b-1,wrong[0])]);
         let d2=canon([...stem,-code(b-1,wrong[1])]);
         let step=res(d1,alo,code(b-1,wrong[0]));
         let last=res(d2,step,code(b-1,wrong[1]));
         assert(JSON.stringify(last)===JSON.stringify(C),"two original-ALO pivots");
         origRes+=2;
       }
       for(let x=0;x<3**b;x++){
         let t=decode(x,b),idx=Math.floor(x/3);
         let expected=valid(t,eps,c);
         assert(sat(clauses[idx],t)===expected,"selected signed clause");
         if(b<=4){
           let failed=0;for(const cl of clauses)if(!sat(cl,t))failed++;
           assert(failed===(expected?0:1),"all-clause exact CNF");
           fullScan++;
         }
         tupleChecks++;
       }
       let t=decode(0,b-1);
       let target=[0,1,2].find(v=>valid([...t,v],eps,c));
       let corrupted=[...clauses[0]].map(l=>l===code(b-1,target)?-l:l);
       assert(!sat(corrupted,[...t,target]),"corrupted signed clause falsifies valid tuple");
       tamperChecks++;cases++;
     }
   }
   let eps=Array(b).fill(1),c=1;
   table.push({boundary_groups:b,prior_negative_only_clauses:2*3**(b-1),exact_optimal_signed_clauses:3**(b-1),signed_clause_width:b,compact_one_hot_ternary_state_clauses:19*(b-1)+1,compact_aux_indicators:3*(b-1)});
   if(b<=5){
    const choices=[[0],[1],[2],[0,1],[0,2],[1,2],[0,1,2]];
    for(let style=0;style<2;style++)for(let charge=0;charge<3;charge++){
     let signs=Array.from({length:b},(_,i)=>style&&i%2?-1:1);
     for(let z=0;z<7**b;z++){
      let u=z,sets=[];for(let i=0;i<b;i++){sets.push(choices[u%7]);u=Math.floor(u/7);}
      let residues=new Set([0]),volume=1;
      for(let i=0;i<b;i++){
       let next=new Set();for(let r of residues)for(let a of sets[i])next.add(mod3(r+signs[i]*a));
       residues=next;volume*=sets[i].length;
      }
      if(!residues.has(charge)){assert(volume<=2,"false rectangle volume");allowedRects++;maxRect=Math.max(maxRect,volume);}
      rectangles++;
     }
    }
   }
 }
 return {status:"PASS",theorem_scope:"q=3; no extra variables, exactly-one boundary promise",families:cases,tuple_checks:tupleChecks,all_clause_scan_tuples:fullScan,original_source_alo_resolution_nodes_checked:origRes,corrupted_signed_clause_rejections:tamperChecks,rectangles_checked:rectangles,valid_clause_rectangles:allowedRects,max_invalid_rectangle_volume:maxRect,table};
}
if(typeof module!=="undefined"&&typeof require!=="undefined"&&require.main===module) console.log(JSON.stringify(main(),null,2));
