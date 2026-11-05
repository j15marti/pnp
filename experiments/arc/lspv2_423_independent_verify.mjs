#!/usr/bin/env node
// LSPV-2/423 independently reconstructs source 3-CNFs; standard library only.
import fs from 'node:fs';
import assert from 'node:assert/strict';
const raw=JSON.parse(fs.readFileSync(process.argv[2] || 'results/raw/arc/2026-11-05_1112_LSPV2_COFACTOR_MASS423_raw.json','utf8'));
let checks=0; const eq=(a,b,msg)=>{assert.deepEqual(a,b,msg);checks++};
function graph(name){let n,edges=[];
 if(name==='K4'){n=4;for(let a=0;a<4;a++)for(let b=a+1;b<4;b++)edges.push([a,b]);}
 if(name==='cube'){n=8;for(let a=0;a<8;a++)for(let b=a+1;b<8;b++){let z=a^b;if(z && !(z&(z-1)))edges.push([a,b]);}}
 if(name==='Petersen'){n=10;for(let i=0;i<5;i++){edges.push([i,(i+1)%5],[i,5+i],[5+i,5+(i+2)%5]);}}
 if(name==='Heawood'){n=14;for(let i=0;i<7;i++)for(const p of [i,(i+1)%7,(i+3)%7])edges.push([p,7+i]);}
 const e=edges.map(([a,b])=>a<b?[a,b]:[b,a]);e.sort((A,B)=>A[0]-B[0]||A[1]-B[1]);
 eq(e.length,3*n/2,'cubic edge size');return {n,e};}
function cnf(n,edges,odd){const rows=[];for(let v=0;v<n;v++){
 const ids=[];for(let k=0;k<edges.length;k++)if(edges[k].includes(v))ids.push(k+1);
 eq(ids.length,3,'degree');
 for(let bits=0;bits<8;bits++){
 const p=((bits&1)!==0)+((bits&2)!==0)+((bits&4)!==0);
 if((p%2)!==(odd&&v===0?1:0))rows.push(ids.map((id,j)=> (bits&(1<<j))?-id:id));
 }}return rows;
}
function count(rows,a){let count=0,overlap=0,tot=0,empty=0;
 for(const row of rows){let trueN=0,assignedN=0;for(const literal of row){const v=String(Math.abs(literal));if(Object.prototype.hasOwnProperty.call(a,v)){assignedN++;if((literal>0?1:0)===a[v])trueN++;}}
 tot+=trueN;overlap+=Math.max(0,trueN-1);if(trueN===0){count++;if(assignedN===row.length)empty++;}}
 return {count,overlap,tot,empty};}
let fixtures=0;for(const r of raw.graph_results){const {n,e}=graph(r.graph);eq(r.vertices,n);eq(r.edges,e.length);
 for(const kind of ['even','odd']){const rows=cnf(n,e,kind==='odd');eq(rows.length,4*n);
 for(let i=1;i<=e.length;i++){eq(rows.filter(row=>row.includes(i)).length,4);eq(rows.filter(row=>row.includes(-i)).length,4);}
 for(const f of r.fixtures.filter(x=>x.charge===kind)){const actual=count(rows,f.assign);eq(actual.count,f.residual,'cofactor count');eq(actual.overlap,f.overlap,'true overlap');eq(actual.tot,f.true_occurrences);eq(actual.empty,f.empty_clauses);eq(actual.count,4*n-4*Object.keys(f.assign).length+actual.overlap); fixtures++;}
 const ma={};for(const i of r['matching_'+kind].edge_ids)ma[i]=i%2;
 const actual=count(rows,ma);eq(actual.overlap,0,'matching overlap');eq(actual.count,r['matching_'+kind].residual);
 for(let s=0;s<(n===4?1<<e.length:64);s++){const a={};for(let i=1;i<=e.length;i++)a[i]=(s>>(i-1))&1;
 if(kind==='odd')eq(count(rows,a).empty>0,true,'odd-charge must be UNSAT');
 }
 }
}
const broken=structuredClone(raw.graph_results[0].fixtures[0]);broken.residual+=1;
const {n,e}=graph('K4');assert.notEqual(count(cnf(n,e,broken.charge==='odd'),broken.assign).count,broken.residual);checks++;
function validClause(row,n){return Array.isArray(row)&&row.length===3&&new Set(row.map(Math.abs)).size===3&&row.every(x=>Number.isInteger(x)&&x!==0&&Math.abs(x)<=n);}
eq(validClause([1,-1,2],6),false);eq(validClause([1,1,2],6),false);eq(validClause([1,2,7],6),false);eq(validClause([1,2,3],6),true);
console.log(JSON.stringify({verification:'PASS',checks,source_fixtures:fixtures,source_count:raw.checks,corruption_control:'rejected',malformed_controls:3}));
