function collisionPhase(record,sha){
 const ck=(v,t)=>{if(!v)throw Error(t)},sort=a=>a.slice().sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y),key=a=>sort(a).join(",");
 function combinations(a,k){let R=[];function go(i,L){if(L.length===k){R.push(L);return}for(let j=i;j<=a.length-k+L.length;j++)go(j+1,L.concat(a[j]))}go(0,[]);return R}
 function bin(n,k){let r=1n;for(let i=1;i<=k;i++)r=r*BigInt(n-i+1)/BigInt(i);return r}
 // regenerate exact source bytes; source-only recovery receives only C and physical n
 let C=[];for(let P of record.phase){let rows=[[]];for(let l of P){let B=record.blocks[Math.abs(l)-1],T=combinations(B,(B.length+1)/2).map(a=>a.map(v=>l>0?v:-v));rows=rows.flatMap(a=>T.map(b=>a.concat(b)))}C.push(...rows.map(sort))}
 let n=record.original_ids.variables[1],bytes=`p cnf ${n} ${C.length}\n`+C.map(c=>c.join(" ")+" 0\n").join("");ck(sha(bytes)===record.instance_id.split(":").at(-1)&&bytes.length*8===record.original_N_bits,"source bytes");
 function recover(C,n){
 let stats={keys:0,keyLits:0,collisions:0,unions:0,verifyLits:0},I=new Map(),pa=Array.from({length:n+1},(_,i)=>i),phase=Array(n+1).fill(0),sz=Array(n+1).fill(1);
 function find(i){let b=0;while(pa[i]!==i){b^=phase[i];i=pa[i]}return[i,b]}
 function join(a,b,s){stats.unions++;let [u,x]=find(a),[v,y]=find(b);if(u===v){ck((x^y)===s,"inconsistent replacement");return}if(sz[u]<sz[v])[u,v]=[v,u];pa[v]=u;phase[v]=s^x^y;sz[u]+=sz[v]}
 let unique=new Set();for(let c of C){let id=key(c);ck(!unique.has(id),"duplicate");unique.add(id);for(let i=0;i<c.length;i++){let k=c.slice(0,i).concat(c.slice(i+1)).join(","),l=c[i];stats.keys++;stats.keyLits+=c.length-1;if(I.has(k)){let t=I.get(k);stats.collisions++;join(Math.abs(l),Math.abs(t),+(l>0)^+(t>0))}else I.set(k,l)}}
 let M=new Map(),mapping=[];for(let i=1;i<=n;i++){let [r,s]=find(i);if(!M.has(r))M.set(r,{id:M.size+1,vs:[]});let q=M.get(r);q.vs.push([i,s]);mapping[i]=[q.id,s]}let blocks=[...M.values()];ck(blocks.every(q=>q.vs.length%2===1),"odd block");
 let groups=new Map();for(let c of C){let G=new Map();for(let l of c){stats.verifyLits++;let [b,s]=mapping[Math.abs(l)],t=(+(l>0)^s)?1:-1;if(!G.has(b))G.set(b,[]);G.get(b).push(t)}let P=[];for(let [b,a] of G){ck(a.length===(blocks[b-1].vs.length+1)/2&&a.every(x=>x===a[0]),"quota");P.push(b*a[0])}P=sort(P);let k=key(P);if(!groups.has(k))groups.set(k,{P,count:0});groups.get(k).count++}
 for(let {P,count} of groups.values()){let expected=P.reduce((a,l)=>{let b=blocks[Math.abs(l)-1].vs.length;return a*bin(b,(b+1)/2)},1n);ck(expected===BigInt(count),"missing response")}
 return{blocks,phase:[...groups.values()].map(q=>q.P),stats,keys:I.size}
 }
 let R=recover(C,n),P=R.phase,r=R.blocks.length,pa=Array.from({length:r+1},(_,i)=>i),sg=Array(r+1).fill(0);
 function find(v){let s=0;while(pa[v]!==v){s^=sg[v];v=pa[v]}return[v,s]}
 function join(v,w,p){let [a,x]=find(v),[b,y]=find(w);if(a===b)return (x^y)===p;pa[b]=a;sg[b]=x^y^p;return true}
 let D=new Set(P.map(key)),joins=0,contr=false;for(let c of P)if(c.length===2&&D.has(key(c.map(l=>-l)))){joins++;if(!join(Math.abs(c[0]),Math.abs(c[1]),1^+(c[0]<0)^+(c[1]<0)))contr=true}
 let roots=[...new Set(Array.from({length:r},(_,i)=>find(i+1)[0]))],dec="UNKNOWN",witness=null,checks=0;if(contr)dec="NO";else if(roots.length<=8){dec="NO";for(let w=0;w<2**roots.length;w++){let a=Array(r+1).fill(0);for(let v=1;v<=r;v++){let [q,s]=find(v);a[v]=(w>>roots.indexOf(q)&1)^s}if(P.every(c=>{checks++;return c.some(l=>a[Math.abs(l)]===+(l>0))})){let A=Array(n+1).fill(0);for(let b of R.blocks)for(let [v,s] of b.vs)A[v]=a[b.id]^s;ck(C.every(c=>c.some(l=>A[Math.abs(l)]===+(l>0))),"lift");witness=A.slice(1).join("");dec="YES";break}}}
 ck(dec===(record.label==="SAT"?"YES":"NO"),"decision");
 // verify original partition up to phase flips only after blind acquisition
 let bkey=a=>a.map(Math.abs).sort((x,y)=>x-y).join(","),aKeys=R.blocks.map(q=>bkey(q.vs.map(p=>p[0]))).sort(),pKeys=record.blocks.map(bkey).sort();ck(aKeys.join("|")===pKeys.join("|"),"partition");for(let B of R.blocks){let q=record.blocks.find(x=>bkey(x)===bkey(B.vs.map(p=>p[0]))),flags=B.vs.map(([v,s])=>s^+(q.find(l=>Math.abs(l)===v)<0));ck(flags.every(x=>x===flags[0]),"phase gauge")}
 return{instance:record.instance,instance_id:record.instance_id,original_N_bits:record.original_N_bits,original_ids:record.original_ids,guard_id:"EMPTY",residual_id:"ROOT",source_pin:record.source_pin,decision:dec,physical:n,clauses:C.length,phaseVars:r,phaseClauses:P.length,afterParity:roots.length,joins,checks,witness,recovery:R}
}
module.exports={collisionPhase};
