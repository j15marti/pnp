"use strict";
function check(x,msg){if(!x)throw Error(msg)}
function audit(h,d){
 const n=2*d*h,s=n,t=n+1, v=(i,j)=>2*d*((i+h)%h)+j, edge=(a,b)=>a<b?a+":"+b:b+":"+a;
 const A=new Set(), B=new Set(), E=new Map(), owner=new Map(), inc=Array.from({length:n+2},()=>[]);
 function add(u,w,a,b,k){let e=edge(u,w);check(!E.has(e),"duplicate");E.set(e,[u,w]);inc[u].push(e);inc[w].push(e);if(a){A.add(e);owner.set(e,k)}if(b)B.add(e)}
 for(let i=0;i<h;i++)for(let j=0;j<2*d;j++)add(v(i,j),v(i,(j+1)%(2*d)),1,j%2===0,i);
 for(let i=0;i<h;i++)for(let j=0;j<d;j++){let u=v(i,d+j),w=v(i+1,j);if(i===h-1&&j<2){for(let z of [u,w])add(z,z%2===0?s:t,0,1)}else add(u,w,0,1)}
 add(s,t,0,0);check(E.size===3*(n+2)/2,"edge count");
 check(inc.every(a=>a.length===3&&a.filter(e=>A.has(e)).length%2===0&&a.filter(e=>B.has(e)).length===2),"degree");
 check([...E.keys()].filter(e=>!A.has(e)&&!B.has(e)).length===1,"zero");
 let side=z=>z===s?1:z===t?0:z%2;
 check([...E.values()].every(([u,w])=>side(u)!==side(w)),"bipartite");
 // Explicit path decomposition of mixed graph. Ladders i contain right rail of cycle i and left rail of cycle i+1.
 const rail=(i,j)=>[v(i,d+j),v(i+1,j)], ends=i=>[...rail(i,0),...rail(i,d-1)];
 const bags=[], phase=i=>"p"+((i+h)%h), row=i=>"r"+i;
 function bag(vertices,ps,extra=[]){const set=new Set([phase(0),"global",...ps,...extra]);for(const u of new Set([...vertices,...ends(0),s,t]))for(const e of inc[u])set.add(e);bags.push(set)}
 for(let i=0;i<h;i++){
  for(let j=0;j<d-1;j++)bag([...ends(i),...rail(i,j),...rail(i,j+1)],[phase(i),phase(i+1)],j===0&&i%2===0?[row(i/2)]:[]);
  if(i<h-1)bag([...ends(i),...ends(i+1)],[phase(i),phase(i+1),phase(i+2)]);
 }
 let vars=[...E.keys(),...Array.from({length:h},(_,i)=>phase(i)),...Array.from({length:h/2},(_,i)=>row(i)),"global"];
 let occurrence=new Map(vars.map(x=>[x,[]]));bags.forEach((b,i)=>{for(let x of b)occurrence.get(x).push(i)});
 for(let [x,p] of occurrence)check(p.length&&p[p.length-1]-p[0]+1===p.length,"noninterval "+x);
 let contains=xs=>bags.some(b=>xs.every(x=>b.has(x)));
 check(inc.every(xs=>contains(xs)),"vertex clique");
 for(let [e,i] of owner)check(contains([e,phase(i)]),"phase edge");
 for(let i=0;i<h;i+=2){check(contains([row(i/2),phase(i)])&&contains([row(i/2),phase(i+1)])&&contains(["global",phase(i)]),"guard edge")}
 // Independently generate alternating companion on selected factors for sample legal guards.
 let witnesses=0;
 for(let j=0;j<Math.min(16,2**(h/2-1));j++){
  let bits=Array(h).fill(0),p=0;for(let k=0;k<h/2-1;k++){bits[2*k]=bits[2*k+1]=(j>>k)&1;p^=bits[2*k]}
  bits[h-2]=bits[h-1]=p^1;
  check(bits.filter((_,i)=>i%2===0).reduce((a,b)=>a^b,0)===1,"guard");
  let F=new Set([...B].filter(e=>!A.has(e)||!bits[owner.get(e)]));for(let e of A)if(bits[owner.get(e)]&&!B.has(e))F.add(e);
  let col=new Map([...E.keys()].filter(e=>!F.has(e)).map(e=>[e,2]));
  for(let e of F){if(col.has(e))continue;let cur=E.get(e)[0],first=e,c=1;
   while(!col.has(e)){col.set(e,c);let [u,w]=E.get(e);cur=cur===u?w:u;e=inc[cur].find(z=>F.has(z)&&z!==e);check(e!==undefined,"factor");c=4-c}
   check(e===first&&c===1,"odd cycle");
  }
  check(inc.every(es=>new Set(es.map(e=>col.get(e))).size===3),"bad color");witnesses++;
 }
 // all nonempty proper switch cuts for small h
 let min=Infinity,cutChecks=0;
 if(h<=12)for(let m=1;m<(1<<h)-1;m++){
  let cut=0;for(let i=0;i<h;i++)if(((m>>i)^(m>>((i+1)%h)))&1)cut+=d;
  if((m&1)&&(m&(1<<(h-1))))cut+=4;
  check(cut>=2*d,"cut");min=Math.min(min,cut);cutChecks++;
 }
 return {h,d,n:n+2,bagWidth:Math.max(...bags.map(b=>b.size))-1,bags:bags.length,rank:h/2+1,phaseWords:String(2n**BigInt(h/2-1)),witnesses,cutChecks,min:cutChecks?min:null}
}
function coreAudit(){
 const E=[[0,2],[0,6],[0,9],[1,3],[1,7],[1,10],[2,10],[2,11],[3,8],[3,11],[4,5],[4,9],[4,11],[5,6],[5,10],[6,7],[7,8],[8,9]],start=[110469,185822],full=(1<<18)-1,prot=full^(1<<5);
 const I=Array.from({length:12},(_,v)=>E.map(([u,w],i)=>u===v||w===v?1<<i:0).reduce((a,b)=>a|b,0));
 const F=[];for(let x=0;x<=full;x++){if(I.every(k=>{let z=x&k,p=0;while(z){z&=z-1;p^=1}return !p}))F.push(x)}
 let pairs=[];for(let a of F)for(let b of F)if(((a|b)&prot)===prot)pairs.push([a,b]);
 let seen=new Set([start.join(",")]),queue=[start];for(let [a,b] of queue){let D=new Set([a,b,a^b]);for(let [c,d] of pairs){let key=[c,d].join(",");if(!seen.has(key)&&[c,d,c^d].some(z=>D.has(z))){seen.add(key);queue.push([c,d])}}}
 check(F.length===128&&pairs.length===30&&queue.length===18&&queue.every(([a,b])=>(a|b)!==full),"FP04 core");
 return {flows:F.length,protected:pairs.length,reachable:queue.length,properReachable:0}
}
function main(){return {families:[[4,3],[6,5],[8,9],[12,11],[20,19],[40,39]].map(([h,d])=>audit(h,d)),core:coreAudit()}}
console.log(JSON.stringify(main(),null,2));