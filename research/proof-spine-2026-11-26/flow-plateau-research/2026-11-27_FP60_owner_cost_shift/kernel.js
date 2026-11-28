function runReparam(F,ps,width=6,sweeps=2,cap=250000,compress=false){
 const start=Date.now(),A=new Map(ps),counts={restrict:0,pair:0,join:0,shift:0,verify:0},total=()=>Object.values(counts).reduce((a,b)=>a+b,0);let peak=0,log=[],status="COMPLETE",bounds=[],Q=[];
 function tick(k,v=1){if(total()+v>cap)throw Error("cap");counts[k]+=v}
 const index=(S,U,w)=>S.reduce((s,v,j)=>s|(((w>>U.indexOf(v))&1)<<j),0),union=(a,b)=>[...new Set([...a,...b])].sort((x,y)=>x-y);
 const bound=()=>Q.reduce((z,f)=>z+Math.min(...f.cost),0),mark=()=>{peak=Math.max(peak,Q.reduce((z,f)=>z+f.cost.length,0))};
 try{
 for(const f of F){const vs=f.vs.filter(v=>!A.has(v));let cost=[];for(let w=0;w<2**vs.length;w++){tick("restrict");let z=f.vs.reduce((s,v,j)=>s|((A.has(v)?A.get(v):(w>>vs.indexOf(v))&1)<<j),0);cost.push(compress?Math.min(4,f.cost[z]):f.cost[z])}Q.push({vs,cost,ids:f.ids.slice()})}mark();bounds.push(bound());
 // Greedy merging of distinct scopes, no duplicated owners, deterministic. Same-scope is width=0.
 for(;;){let best=null;for(let i=0;i<Q.length;i++)for(let j=i+1;j<Q.length;j++){tick("pair");let a=Q[i],b=Q[j],I=a.vs.filter(v=>b.vs.includes(v)),U=union(a.vs,b.vs);if(!I.length||U.length>Math.max(width,Math.max(a.vs.length,b.vs.length))||(!width&&U.length!==I.length))continue;
 let s=I.length*100-U.length;if(!best||s>best.s)best={i,j,U,s}}
 if(!best)break;const {i,j,U}=best,a=Q[i],b=Q[j],cost=[];for(let w=0;w<2**U.length;w++){tick("join",2);cost.push(a.cost[index(a.vs,U,w)]+b.cost[index(b.vs,U,w)])}
 // Replay all rows using a distinct assignment map, no clipped intermediate shifts.
 for(let w=0;w<cost.length;w++){tick("verify",2);let bits=new Map(U.map((v,k)=>[v,(w>>k)&1]));let val=f=>f.cost[f.vs.reduce((s,v,k)=>s|(bits.get(v)<<k),0)];if(cost[w]!==val(a)+val(b))throw Error("join mismatch")}
 log.push({kind:"join",i,j,U,ids:[...a.ids,...b.ids]});Q.splice(j,1);Q.splice(i,1,{vs:U,cost,ids:[...a.ids,...b.ids]});mark();
 }bounds.push(bound());
 for(let t=0;t<sweeps;t++){let prior=bound();for(let i=0;i<Q.length;i++)for(let j=0;j<Q.length;j++){if(i===j)continue;tick("pair");let a=Q[i],b=Q[j],I=a.vs.filter(v=>b.vs.includes(v));if(!I.length)continue;
 let q=Array(2**I.length).fill(Infinity);for(let w=0;w<a.cost.length;w++){tick("shift");let z=index(I,a.vs,w);q[z]=Math.min(q[z],a.cost[w])}if(q.every(z=>z===0))continue;
 let ac=a.cost.map((z,w)=>{tick("shift");return z-q[index(I,a.vs,w)]}),bc=b.cost.map((z,w)=>{tick("shift");return z+q[index(I,b.vs,w)]});
 // Independently check shift equality on all overlap-compatible row pairs by checking the two sides separately.
 for(let w=0;w<ac.length;w++){tick("verify");let bits=I.map(v=>(w>>a.vs.indexOf(v))&1),k=bits.reduce((s,v,j)=>s|(v<<j),0);if(ac[w]<0||a.cost[w]-ac[w]!==q[k])throw Error("bad donor")}
 for(let w=0;w<bc.length;w++){tick("verify");let k=I.map(v=>(w>>b.vs.indexOf(v))&1).reduce((s,v,j)=>s|(v<<j),0);if(bc[w]-b.cost[w]!==q[k])throw Error("bad recipient")}
 let old=Math.min(...a.cost)+Math.min(...b.cost),now=Math.min(...ac)+Math.min(...bc);if(now<old)throw Error("bound decrease");log.push({kind:"shift",i,j,I,q});a.cost=ac;b.cost=bc;
 }bounds.push(bound());if(bound()<prior)throw Error("bad sweep")}
 }catch(e){if(String(e)!=="Error: cap")throw e;status="CAPPED"}
 return {status,width,sweeps,compress,bounds,final:bound(),counts,total:total(),peak,log,elapsed_ms:Date.now()-start,partition:Q.map(f=>({vs:f.vs,ids:f.ids,min:Math.min(...f.cost)}))};
}
function transport(G,n,map,cnf){
 // Verify actual native root sign semantics against the provenance map at every B port.
 const reps=new Map(Object.entries(map.representative_ports).map(([key,[p,s]])=>[key,[n.roots[p],n.sg[p]^s]]));
 const f=reps.get("f");if(f[0]!==n.gauge||f[1]!==0)throw Error("gauge map");
 let uniq=new Set(),owner=new Map(),checks=0,privateRoots=new Map();
 for(const [name,[r,s]] of reps){if(uniq.has(r))throw Error("duplicate logical root");uniq.add(r)}
 for(const v of n.B){const [type,id,i,j,k]=map.vertex_provenance[v];if(type!=="clause")throw Error("owner");const [a,b,c]=map.ternary_clauses[i],lit=x=>["x"+Math.abs(x),Number(x<0)],z="z"+i,expected=j===0?[lit(a),lit(b),[z,0]]:[[z,1],lit(c),["f",0]];expected.push(["w"+i+"_"+j,0]);for(let h=0;h<4;h++){let [name,s]=expected[h],p=4*v+h,[r,b]=reps.get(name);checks++;if(n.roots[p]!==r||n.sg[p]!== (b^s))throw Error("port mapping");if(!name.startsWith("x")||Number(name.slice(1))>map.original_n){if(name!=="f"){if(privateRoots.has(r)&&privateRoots.get(r)!==id)throw Error("cross owner");privateRoots.set(r,id)}}}
 if(!owner.has(id))owner.set(id,[]);owner.get(id).push(n.factors.find(q=>q.ids[0]===v))}
 let evals=0,rows=0,maxAux=0,ownerInfo=[];
 for(let id=1;id<=cnf.length;id++){let fs=owner.get(id),C=cnf[id-1],src=[...new Set(C.map(l=>Math.abs(l)))],roots=src.map(v=>reps.get("x"+v)[0]),all=[...new Set(fs.flatMap(f=>f.vs))],aux=all.filter(v=>!roots.includes(v));
 if(aux.some(r=>privateRoots.get(r)!==id)||roots.some(r=>!all.includes(r)))throw Error("owner scope");maxAux=Math.max(maxAux,aux.length);let minrows=[];
 for(let w=0;w<2**src.length;w++){let best=Infinity,AS=new Map(src.map((v,j)=>[reps.get("x"+v)[0],((w>>j)&1)^reps.get("x"+v)[1]]));
 for(let q=0;q<2**aux.length;q++){let A=new Map(AS);aux.forEach((v,j)=>A.set(v,(q>>j)&1));let cost=0;for(let f of fs){if(++evals>2200000)throw Error("transport cap");cost+=f.cost[f.vs.reduce((s,v,j)=>s|(A.get(v)<<j),0)]}best=Math.min(best,cost)}
 let expected=2*Number(!C.some(l=>((w>>src.indexOf(Math.abs(l)))&1)===Number(l>0)));if(best!==expected)throw Error("energy mismatch");minrows.push(best);rows++}
 ownerInfo.push({id,owners:fs.flatMap(f=>f.ids),src,aux,minrows});
 }
 return {checks,evals,rows,maxAux,ownerInfo};
}
function feedback(C,n,pins=[]){
 const A0=()=>Array(n).fill(0),out=[];const fixed=new Map(pins);let reads=0;
 for(let init of [0,1])for(let mode of ["none","table","mod3"]){let A=A0().fill(init);for(let [v,b] of fixed)A[v]=b;
 const score=()=>{let bad=0,z=0;for(let c of C){let k=0,s=0;for(let l of c){reads++;let v=A[Math.abs(l)-1];let t=l>0?v:v-1;k+=t*t;s+=t}bad+=Number(!k);z+=Number(k>0&&s%3===0)}return [bad,z]};
 let cur=score(),initial=cur[0],steps=0,changed=0;if(mode!=="none")while(steps<4*n&&cur[0]){let options=[];for(let j=0;j<n;j++)if(!fixed.has(j)){A[j]^=1;let q=score();A[j]^=1;if(q[0]<cur[0])options.push([j,...q])}if(!options.length)break;options.sort((a,b)=>a[1]-b[1]||a[0]-b[0]);let old=options[0];if(mode==="mod3")options.sort((a,b)=>a[1]-b[1]||a[2]-b[2]||a[0]-b[0]);let best=options[0];changed+=Number(best[0]!==old[0]);A[best[0]]^=1;cur=score();steps++}
 out.push({init,mode,initial,final:cur[0],steps,changed})}return {out,reads};
}
module.exports={runReparam,transport,feedback};
