const audit = function(){
 let assertions=0;function ok(b){assertions++;if(!b)throw Error("assert "+assertions)}
 function ladder(k){let edges=[],id=new Map(),C=[];function e(u,v){let key=[Math.min(u,v),Math.max(u,v)].join(",");if(!id.has(key)){id.set(key,edges.length);edges.push([u,v])}else{let old=edges[id.get(key)];ok(old[0]===u&&old[1]===v)}return id.get(key)}
 for(let i=0;i<k;i++){let v=[i,i+1,k+2+i,k+1+i];if(i%2)v.reverse();C.push(v.map((x,j)=>e(x,v[(j+1)%4])))}return{V:2*(k+1),edges,C,p:Array.from({length:2*(k+1)},(_,i)=>(i%(k+1)+Math.floor(i/(k+1)))%2)}}
 function solve(F,pins){let D=[];for(let i=0;i<F.edges.length;i++){let [u,v]=F.edges[i],q=F.p[v]-F.p[u],lo=-1,hi=1;if(pins[i]!==-1)lo=hi=2*pins[i]-1;D.push([u,v,Math.floor((hi-q)/2)],[v,u,-Math.ceil((lo-q)/2)])}let d=Array(F.V).fill(0);for(let i=0;i<F.V;i++){let ch=false;for(let [u,v,b] of D)if(d[v]>d[u]+b){d[v]=d[u]+b;ch=true}if(!ch){let x=F.edges.map(([u,v])=>(2*(d[v]-d[u])+F.p[v]-F.p[u]+1)/2);ok(x.every((v,i)=>(v===0||v===1)&&(pins[i]===-1||v===pins[i])));ok(F.C.every(r=>r.reduce((s,i)=>s+x[i],0)===2));return x}if(i===F.V-1)return null}}
 function exact(F,pins){for(let w=0;w<2**F.edges.length;w++){if(pins.some((p,i)=>p!==-1&&(w>>i&1)!==p))continue;if(F.C.every(r=>r.reduce((s,i)=>s+(w>>i&1),0)===2))return true}return false}
 let jobs=0,yes=0,no=0,scalable=[];
 for(let k of [1,2,3]){let F=ladder(k),L=F.edges.length;for(let i=0;i<3**L;i++){if(k===3&&i%37!==0)continue;let w=i,p=[];for(let j=0;j<L;j++){p.push(w%3-1);w=Math.floor(w/3)}let r=solve(F,p);ok(Boolean(r)===exact(F,p));jobs++;if(r)yes++;else no++}}
 for(let k of [8,32,128,512]){let F=ladder(k),p=Array(F.edges.length).fill(-1);ok(solve(F,p));for(let i of F.C[0].slice(0,3))p[i]=1;ok(solve(F,p)===null);scalable.push({k,variables:F.edges.length,clauses:F.C.length})}
 return{jobs,yes,no,scalable,assertions};
};
console.log(JSON.stringify(audit(),null,2));
