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
function encodeDIMACS(nvars,clauses){
 return 'p cnf '+nvars+' '+clauses.length+'\n'+clauses.map(c=>c.join(' ')+' 0').join('\n')+'\n';
}
function parseDIMACS(source){
 const lines=source.trim().split('\n');
 const header=lines.shift().trim().split(/\s+/);
 if(header.length!==4||header[0]!=='p'||header[1]!=='cnf')throw Error('missing DIMACS header');
 const n=Number(header[2]),m=Number(header[3]);
 const clauses=lines.map(l=>{
   const z=l.trim().split(/\s+/).map(Number);
   if(z.pop()!==0||z.some(x=>!Number.isInteger(x)||x===0||Math.abs(x)>n))throw Error('malformed clause');
   return z;
 });
 if(clauses.length!==m)throw Error('wrong DIMACS clause count');
 return {n,clauses};
}
function validateChild(nvars,clauses){
 const check=parseDIMACS(encodeDIMACS(nvars,clauses));
 if(check.n!==nvars||JSON.stringify(check.clauses)!==JSON.stringify(clauses))
    throw Error('invalid source-preserving physical child');
 return encodeDIMACS(nvars,clauses).length;
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
 // Source-identified ordinary DIMACS descendants: all headers/bodies regenerated.
 const rootBytes=validateChild(edges.length,cls);
 const one=cls.filter((_,j)=>j!==0), two=one.filter((_,j)=>j!==0);
 const childBytes=validateChild(edges.length,one),grandchildBytes=validateChild(edges.length,two);
 if(!(rootBytes>childBytes&&childBytes>grandchildBytes))throw Error('child size');
 for(let j=0;j<cls.length;j++)validateChild(edges.length,cls.filter((_,k)=>k!==j));
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
         essential:essential.size,component_counts:r,truth_assignments:2**edges.length,
         dimacs_root_bytes:rootBytes,dimacs_child_bytes:childBytes,dimacs_grandchild_bytes:grandchildBytes};
}
function strictW1Control(){
 // Actual source clause IDs: PCRETRACT1 Appendix A, original W_1.
 const words=[
 "-1 3 -14","2 -8 9","10 -13 14","3 7 -13","-4 -9 -11",
 "5 8 -14","4 -8 -11","1 7 13","1 -7 10","-5 -6 -15",
 "-2 -6 12","-4 9 -10","-2 5 -12","-3 6 -15","6 -7 11",
 "2 -9 11","4 8 -10","-3 12 15","-5 -12 15","-1 13 14"];
 const C=words.map(w=>w.split(' ').map(Number));
 if(C.length!==20||new Set(words).size!==20)throw Error('W1 source');
 for(let v=1;v<=15;v++){
   let pos=C.flat().filter(l=>l===v).length,neg=C.flat().filter(l=>l===-v).length;
   if(pos!==2||neg!==2)throw Error('W1 is not strict signed 2P2N');
 }
 let sat=0,unique=new Set(),qmodels=0;
 validateChild(15,C);
 for(let k=0;k<C.length;k++)validateChild(15,C.filter((_,i)=>i!==k));
 for(let a=0;a<2**15;a++){
   const violated=C.map((cl,i)=>cl.some(l=>(((a>>(Math.abs(l)-1))&1)===Number(l>0)))?-1:i).filter(i=>i>=0);
   if(!violated.length)sat++;
   if(violated.length===1)unique.add(violated[0]);
   if(violated.every(i=>i===7))qmodels++;
 }
 if(sat!==0||unique.size!==20||qmodels!==244)throw Error('W1/Q15 opposite-label control');
 const easy=[{label:'Horn-UNSAT',C:[[1],[-1]],want:false},
             {label:'2SAT-SAT',C:[[1,2],[-1,2]],want:true}];
 for(let e of easy){
   let satEasy=false;
   for(let a=0;a<4;a++)if(e.C.every(cl=>cl.some(l=>(((a>>(Math.abs(l)-1))&1)===Number(l>0)))))satEasy=true;
   if(satEasy!==e.want)throw Error('easy control failed');
 }
 return {original:'PCRETRACT1 Appendix A W_1',nvars:15,clauses:20,
         strict_signed_2P2N:true,original_SAT:false,individually_essential:unique.size,
         Q15_removed_original_clause_id:8,Q15_SAT:true,Q15_model_count:qmodels,
         direct_assignments:2**15,serialized_checks:21,easy_controls:2};
}
function run(){
 let rows=[];
 const strict_control=strictW1Control();
 for(let [name,n,edges] of graphs())
   for(let mask of new Set([1,1<<(n/2),(2**n)-2,0,3]))
      rows.push(runCase(name,n,edges,mask));
 if(rows.length!==25)throw Error('case count');
 if(rows.some(r=>r.odd&&r.essential!==(r.graph==='bridged_subdivided_K4'?36:r.clauses)))
   throw Error('hostile essential count');
 return {id:'TSEITIN-CLAUSE-CRITICAL125',method:'independent exhaustive direct proper CNF and graph component predictions',
         cases:rows.length,truth_assignments:rows.reduce((s,x)=>s+x.truth_assignments,0),
         discrepancies:0,serialized_checks:rows.reduce((s,x)=>s+3+x.clauses,0)+strict_control.serialized_checks,
         strict_control,rows,
         scope:'ordinary proper signed 3CNF; edge variables have four positive and four negative occurrences, not strict (2,2)'};
}
if(typeof module!=='undefined'&&require.main===module)console.log(JSON.stringify(run(),null,2));
