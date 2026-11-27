function finiteAudit(){
 const A=(b,m)=>{if(!b)throw Error(m)},canon=w=>{let M=new Map;return w.map(x=>{if(!M.has(x))M.set(x,M.size+1);return M.get(x)}).join("")};
 const words=Array.from({length:729},(_,j)=>Array.from({length:6},(_,i)=>1+Math.floor(j/3**i)%3)).filter(w=>[1,2,3].every(c=>w.filter(x=>x===c).length%2===0));
 const U=[...new Set(words.map(canon))].sort(),I=new Map(U.map((w,i)=>[w,i]));A(U.length===31,"31");
 const bit=w=>2**I.get(canon(w)),decode=m=>U.filter((_,i)=>m&(2**i)),balanced=U.map((w,i)=>new Set(w).size===3?i:-1).filter(i=>i>=0);
 function pairings(v){if(!v.length)return [[]];let out=[];for(let j=1;j<v.length;j++)for(const p of pairings(v.filter((_,i)=>i!==0&&i!==j)))out.push([[v[0],v[j]],...p]);return out}
 function perm(v){if(!v.length)return [[]];return v.flatMap((x,i)=>perm(v.filter((_,j)=>i!==j)).map(p=>[x,...p]))}
 function orbit(w,a,b,p){let m=0;for(let f=0;f<2**p.length;f++){const z=[...w].map(Number);p.forEach(([i,j],q)=>{if(f>>q&1){z[i]=a+b-z[i];z[j]=a+b-z[j]}});m|=bit(z)}return m}
 const pairs=[[1,2],[1,3],[2,3]], opts=U.map(w=>pairs.map(([a,b])=>pairings([...w].map((x,i)=>+x===a||+x===b?i:-1).filter(i=>i>=0)).map(p=>orbit(w,a,b,p))));
 const K=m=>{for(;;){let n=m;for(let i=0;i<31;i++)if((m&(2**i))&&opts[i].some(row=>!row.some(o=>(o&m)===o)))n&=~(2**i);if(n===m)return n;m=n}};
 const closed=[];for(let a=1;a<32768;a++){let s=0;balanced.forEach((j,i)=>{if(a>>i&1)s|=2**j});if(K(s)===s)closed.push(s)}
 const minimal=closed.filter(s=>!closed.some(t=>s!==t&&(s&t)===t)).sort((a,b)=>decode(a).length-decode(b).length||a-b), seen=new Set(),orbits=[];
 for(const s of minimal){if(seen.has(s))continue;const r=new Set(perm([0,1,2,3,4,5]).map(p=>decode(s).reduce((m,w)=>m|bit(p.map(i=>w[i])),0)));r.forEach(x=>seen.add(x));orbits.push([s,decode(s).length,r.size])}
 A(closed.length===277&&minimal.length===31,"closed classification");A(orbits.length===3&&orbits.map(x=>x[1]).join()==="6,8,10","3 types");
 const target=1553138944,S=decode(target),absent=balanced.map(i=>U[i]).filter(w=>!S.includes(w)); const blocks=w=>[1,2,3].map(c=>[...w].map((x,i)=>+x===c?i:-1).filter(i=>i>=0).join(""));
 A(absent.length===5&&new Set(absent.flatMap(blocks)).size===15,"factorization");let edge=[];for(let i=0;i<S.length;i++)for(let j=i+1;j<S.length;j++)if(blocks(S[i]).some(x=>blocks(S[j]).includes(x)))edge.push([i,j]);A(edge.length===15,"cubic support");
 const noncross=(p,o)=>{const pos=o.reduce((z,v,i)=>(z[v]=i,z),[]);for(let a=0;a<p.length;a++)for(let b=a+1;b<p.length;b++){let [x,y]=p[a].map(i=>pos[i]).sort((a,b)=>a-b),[u,v]=p[b].map(i=>pos[i]).sort((a,b)=>a-b);if(x<u&&u<y&&y<v||u<x&&x<v&&v<y)return false}return true};
 let orders=0,pass=0;for(const p of perm([1,2,3,4,5])){const o=[0,...p];orders++;if(S.every(w=>pairs.every(([a,b])=>pairings([...w].map((x,i)=>+x===a||+x===b?i:-1).filter(i=>i>=0)).some(q=>noncross(q,o)&&(orbit(w,a,b,q)&target)===orbit(w,a,b,q)))))pass++}
 A(orders===120&&pass===0,"planar obstruction");return {closed:closed.length,minimal:minimal.length,orbits,target,states:S,absent,edge,orders,pass}
}
console.log(JSON.stringify(finiteAudit(),null,2));
