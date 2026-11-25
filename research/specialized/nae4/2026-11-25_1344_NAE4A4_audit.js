function audit(){
 let checks=0; const ck=(x,msg)=>{checks++;if(!x)throw Error(msg)};
 const nae=(x,t)=>x[t[0]]!==x[t[1]]||x[t[1]]!==x[t[2]];
 const plane=[];for(let q=0;q<3;q++)for(let b=0;b<3;b++)plane.push({p:q,t:[0,1,2].map(i=>3*i+(q*i+b)%3)});for(let i=0;i<3;i++)plane.push({p:3,t:[3*i,3*i+1,3*i+2]});
 const G=plane.filter((c,i)=>i!==0&&i!==1),gw=[0,1,0,0,1,0,0,1,1];
 let gadgetModels=0;
 for(let z=0;z<512;z++){let x=Array.from({length:9},(_,i)=>(z>>i)&1);if(G.every(c=>nae(x,c.t))){gadgetModels++;ck(x[0]===x[3]&&x[3]===x[6]&&x[1]===x[4]&&x[4]===x[7]&&x[0]!==x[1],"gadget projection")}}
 ck(G.every(c=>nae(gw,c.t)),"gadget witness");
 function compile(n,src){
   const C=[], occ=Array.from({length:2*n+3},()=>[]), wires=[], slots=[], fixed=[];
   let size=0;const alloc=k=>{let a=size;size+=k;return a},add=(p,t,type)=>{C.push({p,t,type});return C.length-1};
   function external(lits){let t=lits.map(([v,s])=>{let id=alloc(1);occ[v].push({id,s});slots.push({id,v,s});return id});add(0,t,"external")}
   external([0,1,2].map(j=>[2*n+j,0]));
   for(let i=0;i<n;i++)for(let j=0;j<3;j++)external([[2*n+j,1],[2*i,0],[2*i+1,0]]);
   for(const [a,b,c] of src)external([[2*a+1,1],[2*b,0],[2*c,0]]);
   function wire(a,b,p){let h=alloc(9);wires.push({a,b,h});for(const o of G)add((o.p+p)%4,o.t.map(v=>v+h),"wire");add(p,[a,h,h+3],"wire");add(p,[b,h+1,h+4],"wire")}
   const mid=[];
   for(const list of occ){let p=1;for(let j=1;j<list.length;j++){const a=list[j-1],b=list[j];if(a.s!==b.s){wire(a.id,b.id,p);p=3-p}else{let v=alloc(1);mid.push({id:v,from:a.id});wire(a.id,v,p);p=3-p;wire(v,b.id,p);p=3-p}}}
   while(size%3)fixed.push([alloc(1),0]);
   const old=size, seen=Array.from({length:4},()=>new Uint8Array(old));
   for(const c of C)for(const v of c.t){ck(!seen[c.p][v],"partial overlap");seen[c.p][v]=1}
   function fill(p,ids){
     const starts=[alloc(21),alloc(21)], special=[];
     for(let side=0;side<2;side++){let h=starts[side];for(let i=0;i<21;i++)fixed.push([h+i,(i>=7&&i<14?1:0)^side]);
       for(let q=0;q<4;q++)for(let k=0;k<7;k++){let t=[h+k,h+7+(k+q)%7,h+14+(k+2*q)%7];if(q===p&&k===0)special.push(t);else add(q,t,"filler")}}
     for(let j=0;j<3;j++)add(p,[ids[j],special[0][j],special[1][j]],"attachment")
   }
   for(let p=0;p<4;p++){let missing=[];for(let v=0;v<old;v++)if(!seen[p][v])missing.push(v);ck(missing.length%3===0,"completion multiple");for(let j=0;j<missing.length;j+=3)fill(p,missing.slice(j,j+3))}
   function lift(base){let x=new Uint8Array(size);for(const {id,v,s} of slots)x[id]=base[v]^s;for(const {id,from} of mid)x[id]=1^x[from];for(const {a,b,h} of wires){ck(x[a]!==x[b],"wire terminals");for(let k=0;k<9;k++)x[h+k]=gw[k]^(1^x[a])}for(const [v,b] of fixed)x[v]=b;return x}
   let y=lift(new Uint8Array(2*n+3)),x=y.slice();x[0]^=1;
   const P=Array.from({length:4},()=>new Uint8Array(size)),pairs=new Set();
   for(const c of C){ck(new Set(c.t).size===3,"distinct vertices");for(let v of c.t){ck(!P[c.p][v],"perfect partition overlap");P[c.p][v]=1}for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){let a=c.t[i],b=c.t[j],k=Math.min(a,b)*size+Math.max(a,b);ck(!pairs.has(k),"linearity");pairs.add(k)}}
   for(const p of P)ck(p.every(b=>b===1),"perfect");
   ck(C.length===4*size/3,"owner count");
   let A=C.filter(c=>c.p===0||c.p===3), B=C.filter(c=>c.p===1||c.p===2);
   ck(A.every(c=>nae(x,c.t))&&B.every(c=>nae(y,c.t)),"side anchors");
   ck(C.filter(c=>!nae(y,c.t)).length===1&&!nae(y,C[0].t),"near anchor");
   function blocker(side,w){return side.filter(c=>c.t.includes(0)&&!nae(w,c.t.map(v=>v))).length}
   function countBlock(side,w){let z=w.slice();z[0]^=1;return side.filter(c=>!nae(z,c.t)).length}
   ck(countBlock(A,x)===1&&countBlock(B,y)===1,"exact blockers");
   let opposite=(t)=>[[t[0],t[1]],[t[0],t[2]],[t[1],t[2]]].filter(([a,b])=>y[a]!==y[b]);
   let E=B.map(c=>c.type==="attachment"?c.t.slice(1):opposite(c.t)[0]);
   function components(){
      const adj=Array.from({length:size},()=>[]);
      E.forEach(([a,b],i)=>{adj[a].push([b,i]);adj[b].push([a,i]);ck(y[a]!==y[b],"chart anchor")});
      const mark=new Int32Array(size).fill(-1),groups=[];
      for(let v=0;v<size;v++){ck(adj[v].length<=2,"degree");if(mark[v]!==-1)continue;let vertices=[v],ids=new Set(),k=groups.length;mark[v]=k;for(let j=0;j<vertices.length;j++)for(const [u,e] of adj[vertices[j]]){ids.add(e);if(mark[u]===-1){mark[u]=k;vertices.push(u)}}groups.push({vertices,ids:[...ids]})}
      return {mark,groups}
   }
   let opened=0, rounds=0, data;
   for(;;){data=components();const cycles=data.groups.filter(g=>g.vertices.length===g.ids.length);if(!cycles.length)break;rounds++;
      for(const g of cycles){const e=g.ids.find(i=>B[i].type!=="attachment");ck(e!==undefined,"cycle has flexible owner");let old=E[e],alt=opposite(B[e].t).find(([a,b])=>!old.includes(a)||!old.includes(b));ck(!!alt,"alternative pair");E[e]=alt;opened++}
   }
   ck(data.groups.length===size/3,"n/3 phases");
   // Paid chart-guarded closure: equality of flip bits on selected B edges;
   // if two actual A literals forced equal, force the third opposite.
   const parent=Int32Array.from({length:size},(_,i)=>i),par=new Uint8Array(size),rank=new Uint8Array(size);
   function find(v){if(parent[v]===v)return [v,0];const [r,p]=find(parent[v]);par[v]^=p;parent[v]=r;return [r,par[v]]}
   let joins=0, scans=0, contradiction=false;
   function join(a,b,d){let [ra,pa]=find(a),[rb,pb]=find(b);if(ra===rb){if((pa^pb)!==d)contradiction=true;return false}if(rank[ra]>rank[rb]){[ra,rb]=[rb,ra];[pa,pb]=[pb,pa]}parent[ra]=rb;par[ra]=pa^pb^d;if(rank[ra]===rank[rb])rank[rb]++;return true}
   for(const [a,b] of E)ck(join(a,b,1),"forest join");
   let changed=true;while(changed&&!contradiction){changed=false;for(const {t} of A){scans++;for(let i=0;i<3;i++){let a=t[i],b=t[(i+1)%3],c=t[(i+2)%3],u=find(a),v=find(b);if(u[0]===v[0]&&u[1]===v[1]){if(join(a,c,1)){changed=true;joins++}}}if(contradiction)break}}
   function verifySource(w,sel){let base=new Uint8Array(2*n+3);for(let i=0;i<n;i++){base[2*i]=w[i];base[2*i+1]=1^w[i]}for(let j=0;j<3;j++)base[2*n+j]=sel[j];let z=lift(base);ck(C.every(c=>nae(z,c.t)),"source lift all owners");ck(E.every(([a,b])=>z[a]!==z[b]),"lift chart");ck(!contradiction,"closure sound");for(let i=0;i<size;i++){const [r,p]=find(i);ck((z[i]^z[r])===p,"closure parity")};for(const {id,v,s} of slots)ck((z[id]^s)===base[v],"decode");for(const side of [A,B]){let q=[0,0];for(const c of side){let sum=c.t.reduce((s,v)=>s+z[v],0);ck(sum===1||sum===2,"quota");q[c.p===side[0].p?0:1]+=sum}ck(q[0]===q[1],"hub balance")}}
   // Both chart anchor and its global complement are valid B words; all original A words similarly.
   ck(B.every(c=>nae(y.map(b=>b^1),c.t)),"B complement");ck(A.every(c=>nae(x.map(b=>b^1),c.t)),"A complement");
   return {size,owners:C.length,phases:data.groups.length,opened,rounds,joins,scans,contradiction,verifySource};
 }
 const T=[];for(let p=0;p<4;p++)for(let k=0;k<7;k++)T.push([k,7+(k+p)%7,14+(k+2*p)%7]);
 const inputs=[{name:"genuine-plane",n:9,src:plane.map(c=>c.t)},{name:"plane-minus-one",n:9,src:plane.slice(1).map(c=>c.t)},{name:"plane-minus-two",n:9,src:G.map(c=>c.t)},{name:"one-triple",n:3,src:[[0,1,2]]},{name:"genuine-cyclic-21",n:21,src:T}];
 const results=[];
 for(const {name,n,src} of inputs){let witnesses=[],exhaustive=n<=9; if(exhaustive){for(let k=0;k<2**n;k++){let w=Array.from({length:n},(_,i)=>(k>>i)&1);if(src.every(t=>nae(w,t)))witnesses.push(w)}}else{let w=Array.from({length:n},(_,i)=>i>=7&&i<14?1:0);ck(src.every(t=>nae(w,t)),"known SAT");witnesses=[w,w.map(b=>b^1)]}
   const q=compile(n,src);let lifted=0;for(const w of witnesses)for(let k=1;k<7;k++){q.verifySource(w,[k&1,(k>>1)&1,(k>>2)&1]);lifted++}
   const {verifySource,...stats}=q;results.push({name,n,sourceOwners:src.length,exhaustive,sourceWitnesses:witnesses.length,lifted,...stats})
 }
 return {gadgetModels,checks,results};
}
console.log(JSON.stringify(audit(),null,2));
