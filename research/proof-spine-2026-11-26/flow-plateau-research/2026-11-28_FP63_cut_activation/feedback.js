function feedback(C,width,mode,cap=180000){
 let work=0,ops={table:0,pairs:0,resolution:0,search:0,check:0},tick=(k,n=1)=>{if(work+n>cap)throw Error("cap");work+=n;ops[k]+=n},V=[...new Set(C.flat().map(Math.abs))].sort((a,b)=>a-b),D=C.map(a=>[...new Set(a)].sort((a,b)=>a-b)),key=a=>a.join(","),seen=new Set(D.map(key)),learn=[],moves=[],ties=0,peak=D.reduce((s,c)=>s+c.length,0)+V.length,decision="UNKNOWN",tree=null,nodes=0,reason=null,A;
 const flip=(mode==="flips"||mode==="table"||mode==="residue"),ded=(mode==="deductions"||mode==="table"||mode==="residue");
 const score=(A)=>D.map(c=>{let k=0,d=0;for(let l of c){tick("table");let x=A.get(Math.abs(l)),s=l>0?x:x-1;k+=s*s;d+=s}return [k,k%3,(d%3+3)%3]});
 const counts=T=>{let bad=0,z=0;for(let [k,r,d] of T){tick("table");bad+=Number(k===0);z+=Number(k>0&&d===0)}return [bad,z]};
 function optimize(init){let A=new Map(V.map(v=>[v,init])),T=score(A),q=counts(T),initial=q;for(let step=0;step<4*V.length;step++){let best=q[0],plain=null,pick=null,z=Infinity,bT;for(let v of V){A.set(v,1-A.get(v));let S=score(A),[bad,r]=counts(S);A.set(v,1-A.get(v));if(bad<best){best=bad;plain=v;pick=v;z=r;bT=S}else if(bad===best&&bad<q[0]&&mode==="residue"&&r<z){pick=v;z=r;bT=S}}if(pick===null)break;if(pick!==plain)ties++;A.set(pick,1-A.get(pick));moves.push({init,v:pick,plain,before:q,after:[best,z]});T=bT;q=counts(T)}return {A,T,q,initial}}
 try{
 // Unconditional early unit closure and exact original binary implications only; no unverified bits.
 let init=new Map();let changed=true;while(changed){changed=false;for(let c of D){let u=[],sat=false;for(let l of c){tick("search");if(!init.has(Math.abs(l)))u.push(l);else if(init.get(Math.abs(l))===Number(l>0)){sat=true;break}}if(sat)continue;if(!u.length){decision="UNSAT";tree=null;changed=false;break}if(u.length===1){init.set(Math.abs(u[0]),Number(u[0]>0));changed=true}}if(decision==="UNSAT")break}
 // Benchmark roots have no initial unit pins; stage unreachable if nonempty to avoid changing exact guard.
 if(init.size||decision==="UNSAT")return {mode,width,decision:"UNKNOWN",reason:"nonempty initial closure; stage not exercised",ops,work,learn,moves,ties};
 let seed=null;if(flip){let a=optimize(0),b=optimize(1);seed=a.q[0]<=b.q[0]?a:b;A=seed.A}
 if(ded){let order=D.map((_,i)=>i);if(seed)order.sort((a,b)=>seed.T[a][0]-seed.T[b][0]||a-b);outer:for(let i of order)for(let j of order){if(i>=j)continue;tick("pairs");for(let l of D[i])if(D[j].includes(-l)){let R=[...new Set([...D[i].filter(x=>x!==l),...D[j].filter(x=>x!==-l)])].sort((a,b)=>a-b);tick("resolution",D[i].length+D[j].length+R.length);if(R.length>width||R.some(v=>R.includes(-v))||seen.has(key(R)))continue;
 // independently check exact resolution with occurrence-set equality.
 let Q=new Set();for(let x of D[i])if(x!==l)Q.add(x);for(let x of D[j])if(x!==-l)Q.add(x);tick("check",D[i].length+D[j].length+R.length);if(Q.size!==R.length||!R.every(x=>Q.has(x)))throw Error("invalid resolvent");
 learn.push({i,j,pivot:l,row:R});D.push(R);seen.add(key(R));peak+=R.length;if(learn.length>=16)break outer;}}
 if(flip){let a=optimize(0),b=optimize(1);A=(a.q[0]<=b.q[0]?a:b).A}}
 function close(pins,k){let M=new Map(pins);while(true){let change=false,S=new Map();for(let c of D){let u=[],sat=false;for(let l of c){tick(k);if(!M.has(Math.abs(l)))u.push(l);else if(M.get(Math.abs(l))===Number(l>0)){sat=true;break}}if(sat)continue;if(!u.length)return null;if(u.length===1){M.set(Math.abs(u[0]),Number(u[0]>0));change=true}else for(let l of u)S.set(Math.abs(l),(S.get(Math.abs(l))||0)+1)}if(!change)return {M,S}}}
 function visit(pins){nodes++;let q=close(pins,"search");if(!q)return null;if(!q.S.size)throw Error("SAT found, witness not implemented in NO regression");let v=[...q.S].sort((a,b)=>b[1]-a[1]||a[0]-b[0])[0][0];let t=A?.get(v)||0,child=[];child[t]=visit([...q.M,[v,t]]);child[1-t]=visit([...q.M,[v,1-t]]);return [v,child[0],child[1]]}
 tree=visit([]);
 // separate row-oriented replay; does not call discovery closure.
 function check(pins,t){let M=new Map(pins);while(true){let ch=false;for(let c of D){let possible=c.filter(l=>{tick("check");return !M.has(Math.abs(l))||M.get(Math.abs(l))===Number(l>0)});if(!possible.length)return;if(possible.some(l=>M.has(Math.abs(l))))continue;if(possible.length===1){let l=possible[0];M.set(Math.abs(l),Number(l>0));ch=true}}if(!ch)break}if(!Array.isArray(t)||M.has(t[0]))throw Error("bad proof");check([...M,[t[0],0]],t[1]);check([...M,[t[0],1]],t[2])}
 check([],tree);decision="UNSAT";
 }catch(e){reason=e.message;if(!/cap|SAT found/.test(reason))throw e}
 return {mode,width,decision,reason,ops,work,learn,moves,ties,nodes,peakLogicalLiteralSlots:peak,tree:decision==="UNSAT"?tree:null}
}
if(typeof module!=="undefined")module.exports={feedback};
