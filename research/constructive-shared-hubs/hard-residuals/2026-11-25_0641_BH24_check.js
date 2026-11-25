const inputs = [{"n":7,"root":[{"t":[0,1,2],"bad":[0,7]},{"t":[0,3,4],"bad":[0,7]},{"t":[0,5,6],"bad":[0,7]},{"t":[1,3,5],"bad":[0,7]},{"t":[1,4,6],"bad":[0,7]},{"t":[2,3,6],"bad":[0,7]},{"t":[2,4,5],"bad":[0,7]}],"sat":[{"t":[0,1,2],"bad":[2,5]},{"t":[0,3,4],"bad":[0,7]},{"t":[0,5,6],"bad":[0,7]},{"t":[1,3,5],"bad":[0,7]},{"t":[1,4,6],"bad":[0,7]},{"t":[2,3,6],"bad":[0,7]},{"t":[2,4,5],"bad":[0,7]}],"guards":[]},{"n":15,"root":[{"t":[0,1,2],"bad":[2,5]},{"t":[0,3,4],"bad":[1,6]},{"t":[0,5,6],"bad":[3,4]},{"t":[0,7,8],"bad":[2,5]},{"t":[0,9,10],"bad":[3,4]},{"t":[0,11,12],"bad":[3,4]},{"t":[0,13,14],"bad":[1,6]},{"t":[1,3,5],"bad":[2,5]},{"t":[1,4,6],"bad":[3,4]},{"t":[1,7,9],"bad":[1,6]},{"t":[1,8,10],"bad":[3,4]},{"t":[1,11,13],"bad":[1,6]},{"t":[1,12,14],"bad":[2,5]},{"t":[2,3,6],"bad":[1,6]},{"t":[2,4,5],"bad":[2,5]},{"t":[2,7,10],"bad":[3,4]},{"t":[2,8,9],"bad":[2,5]},{"t":[2,11,14],"bad":[1,6]},{"t":[2,12,13],"bad":[1,6]},{"t":[3,7,11],"bad":[3,4]},{"t":[3,8,12],"bad":[3,4]},{"t":[3,9,13],"bad":[3,4]},{"t":[3,10,14],"bad":[3,4]},{"t":[4,7,12],"bad":[1,6]},{"t":[4,8,11],"bad":[2,5]},{"t":[4,9,14],"bad":[2,5]},{"t":[4,10,13],"bad":[1,6]},{"t":[5,7,13],"bad":[1,6]},{"t":[5,8,14],"bad":[3,4]},{"t":[5,9,11],"bad":[2,5]},{"t":[5,10,12],"bad":[2,5]},{"t":[6,7,14],"bad":[3,4]},{"t":[6,8,13],"bad":[2,5]},{"t":[6,9,12],"bad":[2,5]},{"t":[6,10,11],"bad":[0,7]}],"sat":[{"t":[0,1,2],"bad":[2,5]},{"t":[0,3,4],"bad":[1,6]},{"t":[0,5,6],"bad":[3,4]},{"t":[0,7,8],"bad":[2,5]},{"t":[0,9,10],"bad":[3,4]},{"t":[0,11,12],"bad":[3,4]},{"t":[0,13,14],"bad":[1,6]},{"t":[1,3,5],"bad":[2,5]},{"t":[1,4,6],"bad":[3,4]},{"t":[1,7,9],"bad":[1,6]},{"t":[1,8,10],"bad":[3,4]},{"t":[1,11,13],"bad":[1,6]},{"t":[1,12,14],"bad":[2,5]},{"t":[2,3,6],"bad":[1,6]},{"t":[2,4,5],"bad":[2,5]},{"t":[2,7,10],"bad":[3,4]},{"t":[2,8,9],"bad":[2,5]},{"t":[2,11,14],"bad":[1,6]},{"t":[2,12,13],"bad":[1,6]},{"t":[3,7,11],"bad":[3,4]},{"t":[3,8,12],"bad":[3,4]},{"t":[3,9,13],"bad":[3,4]},{"t":[3,10,14],"bad":[3,4]},{"t":[4,7,12],"bad":[1,6]},{"t":[4,8,11],"bad":[2,5]},{"t":[4,9,14],"bad":[2,5]},{"t":[4,10,13],"bad":[1,6]},{"t":[5,7,13],"bad":[1,6]},{"t":[5,8,14],"bad":[3,4]},{"t":[5,9,11],"bad":[2,5]},{"t":[5,10,12],"bad":[2,5]},{"t":[6,7,14],"bad":[3,4]},{"t":[6,8,13],"bad":[2,5]},{"t":[6,9,12],"bad":[2,5]},{"t":[6,10,11],"bad":[2,5]}],"guards":[[4,6,0],[6,8,0],[0,3,0],[1,2,0],[2,3,0],[3,5,1],[5,7,1]]}];
const run = function run(inputs){
const mod=x=>(x%3+3)%3,pc=x=>{let c=0;while(x){x&=x-1;c++}return c},bit=i=>1<<i;
const stats={referenceWords:0,closureScans:0,rows:0,reductions:0,pairProbes:0,rounds:0,checks:0};
function check(x){stats.checks++;if(!x)throw Error("assert "+stats.checks)}
function solve(n,E,G,D){
 let guards=G.slice(),seen=new Map(G.map(([i,j,b])=>[bit(i)^bit(j),b])),derived=0,rank=0;
 function add(i,j,b){let k=bit(i)^bit(j);if(seen.has(k))return seen.get(k)===b?0:-1;seen.set(k,b);guards.push([i,j,b]);derived++;return 1}
 while(true){
 let changed=false;stats.rounds++;
 // Complete local domain/pair closure relative to parity guards.
 let p=Array.from({length:n},(_,i)=>i),z=Array(n).fill(0);
 function find(i){let b=0;while(i!==p[i]){b^=z[i];i=p[i]}return [i,b]}
 for(let [i,j,b] of guards){let [u,a]=find(i),[v,c]=find(j);if(u===v){if((a^c)!==b)return {state:"UNSAT",derived,rank};}else{p[u]=v;z[u]=a^c^b}}
 for(let e of E){stats.closureScans++;let W=[];for(let w=0;w<8;w++){if(e.bad.includes(w))continue;let ok=true;for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){let [u,a]=find(e.t[i]),[v,b]=find(e.t[j]);if(u===v&&((w>>i^w>>j)&1)!==(a^b))ok=false}if(ok)W.push(w)}if(!W.length)return {state:"UNSAT",derived,rank};for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){let b=(W[0]>>i^W[0]>>j)&1;if(W.every(w=>((w>>i^w>>j)&1)===b)){let a=add(e.t[i],e.t[j],b);if(a<0)return {state:"UNSAT",derived,rank};if(a)changed=true}}}
 if(changed)continue;
 const masks=[0];for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)masks.push(bit(i)^bit(j));
 if(D===4)for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)for(let k=j+1;k<n;k++)for(let l=k+1;l<n;l++)masks.push(bit(i)^bit(j)^bit(k)^bit(l));
 const idx=new Map(masks.map((m,i)=>[m,i])),mult=masks.filter(m=>pc(m)<=D-2),B=new Map();
 function reduce(row){while(row.size){let pivot=-1;for(let k of row.keys())if(k>pivot)pivot=k;let q=B.get(pivot);if(!q)break;let c=row.get(pivot);stats.reductions++;for(let [k,v] of q){let t=mod((row.get(k)||0)-c*v);if(t)row.set(k,t);else row.delete(k)}}return row}
 function insert(terms){let row=new Map();for(let [m,c] of terms){let k=idx.get(m),v=mod((row.get(k)||0)+c);if(v)row.set(k,v);else row.delete(k)}stats.rows++;reduce(row);if(!row.size)return true;let pivot=Math.max(...row.keys());if(pivot===0)return false;let inv=row.get(pivot);if(inv===2)for(let [k,v] of row)row.set(k,mod(2*v));B.set(pivot,row);return true}
 const equations=E.map(e=>{let t=[[0,1]];for(let i=0;i<3;i++)for(let j=i+1;j<3;j++)t.push([bit(e.t[i])^bit(e.t[j]),((e.bad[0]>>i^e.bad[0]>>j)&1)?-1:1]);return t}).concat(guards.map(([i,j,b])=>[[bit(i)^bit(j),1],[0,b?1:-1]]));
 for(let eq of equations)for(let m of mult)if(!insert(eq.map(([a,c])=>[a^m,c])))return {state:"UNSAT",derived,rank:B.size};
 rank=B.size;
 for(let i=0;i<n;i++)for(let j=i+1;j<n;j++){stats.pairProbes++;let row=reduce(new Map([[idx.get(bit(i)^bit(j)),1]]));if(row.size===0)return {state:"UNSAT",derived,rank};if(row.size===1&&row.has(0)){let v=row.get(0);let a=add(i,j,v===2?1:0);if(a<0)return {state:"UNSAT",derived,rank};if(a)changed=true}}
 if(changed)continue;
 // only return SAT from an actual source witness (canonical parity representative).
 let w=0;for(let i=0;i<n;i++)if(find(i)[1])w|=bit(i);let valid=E.every(e=>!e.bad.includes(e.t.reduce((a,v,j)=>a|(((w>>v)&1)<<j),0)))&&guards.every(([i,j,b])=>((w>>i^w>>j)&1)===b);
 return {state:valid?"SAT":"OPEN",derived,rank,witness:valid?w:null,guards};
 }
}
let results=[];
for(let u of inputs){let jobs=[["root","raw",[]],["sat","raw",[]]];if(u.guards.length)jobs.push(["root","first",u.guards.slice(0,1)],["root","seven",u.guards]);for(let [label,guard,G] of jobs){let E=u[label],models=[];for(let w=0;w<1<<u.n;w++){stats.referenceWords++;if(G.every(([i,j,b])=>((w>>i^w>>j)&1)===b)&&E.every(e=>!e.bad.includes(e.t.reduce((a,v,j)=>a|(((w>>v)&1)<<j),0))))models.push(w)}
let a=solve(u.n,E,G,2),b=solve(u.n,E,G,4);for(let v of [a,b]){check(v.state!=="UNSAT"||!models.length);check(v.state!=="SAT"||models.includes(v.witness));if(v.guards)check(models.every(w=>v.guards.every(([i,j,c])=>((w>>i^w>>j)&1)===c)))}results.push({n:u.n,label,guard,models:models.length,degree2:a,degree4:b})}}
return {results,stats};
};
console.log(JSON.stringify(run(inputs),null,2));
