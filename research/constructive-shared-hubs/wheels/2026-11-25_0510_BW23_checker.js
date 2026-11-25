const inputs = [{"n":7,"root":[{"t":[0,1,2],"bad":[0,7]},{"t":[0,3,4],"bad":[0,7]},{"t":[0,5,6],"bad":[0,7]},{"t":[1,3,5],"bad":[0,7]},{"t":[1,4,6],"bad":[0,7]},{"t":[2,3,6],"bad":[0,7]},{"t":[2,4,5],"bad":[0,7]}],"sat":[{"t":[0,1,2],"bad":[2,5]},{"t":[0,3,4],"bad":[0,7]},{"t":[0,5,6],"bad":[0,7]},{"t":[1,3,5],"bad":[0,7]},{"t":[1,4,6],"bad":[0,7]},{"t":[2,3,6],"bad":[0,7]},{"t":[2,4,5],"bad":[0,7]}],"guards":[]},{"n":15,"root":[{"t":[0,1,2],"bad":[2,5]},{"t":[0,3,4],"bad":[1,6]},{"t":[0,5,6],"bad":[3,4]},{"t":[0,7,8],"bad":[2,5]},{"t":[0,9,10],"bad":[3,4]},{"t":[0,11,12],"bad":[3,4]},{"t":[0,13,14],"bad":[1,6]},{"t":[1,3,5],"bad":[2,5]},{"t":[1,4,6],"bad":[3,4]},{"t":[1,7,9],"bad":[1,6]},{"t":[1,8,10],"bad":[3,4]},{"t":[1,11,13],"bad":[1,6]},{"t":[1,12,14],"bad":[2,5]},{"t":[2,3,6],"bad":[1,6]},{"t":[2,4,5],"bad":[2,5]},{"t":[2,7,10],"bad":[3,4]},{"t":[2,8,9],"bad":[2,5]},{"t":[2,11,14],"bad":[1,6]},{"t":[2,12,13],"bad":[1,6]},{"t":[3,7,11],"bad":[3,4]},{"t":[3,8,12],"bad":[3,4]},{"t":[3,9,13],"bad":[3,4]},{"t":[3,10,14],"bad":[3,4]},{"t":[4,7,12],"bad":[1,6]},{"t":[4,8,11],"bad":[2,5]},{"t":[4,9,14],"bad":[2,5]},{"t":[4,10,13],"bad":[1,6]},{"t":[5,7,13],"bad":[1,6]},{"t":[5,8,14],"bad":[3,4]},{"t":[5,9,11],"bad":[2,5]},{"t":[5,10,12],"bad":[2,5]},{"t":[6,7,14],"bad":[3,4]},{"t":[6,8,13],"bad":[2,5]},{"t":[6,9,12],"bad":[2,5]},{"t":[6,10,11],"bad":[0,7]}],"sat":[{"t":[0,1,2],"bad":[2,5]},{"t":[0,3,4],"bad":[1,6]},{"t":[0,5,6],"bad":[3,4]},{"t":[0,7,8],"bad":[2,5]},{"t":[0,9,10],"bad":[3,4]},{"t":[0,11,12],"bad":[3,4]},{"t":[0,13,14],"bad":[1,6]},{"t":[1,3,5],"bad":[2,5]},{"t":[1,4,6],"bad":[3,4]},{"t":[1,7,9],"bad":[1,6]},{"t":[1,8,10],"bad":[3,4]},{"t":[1,11,13],"bad":[1,6]},{"t":[1,12,14],"bad":[2,5]},{"t":[2,3,6],"bad":[1,6]},{"t":[2,4,5],"bad":[2,5]},{"t":[2,7,10],"bad":[3,4]},{"t":[2,8,9],"bad":[2,5]},{"t":[2,11,14],"bad":[1,6]},{"t":[2,12,13],"bad":[1,6]},{"t":[3,7,11],"bad":[3,4]},{"t":[3,8,12],"bad":[3,4]},{"t":[3,9,13],"bad":[3,4]},{"t":[3,10,14],"bad":[3,4]},{"t":[4,7,12],"bad":[1,6]},{"t":[4,8,11],"bad":[2,5]},{"t":[4,9,14],"bad":[2,5]},{"t":[4,10,13],"bad":[1,6]},{"t":[5,7,13],"bad":[1,6]},{"t":[5,8,14],"bad":[3,4]},{"t":[5,9,11],"bad":[2,5]},{"t":[5,10,12],"bad":[2,5]},{"t":[6,7,14],"bad":[3,4]},{"t":[6,8,13],"bad":[2,5]},{"t":[6,9,12],"bad":[2,5]},{"t":[6,10,11],"bad":[2,5]}],"guards":[[4,6,0],[6,8,0],[0,3,0],[1,2,0],[2,3,0],[3,5,1],[5,7,1]]}];
const run = function run(inputs){
 let checks=0, scans=0, refWords=0, physicalLifts=0, sourceChecks=0;
 const ck=(v)=>{checks++;if(!v)throw Error("check "+checks)},bit=(x,i)=>(x>>i)&1,xor=a=>a.reduce((s,v)=>s^v,0),good=(O,x)=>O.every(o=>{sourceChecks++;return !o.bad.includes(o.t.reduce((s,v,j)=>s|(bit(x,v)<<j),0))});
 function native(){
  let V=[],W=[],P=[];
  function v(type,vals){let i=V.length;V.push(type);let a=[];for(let j=0;j<4;j++){a.push(P.length);P.push(vals?vals[j]:null)}return a}
  function w(a,b,s=0){ck(a!==b);W.push([a,b,s]);if(P[a]!==null&&P[b]!==null)ck((P[a]^P[b])===s)}
  function k4(bits){let a=Array.from({length:4},()=>v("B"));let es=[];for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)es.push([i,j]);let deg=[1,1,1,1],chosen=null;
   if(bits){ck(xor(bits)===0);for(let m=0;m<64;m++){let d=bits.slice();es.forEach(([i,j],k)=>{d[i]+=bit(m,k);d[j]+=bit(m,k)});if(d.every(z=>z===2)){chosen=m;break}}ck(chosen!==null);a.forEach((q,i)=>P[q[0]]=bits[i])}
   es.forEach(([i,j],k)=>{let p=a[i][deg[i]++],q=a[j][deg[j]++];if(bits)P[p]=P[q]=bit(chosen,k);w(p,q)});return a.map(q=>q[0])
  }
  function k5(bits){let a=Array.from({length:5},()=>v("B")),deg=[1,1,0,0,0];if(bits){ck(bits[0]===bits[1]);P[a[0][0]]=bits[0];P[a[1][0]]=bits[1]}let cyc=new Set(["0,2","1,2","1,3","3,4","0,4"]);
   for(let i=0;i<5;i++)for(let j=i+1;j<5;j++){if(i===0&&j===1)continue;let p=a[i][deg[i]++],q=a[j][deg[j]++];if(bits)P[p]=P[q]=Number(cyc.has(i+","+j))^bits[0];w(p,q)}return [a[0][0],a[1][0]]
  }
  function block(d,bits){ck(d>=2&&d%2===0);if(bits)ck(bits.length===d&&xor(bits)===0);if(d===2)return k5(bits);if(d===4)return k4(bits);
   let h=bits?xor(bits.slice(0,3)):0,a=k4(bits?[...bits.slice(0,3),h]:null),b=block(d-2,bits?[h,...bits.slice(3)]:null);w(a[3],b[0]);return [...a.slice(0,3),...b.slice(1)]
  }
  function finish(lift){let old=W;W=[];let oldV=V.length;
   // Every old wire is replaced using a private K5-pq B4 wire gadget, including loops.
   for(let [a,b,s] of old){let q=k5(lift?[P[b],P[b]]:null);w(a,q[0],s);w(q[1],b)}
   let seen=new Set(),ports=new Set();for(let [a,b,s] of W){let i=Math.floor(a/4),j=Math.floor(b/4),key=[Math.min(i,j),Math.max(i,j)].join(",");ck(i!==j&&!seen.has(key));seen.add(key);ck(!ports.has(a)&&!ports.has(b));ports.add(a);ports.add(b);if(lift)ck((P[a]^P[b])===s)}
   ck(ports.size===P.length);if(lift){physicalLifts++;for(let i=0;i<V.length;i++){let b=P.slice(4*i,4*i+4);ck(b.every(x=>x===0||x===1));ck(V[i]==="B"?b.reduce((a,v)=>a+v,0)===2:b.every(x=>x===b[0]))}}
   return {V:V.length,E:V.filter(x=>x==="E").length,B:V.filter(x=>x==="B").length,W:W.length,preWireVertices:oldV,preWires:old.length}
  }
  return {v,w,block,finish,P}
 }
 function compile(n,O,x=null){
  let g=native(),occ=Array.from({length:n},()=>[]),col=[],charge=0,has=x!==null;
  for(let o of O){let f=o.bad[0],s=[0,1,2].map(j=>bit(f,j)),a=has?o.t.map((v,j)=>bit(x,v)^s[j]):null;
   if(has)ck(a[0]+a[1]+a[2]===1||a[0]+a[1]+a[2]===2);
   let p=g.v("B",has?[...a,2-a.reduce((u,v)=>u+v,0)]:null);col.push(p[3]);charge^=xor(s);
   o.t.forEach((v,j)=>occ[v].push([p[j],s[j]]));
  }
  let baseline=0,expected=0;for(let i=0;i<n;i++){let L=occ[i],t=L.length;if(!t)continue;baseline+=t-1;expected+=Math.ceil(t/2)-1;
   if(t===1){col.push(L[0][0]);charge^=L[0][1];continue}
   if(t===2){g.w(L[0][0],L[1][0],L[0][1]^L[1][1]);continue}
   let k=Math.ceil(t/2)-1,A=Array.from({length:k},()=>g.v("E",has?Array(4).fill(bit(x,i)):null));for(let j=0;j<k-1;j++)g.w(A[j][3],A[j+1][0]);
   let free=A.flatMap((p,j)=>p.filter((_,u)=>!(u===0&&j>0)&&!(u===3&&j<k-1)));ck(free.length===t+(t%2));for(let j=0;j<t;j++)g.w(L[j][0],free[j],L[j][1]);if(t%2)col.push(free[t])
  }
  ck(col.length%2===0);if(col.length){let b=has?col.map(p=>g.P[p]):null;if(b){ck(xor(b)===charge);b[0]^=charge}let q=g.block(col.length,b);col.forEach((p,j)=>g.w(p,q[j],j===0?charge:0))}
  let z=g.finish(has);ck(z.E===expected);if(has){for(let o of O)ck(good([o],x))}
  return {...z,baselineTags:baseline,collectorPorts:col.length}
 }
 function close(n,O,G){let p=Array.from({length:n},(_,i)=>i),d=Array(n).fill(0);function find(i){if(p[i]===i)return [i,0];let [r,s]=find(p[i]);return [r,s^d[i]]}
  function join(a,b,c){let [r,s]=find(a),[q,t]=find(b);if(r===q)return (s^t)===c?0:-1;p[r]=q;d[r]=s^t^c;return 1}
  for(let [a,b,c] of G)if(join(a,b,c)<0)return {no:true};
  while(true){scans++;let R=[],change=false;for(let o of O){let f=o.bad[0],L=o.t.map((v,j)=>{let [r,s]=find(v);return [r,s^bit(f,j)]});let opp=false;for(let i=0;i<3;i++)for(let j=i+1;j<3;j++)if(L[i][0]===L[j][0]&&L[i][1]!==L[j][1])opp=true;if(opp)continue;
    let ij=null;for(let i=0;i<3;i++)for(let j=i+1;j<3;j++)if(L[i][0]===L[j][0])ij=[i,j];if(ij){let [i,j]=ij,k=3-i-j,a=L[i],b=L[k],z=join(a[0],b[0],1^a[1]^b[1]);if(z<0)return {no:true};ck(z===1);change=true;break}
    let bad=L.reduce((s,v,j)=>s|(v[1]<<j),0);R.push({t:L.map(v=>v[0]),bad:[bad,bad^7]})
   }if(!change)return {R,find}}
 }
 let jobs=[];for(let src of inputs){for(let [label,O,G] of [["root",src.root,[]],["neighbor",src.sat,[]],...(src.guards.length?[["first-cut",src.root,src.guards.slice(0,1)],["all-cuts",src.root,src.guards]]:[])]){
   let cl=close(src.n,O,G),count=0,words=[];for(let x=0;x<2**src.n;x++){refWords++;if(!G.every(([a,b,c])=>(bit(x,a)^bit(x,b))===c))continue;let valid=good(O,x);if(cl.no)ck(!valid);else{let q=0;for(let i=0;i<src.n;i++){let [r,s]=cl.find(i);ck((bit(x,r)^s)===bit(x,i));q|=bit(x,r)<<r}ck(good(cl.R,q)===valid);if(valid)words.push(q)}if(valid)count++}
   let geo=cl.no?null:compile(src.n,cl.R);for(let x of words){let g=compile(src.n,cl.R,x);ck(g.E===geo.E&&g.V===geo.V)}
   jobs.push({n:src.n,label,count,closure:cl.no?"UNSAT":cl.R.length?"OPEN":"SAT",remaining:cl.no?0:cl.R.length,geo})
 }}
 // Independent source geometry controls: K4 and Petersen, all zero charges and a single changed charge.
 let parityJobs=[];let graphs=[{n:4,edges:Array.from({length:4},(_,i)=>Array.from({length:4-i-1},(_,j)=>[i,i+j+1])).flat()},{n:10,edges:[...Array.from({length:5},(_,i)=>[i,(i+1)%5]),...Array.from({length:5},(_,i)=>[i,i+5]),...Array.from({length:5},(_,i)=>[i+5,5+(i+2)%5])]}];
 for(let {n,edges} of graphs){let inc=Array.from({length:n},()=>[]);edges.forEach(([u,v],i)=>{inc[u].push(i);inc[v].push(i)});ck(inc.every(a=>a.length===3));
  for(let b of [Array(n).fill(0),Array.from({length:n},(_,i)=>i===0?1:0),Array.from({length:n},(_,i)=>i<2?1:0)]){
   // Exact forest elimination, choosing non-tree variables zero.
   let parent=Array(n).fill(-1),edge=Array(n).fill(-1),order=[0],val=Array(edges.length).fill(0),r=b.slice();parent[0]=0;for(let i=0;i<order.length;i++)for(let e of inc[order[i]]){let [a,c]=edges[e],u=a^c^order[i];if(parent[u]===-1){parent[u]=order[i];edge[u]=e;order.push(u)}}
   ck(order.length===n);for(let v of order.slice(1).reverse()){val[edge[v]]=r[v];r[parent[v]]^=r[v]}let sat=r[0]===0;ck(sat===(xor(b)===0));
   let g=native(),ports=[],offset=[];for(let v=0;v<n;v++){let off=[b[v],0,0,0,0,0];offset.push(off);let bits=sat?inc[v].flatMap(e=>[0,val[e]]).map((z,i)=>z^off[i]):null;ports.push(g.block(6,bits))}
   edges.forEach(([u,v],e)=>{let i=2*inc[u].indexOf(e),j=2*inc[v].indexOf(e);for(let k=0;k<2;k++)g.w(ports[u][i+k],ports[v][j+k],offset[u][i+k]^offset[v][j+k])});
   let geo=g.finish(sat);ck(geo.E===0);
   // DA23 source reverse map: phase zero, four forbidden triples per cubic owner.
   if(sat)for(let v=0;v<n;v++){let u=inc[v].map(e=>val[e]);ck(xor(u)===b[v]);for(let f=0;f<8;f++)if(xor([bit(f,0),bit(f,1),bit(f,2)])!==b[v]){let l=u.map((z,i)=>z^bit(f,i)),y=(1-l[0])*(1-l[1]);ck(new Set([l[0],l[1],y]).size===2);ck(new Set([y^1,l[2],0]).size===2)}}
   parityJobs.push({n,charge:xor(b),charges:b,label:sat?"SAT":"UNSAT",geo})
  }
 }
 return {checks,scans,refWords,physicalLifts,sourceChecks,jobs,parityJobs}
};
console.log(JSON.stringify(run(inputs),null,2));
