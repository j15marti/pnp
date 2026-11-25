const run = function(){
 const assert=(q,m)=>{if(!q)throw Error(m)};
 const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]].map(([a,b,c])=>({rows:[(1<<a)^(1<<b),(1<<a)^(1<<c)],rhs:[0,0]}));
 const product=(base,n,r)=>{let p=[{rows:[],rhs:[]}];for(let j=0;j<r;j++)p=p.flatMap(x=>base.map(y=>({rows:x.rows.concat(y.rows.map(a=>a<<(j*n))),rhs:x.rhs.concat(y.rhs)})));return p};
 function factor(p,d){
   let parent=Array.from({length:d},(_,i)=>i);
   const find=i=>{while(parent[i]!==i)i=parent[i];return i};
   for(const packet of p)for(let a of packet.rows){let s=[];for(let i=0;i<d;i++)if(a&(1<<i))s.push(i);for(let i=1;i<s.length;i++)parent[find(s[i])]=find(s[0]);}
   let blocks=Array.from(new Set(parent.map((_,i)=>find(i)))).map(k=>parent.map((_,i)=>i).filter(i=>find(i)===k));
   const canonical=(q)=>{let b=Array(d).fill(0),rhs=Array(d).fill(0);for(let i=0;i<q.rows.length;i++){let a=q.rows[i],v=q.rhs[i];for(let j=d-1;j>=0;j--)if((a&(1<<j))&&b[j]){a^=b[j];v^=rhs[j]}if(!a){if(v)throw Error("empty packet");continue}let j=31-Math.clz32(a);b[j]=a;rhs[j]=v;for(let k=0;k<d;k++)if(k!==j&&(b[k]&(1<<j))){b[k]^=a;rhs[k]^=v}}return b.flatMap((a,j)=>a?[[a,rhs[j]]]:[])};
   const tuples=new Set(),tables=blocks.map(()=>new Set());let mass=0;
   for(let q of p){let t=blocks.map((s,j)=>{let mask=s.reduce((a,i)=>a|(1<<i),0),pairs=canonical(q).filter(([a])=>a&mask);assert(pairs.every(([a])=>(a&mask)===a),"block");let key=JSON.stringify(pairs);tables[j].add(key);return key});const key=JSON.stringify(t);if(!tuples.has(key)){tuples.add(key);mass+=canonical(q).length}}
   const cap=tables.reduce((a,t)=>a*BigInt(t.size),1n);
   const childMass=tables.map(t=>Array.from(t).reduce((a,k)=>a+JSON.parse(k).length,0));
   return {blocks:blocks.map(b=>b.length),registry:tuples.size,productCapacity:String(cap),exact:cap===BigInt(tuples.size),parentMass:mass,childMass,childCredit:childMass.reduce((a,m)=>a+1+m,0)};
 }
 const root=product(fano,7,2),sat=product(fano.slice(1),7,2);
 const result={root:factor(root,14),sat:factor(sat,14),onePacketDeletion:factor(root.slice(1),14)};
 assert(result.root.exact&&result.sat.exact&&!result.onePacketDeletion.exact,"factoring");
 assert(result.root.childCredit<=result.root.parentMass&&result.sat.childCredit<=result.sat.parentMass,"credits");
 return result;
};
console.log(JSON.stringify(run(),null,2));
