#!/usr/bin/env node
/* Independently replay full ER2 proof. No import from the producer. */
const fs=require('fs'),assert=require('assert');
let checks=0;function ck(x){assert.ok(x);checks++;}
const edges=[];for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)edges.push([i,j]);
function c(a){if(!Array.isArray(a))throw Error('clause');let s=new Set(a);if([...s].some(x=>!Number.isInteger(x)||x===0||Math.abs(x)>18||s.has(-x)))throw Error('bad clause');return [...s].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);}
function eq(a,b){return JSON.stringify(a)===JSON.stringify(b)}
function expected(ch){let o=[];for(let v=0;v<4;v++){let inc=edges.map((e,j)=>e.includes(v)?j:-1).filter(j=>j>=0);for(let t=0;t<64;t++){let parity=0;for(let k=0;k<3;k++)parity^=((t>>(2*k))&1)&((t>>(2*k+1))&1);if(parity===ch[v])continue;let lits=[];for(let k=0;k<3;k++)for(let b=0;b<2;b++){let z=1+2*inc[k]+b;lits.push(t>>(2*k+b)&1?-z:z);}o.push({v,clause:c(lits)});}}return o;}
function sat(cl,m){return cl.some(z=>z>0?m>>(z-1)&1:!(m>>(-z-1)&1));}
function verify(p){
 ck(eq(p.charges,[1,0,0,0])&&eq(p.edges,edges));
 let src=expected([1,0,0,0]);ck(p.sources.length===120);
 let srcSet=new Set(src.map(x=>x.v+':'+x.clause.join(',')));
 let refs=new Map(),seen=new Set();for(let i=0;i<p.sources.length;i++){
  let s=p.sources[i],cl=c(s.clause),key=s.v+':'+cl.join(',');ck(srcSet.has(key)&&!seen.has(key));seen.add(key);refs.set('S'+i,cl);
 }ck(seen.size===120);
 let ds=new Set();for(let d of p.definitions){let i=Number(d.id.slice(1));ck(Number.isInteger(i)&&i>=0&&i<6&&!ds.has(i));ds.add(i);let a=2*i+1,b=a+1,z=13+i;ck(d.output===z&&d.a===a&&d.b===b);let slots=[c([-z,a]),c([-z,b]),c([z,-a,-b])];ck(d.slots.length===3);for(let j=0;j<3;j++){ck(eq(c(d.slots[j]),slots[j]));refs.set(d.id+'.'+j,slots[j]);}}
 let count=0;for(let t of p.steps){ck(/^R\d+$/.test(t.id)&&!refs.has(t.id));let x=refs.get(t.left),y=refs.get(t.right);ck(!!x&&!!y);ck(x.includes(t.pivot)&&y.includes(-t.pivot));let z=c([...x.filter(v=>v!==t.pivot),...y.filter(v=>v!==-t.pivot)]);ck(eq(c(t.clause),z));refs.set(t.id,z);count++;}
 ck(refs.has(p.final)&&refs.get(p.final).length===0);ck(count===307&&ds.size===6&&p.summary.logical_nodes===313);
 let cover=new Set(),odd=0;for(let m=0;m<4096;m++){let fail=[];for(let i=0;i<src.length;i++)if(!sat(src[i].clause,m))fail.push(i);if(fail.length===0)odd++;if(fail.length===1){let i=fail[0];cover.add(i);for(let lit of src[i].clause){let flip=src[i].clause.map(z=>z===lit?-z:z);ck(sat(flip,m));}}}
 ck(odd===0&&cover.size===120);let ev=[];for(let v=0;v<4;v++){let ch=[1,0,0,0];ch[v]^=1;let ss=expected(ch),models=0;for(let m=0;m<4096;m++)if(ss.every(z=>sat(z.clause,m)))models++;ck(models>0);ev.push(models);}
 return {assertions:checks,source_count:src.length,definitions:ds.size,resolution_steps:count,derived_nodes:count+ds.size,source_deletion_witnesses:cover.size,sign_flip_witnesses:720,odd_models:odd,even_models:ev};
}
let p=JSON.parse(fs.readFileSync(process.argv[2]||'lspv3_358_complete_k4.json'));console.log(JSON.stringify(verify(p),null,2));
