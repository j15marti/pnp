'use strict';
// LSPV-1/472 standalone finite verification. NOT historical R_mix341.
function check(b,s){if(!b)throw Error(s||'assertion');checks++}
let checks=0;
function pc(x){let k=0;while(x){x&=x-1;k++}return k}
function clauses(n){let C=[];for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)for(let k=j+1;k<n;k++)for(let sign=0;sign<8;sign++){let lits=[i,j,k].map((v,t)=>sign>>t&1?-(v+1):v+1),bad=0;for(let a=0;a<2**n;a++)if(lits.every(v=>(a>>(Math.abs(v)-1)&1)===(v<0?1:0)))bad=(bad|(1<<a))>>>0;C.push({lits,bad,support:i+','+j+','+k})}return C}
function affine(n){let A=new Map();for(let m=1;m<2**n;m++)for(let t=0;t<2;t++){let b=0;for(let a=0;a<2**n;a++)if((pc(a&m)&1)===t)b=(b|(1<<a))>>>0;A.set(b,m)}return A}
function audit(n){let C=clauses(n),A=affine(n),tr=0,qu=0,aff=0,nonpacket=0,distinct=0,weights={};for(let i=0;i<C.length;i++)for(let j=i+1;j<C.length;j++)for(let k=j+1;k<C.length;k++){tr++;let base=(C[i].bad|C[j].bad|C[k].bad)>>>0;check(!A.has(base),'3-clause affine');for(let l=k+1;l<C.length;l++){qu++;let mask=A.get((base|C[l].bad)>>>0);if(mask===undefined)continue;aff++;let d=new Set([C[i],C[j],C[k],C[l]].map(z=>z.support)).size;if(d>1)nonpacket++;if(d===4)distinct++;check(d<4,'four distinct supports');let w=pc(mask);weights[w]=(weights[w]||0)+1}}return {n,triples:tr,quartets:qu,affine_quartets:aff,non_packet_affine:nonpacket,all_distinct_supports:distinct,by_row_weight:weights}}
let a4=audit(4),a5=audit(5);
check(a4.affine_quartets===128&&a5.affine_quartets===500,'affine counts');
check(a4.non_packet_affine===72&&a5.non_packet_affine===360,'nonpacket counts');
let xor=[[1,2,3],[1,2,-3],[-1,-2,4],[-1,-2,-4]];
for(let a=0;a<16;a++){let v=xor.every(C=>C.some(l=>(a>>(Math.abs(l)-1)&1)===(l>0?1:0)));check(v===(((a&1)^((a>>1)&1))===1),'non-packet XOR')}
let edge=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
function tseitin(charges){let C=[];for(let v=0;v<4;v++){let inds=edge.map((e,i)=>e.includes(v)?i:-1).filter(i=>i>=0);for(let p=0;p<8;p++)if((pc(p)&1)!==charges[v])C.push(inds.map((e,t)=>(p>>t&1)?-(e+1):(e+1)))}return C}
function count(C){let z=0;for(let a=0;a<64;a++)if(C.every(c=>c.some(l=>(a>>(Math.abs(l)-1)&1)===(l>0?1:0))))z++;return z}
let odd=tseitin([1,0,0,0]),even=tseitin([0,0,0,0]);check(odd.length===16&&count(odd)===0,'odd Tseitin');check(count(even)===8,'even Tseitin');for(let i=0;i<16;i++)check(count(odd.filter((_,j)=>i!==j))>0,'source deletion');
let summary={run:'LSPV1/472',scope:'original-source-only, proper signed 3-CNF',n4:a4,n5:a5,non_packet_control:'(x|y|a)&(x|y|-a)&(-x|-y|b)&(-x|-y|-b) iff x XOR y=1',K4:{odd_UNSAT:true,even_models:8,deleted_clause_SAT:16},checks,historical_checker:false,P_vs_NP:'OPEN'};
console.log(JSON.stringify(summary,null,2));
