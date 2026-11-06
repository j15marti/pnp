// Standalone LSPV-2/430 compact extensional SAT oracle replay. node <this-file>
import assert from 'node:assert/strict';
const graphs=[
 ['K4',4,[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]]],
 ['cube',8,Array.from({length:8},(_,x)=>[0,1,2].filter(b=>!(x&(1<<b))).map(b=>[x,x^(1<<b)])).flat()],
 ['Petersen',10,[[0,1],[1,2],[2,3],[3,4],[4,0],[5,7],[7,9],[9,6],[6,8],[8,5],[0,5],[1,6],[2,7],[3,8],[4,9]]]
];
let checks=0;function ok(x){assert.ok(x);checks++}
function make(H,edges,p){let m=edges.length,inc=Array.from({length:H},()=>[]);edges.forEach(([a,b],i)=>{inc[a].push(i+1);inc[b].push(i+1)});ok(inc.every(r=>r.length===3));let C=[];for(let v=0;v<H;v++)for(let z=0;z<8;z++){let bits=[z&1,(z>>1)&1,(z>>2)&1];if((bits[0]^bits[1]^bits[2])===(v===0?p:0))continue;C.push(inc[v].map((e,i)=>bits[i]?-e:e))}return {m,C}}
function truth(f,x){return f.C.every(c=>c.some(l=>((((x>>(Math.abs(l)-1))&1)===1)===(l>0))))}
function brute(f,ass={}){for(let x=0;x<(1<<f.m);x++){if(Object.keys(ass).some(k=>((x>>(k-1))&1)!==ass[k]))continue;if(truth(f,x))return true}return false}
function dpll(f,ass={}){let cs=f.C.map(c=>c.slice());let init={...ass};function go(a){for(;;){let changed=false;for(let c of cs){if(c.some(l=>a[Math.abs(l)]!==undefined && ((a[Math.abs(l)]===1)===(l>0))))continue;let u=c.filter(l=>a[Math.abs(l)]===undefined);if(!u.length)return false;if(u.length===1){let k=Math.abs(u[0]),b=u[0]>0?1:0;if(a[k]!==undefined && a[k]!==b)return false;if(a[k]===undefined){a[k]=b;changed=true}}}if(!changed)break}let v=null;for(let c of cs){if(c.some(l=>a[Math.abs(l)]!==undefined && ((a[Math.abs(l)]===1)===(l>0))))continue;for(let l of c)if(a[Math.abs(l)]===undefined){v=Math.abs(l);break}if(v!==null)break}if(v===null)return true;return go({...a,[v]:0})||go({...a,[v]:1})}return go(init)}
function W(f,guest){let Q=[];function ask(a){let s=Object.keys(a).sort().map(k=>k+':'+a[k]).join(','),v=guest(f,a);Q.push(s+':'+Number(v));return v}let r=ask({}),a=ask({1:0}),b=ask({1:1});ok(r===(a||b));let v=a?0:1;ask({1:v,2:0});ask({1:v,2:1});return Q}
for(let [name,H,E] of graphs)for(let p of [0,1]){let f=make(H,E,p);ok(f.C.length===4*H);ok(brute(f)===(p===0));ok(brute(f)===dpll(f));let q1=W(f,brute),q2=W(f,dpll),q3=W(f,(f,a)=>{let b=dpll(f,a);for(let i=0,x=0;i<100;i++)x+=i;return b});ok(JSON.stringify(q1)===JSON.stringify(q2));ok(JSON.stringify(q2)===JSON.stringify(q3));}
console.log(JSON.stringify({checks,families:graphs.length*2,sourceStatus:'COMPUTATIONAL'}));