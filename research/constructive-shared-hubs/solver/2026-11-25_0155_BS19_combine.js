const fs=require('node:fs');
function combine(data){
let n=data.source.n,F=data.source.O.map(o=>o.t.map(v=>v+1));
function lit(l,a){return a[Math.abs(l)-1]^(l<0?1:0)}
function ok(C,a){return C.every(c=>c.some(l=>lit(l,a)!==lit(c[0],a)))}
function subsume(C){let order=[...C].sort((a,b)=>a.length-b.length),keep=[],checks=0;for(let c of order){let set=new Set(c);if(keep.some(p=>{checks++;return p.every(l=>set.has(l))||p.every(l=>set.has(-l))}))continue;keep.push(c)}return {keep,checks}}
function direct(C){let nodes=0,scans=0,vars=[...new Set(C.flat().map(l=>Math.abs(l)-1))].sort((a,b)=>a-b);function go(a){if(++nodes>128)return null;while(true){let changed=false;for(let c of C){scans++;let vals=c.filter(l=>a[Math.abs(l)-1]!==-1).map(l=>lit(l,a));if(vals.includes(0)&&vals.includes(1))continue;let u=c.filter(l=>a[Math.abs(l)-1]===-1);if(!u.length)return false;if(u.length===1&&vals.length){let l=u[0];a[Math.abs(l)-1]=1^vals[0]^Number(l<0);changed=true}}if(!changed)break}
let v=vars.find(i=>a[i]===-1);if(v===undefined)return a;for(let b of [0,1]){let t=a.slice();t[v]=b;let q=go(t);if(q!==false)return q}return false}let a=go(Array(n).fill(-1));return {status:a===null?"OPEN":a===false?"UNSAT":"SAT",nodes,scans,a}}
let out=[];for(let entry of data.common.filter(x=>x.K>=4)){for(let sub of [false,true]){let C=entry.residual.C, before=C.length,checks=0;if(sub){let s=subsume(C);C=s.keep;checks=s.checks}let z=direct(C),word=null;if(z.status==="SAT"){let a=z.a.map(v=>v===-1?0:v);for(let e of [...entry.residual.log].reverse()){if(e.w){a[e.v-1]=a[e.w-1]^e.delta;continue}let required=new Set();for(let c of e.bucket){let q=c.map(l=>lit(l,a));if(q.every(t=>t===q[0]))required.add(1^q[0])}if(required.size>1)throw Error("bad lift");a[e.v-1]=[...required][0]??0}if(!ok(F,a))throw Error("source witness");word=a.reduce((s,b,i)=>s+b*2**i,0)}out.push({K:entry.K,sub,before,after:C.length,checks,status:z.status,nodes:z.nodes,scans:z.scans,word})}}
return out}
console.log(JSON.stringify(combine(JSON.parse(fs.readFileSync(process.argv[2],'utf8'))),null,2));
