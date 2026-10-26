'use strict';
// TSEITIN-CLAUSE-CRITICAL125, reproducible exhaustive clause-level audit.
// Standard JavaScript only: node this_file.js
function graphs(){
 const K4=[],K33=[],prism=[],cube=[],bridge=[];
 for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)K4.push([i,j]);
 for(let i=0;i<3;i++)for(let j=3;j<6;j++)K33.push([i,j]);
 for(let o of [0,3])for(let i=0;i<3;i++)prism.push([o+i,o+(i+1)%3]);
 for(let i=0;i<3;i++)prism.push([i,i+3]);
 for(let i=0;i<8;i++)for(let b=0;b<3;b++){const j=i^(1<<b);if(i<j)cube.push([i,j]);}
 for(let o of [0,5]){
   for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)
     if(!(i===0&&j===1))bridge.push([o+i,o+j]);
   bridge.push([o,o+4],[o+1,o+4]);
 }
 bridge.push([4,9]);
 return [['K4',4,K4],['K33',6,K33],['prism',6,prism],['cube',8,cube],['bridged_subdivided_K4',10,bridge]];
}
function components(n,edges,removed){
 const rest=new Set(Array.from({length:n},(_,i)=>i).filter(v=>v!==removed)),out=[];
 while(rest.size){
   let start=Math.min(...rest),H=new Set([start]),stack=[start];rest.delete(start);
   while(stack.length){
     let u=stack.pop();
     for(let [a,b] of edges){
       let v=a===u?b:(b===u?a:-1);
       if(v!==removed&&rest.has(v)){rest.delete(v);H.add(v);stack.push(v);}
     }
   }
   out.push(H);
 }
 return out;
}
function runCase(name,n,edges,mask){
 const charge=Array.from({length:n},(_,v)=>(mask>>v)&1), odd=charge.reduce((x,y)=>x^y,0);
 const inc=Array.from({length:n},()=>[]);
 edges.forEach(([u,v],j)=>{inc[u].push(j);inc[v].push(j);});
 if(inc.some(L=>L.length!==3))throw Error('noncubic input');
 const cls=[],meta=[];
 for(let v=0;v<n;v++)for(let w=0;w<8;w++){
   let bits=[w&1,(w>>1)&1,(w>>2)&1];
   if((bits[0]^bits[1]^bits[2])!==charge[v]){
     cls.push(inc[v].map((e,k)=>bits[k]===0?e+1:-(e+1)));
     meta.push({v,bits});
   }
 }
 if(cls.length!==4*n||new Set(cls.map(C=>C.join(','))).size!==cls.length)throw Error('clause grammar');
 let p=Array(edges.length).fill(0),q=Array(edges.length).fill(0);
 for(let C of cls){if(C.length!==3||new Set(C.map(Math.abs)).size!==3)throw Error('improper clause');
   for(let lit of C)(lit>0?p:q)[Math.abs(lit)-1]++;
 }
 if(p.some(x=>x!==4)||q.some(x=>x!==4))throw Error('source occurrence');
 const essential=new Set();let foundSAT=false;
 // This independent test evaluates the literal strings, not vertex equations.
 for(let a=0;a<2**edges.length;a++){
   let bad=-1,count=0;
   for(let j=0;j<cls.length;j++){
     let clauseSAT=cls[j].some(lit=>(((a>>(Math.abs(lit)-1))&1)===Number(lit>0)));
     if(!clauseSAT){count++;bad=j;if(count>1)break;}
   }
   if(count===0)foundSAT=true;
   if(count===1)essential.add(bad);
 }
 if(foundSAT!==!odd)throw Error('SAT mismatch');
 let r=Array.from({length:n},(_,v)=>components(n,edges,v).length),pred=new Set();
 if(odd)for(let j=0;j<cls.length;j++){
   let {v,bits}=meta[j],Hlist=components(n,edges,v);
   let good=Hlist.every(H=>{
      let need=0,seen=0;
      for(let z of H)need^=charge[z];
      for(let k=0;k<3;k++){
        let [a,b]=edges[inc[v][k]],neighbor=a===v?b:a;
        if(H.has(neighbor))seen^=bits[k];
      }
      return need===seen;
   });
   if(good)pred.add(j);
 }
 if(essential.size!==pred.size||[...essential].some(j=>!pred.has(j)))throw Error('formula-component discrepancy');
 if(odd)for(let v=0;v<n;v++)
   if([...essential].filter(j=>meta[j].v===v).length!==2**(3-r[v]))throw Error('count formula');
 return {graph:name,vertices:n,edges:edges.length,clauses:cls.length,charge_mask:mask,odd:!!odd,
         essential:essential.size,component_counts:r,truth_assignments:2**edges.length};
}
function run(){
 let rows=[];
 for(let [name,n,edges] of graphs())
   for(let mask of new Set([1,1<<(n/2),(2**n)-2,0,3]))
      rows.push(runCase(name,n,edges,mask));
 if(rows.length!==25)throw Error('case count');
 if(rows.some(r=>r.odd&&r.essential!==(r.graph==='bridged_subdivided_K4'?36:r.clauses)))
   throw Error('hostile essential count');
 return {id:'TSEITIN-CLAUSE-CRITICAL125',method:'independent exhaustive direct proper CNF and graph component predictions',
         cases:rows.length,truth_assignments:rows.reduce((s,x)=>s+x.truth_assignments,0),
         discrepancies:0,rows,
         scope:'ordinary proper signed 3CNF; edge variables have four positive and four negative occurrences, not strict (2,2)'};
}
if(typeof module!=='undefined'&&require.main===module)console.log(JSON.stringify(run(),null,2));
