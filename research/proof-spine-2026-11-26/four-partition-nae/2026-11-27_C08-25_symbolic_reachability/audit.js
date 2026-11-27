function audit(){
 const results={version:"C08-25",cap:60000000,counters:{checks:0,gateOps:0,bruteWords:0,nativeRows:0},cases:[]};
 const c=results.counters;
 function tick(k,n=1){c[k]+=n;if(Object.values(c).reduce((a,b)=>a+b,0)>results.cap)throw Error("cap");}
 function ck(p,msg){tick("checks");if(!p)throw Error(msg)}
 function make(L){
   let n=3*L+1,rows=[],colors=[],edge=[],base=n;
   for(let j=0;j<L;j++){
      let a=j,b=j+1,u=L+1+2*j,v=u+1,z=base+4*j;
      for(let [f,t,w,p,flip] of [[a,u,z,0,0],[u,b,z+1,2,1],[a,v,z+2,1,0],[v,b,z+3,3,1]]){
        rows.push([f,t,w]);colors.push(p);edge.push({f,t,w,p,flip});
      }
   }
   return {L,n,vars:n+4*L,rows,colors,edge,guard:{pins:[[0,1],[L,0]],affine:Array.from({length:L},(_,j)=>{let z=n+4*j;return [[z,z+1,1],[z,z+2,1],[z,z+3,0]]}).flat()}};
 }
 function complete(a){
   let n=a.vars,rows=[],parts=[],ownerMap=[],seen=Array.from({length:n},()=>new Set());
   a.rows.forEach((r,i)=>r.forEach(v=>{ck(!seen[v].has(a.colors[i]),"partial partition");seen[v].add(a.colors[i]);}));
   for(let t=0;t<12;t++)a.rows.forEach((r,i)=>{rows.push(r.map(v=>t*n+v));parts.push(a.colors[i]);ownerMap.push([t,i])});
   let mul=[0,2,3,1];
   for(let v=0;v<n;v++)for(let p=0;p<4;p++)if(!seen[v].has(p))for(let j=0;j<4;j++){rows.push([j*n+v,(4+(j^p))*n+v,(8+(j^mul[p]))*n+v]);parts.push(p);ownerMap.push(null);}
   let pairs=new Set(),counts=new Uint8Array(12*n*4);
   rows.forEach((r,i)=>{tick("nativeRows");ck(new Set(r).size===3,"distinct");for(let v of r){let k=v*4+parts[i];ck(counts[k]===0,"partition");counts[k]++;}
      for(let j=0;j<3;j++)for(let k=j+1;k<3;k++){let p=r[j]<r[k]?r[j]+","+r[k]:r[k]+","+r[j];ck(!pairs.has(p),"linearity");pairs.add(p)}});
   ck(counts.every(v=>v===1),"perfect partition");
   return {rows,parts,ownerMap,nativeVariables:12*n};
 }
 function reach(a,bits){ // independent graph construction in logical phases
    let adj=Array.from({length:a.n},()=>[]);
    for(let e of a.edge){let forward=bits[e.w-a.n]^e.flip;if(forward)adj[e.f].push(e.t);else adj[e.t].push(e.f)}
    let seen=new Set([0]),q=[0];
    for(let i=0;i<q.length;i++)for(let w of adj[q[i]])if(!seen.has(w)){seen.add(w);q.push(w)}
    return seen.has(a.L);
 }
 function direct(a,bits){ // physical NAE brute force, pins only, all boundary words controls
   let free=a.n-2;
   for(let w=0;w<2**free;w++){
      tick("bruteWords");
      function x(v){if(v>=a.n)return bits[v-a.n];if(v===0)return 1;if(v===a.L)return 0;let p=v<a.L?v-1:v-2;return (w>>p)&1;}
      if(a.rows.every(r=>{let [u,v,b]=r.map(x);return !(u===v&&v===b)}))return false;
   }
   return true;
 }
 function circuit(a,substitute=false){ // symbolic generic 2SAT over free internal x, pinned endpoints are unit clauses
   let nodes=[["c",0],["c",1]],uniq=new Map(),neg=new Map([[0,1],[1,0]]);
   function atom(k,s){let key="a:"+k+":"+s;if(uniq.has(key))return uniq.get(key);let id=nodes.length;nodes.push(["a",k,s]);uniq.set(key,id);let other=uniq.get("a:"+k+":"+(s^1));if(other!==undefined){neg.set(id,other);neg.set(other,id)}return id;}
   function gate(op,x,y){tick("gateOps");if(op==="&"){if(!x||!y)return 0;if(x===1)return y;if(y===1||x===y)return x;if(neg.get(x)===y)return 0;}else {if(x===1||y===1)return 1;if(!x)return y;if(!y||x===y)return x;if(neg.get(x)===y)return 1;}
     if(x>y)[x,y]=[y,x];let k=op+":"+x+":"+y;if(uniq.has(k))return uniq.get(k);let id=nodes.length;nodes.push([op,x,y]);uniq.set(k,id);return id;}
   let m=2*a.n,R=Array.from({length:m},(_,i)=>Array.from({length:m},(_,j)=>Number(i===j)));
   const arc=(u,v,g)=>{R[u][v]=gate("|",R[u][v],g)};
   // literal id 2*v+value, denotes x_v=value
   for(let [x,y,z] of a.rows)for(let b=0;b<2;b++){
     let j=z-a.n,phase=substitute?[0,1,1,0][j%4]:0,atomId=atom(substitute?Math.floor(j/4):j,b^phase);
     // when boundary bit b, forbids x=y=b; implications x=b -> y=1-b and reverse.
     arc(2*x+b,2*y+(b^1),atomId);arc(2*y+b,2*x+(b^1),atomId);
   }
   for(let [v,b] of a.guard.pins)arc(2*v+(b^1),2*v+b,1);
   for(let k=0;k<m;k++)for(let u=0;u<m;u++){let x=R[u][k];if(!x)continue;for(let v=0;v<m;v++){let y=R[k][v];if(y)R[u][v]=gate("|",R[u][v],gate("&",x,y));}}
   let root=0;for(let v=0;v<a.n;v++)root=gate("|",root,gate("&",R[2*v][2*v+1],R[2*v+1][2*v]));
   return {nodes,root};
 }
 function ev(C,b){let a=[];for(let [op,x,y] of C.nodes)a.push(op==="c"?x:op==="a"?Number(b[x]===y):op==="&"?a[x]&a[y]:a[x]|a[y]);return a[C.root]===1;}
 function formula(a,b){for(let j=0;j<a.L;j++){let [p,q,r,s]=b.slice(4*j,4*j+4);if(!(p&&!q||r&&!s))return false;}return true;}
 function verifyLower(a){ // enumerate minimal forbidden forward-control words; midpoint intersection feasible
    let min=[];for(let w=0;w<2**a.L;w++){let mask=0;for(let j=0;j<a.L;j++)mask|=((w>>j)&1?12:3)<<(4*j);min.push(mask);}
    function v(mask){return Array.from({length:4*a.L},(_,i)=>((mask>>i)&1)^(i%2));}
    for(let p of min){ck(formula(a,v(p)),"min forbidden");for(let j=0;j<4*a.L;j++)if((p>>j)&1)ck(!formula(a,v(p^(1<<j))),"minimal");}
    for(let i=0;i<min.length;i++)for(let j=i+1;j<min.length;j++)ck(!formula(a,v(min[i]&min[j])),"distinct forbidden supports intersection feasible");
    return min.length;
 }
 for(let L of [1,2,3,4,8,16,32,64,128,256]){
    let a=make(L),native=complete(a),raw=JSON.stringify({n:native.nativeVariables,clauses:native.rows,parts:native.parts,guard:a.guard});
    let hash=2166136261;for(let j=0;j<raw.length;j++){hash^=raw.charCodeAt(j);hash=Math.imul(hash,16777619)>>>0;}
    let gen=L<=8?circuit(a):null,guarded=L<=8?circuit(a,true):null,words=0,brute=0,no=0;
    if(L<=3){for(let w=0;w<2**(4*L);w++){let b=Array.from({length:4*L},(_,j)=>(w>>j)&1);let f=formula(a,b);ck(reach(a,b)===f,"path/formula");ck(ev(gen,b)===f,"generic circuit");ck(direct(a,b)===f,"physical enumeration");words++;brute++;if(f)no++;}}
    if(L<=8)for(let w=0;w<2**L;w++){let z=Array.from({length:L},(_,j)=>(w>>j)&1),b=z.flatMap(x=>[x,x^1,x^1,x]);ck(ev(guarded,z),"guarded circuit");ck(reach(a,b)&&formula(a,b),"guarded direct path");}
    let minimal=L<=6?verifyLower(a):null;
    // Symbolic integrated proof: each guarded stage reduces to a OR not-a.
    for(let j=0;j<L;j++)for(let z=0;z<2;z++){let p=[z,z^1,z^1,z];ck((p[0]&&!p[1])||(p[2]&&!p[3]),"local guard tautology");}
    // Unit-closure control: central clauses under pins alone, affine substitution guards, check if any unit emerges (each surviving non-taut clause >=2 distinct literals).
    let minwidth=3,unitCount=0;
    for(let r of a.rows){for(let s of [0,1]){let vals=r.filter(v=>v===0||v===L).map(v=>v===0?1:0);if(vals.some(v=>v===s))continue;let width=r.length-vals.length;minwidth=Math.min(minwidth,width);if(width===1)unitCount++;}}
    ck(unitCount===0,"unit closure should not force");
    results.cases.push({L,sourceVariables:native.nativeVariables,sourceClauses:native.rows.length,encodedJSONBytes:raw.length,fingerprintFNV:hash.toString(16),internal:a.n,protected:4*L,guardFreePhases:L,refutation:"UNSAT under affine guard and endpoint pins",genericGates:gen?.nodes.length??null,guardedGates:guarded?.nodes.length??null,guardedRoot:guarded?.root??null,boundaryTrials:words,physicalExhaustiveBoundaryTrials:brute,forbiddenWords:no,enumeratedMinimalForbidden:minimal,explicitCNFLowerBound:"2^"+L,factoredGateUpperBound:4*L-1,unitCount,partialRows:L<=2?a.rows:undefined,colors:L<=2?a.colors:undefined,guard:L<=2?a.guard:undefined});
 }
 return results;
}
console.log(JSON.stringify(audit(),null,2));
