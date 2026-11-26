function audit(){
 const out=[],F=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
 let assertions=0;function ok(v){assertions++;if(!v)throw Error("assertion "+assertions)}
 function make(k,no){const n=7*k, ts=[];for(let j=0;j<k;j++)for(let i=0;i<7;i++)if(i!==0||(no&&j===0))ts.push(F[i].map(x=>x+7*j));
 const base=ts.length;for(let i=0;i<n;i++)for(let j=0;j<6;j++)ts.push([i,n+(i+j)%n,2*n+(i+2*j)%n]);let cs=ts.map((t,i)=>[...t,3*n+i]);return {n,base,cs,vars:3*n+cs.length}}
 function reverse(q){return {...q,cs:q.cs.map(c=>c.map(x=>q.vars-1-x).reverse()).reverse()}}
 function analyze(cs,V){const deg=new Int32Array(V);for(const c of cs){ok(c.length===4&&new Set(c).size===4);for(const x of c)deg[x]++}
 const core=[],ts=[],w=[];for(let x=0;x<V;x++)if(deg[x]>1)core.push(x);
 const pair=new Set();for(const c of cs){let p=c.filter(x=>deg[x]===1);ok(p.length===1);w.push(p[0]);let t=c.filter(x=>x!==p[0]);ts.push(t);
 for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){let a=Math.min(t[i],t[j]),b=Math.max(t[i],t[j]),key=a+":"+b;ok(!pair.has(key));pair.add(key)}}
 return {deg,core,ts,w,pair}}
 function propagate(cs,V,pins){let d=new Int8Array(V);d.fill(-1);for(const [x,b] of pins){if(d[x]!==-1&&d[x]!==b)return null;d[x]=b}
 let change=true;while(change){change=false;for(const c of cs){let s=0,u=[];for(const x of c){if(d[x]===-1)u.push(x);else s+=d[x]}if(s>2||s+u.length<2)return null;if(u.length&&(s===2||s+u.length===2)){let b=s===2?0:1;for(const x of u){d[x]=b;change=true}}}}
 return d}
 function closure(cs,V,pins=[]){let d=propagate(cs,V,pins),probes=0,forced=0;if(!d)return {no:true,probes,forced};let progress=true;
 while(progress){progress=false;const p=Array.from(d.entries()).filter(z=>z[1]!==-1);
 for(let x=0;x<V;x++)if(d[x]===-1){let a=propagate(cs,V,[...p,[x,0]]),b=propagate(cs,V,[...p,[x,1]]);probes+=2;if(!a&&!b)return {no:true,probes,forced};if(!a||!b){d=(!a?b:a);forced++;progress=true;break}}}return {no:false,probes,forced}}
 function lpPins(q,a){let cnt=0;for(let x=0;x<q.vars;x++)for(let bit=0;bit<2;bit++){let val=new Int8Array(q.vars);val.fill(3);if(a.deg[x]>1)val[x]=0;else{let i=a.w.indexOf(x);for(const y of a.ts[i])val[y]=4}
 for(let i=0;i<a.ts.length;i++)val[a.w[i]]=12-a.ts[i].reduce((s,y)=>s+val[y],0);if(bit)for(let y=0;y<val.length;y++)val[y]=6-val[y];ok(val[x]===6*bit);ok(val.every(v=>v>=0&&v<=6));for(const c of q.cs)ok(c.reduce((s,y)=>s+val[y],0)===12);cnt++}return cnt}
 function triAudit(a){const rows=a.core.map(x=>[[x,1]]).concat(a.ts.map(t=>t.slice().sort((a,b)=>a-b).map(x=>[x,2])));
 function norm(row){if(!row.length)return "";let k=row[0][1];return row.map(([x,y])=>x+":"+((y*k)%3)).join(",")}
 let keys=new Set(rows.map(norm));ok(keys.size===rows.length&&!keys.has(""));let checks=0;
 for(let i=0;i<rows.length;i++)for(let j=i+1;j<rows.length;j++)for(let sign of [1,2]){
 let z=new Map(rows[i]);for(const [x,y] of rows[j])z.set(x,((z.get(x)||0)+sign*y)%3);let key=norm([...z].filter(p=>p[1]).sort((a,b)=>a[0]-b[0]));ok(key!==""&&!keys.has(key));checks++}
 return checks}
 function seamCheck(a,exhaust){const core=a.core,adj=new Map(core.map(x=>[x,new Set()]));for(const t of a.ts)for(const x of t)for(const y of t)if(x!==y)adj.get(x).add(y);
 const adj2=core.map(x=>[...adj.get(x)]);const map=new Map(core.map((x,i)=>[x,i]));const adj3=adj2.map(v=>v.map(x=>map.get(x)));let tested=0,visited=new Int8Array(core.length),blocked=new Int8Array(core.length),queue=new Int32Array(core.length);
 function test(ids){blocked.fill(0);visited.fill(0);for(const i of ids)blocked[i]=1;let u=blocked.indexOf(0);let tail=1,head=0;queue[0]=u;visited[u]=1;while(head<tail){let v=queue[head++];for(const j of adj3[v])if(!blocked[j]&&!visited[j]){visited[j]=1;queue[tail++]=j}}ok(tail===core.length-ids.length);tested++}
 if(exhaust){function rec(start,ids){test(ids);if(ids.length===4)return;for(let i=start;i<core.length;i++)rec(i+1,[...ids,i])}rec(0,[])}
 else{let seed=20261126;for(let i=0;i<512;i++){let s=new Set();while(s.size<4){seed=(Math.imul(seed,1664525)+1013904223)>>>0;s.add(seed%core.length)}test([...s])}}
 return tested}
 function retract(a){let low=new Set(a.core.filter(x=>a.deg[x]===6)),adj=new Map([...low].map(x=>[x,[]])),keep=[],remove=[];
 for(let i=0;i<a.ts.length;i++){let t=a.ts[i],l=t.filter(x=>low.has(x));if(!l.length){keep.push(i);continue}if(l.length!==2)return null;adj.get(l[0]).push(l[1]);adj.get(l[1]).push(l[0]);remove.push(i)}
 const bits=new Map();for(const x of low)if(!bits.has(x)){bits.set(x,0);let q=[x];for(let i=0;i<q.length;i++){let u=q[i];for(let v of adj.get(u)){if(bits.has(v)){if(bits.get(u)===bits.get(v))return null}else{bits.set(v,1-bits.get(u));q.push(v)}}}}
 return {low,bits,keep,remove}}
 function solve(q,a,r,pins=[]){const retain=new Set(r.keep.flatMap(i=>a.ts[i]));if(pins.some(([x])=>!retain.has(x)))return {status:"UNKNOWN"};
 let reduced=r.keep.map(i=>q.cs[i]);let c=closure(reduced,q.vars,pins);if(c.no)return {status:"UNSAT",probes:c.probes,forced:c.forced,words:0};
 let adj=new Map([...retain].map(x=>[x,[]]));for(const i of r.keep)for(const x of a.ts[i])for(const y of a.ts[i])if(x!==y)adj.get(x).push(y);
 let bits=new Map(r.bits),seen=new Set(),words=0;for(const x of retain)if(!seen.has(x)){let vs=[x];seen.add(x);for(let i=0;i<vs.length;i++)for(const y of adj.get(vs[i]))if(!seen.has(y)){seen.add(y);vs.push(y)}
 if(vs.length>14)return {status:"UNKNOWN",words};let set=new Set(vs),rows=r.keep.filter(i=>set.has(a.ts[i][0])),p=pins.filter(([v])=>set.has(v));let chosen=null;
 for(let mask=0;mask<2**vs.length;mask++){words++;const z=new Map(vs.map((v,i)=>[v,(mask>>i)&1]));if(p.every(([v,b])=>z.get(v)===b)&&rows.every(i=>{let s=a.ts[i].reduce((s,v)=>s+z.get(v),0);return s===1||s===2})){chosen=z;break}}
 if(!chosen)return {status:"UNSAT",words,probes:c.probes,forced:c.forced};for(const [v,b] of chosen)bits.set(v,b)}
 for(let i=0;i<a.ts.length;i++){let s=a.ts[i].reduce((s,v)=>s+bits.get(v),0);ok(s===1||s===2);bits.set(a.w[i],2-s)}
 for(const row of q.cs)ok(row.reduce((s,v)=>s+bits.get(v),0)===2);ok(pins.every(([x,b])=>bits.get(x)===b));return {status:"SAT",words,probes:c.probes,forced:c.forced}}
 for(let k of [2,4,8,16])for(let no of [false,true]){let q=reverse(make(k,no)),a=analyze(q.cs,q.vars);let cl=closure(q.cs,q.vars);ok(!cl.no&&cl.forced===0);let lp=lpPins(q,a),tri=triAudit(a);let cuts=seamCheck(a,k===2&&!no);
 let stagnation=closure(q.cs,q.vars);ok(!stagnation.no&&stagnation.forced===0);let r=retract(a);ok(r!==null&&r.remove.length===6*q.n&&r.keep.length===q.base);let ans=solve(q,a,r);ok(ans.status===(no?"UNSAT":"SAT"));let guards=[];
 if(!no&&k===2){for(let p of [[[q.vars-1,0]],[[q.vars-1,1]],[[q.vars-1,0],[q.vars-2,1]]]){let z=solve(q,a,r,p);ok(z.status===(p.length===2?"UNSAT":"SAT"));guards.push(z)}}
 out.push({k,no,n:q.n,variables:q.vars,clauses:q.cs.length,maxDegree:Math.max(...a.deg),closureProbes:cl.probes+stagnation.probes,lpPins:lp,trianglePairTests:tri,coreDeletionTests:cuts,removed:r.remove.length,retained:r.keep.length,answer:ans,guards})}
 return {cases:out,assertions,notes:"Exhaustive core deletions through four on first SAT control; 512 deterministic four-deletion samples per other job. Original Fano module reference bounded enumeration; all IDs and clause orders reversed. No generic matching/TU/SDP backend."}
}
console.log(JSON.stringify(audit(),null,2));
