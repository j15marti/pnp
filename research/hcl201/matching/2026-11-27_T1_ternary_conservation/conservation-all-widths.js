function run(corpus){
const mod=(x,p)=>(x%p+p)%p;
function groups(C){let keys=new Map(C.map((c,i)=>[c.slice().sort((a,b)=>a-b).join(","),i+1]));return C.flatMap((c,i)=>{if(c.length<1||!c.every(x=>x>0)||new Set(c).size!==c.length)return[];let ids=[i+1];for(let a=0;a<c.length;a++)for(let b=a+1;b<c.length;b++){let j=keys.get([-c[a],-c[b]].sort((a,b)=>a-b).join(","));if(!j)return[];ids.push(j)}return[{v:c,ids}]})}
function test(E,n,p,H){let rows=E.map(e=>({a:Array.from({length:n},(_,i)=>Number(e.v.includes(i+1))).concat(1),ids:e.ids})).concat(H.map(l=>({a:Array.from({length:n},(_,i)=>Number(i+1===Math.abs(l))).concat(+(l>0)),ids:[]})));let m=rows.length,B=new Map,ops=0;function sub(r,q,c){for(let i=0;i<r.length;i++){r[i]=mod(r[i]-c*q[i],p);ops++}}
for(let k=0;k<m;k++){let a=rows[k].a.slice(),z=Array.from({length:m},(_,i)=>+(i===k));for(let j=0;j<n;j++)if(a[j]){if(B.has(j)){let q=B.get(j),c=a[j];sub(a,q.a,c);sub(z,q.z,c)}else{let c=a[j]===1?1:2;for(let i=0;i<a.length;i++)a[i]=mod(c*a[i],p);for(let i=0;i<m;i++)z[i]=mod(c*z[i],p);B.set(j,{a,z});break}}if(a.slice(0,n).every(v=>!v)&&a[n])return cert(a,z)}
for(let j of [...B.keys()].sort((a,b)=>b-a))for(let [k,q] of B)if(k<j&&q.a[j]){let c=q.a[j];sub(q.a,B.get(j).a,c);sub(q.z,B.get(j).z,c)}
let forced=[];for(let q of B.values())if(q.a.slice(0,n).filter(Boolean).length===1){if(q.a[n]===2)return cert(q.a,q.z);forced.push([q.a.findIndex(Boolean)+1,q.a[n]])}
return {bad:false,rank:B.size,ops,forced};
function cert(a,z){let b=Array.from({length:n+1},(_,i)=>mod(rows.reduce((s,r,j)=>s+z[j]*r.a[i],0),p));if(JSON.stringify(b)!==JSON.stringify(a))throw Error("certificate");return{bad:true,rank:B.size,ops,coeff:z,derived:b,originalIds:[...new Set(rows.flatMap((r,j)=>z[j]?r.ids:[]))].sort((a,b)=>a-b)}}
}
function encode(E){let C=[];for(let v of E){C.push(v);for(let i=0;i<v.length;i++)for(let j=i+1;j<v.length;j++)C.push([-v[i],-v[j]])}return C}
let out=[];for(let x of corpus.instances.filter(x=>["JOINT-24","RANDOM-3CNF-40"].includes(x.id))){let C=x.dimacs.trimEnd().split("\n").slice(1).map(s=>s.split(/\s+/).map(Number).slice(0,-1)),E=groups(C),n=x.nvars,guards=[[],[1],[-1,2],[-1,-2,3],[-1,-2,-3,4],[-1,-2,-3,-4]];out.push({id:x.id,E,guards:guards.map(H=>({H,F2:test(E,n,2,H),F3:test(E,n,3,H)}))})}
let controls=[];for(let S of [[[1,2,3],[1,2,4],[1,3,4],[2,3,4]],[[1,2,3],[1,2,4],[1,3,4]]]){let C=encode(S),E=groups(C),solutions=[];for(let a=0;a<16;a++)if(S.every(v=>v.reduce((s,x)=>s+(a>>(x-1)&1),0)===1))solutions.push(a);controls.push({S,C,solutions,F2:test(E,4,2,[]),F3:test(E,4,3,[])})}return{out,controls}
}
module.exports=run;
