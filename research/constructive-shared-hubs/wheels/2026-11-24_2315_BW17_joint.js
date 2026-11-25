
function experiment(f){
const n=f.n,O=f.O,x=BigInt(f.x),y=BigInt(f.y),B=i=>1n<<BigInt(i),bit=(w,i)=>Number((w>>BigInt(i))&1n);
const a=O.filter(o=>o.p<2),b=O.filter(o=>o.p>=2);
let st={ownerChecks:0,commonTests:0,closureScans:0,pairTests:0,forced:0,choices:0};
function ok(O,w){for(const o of O){st.ownerChecks++;const t=o.t.map(i=>bit(w,i));if(t.every(k=>k===t[0]))return false}return true}
let first=null,counts=[];
for(let k=1;k<=6&&!first;k++){let count=0;function go(start,left,mask){if(!left){st.commonTests++;let u=x^mask,v=y^mask;if(ok(a,u)&&ok(b,v)){count++;if(!first)first={k,mask:String(mask),x:String(u),y:String(v)}}return}for(let i=start;i<n;i++)if(i!==f.d)go(i+1,left-1,mask|B(i))}go(0,k,0n);counts.push(count)}
const pairs=O.map(o=>{let w=o.p<2?x:y,t=o.t;let p=[];for(let i=0;i<3;i++)for(let j=i+1;j<3;j++)if(bit(w,t[i])!==bit(w,t[j]))p.push([t[i],t[j]]);return p});
let trials=[],rng=1234567;function rand(n){rng^=rng<<13;rng^=rng>>>17;rng^=rng<<5;return (rng>>>0)%n}
for(let s=0;s<32;s++){let p=Array.from({length:n},(_,i)=>i),q=Array(n).fill(0),size=Array(n).fill(1),order=Array.from({length:O.length},(_,i)=>i),log=[];
if(s>0)for(let i=order.length-1;i>0;i--){let j=rand(i+1);[order[i],order[j]]=[order[j],order[i]]}
function find(i){let w=0;while(p[i]!==i){w^=q[i];i=p[i]}return [i,w]}
function type([i,j]){st.pairTests++;let [u,a]=find(i),[v,b]=find(j);return u===v?(a^b?1:-1):0}
function join([i,j],id,kind){let [u,a]=find(i),[v,b]=find(j);if(u===v)return;if(size[u]<size[v])[u,v]=[v,u];p[v]=u;q[v]=a^b^1;size[u]+=size[v];log.push({id,pair:[i,j],kind});st[kind==="forced"?"forced":"choices"]++}
let outcome="UNKNOWN";
while(true){st.closureScans++;let open=[],restart=false,conflict=false;for(let id of order){let ps=pairs[id],ts=ps.map(type);if(ts.includes(1))continue;if(ts.every(t=>t===-1)){conflict=true;break}let options=ps.filter((_,j)=>ts[j]===0);if(options.length===1){join(options[0],id,"forced");restart=true;break}open.push({id,options})}if(conflict)break;if(restart)continue;if(!open.length){let w=0n;for(let i=0;i<n;i++)if(find(i)[1])w|=B(i);if(!ok(O,w))throw Error("bad source witness");outcome="SAT";trials.push({s,outcome,word:String(w),log});break}let {id,options}=open[0];options.sort((a,b)=>{let cost=([i,j])=>size[find(i)[0]]*size[find(j)[0]];return cost(a)-cost(b)});join(options[0],id,"choice")}
if(outcome==="UNKNOWN")trials.push({s,outcome,log});
}
return {counts,first,anchoredSuccess:trials.filter(t=>t.outcome==="SAT").length,trials,st}
}

console.log(JSON.stringify(experiment(JSON.parse(require("fs").readFileSync(process.argv[2],"utf8"))),null,2));
