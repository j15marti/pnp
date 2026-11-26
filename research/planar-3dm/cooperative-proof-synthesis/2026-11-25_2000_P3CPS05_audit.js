function audit(){
 const B=[[0,0,0],[1,1,1],[0,0,1],[1,1,0],[0,1,0],[1,0,1]], F=[[0,0,0],[1,1,0],[0,0,1],[1,1,1]];
 let checks=0; const assert=(x,msg)=>{checks++;if(!x)throw Error(msg)};
 const bit=(x,i)=>(x>>i)&1;
 const seq=n=>Array.from({length:n},(_,i)=>i);
 const source=(T,n)=>({n,T,V:seq(T.length+3*n),E:T.flatMap((t,i)=>t.map((v,c)=>({id:3*i+c,t:i,e:T.length+c*n+v,c,u:i,v:T.length+c*n+v})))});
 const verify=(T,n,sel)=>sel.length===n && seq(3).every(c=>new Set(sel.map(i=>T[i][c])).size===n);
 function allcovers(T,n){let out=[];function rec(i,chosen,used){if(i===T.length){if(verify(T,n,chosen))out.push(chosen.slice());return}rec(i+1,chosen,used);if(T[i].every((v,c)=>!used[c].has(v))){T[i].forEach((v,c)=>used[c].add(v));chosen.push(i);rec(i+1,chosen,used);chosen.pop();T[i].forEach((v,c)=>used[c].delete(v))}}rec(0,[],[new Set(),new Set(),new Set()]);return out}
 function envelope(S,g,ids){const set=new Set(S),a=seq(3).map(c=>seq(g.n).filter(v=>set.has(g.T.length+c*g.n+v)).length);return seq(1<<ids.length).filter(mask=>{let z=a.slice();ids.forEach((id,i)=>{const e=g.E[id];z[e.c]+=(set.has(e.t)?1:-1)*bit(mask,i)});return z[0]===z[1]&&z[1]===z[2]})}
 function pinRepresentable(rows,sub,k){return rows.filter(r=>seq(k).every(i=>!sub.every(s=>bit(s,i)===bit(sub[0],i))||bit(r,i)===bit(sub[0],i))).join(",")===sub.join(",")}
 // All sign/color and count-offset combinations, normalized to finite offsets (only differences <=3 matter).
 let patterns=0,subsets=0;
 for(let k=1;k<=3;k++)for(let cc=0;cc<3**k;cc++)for(let types=0;types<1<<k;types++)for(let x=-3;x<=3;x++)for(let y=-3;y<=3;y++){
  let c=seq(k).map(i=>Math.floor(cc/3**i)%3),a=[0,x,y];
  let rows=seq(1<<k).filter(r=>{let v=a.slice();c.forEach((d,i)=>v[d]+=(bit(types,i)?1:-1)*bit(r,i));return v[0]===v[1]&&v[1]===v[2]});
  assert(rows.length<=3,"too many rows");patterns++;
  for(let s=1;s<1<<rows.length;s++){let sub=rows.filter((_,i)=>bit(s,i));assert(pinRepresentable(rows,sub,k),"not pin representable");subsets++}
 }
 // T-port exact-one gadget obtained by deleting element (color 2, label 0) from B.
 let ports=B.map((t,i)=>t[2]===0?i:-1).filter(i=>i>=0),rows=[];
 for(let s=0;s<1<<B.length;s++){
  if(seq(3).every(c=>seq(2).every(v=>(c===2&&v===0)||B.reduce((a,t,i)=>a+(t[c]===v?bit(s,i):0),0)===1)))rows.push(ports.reduce((a,i,j)=>a+(bit(s,i)<<j),0));
 }
 assert([...new Set(rows)].sort().join(",")==="1,2,4","gadget signature");
 // Full exact source closure, including indexed pair projection support.
 function closure(g){let p=Array(g.T.length).fill(-1),work=0;const inc=seq(3*g.n).map(i=>g.E.filter(e=>e.e===g.T.length+i).map(e=>e.t));
  function pin(i,b){if(p[i]!==-1&&p[i]!==b)return false;p[i]=b;return true}
  function match(a,b,force=-1){work++;let usedA=-1,usedB=-1;if(force>=0){if(p[force]===0)return false;usedA=g.T[force][a];usedB=g.T[force][b]}
   let adj=seq(g.n).map(()=>[]);g.T.forEach((t,i)=>{if(p[i]!==0&&t[a]!==usedA&&t[b]!==usedB)adj[t[a]].push(t[b])});let owner=Array(g.n).fill(-1);
   function aug(x,seen){for(let y of adj[x])if(!seen.has(y)){seen.add(y);if(owner[y]===-1||aug(owner[y],seen)){owner[y]=x;return true}}return false}
   return seq(g.n).every(x=>x===usedA||aug(x,new Set()))
  }
  while(true){let before=p.join(",");
   for(let ids of inc){let live=ids.filter(i=>p[i]!==0),yes=ids.filter(i=>p[i]===1);if(!live.length||yes.length>1)return {no:true,p,work};if(yes.length===1){for(let i of live)if(i!==yes[0]&&!pin(i,0))return {no:true,p,work}}else if(live.length===1&&!pin(live[0],1))return {no:true,p,work}}
   for(let [a,b] of [[0,1],[0,2],[1,2]]){if(!match(a,b))return {no:true,p,work};for(let i=0;i<p.length;i++)if(p[i]!==0&&!match(a,b,i)){if(!pin(i,0))return {no:true,p,work}}}
   if(before===p.join(","))return {no:false,p,work}
  }
 }
 function expand(T,n,i){let old=T[i],next=[n+1,n+1,n+1],newT=T.filter((_,j)=>j!==i).concat([[n,n,n]]);for(let c=0;c<3;c++){let a=[n,n,n],b=old.slice();for(let d=0;d<3;d++)if(d!==c)a[d]=b[d]=next[d]++;newT.push(a,b)}return [newT,n+3]}
 function splitDP(g,p){
  let atoms=[{V:g.V.slice(),E:g.E.map(e=>[e.u,e.v,e.id])}],links=[],next=g.V.length,probes=0;
  function cut(A){let ids=seq(A.E.length);function trycut(rem){probes++;let skip=new Set(rem),adj=new Map(A.V.map(v=>[v,[]]));A.E.forEach(([u,v],i)=>{if(!skip.has(i)){adj.get(u).push(v);adj.get(v).push(u)}});let left=new Set(),stack=[A.V[0]];while(stack.length){let u=stack.pop();if(left.has(u))continue;left.add(u);for(let v of adj.get(u))if(!left.has(v))stack.push(v)}
    if(left.size<2||A.V.length-left.size<2)return null;
    let crossing=ids.filter(i=>left.has(A.E[i][0])!==left.has(A.E[i][1]));if(crossing.length!==rem.length||!crossing.every(i=>skip.has(i)))return null;
    let right=A.V.filter(v=>!left.has(v)),seen=new Set(),st=[right[0]];while(st.length){let u=st.pop();if(seen.has(u))continue;seen.add(u);for(let v of adj.get(u))if(!seen.has(v))st.push(v)}if(seen.size!==right.length)return null;
    return {left,right,ids:crossing}
   }
   for(let k=1;k<=3;k++){let found=null;function go(start,arr){if(found)return;if(arr.length===k){found=trycut(arr);return}for(let i=start;i<=ids.length-(k-arr.length)&&!found;i++)go(i+1,arr.concat(i))}go(0,[]);if(found)return found}return null
  }
  let done=[];while(atoms.length){let A=atoms.pop(),C=cut(A);if(!C){done.push(A);continue}let ma=next++,mb=next++,ae=[],be=[],cross=[];for(let [u,v,id] of A.E){let U=C.left.has(u),V=C.left.has(v);if(U&&V)ae.push([u,v,id]);else if(!U&&!V)be.push([u,v,id]);else{ae.push([U?u:v,ma,id]);be.push([U?v:u,mb,id]);cross.push(id)}}links.push({ma,mb,ids:cross.sort((a,b)=>a-b)});atoms.push({V:[...C.left,ma],E:ae},{V:[...C.right,mb],E:be})}
  let owner=new Map();done.forEach((A,i)=>A.V.forEach(v=>owner.set(v,i)));let adj=done.map(()=>[]);links.forEach(L=>{let a=owner.get(L.ma),b=owner.get(L.mb);adj[a].push({to:b,...L});adj[b].push({to:a,...L})});assert(links.length===done.length-1,"not tree");
  let maxrows=0,maxedges=0,enumerated=0,joins=0,foundCuts=[0,0,0,0];links.forEach(l=>foundCuts[l.ids.length]++);
  function dfs(i,parent,up){let A=done[i],children=adj[i].filter(l=>l.to!==parent).map(l=>({l,res:dfs(l.to,i,l)})),vertices=A.V.filter(v=>v<g.V.length).concat(...children.map(c=>c.res.vertices));let ids=up?up.ids:[],candidates=up?envelope(vertices,g,ids):[0];if(up){let set=new Set(vertices),actual=g.E.filter(e=>set.has(e.t)!==set.has(e.e)).map(e=>e.id).sort((a,b)=>a-b);assert(actual.join(",")===ids.join(","),"cut expansion mismatch")}
   let table=new Map(),index=new Map(A.E.map((e,j)=>[e[2],j]));maxedges=Math.max(maxedges,A.E.length);if(A.E.length>20)throw Error("audit atom cap");
   let real=A.V.filter(v=>v<g.V.length).map(v=>({v,es:A.E.map((e,j)=>e[0]===v||e[1]===v?j:-1).filter(j=>j>=0)}));
   function maskOf(row,ids){return ids.reduce((a,id,j)=>a+(bit(row,index.get(id))<<j),0)}
   for(let row=0;row<1<<A.E.length;row++){enumerated++;
    if(!real.every(({v,es})=>{let val=es.map(j=>bit(row,j));return v<g.T.length?val.every(b=>b===val[0])&&(p[v]===-1||p[v]===val[0]):val.reduce((a,b)=>a+b,0)===1}))continue;
    let r=maskOf(row,ids);if(!candidates.includes(r)||table.has(r))continue;
    let childRows=children.map(c=>c.res.table.get(maskOf(row,c.l.ids)));joins+=children.length;if(childRows.some(x=>!x))continue;
    let witness=new Map(A.E.map((e,j)=>[e[2],bit(row,j)]));for(let child of childRows)for(let [id,b] of child){assert(!witness.has(id)||witness.get(id)===b,"inconsistent lift");witness.set(id,b)}table.set(r,witness)
   }
   maxrows=Math.max(maxrows,table.size);return {vertices,table}
  }
  let root=dfs(0,-1,null),w=root.table.get(0),sel=w?seq(g.T.length).filter(i=>w.get(3*i)===1):[];
  if(w)assert(verify(g.T,g.n,sel),"invalid witness");
  return {yes:!!w,atoms:done.length,foundCuts,maxrows,maxedges,enumerated,joins,probes,selected:sel.length}
 }
 let tests=[],T=B,n=2;
 for(let k=0;k<=32;k++){
  if([0,1,2,4,8,16,32].includes(k)){
   for(let del of [false,true]){let U=del?T.filter((_,i)=>i!==T.length-1):T;let g=source(U,n),c=closure(g);let d=c.no?null:splitDP(g,c.p);
    // The deletion is SAT: choose the base cover avoiding the expanded triple. Two additional deletions below create NO.
    assert(!c.no&&d.yes,"SAT chain/deletion lost");tests.push({k,triples:U.length,kind:del?"one deletion SAT":"SAT",pins:c.p.filter(x=>x!==-1).length,matching:c.work,...d})
   }
   let U=T.filter(t=>t[0]!==0),g=source(U,n),c=closure(g);assert(c.no,"isolated-element NO missed");tests.push({k,triples:U.length,kind:"isolated X UNSAT",matching:c.work});
  }
  [T,n]=expand(T,n,T.length-1)
 }
 // Genuine 4-port counterexample.
 let g=source(F,2),S=[0,1,F.length+2*2+0],ids=g.E.filter(e=>S.includes(e.t)!==S.includes(e.e)).map(e=>e.id).sort((a,b)=>a-b);
 let env=envelope(S,g,ids),sol=allcovers(F,2),actual=[...new Set(sol.map(s=>ids.reduce((a,id,j)=>a+(s.includes(g.E[id].t)?1<<j:0),0)))].sort((a,b)=>a-b);
 assert(env.length===4&&actual.length===2&&!pinRepresentable(env,actual,4),"4-port obstruction missing");
 assert(closure(g).p.every(b=>b===-1),"4-port example unexpectedly pinned");
 return {checks,patterns,subsets,gadgetRows:rows,tests,fourPort:{ids,env,actual,solutions:sol}}
}
console.log(JSON.stringify(audit(),null,2));
