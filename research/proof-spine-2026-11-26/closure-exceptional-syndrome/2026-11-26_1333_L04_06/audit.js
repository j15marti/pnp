function run(){
let assertions=0;const check=(x)=>{assertions++;if(!x)throw Error("assert "+assertions)};
const frame=s=>"1".repeat(s.length)+"0"+s,bin=n=>n.toString(2);
function source(k,mode,t,N){
 const n=k+1,Q=n*n, id=(x,y,m)=>{let r=m*Q+x*n+y;return r===1?Q-1:r===Q-1?1:r};
 let R=[];const edge=(a,b)=>R.push([a,0,0,b,0,0,2,2]);
 for(let x=0;x<=k;x++)for(let y=0;y<=k;y++){
 if(x<k&&!(mode==="blocked"&&x===k-1&&y===k))edge(id(x,y,0),id(x+1,y,0));
 if(y<k&&!(mode==="blocked"&&x===k&&y===k-1))edge(id(x,y,0),id(x,y+1,0));
 if(x<k&&y<k)edge(id(x,y,1),x===k-1&&y===k-1?1:id(x+1,y+1,1));
 }
 if(mode==="shortcut")edge(0,id(0,0,1));
 const w=frame(R.map(r=>r.map(z=>frame(bin(z))).join("")).join(""))+frame("")+frame(bin(t));
 return w+"0".repeat(Math.max(0,(N||w.length)-w.length));
}
function decode(w,k,meter){
 let p=0;function get(s,j){let z=j;while(s[z]==="1"){z++;meter(1)}if(s[z]!=="0"||2*z+1-j>s.length)throw Error("frame");meter(z-j+1);return[s.slice(z+1,2*z+1-j),2*z+1-j]}
 let a,x,t;[a,p]=get(w,p);[x,p]=get(w,p);[t,p]=get(w,p);meter(w.length-p);if(x!==""||!/^0*$/.test(w.slice(p))||!/^(0|1[01]*)$/.test(t))throw Error("promise");
 const T=Number.parseInt(t,2),n=k+1,Q=n*n,rows=[];if(!Number.isSafeInteger(T)||BigInt(T)>BigInt(w.length)**2n)throw Error("clock");
 let j=0;while(j<a.length){let r=[];for(let i=0;i<8;i++){let y;[y,j]=get(a,j);if(!/^(0|1[01]*)$/.test(y))throw Error("bin");r.push(parseInt(y,2))}
 if(r[0]===1||r[1]||r[2]||r[4]||r[5]||r[6]!==2||r[7]!==2||r[0]>=2*Q||r[3]>=2*Q)throw Error("rule");rows.push([r[0],r[3],rows.length]);
 }
 const coord=q=>{let r=q===1?Q-1:q===Q-1?1:q;let m=Math.floor(r/Q),z=r%Q;return [Math.floor(z/n),z%n,m]};
 let hash=2166136261;for(const b of w){hash=Math.imul(hash^b.charCodeAt(0),16777619);meter(1)}
 return {T,rows,coord,N:w.length,k,hash:(hash>>>0).toString(16).padStart(8,"0"),V:2*Q};
}
function budget(N){let used=0,cap=100*N;return {tick:n=>{used+=n;if(used>cap)throw Error("cap")},get:()=>used,cap}}
function projection(w,k,B){let F=decode(w,k,B.tick),adj=Array.from({length:k+1},()=>[]);for(const [u,v] of F.rows){adj[F.coord(v)[0]].push(F.coord(u)[0]);B.tick(1)}
 let D=Array(k+1).fill(Infinity),Q=[k];D[k]=0;for(let p=0;p<Q.length;p++)for(const j of adj[Q[p]]){B.tick(1);if(D[j]===Infinity){D[j]=D[Q[p]]+1;Q.push(j)}}
 if(D.some(x=>!Number.isFinite(x)))throw Error("unexpected projection");
 return {hash:F.hash,D,label:D[0]>F.T?"NO":"UNKNOWN"};
}
function cut(w,k,B){let F=decode(w,k,B.tick);for(const [u,v] of F.rows){B.tick(1);if(F.coord(v)[1]-F.coord(u)[1]>1)throw Error("cut");}return {hash:F.hash,k,label:k>F.T?"NO":"UNKNOWN"}}
function audit(w,k,B){let F=decode(w,k,B.tick),closed=true,viol=0;for(const [u,v] of F.rows){B.tick(1);let a=F.coord(u),b=F.coord(v);if(a[2]===0&&b[2]!==0)closed=false;if(b[0]+b[1]-a[0]-a[1]>1)viol++}return{hash:F.hash,closed,viol,label:"UNKNOWN"}}
function integrated(w,k,A,B,C,M){let F=decode(w,k,M.tick);check(A.hash===F.hash&&B.hash===F.hash&&C.hash===F.hash);
 let guard=C.closed,valid=guard;
 for(const [u,v] of F.rows){let a=F.coord(u),b=F.coord(v);M.tick(1);
 if(A.D[a[0]]-A.D[b[0]]>1||b[1]-a[1]>1)throw Error("bad import");
 if(a[2]===0&&(b[2]!==0||A.D[a[0]]-A.D[b[0]]+b[1]-a[1]>1))valid=false;
 }
 let bound=valid?A.D[0]+B.k:Math.max(A.D[0],B.k);
 // closure: only valid guard+potential deductions can restrict reachable states.
 if(bound>F.T)return{label:"NO",bound,guard:valid,lift:0};
 // additional constructive attempt: acquire a monotone concrete path via rule IDs.
 let outgoing=new Map();for(const [u,v,id] of F.rows){M.tick(1);if(!outgoing.has(u))outgoing.set(u,[]);outgoing.get(u).push([v,id]);}
 function tryPath(preferShortcut){let u=0,ids=[];while(u!==1&&ids.length<F.T){let opts=outgoing.get(u)||[],best=null;for(const e of opts){M.tick(1);let a=F.coord(u),b=F.coord(e[0]);if(b[0]+b[1]>a[0]+a[1]||(preferShortcut&&u===0&&b[2]===1)){if(!best||preferShortcut&&b[2]===1)best=e;}}if(!best)break;ids.push(best[1]);u=best[0];}
 if(u!==1)return null;let q=0;for(const i of ids){M.tick(1);const [a,b]=F.rows[i];check(a===q);q=b;}check(q===1&&ids.length<=F.T);return ids;}
 let path=tryPath(false)||tryPath(true);return{label:path?"YES":"UNKNOWN",bound,guard:valid,lift:path?path.length:0};
}
function reference(w,k,M){let F=decode(w,k,M.tick),adj=Array.from({length:F.V},()=>[]);for(const [u,v] of F.rows){M.tick(1);adj[u].push(v)}
 let d=Array(F.V).fill(-1),q=[0];d[0]=0;for(let i=0;i<q.length;i++)for(const v of adj[q[i]]){M.tick(1);if(d[v]<0){d[v]=d[q[i]]+1;q.push(v)}}
 return d[1]<0?null:d[1];
}
let records=[],tot={A:0,B:0,C:0,combined:0,reference:0},summary={YES:0,NO:0,UNKNOWN:0};
for(const k of [2,4,8,16,32,64]){
 const inputs=[["deadlineYES","normal",2*k],["deadlineNO","normal",2*k-1],["shortcutYES","shortcut",2*k-1],["blockedNO","blocked",2*k]];
 let N=Math.max(...inputs.map(([_,m,t])=>source(k,m,t).length));
 for(const [name,m,t] of inputs){
  const w=source(k,m,t,N);check(w.length===N);const a=budget(N),b=budget(N),c=budget(N),d=budget(N),r=budget(N);
  const A=projection(w,k,a),B=cut(w,k,b),C=audit(w,k,c),I=integrated(w,k,A,B,C,d),dist=reference(w,k,r),truth=dist!==null&&dist<=t?"YES":"NO";
  check(A.label==="UNKNOWN"&&B.label==="UNKNOWN"&&C.label==="UNKNOWN");
  check(I.label==="UNKNOWN"||I.label===truth);check(I.bound<=(dist===null?Infinity:dist));
  check(C.viol>0);check(C.closed===(m!=="shortcut"));check(I.guard===(m!=="shortcut"));
  check(name==="blockedNO"?I.label==="UNKNOWN":I.label===truth);
  check(dist===(m==="blocked"?null:m==="shortcut"?k+1:2*k));
  summary[I.label]++;let ops={A:a.get(),B:b.get(),C:c.get(),combined:d.get(),reference:r.get()};for(let z in ops)tot[z]+=ops[z];
  check(ops.A+ops.B+ops.C+ops.combined<=400*N);records.push({k,N,name,t,hash:A.hash,dist,A:A.label,B:B.label,C:C.label,combined:I.label,bound:I.bound,guard:I.guard,unguardedViolations:C.viol,lift:I.lift,ops});
 }
}
return{assertions,summary,tot,records,scope:"finite-control U_2, original rule IDs; independent sequential replicas; instrumented scan/event units not bit-time measurements; proposed coordinate chart k checked, not universal acquisition"};
}
console.log(JSON.stringify(run(),null,2));
