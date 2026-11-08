function verify485(){
 const assert=(c,m)=>{if(!c)throw Error(m||"assert")};
 let seed=48520261107;
 const rnd=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed};
 const shuffle=a=>{for(let i=a.length-1;i>0;i--){const j=rnd()%(i+1);[a[i],a[j]]=[a[j],a[i]]}return a};
 const parity=n=>{let p=0;while(n){p^=n&1;n>>=1}return p};
 const cmp=(a,b)=>a.length-b.length||(a<b?-1:a>b?1:0);
 const graphs=[
 ["K4",4,Array.from({length:4},(_,i)=>Array.from({length:4-i-1},(_,j)=>[i,i+j+1])).flat()],
 ["K33",6,Array.from({length:3},(_,i)=>Array.from({length:3},(_,j)=>[i,j+3])).flat()],
 ["Q3",8,Array.from({length:8},(_,i)=>[0,1,2].map(k=>[i,i^(1<<k)]).filter(p=>p[0]<p[1])).flat()],
 ["Petersen",10,[...Array.from({length:5},(_,i)=>[i,(i+1)%5]),...Array.from({length:5},(_,i)=>[i+5,((i+2)%5)+5]),...Array.from({length:5},(_,i)=>[i,i+5])]],
 ];
 graphs.push(["K4x2",8,[...graphs[0][2],...graphs[0][2].map(([u,v])=>[u+4,v+4])]]);
 function mk(n,edges,charges){
   const names=edges.map((_,i)=>String(BigInt(10)**BigInt(16+(i%3)*12)+BigInt(41+i*13)));
   const clauses=[];
   for(let v=0;v<n;v++){
     const inc=edges.map(([u,w],i)=>u==v||w==v?i:-1).filter(i=>i>=0);
     assert(inc.length===3,"non-cubic");
     for(let mask=0;mask<8;mask++){
       if(parity(mask)!==charges[v]){
         const lit=inc.map((i,j)=>(mask&(1<<j)?"-":"")+names[i]);
         shuffle(lit);clauses.push(lit);
       }
     }
   }
   shuffle(clauses);
   const max=names.slice().sort(cmp).at(-1);
   return `p cnf ${max} ${clauses.length}\n`+clauses.map(c=>c.join(" ")+" 0").join("\n")+"\n";
 }
 function recognize(src){
   let lines=src.trim().split(/\r?\n/).filter(l=>!l.startsWith("c ")&&l.trim().length);
   if(!/^p cnf [1-9][0-9]* [1-9][0-9]*$/.test(lines[0]||""))return {kind:"BAD_FORMAT"};
   let [, ,max,m]=lines[0].split(" ");
   if(lines.length-1!==Number(m))return {kind:"BAD_FORMAT"};
   let clauses=[],groups=new Map(),firstIndex=new Map();
   for(let i=1;i<lines.length;i++){
     const t=lines[i].trim().split(/\s+/);
     if(t.length!==4||t[3]!=="0")return {kind:"BAD_FORMAT"};
     const ls=[];
     for(let j=0;j<3;j++){
       if(!/^-?[1-9][0-9]*$/.test(t[j]))return {kind:"BAD_FORMAT"};
       const neg=t[j].startsWith("-"),v=neg?t[j].slice(1):t[j];
       if(cmp(v,max)>0)return {kind:"BAD_FORMAT"};
       if(!firstIndex.has(v))firstIndex.set(v,firstIndex.size);
       ls.push({v,neg});
     }
     if(new Set(ls.map(x=>x.v)).size!==3)return {kind:"OUTSIDE"};
     clauses.push(ls);
     const s=ls.map(x=>x.v).sort(cmp);const k=s.join("|");
     if(!groups.has(k))groups.set(k,{s,masks:[],charge:null});
     let mask=0;for(let j=0;j<3;j++)if(ls.find(x=>x.v===s[j]).neg)mask|=1<<j;
     groups.get(k).masks.push(mask);
   }
   for(const g of groups.values()){
     if(g.masks.length!==4||new Set(g.masks).size!==4)return {kind:"OUTSIDE"};
     if(!g.masks.every(mask=>parity(mask)===parity(g.masks[0])))return {kind:"OUTSIDE"};
     g.charge=parity(g.masks[0])^1;
   }
   const vs=[...groups.values()];
   let incident=new Map();
   for(let i=0;i<vs.length;i++)for(const v of vs[i].s){
     if(!incident.has(v))incident.set(v,[]);
     incident.get(v).push(i);
   }
   if([...incident.values()].some(a=>a.length!==2||a[0]===a[1]))return {kind:"OUTSIDE"};
   const es=[...incident.entries()].sort((a,b)=>firstIndex.get(a[0])-firstIndex.get(b[0])).map(([v,[u,w]])=>({v,u,w}));
   const pairs=new Set();
   for(const e of es){
     const k=[e.u,e.w].sort((a,b)=>a-b).join("|");
     if(pairs.has(k))return {kind:"OUTSIDE"};
     pairs.add(k);
   }
   return {kind:"OK",vs,es,clauses};
 }
 function connected(n,es,s,t,filter=()=>true){
   if(s===t)return true;
   const seen=new Set([s]),q=[s];
   for(let i=0;i<q.length;i++){
     const v=q[i];
     for(let k=0;k<es.length;k++)if(filter(k)){
       const e=es[k];let w=e.u===v?e.w:e.w===v?e.u:-1;
       if(w===t)return true;
       if(w!==-1&&!seen.has(w)){seen.add(w);q.push(w)}
     }
   }
   return false;
 }
 function solve(r){
   const n=r.vs.length, es=r.es;
   const tree=es.map((e,i)=>!connected(n,es,e.u,e.w,j=>j<i));
   const treeEdgeCount=tree.filter(Boolean).length;
   let compCount=0;
   for(let v=0;v<n;v++){
     if([...Array(v).keys()].some(u=>connected(n,es,u,v)))continue;
     compCount++;
     let xor=0;
     for(let u=0;u<n;u++)if(connected(n,es,u,v))xor^=r.vs[u].charge;
     if(xor!==0)return {kind:"UNSAT",treeEdgeCount,compCount};
   }
   const values={};
   for(let i=0;i<es.length;i++){
     if(!tree[i]){values[es[i].v]=0;continue;}
     const {u}=es[i];let xor=0;
     for(let v=0;v<n;v++)if(connected(n,es,u,v,j=>tree[j]&&j!==i))xor^=r.vs[v].charge;
     values[es[i].v]=xor;
   }
   return {kind:"SAT",values,treeEdgeCount,compCount};
 }
 function evalClauses(clauses,values){
   return clauses.every(c=>c.some(l=>values[l.v]!==Number(l.neg)));
 }
 function exhaustive(r){
   let ids=r.es.map(e=>e.v);
   for(let j=0;j<(1<<ids.length);j++){
     const a={};for(let i=0;i<ids.length;i++)a[ids[i]]=(j>>i)&1;
     if(evalClauses(r.clauses,a))return true;
   }
   return false;
 }
 const out={cases:0,sat:0,unsat:0,exhaustiveChecks:0,clausesChecked:0,malformedRejected:0,outsideRejected:0,forestChecks:0,byGraph:{}};
 for(const [name,n,orig] of graphs){
   const ntests=name==="K4"?16:name==="Petersen"?8:20;
   const tally={cases:0,sat:0,unsat:0};
   for(let j=0;j<ntests;j++){
     const es=shuffle(orig.map(x=>x.slice()));
     let chi=j===0?Array(n).fill(0):j===1?[1,...Array(n-1).fill(0)]:name==="K4x2"&&j===2?[1,0,0,0,1,0,0,0]:Array.from({length:n},()=>rnd()&1);
     const raw=mk(n,es,chi),r=recognize(raw);
     assert(r.kind==="OK",name+" recognized "+r.kind);
     const ans=solve(r);
     assert(ans.treeEdgeCount===n-(name==="K4x2"?2:1),"tree cardinality");
     const sat=ans.kind==="SAT";
     if(j<6||name==="K4"){assert(exhaustive(r)===sat,"exhaustive "+name);out.exhaustiveChecks++;}
     if(sat){assert(evalClauses(r.clauses,ans.values),"clauses "+name);out.clausesChecked+=r.clauses.length;out.sat++;tally.sat++}
     else{out.unsat++;tally.unsat++}
     out.forestChecks+=r.es.length;out.cases++;tally.cases++;
     if(j===0&&name==="K4"){
       let body=raw.trim().split("\n"),bad=[
         body.slice(0,-1).join("\n"),raw.replace("p cnf","p cnfx"),
         raw.replace(/ 0\n/," 1\n"),raw.replace(/(\d+) 0\n/,"$1 1 0\n"),
         raw.replace(/\n/," 0\n"),
       ];
       for(const s of bad){const rr=recognize(s);if(rr.kind!=="OK")out.malformedRejected++}
       let broken=raw.trim().split("\n");broken[2]=broken[1];assert(recognize(broken.join("\n")).kind==="OUTSIDE","duplicate quartet");out.outsideRejected++;
     }
   }
   out.byGraph[name]=tally;
 }
 assert(out.malformedRejected>=4,"corrupt controls");
 assert(out.outsideRejected>=1,"outside controls");
 return out;
}
console.log(JSON.stringify(verify485(),null,2));
