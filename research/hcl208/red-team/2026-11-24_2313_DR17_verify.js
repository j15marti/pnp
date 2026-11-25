function verify(j){
const {registry:O,x,y,witness:w}=j,n=x.length,d=0;
const assert=(v)=>{if(!v)throw Error("check failed")};
const ok=(v,t)=>t.some(i=>v[i]!==v[t[0]]);
const pairs=new Set();for(let p=0;p<4;p++){let a=O.filter(o=>o.p===p).flatMap(o=>o.t);assert(a.length===n&&new Set(a).size===n);}
for(const {t} of O)for(let a=0;a<3;a++)for(let b=a+1;b<3;b++){let k=[t[a],t[b]].sort((a,b)=>a-b).join(",");assert(!pairs.has(k));pairs.add(k);}
assert(O.every(o=>ok(w,o.t)));
const adj=Array.from({length:n},()=>new Set()),block=Array.from({length:n},()=>[]);
for(const o of O){let v=o.p<2?x:y;assert(ok(v,o.t));let m=o.t.find(i=>o.t.filter(k=>v[k]===v[i]).length===1);block[m].push(o);for(const k of o.t)if(k!==m)adj[m].add(k);}
assert(block.every(a=>a.length));
let girth=Infinity;for(let s=1;s<n;s++){let q=[s],dist=Array(n).fill(-1);dist[s]=0;for(let i=0;i<q.length;i++){let u=q[i];for(let v of adj[u]){if(v===d)continue;if(v===s)girth=Math.min(girth,dist[u]+1);else if(dist[v]===-1){dist[v]=dist[u]+1;q.push(v)}}}}
let seen=new Set([0]),q=[0];for(let i=0;i<q.length;i++)for(let o of O)if(o.t.includes(q[i]))for(let v of o.t)if(!seen.has(v)){seen.add(v);q.push(v);}
let counts=[],first=null;for(let k=1;k<=5&&!first;k++){let tests=0,valid=0;const S=new Set();function dfs(start,left){if(left===0){tests++;if(O.every(o=>{let v=o.p<2?x:y,t=o.t;return t.some(i=>(v[i]^Number(S.has(i)))!==(v[t[0]]^Number(S.has(t[0]))))})){valid++;if(!first)first=[...S]}return;}for(let i=start;i<=n-left;i++){S.add(i);dfs(i+1,left-1);S.delete(i)}}dfs(1,k);counts.push({k,tests,valid});}
return {verified:true,n,pairs:pairs.size,connected:seen.size===n,blockCounts:block.map(a=>a.length),directedGirth:girth,counts,first};
}
if(require.main===module)console.log(JSON.stringify(verify(JSON.parse(require("fs").readFileSync(process.argv[2],"utf8"))),null,2));
