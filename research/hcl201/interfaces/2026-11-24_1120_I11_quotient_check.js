const run = function(){
 const A=(v,m="assert")=>{if(!v)throw Error(m)};
 const stats={cases:0,sat:0,unsat:0,closureCalls:0,deleted:0,joins:0,lifts:0,rank2Rows:0,rank0Rows:0};
 function basis(vs){let b=new Map;for(let x of vs)while(x){let i=x.toString(2).length-1;if(b.has(i))x^=b.get(i);else{b.set(i,x);break}}return b}
 function contains(b,x){while(x){let i=x.toString(2).length-1;if(!b.has(i))return false;x^=b.get(i)}return true}
 function aff(rs){let a=0n,d=[];for(let r of rs){a^=r[0].tag;for(let x of r)d.push(x.tag^r[0].tag)}return {a,b:basis(d)}}
 function solve(n,E){
 let root=Array.from({length:n},(_,i)=>i),adj=Array.from({length:n},()=>[]),chords=[];
 function f(v){while(root[v]!==v)v=root[v];return v}
 E.forEach(([a,b],i)=>{let u=f(a),v=f(b);if(u===v)chords.push(i);else{root[v]=u;adj[a].push([b,i]);adj[b].push([a,i])}});
 let c=n-E.length+chords.length,cols=E.map(()=>0n);
 chords.forEach((i,j)=>{let [a,b]=E[i],mask=1n<<BigInt(2*j);cols[i]|=mask;function walk(u,p){if(u===b)return true;for(const [v,e] of adj[u])if(v!==p&&walk(v,u)){cols[e]|=mask;return true}return false}A(walk(a,-1));});
 let rows=E.map(([a,b,s],i)=>[0,1,2,3].filter(d=>d!==s).map(d=>({d,tag:((d&1)?cols[i]:0n)^((d&2)?cols[i]<<1n:0n)})));
 for(let r of rows){let rank=aff([r]).b.size;A(rank===0||rank===2);stats[rank===2?"rank2Rows":"rank0Rows"]++}
 const rank=aff(rows).b.size;A(rank===2*chords.length);
 while(true){stats.closureCalls++;let changed=false;for(let i=0;i<rows.length&&!changed;i++){let {a,b}=aff(rows.filter((_,j)=>i!==j));for(let j=0;j<rows[i].length;j++)if(!contains(b,a^rows[i][j].tag)){rows[i].splice(j,1);stats.deleted++;changed=true;break}if(!rows[i].length)return {count:0n,rank,width:0,peak:0}}if(!changed)break}
 let full=aff(rows).b.size,suffix=rows.map((_,i)=>aff(rows.slice(i+1))),tab=new Map([[0n,{cnt:1n,path:[]}]]),width=0,peak=1;
 for(let i=0;i<rows.length;i++){let {a,b}=suffix[i],w=aff(rows.slice(0,i+1)).b.size+b.size-full;width=Math.max(width,w);let next=new Map;for(let [s,v] of tab)for(let r of rows[i]){stats.joins++;let t=s^r.tag;if(!contains(b,t^a))continue;let old=next.get(t);if(old)old.cnt+=v.cnt;else next.set(t,{cnt:v.cnt,path:[...v.path,r.d]})}tab=next;A(tab.size<=2**w);peak=Math.max(peak,tab.size);if(!tab.size)break}
 let end=tab.get(0n);if(!end)return {count:0n,rank,width,peak};let x=Array(n).fill(-1);
 function assign(u){for(let [v,i] of adj[u])if(x[v]<0){x[v]=x[u]^end.path[i];assign(v)}}
 for(let i=0;i<n;i++)if(x[i]<0){x[i]=0;assign(i)}
 E.forEach(([a,b,s],i)=>A((x[a]^x[b])===end.path[i]&&end.path[i]!==s));stats.lifts++;return {count:end.cnt*4n**BigInt(c),rank,width,peak};
 }
 function edges(n){let e=[];for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)e.push([i,j,0]);return e}
 function ref(n,E){let x=Array(n).fill(0),count=0n;function v(i){if(i===n){if(E.every(([a,b,s])=>(x[a]^x[b])!==s))count++;return}for(let z=0;z<4;z++){x[i]=z;v(i+1)}}v(0);return count}
 function check(n,E,want){let r=solve(n,E);A(r.count===want,"count");stats.cases++;stats[want?"sat":"unsat"]++;return {...r,count:String(r.count)}}
 let seed=71241120;function rng(){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed}
 for(let z=0;z<100;z++){let n=3+rng()%4,E=edges(n).filter(()=>rng()%5<3).map(([a,b])=>[a,b,z%2?rng()%4:0]);check(n,E,ref(n,E))}
 let critical=[];for(let d=-1;d<10;d++){let E=edges(5).filter((_,i)=>i!==d);critical.push({deleted:d,...check(5,E,ref(5,E))})}
 let scales=[];for(let k of [1,4,8,16,32])for(let bad of [false,true]){let E=[];for(let j=0;j<k;j++){let e=edges(5);if(!bad||j!==k-1)e.pop();E.push(...e.map(([a,b,s])=>[a+5*j,b+5*j,s]))}scales.push({k,bad,...check(5*k,E,bad?0n:24n**BigInt(k))})}
 return {seed:71241120,stats,critical,scales}
};
console.log(JSON.stringify(run(),null,2));
