// Standalone LSPV-2/429 deterministic black-box pointer port and Tseitin controls.
// Run: node lspv2_429_compact_replay.mjs
let checks=0;
function ok(p,s){if(!p)throw Error(s);checks++}
function endpoint(f,k){let x=0;for(let i=0;i<k;i++)x=f[x];return x}
function casePair(k,mode){const M=4*k+8,seen=new Map(),trace=[],chain=[0];
 function ask(x){if(!seen.has(x)){if(x===chain.at(-1)){
   let y=0;while(seen.has(y)||chain.includes(y))y++;
   seen.set(x,y);chain.push(y)}else seen.set(x,x)}trace.push([x,seen.get(x)])}
 for(let i=0;i<k-1;i++)ask(mode==='follow'?chain.at(-1):mode==='down'?M-1-i:mode==='up'?i:((i&1)?M-1-i:chain.at(-1)));
 let used=new Set([...seen.keys(),...chain]);
 while(chain.length<k){let y=0;while(used.has(y))y++;seen.set(chain.at(-1),y);chain.push(y);used.add(y)}
 let a=0;while(used.has(a)||(a&1)!==0)a++;
 let b=0;while(used.has(b)||(b&1)!==1)b++;
 let f0=Array.from({length:M},(_,i)=>i),f1=[...f0];
 for(const [x,y]of seen){f0[x]=y;f1[x]=y}
 f0[chain.at(-1)]=a;f1[chain.at(-1)]=b;
 for(const [x,y]of trace)ok(f0[x]===y&&f1[x]===y,'shared transcript');
 ok(endpoint(f0,k)===a&&endpoint(f1,k)===b&&a%2===0&&b%2===1,'opposite checkpoint');
 ok(trace.length===k-1,'q<k');
 return {k,M,mode,query_count:trace.length,first:trace[0],last:trace.at(-1),end0:a,end1:b};
}
function tseitin(edges,n,charge){const adj=Array.from({length:n},()=>[]);edges.forEach(([u,v],i)=>{adj[u].push(i+1);adj[v].push(i+1)});
 ok(adj.every(x=>x.length===3),'cubic');let cls=[];
 adj.forEach((ids,v)=>{for(let t=0;t<8;t++){
 const bits=[t&1,(t>>1)&1,(t>>2)&1];if((bits[0]^bits[1]^bits[2])!==charge[v])cls.push(ids.map((x,j)=>bits[j]?-x:x))}});
 ok(cls.length===4*n,'4n 3clauses');let sat=false;
 for(let mask=0;mask<(1<<edges.length);mask++){
 if(cls.every(c=>c.some(x=>x>0?((mask>>(x-1))&1):!((mask>>(-x-1))&1)))){sat=true;break}}
 return {n,vars:edges.length,clauses:cls.length,sat};
}
const cases=[];for(let k=2;k<=15;k++)for(const mode of ['follow','down','up','alternate'])cases.push(casePair(k,mode));
const k4=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
const cube=[];for(let u=0;u<8;u++)for(let v=u+1;v<8;v++)if(((u^v).toString(2).match(/1/g)||[]).length===1)cube.push([u,v]);
const controls=[];for(const [name,edges,n] of [['K4',k4,4],['cube',cube,8]])for(const odd of [false,true]){
 const charges=Array(n).fill(0);charges[0]=Number(odd);
 const c=tseitin(edges,n,charges);ok(c.sat===!odd,'both charge labels');controls.push({name,odd,...c});
}
for(const k of [2,3,5,8,13]){let M=4*k+8;let f=Array.from({length:M},(_,i)=>i^1);ok(endpoint(f,k)===(k%2),'white-box XOR shortcut')}
console.log(JSON.stringify({status:'RESTRICTED',cases:cases.length,checks,controls,
 limits:'opaque successor entry queries only; unrestricted all-input FLMV open'}));
