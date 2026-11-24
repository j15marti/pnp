"use strict";
function main(){
 const L={assertions:0,closureSweeps:0,closureScans:0,pins:0,eliminations:0,tableRows:0,lookups:0,discoveryScans:0,reconstructionChecks:0,peakTableRows:0,peakScope:0,referenceWords:0}; const ok=(x)=>{L.assertions++;if(!x)throw Error("assertion "+L.assertions)};
 const bit=(w,i)=>(w>>i)&1, range=n=>Array.from({length:n},(_,i)=>i);
 const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
 const make=(s,mask=3)=>({s:[...s],t:range(8).map(w=>!((w===0&&(mask&1))||(w===7&&(mask&2))))});
 function legal(f,vals){let w=0;for(let i=0;i<f.s.length;i++)w|=vals[f.s[i]]<<i;L.lookups++;return f.t[w]}
 function star(w,d,masks){let U=1,V=1;for(let i=0;i<d;i++){let a=bit(w,2*i),b=bit(w,2*i+1);if(a===b){if(a===0&&(masks[i]&1))U=0;if(a===1&&(masks[i]&2))V=0}}return [U+V,U+V-U*V]}
 const starTests=[];for(let d=2;d<=7;d++){let m=2*d,coeff=Array(m*(m-1)/2).fill(0),countCoeff=coeff.slice(),legalCount=0;for(let w=0;w<2**m;w++){let [f,g]=star(w,d,Array(d).fill(3));let [ff,gg]=star(w^((1<<m)-1),d,Array(d).fill(3));ok(f===ff&&g===gg);let actual=0;for(let h=0;h<2;h++){let valid=true;for(let i=0;i<d;i++)if(bit(w,2*i)===h&&bit(w,2*i+1)===h)valid=false;actual+=+valid}ok(f===actual&&g===+(actual>0));legalCount+=g;let k=0;for(let i=0;i<m;i++)for(let j=i+1;j<m;j++){let s=bit(w,i)===bit(w,j)?1:-1;coeff[k]+=s*g;countCoeff[k++]+=s*f}for(let mask of [1,2]){let mm=Array(d).fill(3);mm[0]=mask;let [v,a]=star(w,d,mm);let ref=0;for(let h=0;h<2;h++){let valid=true;for(let i=0;i<d;i++)if(bit(w,2*i)===h&&bit(w,2*i+1)===h&&(mm[i]&(1<<h)))valid=false;ref+=+valid}ok(v===ref&&a===+(ref>0))}}
 let k=0;for(let i=0;i<m;i++)for(let j=i+1;j<m;j++){ok(coeff[k]===(i>>1==j>>1?2**d-2*3**(d-1):2*3**(d-2)));ok(countCoeff[k++]!==0)}starTests.push({d,rank:2*d-1,legalCount,pairCoefficients:[...new Set(coeff)]})}
 function solve(n,source,cap=12,initialStar=null){
  let fs=source.map(f=>({s:f.s.slice(),t:f.t.slice()})), vals=Array(n).fill(-1), stack=[],done=new Set(),maxScope=0;
  function mem(){L.peakTableRows=Math.max(L.peakTableRows,fs.reduce((s,f)=>s+f.t.length,0)+stack.reduce((s,q)=>s+q.bucket.reduce((a,f)=>a+f.t.length,0),0))}
  function close(){while(true){L.closureSweeps++;let changed=false;for(let f of fs){L.closureScans++;let support=f.s.map(()=>0),any=false;for(let w=0;w<f.t.length;w++){if(!f.t[w])continue;let good=f.s.every((v,i)=>vals[v]<0||vals[v]===bit(w,i));if(!good)continue;any=true;f.s.forEach((v,i)=>support[i]|=1<<bit(w,i))}if(!any)return false;for(let i=0;i<f.s.length;i++)if(vals[f.s[i]]<0&&(support[i]===1||support[i]===2)){vals[f.s[i]]=support[i]===1?0:1;L.pins++;changed=true;break}if(changed)break}if(!changed)return true}}
  mem();if(!close())return {status:"UNSAT",maxScope};
  while(fs.length){
   // Remove factors whose entire scope has certified fixed pins.
   fs=fs.filter(f=>f.s.some(v=>vals[v]<0));
   if(!fs.length)break;
   let best=null;
   for(let v=0;v<n;v++){if(vals[v]>=0||done.has(v))continue;L.discoveryScans++;let bucket=fs.filter(f=>f.s.includes(v));if(!bucket.length)continue;let boundary=[...new Set(bucket.flatMap(f=>f.s).filter(u=>u!==v&&vals[u]<0))].sort((a,b)=>a-b);if(!best||boundary.length<best.boundary.length||v===initialStar)best={v,bucket,boundary};if(v===initialStar)break}
   if(!best)throw Error("no bucket");let {v,bucket,boundary}=best;initialStar=null;
   maxScope=Math.max(maxScope,boundary.length);L.peakScope=Math.max(L.peakScope,boundary.length);if(boundary.length>cap)return {status:"UNKNOWN",maxScope};
   let t=[],tmp=vals.slice();for(let w=0;w<2**boundary.length;w++){L.tableRows++;boundary.forEach((u,i)=>tmp[u]=bit(w,i));let yes=false;for(let b=0;b<2;b++){tmp[v]=b;if(bucket.every(f=>legal(f,tmp))){yes=true;break}}t.push(yes)}
   fs=fs.filter(f=>!bucket.includes(f));fs.push({s:boundary,t});stack.push({v,bucket});done.add(v);L.eliminations++;mem();if(!close())return {status:"UNSAT",maxScope};
  }
  for(let v=0;v<n;v++)if(vals[v]<0&&!done.has(v))vals[v]=0;
  for(let {v,bucket} of stack.reverse()){ok(vals[v]===-1);let yes=false;for(let b=0;b<2;b++){vals[v]=b;L.reconstructionChecks++;if(bucket.every(f=>legal(f,vals))){yes=true;break}}ok(yes)}
  ok(source.every(f=>legal(f,vals)));return {status:"SAT",maxScope,witness:vals}
 }
 function ref(n,fs){let count=0;for(let w=0;w<2**n;w++){L.referenceWords++;if(fs.every(f=>legal(f,range(n).map(i=>bit(w,i)))))count++}return count}
 let results={starTests,fano:[],random:{SAT:0,UNSAT:0,UNKNOWN:0},do02:[],looseCycles:[]};
 for(let i=-1;i<14;i++){let fs=fano.map((s,j)=>make(s,i>=0&&j===(i>>1)?(i%2?1:2):3)),c=ref(7,fs);ok(c===(i<0?0:5));for(let v=0;v<7;v++){let r=solve(7,fs,12,v);ok(r.status===(c?"SAT":"UNSAT"));results.fano.push({neighbor:i,first:v,count:c,status:r.status,maxScope:r.maxScope})}}
 let seed=20261124;function rnd(){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed}
 for(let z=0;z<100;z++){let n=9,used=new Set(),fs=[];for(let q=0;q<100;q++){let s=[...new Set(range(3).map(()=>rnd()%n))].sort((a,b)=>a-b);if(s.length!==3)continue;let p=[s[0]+","+s[1],s[0]+","+s[2],s[1]+","+s[2]];if(p.some(x=>used.has(x)))continue;if(rnd()%5===0)continue;p.forEach(x=>used.add(x));fs.push(make(s,rnd()%4===0?1+rnd()%2:3))}let c=ref(n,fs),r=solve(n,fs);ok(r.status===(c?"SAT":"UNSAT"));results.random[r.status]++}
 // DO02 explicit 49/49 weak equality chains (two branches of 4 gadgets).
 let edges=[],next=1,ends=[];for(let j=0;j<2;j++){let a=0;for(let i=0;i<4;i++){let b=next++,p=next++,u=next++,v=next++,w=next++,x=next++;edges.push([a,u,v],[a,w,x],[b,u,w],[b,v,x],[p,u,x],[p,v,w]);a=b}ends.push(a)}edges.push([0,...ends]);ok(next===49&&edges.length===49);
 for(let i=-1;i<98;i++){let fs=edges.map((s,j)=>make(s,i>=0&&j===(i>>1)?(i%2?1:2):3));let r=solve(next,fs);ok(r.status===(i<0?"UNSAT":"SAT"));results.do02.push({neighbor:i,status:r.status,maxScope:r.maxScope})}
 for(let k of [4,8,16,32,64]){let fs=range(k).map(i=>make([i,(i+1)%k,k+i]));let r=solve(2*k,fs);ok(r.status==="SAT");results.looseCycles.push({girth:k,n:2*k,status:r.status,maxScope:r.maxScope})}
 let hostile=solve(7,fano.map(s=>make(s)),2);ok(hostile.status==="UNKNOWN");results.cap=hostile;results.ledger=L;return results;
}
console.log(JSON.stringify(main(),null,2));
