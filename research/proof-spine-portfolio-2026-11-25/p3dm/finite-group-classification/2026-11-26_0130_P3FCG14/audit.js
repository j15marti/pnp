function audit(){
 const assert=(x,m)=>{if(!x)throw Error(m)};
 const cp=x=>JSON.parse(JSON.stringify(x));
 let next=0, fresh=0;
 function make(T){next=T.length;fresh=0;return {T:T.map((a,i)=>({i,a:a.map((v,c)=>c+":"+v)})),R:[...new Set(T.flatMap(a=>a.map((v,c)=>c+":"+v)))]}}
 const col=r=>+r[0], sz=P=>P.T.length+P.R.length;
 function balanced(P){let n=[0,0,0];for(const r of P.R)n[col(r)]++;return n[0]===n[1]&&n[1]===n[2]}
 function valid(P,S){let d=new Map(P.R.map(r=>[r,0]));for(const t of P.T)if(S.includes(t.i))for(const r of t.a){if(!d.has(r))return false;d.set(r,d.get(r)+1)}return [...d.values()].every(x=>x===1)}
 function all(P){assert(P.T.length<=20,"brute cap");let A=[];function rec(j,S,D){if(j===P.T.length){if(D.size===P.R.length)A.push([...S]);return}rec(j+1,S,D);let t=P.T[j];if(t.a.every(r=>!D.has(r))){t.a.forEach(r=>D.add(r));S.push(t.i);rec(j+1,S,D);S.pop();t.a.forEach(r=>D.delete(r))}}rec(0,[],new Set());return A}
 function graph(P){let V=[...P.R.map(r=>"r"+r),...P.T.map(t=>"t"+t.i)],E=P.T.flatMap(t=>t.a.map((r,c)=>({u:"t"+t.i,v:"r"+r,i:t.i,r,c}))),A=new Map(V.map(v=>[v,[]]));E.forEach((e,j)=>{A.get(e.u).push([e.v,j]);A.get(e.v).push([e.u,j])});return {V,E,A}}
 function components(g,skip=new Set()){let seen=new Set(),out=[];for(const v of g.V)if(!seen.has(v)){let a=[v];seen.add(v);for(let j=0;j<a.length;j++)for(const [u,e] of g.A.get(a[j]))if(!skip.has(e)&&!seen.has(u)){seen.add(u);a.push(u)}out.push(new Set(a))}return out}
 function signatures(g){let par=new Map(),pe=new Map(),dep=new Map(),tree=new Set();for(const root of g.V)if(!dep.has(root)){let q=[root];dep.set(root,0);for(let j=0;j<q.length;j++)for(const [v,e]of g.A.get(q[j]))if(!dep.has(v)){dep.set(v,dep.get(q[j])+1);par.set(v,q[j]);pe.set(v,e);tree.add(e);q.push(v)}}let a=g.E.map(()=>0n),b=1n;for(let j=0;j<g.E.length;j++)if(!tree.has(j)){let {u,v}=g.E[j];a[j]|=b;while(u!==v){if(dep.get(u)<dep.get(v))[u,v]=[v,u];a[pe.get(u)]|=b;u=par.get(u)}b<<=1n}let groups=new Map();a.forEach((x,j)=>{if(x){let k=x.toString();if(!groups.has(k))groups.set(k,[]);groups.get(k).push(j)}});return [...groups.values()].filter(g=>g.length>1)}
 function cuts(P,cap=12){let g=graph(P),out=[];for(const C of signatures(g))for(let a=0;a<C.length;a++)for(let b=a+1;b<C.length;b++){let E=[g.E[C[a]],g.E[C[b]]],cc=components(g,new Set([C[a],C[b]]));if(cc.length!==2)continue;for(const S of cc){if(!E.every(e=>S.has(e.u)!==S.has(e.v)))continue;let t=P.T.filter(t=>S.has("t"+t.i));if(t.length<=cap)out.push({S,E,tlen:t.length})}}return out.sort((a,b)=>a.tlen-b.tlen)}
 function local(P,S,E,w){let T=P.T.filter(t=>S.has("t"+t.i)),R=P.R.filter(r=>S.has("r"+r)),D=new Map(R.map(r=>[r,1])),pins=new Map();for(let j=0;j<2;j++){let e=E[j],v=w[j];if(S.has(e.u)){if(pins.has(e.i)&&pins.get(e.i)!==v)return [];pins.set(e.i,v)}else D.set(e.r,D.get(e.r)-v)}if([...D.values()].some(x=>x<0))return [];let out=[];function rec(j,L){if(j===T.length){if([...D.values()].every(x=>x===0))out.push([...L]);return}let t=T[j],p=pins.get(t.i),rows=t.a.filter(r=>D.has(r));if(p!==1)rec(j+1,L);if(p!==0&&rows.every(r=>D.get(r)>0)){rows.forEach(r=>D.set(r,D.get(r)-1));L.push(t.i);rec(j+1,L);L.pop();rows.forEach(r=>D.set(r,D.get(r)+1))}}rec(0,[]);return out}
 function conservation(P,S,E,w){let n=[0,0,0];for(const r of P.R)if(S.has("r"+r))n[col(r)]++;for(let j=0;j<2;j++)n[E[j].c]+=(S.has(E[j].u)?1:-1)*w[j];return n[0]===n[1]&&n[1]===n[2]}
 const words=[[0,0],[0,1],[1,0],[1,1]];
 function patch(P,cut){let {S,E}=cut, W=words.filter(w=>conservation(P,S,E,w));assert(W.length<=2,"conservation bound");let table=new Map();for(const w of W){let z=local(P,S,E,w);if(z.length)table.set(w.join(""),z)}
 let Q={T:cp(P.T.filter(t=>!S.has("t"+t.i))),R:P.R.filter(r=>!S.has("r"+r))},old=new Set(Q.T.map(t=>t.i)),K=new Set([...P.R.map(r=>"r"+r),...P.T.map(t=>"t"+t.i)].filter(v=>!S.has(v)));
 if(!table.size)return {no:true,table};
 let fixed=[],decode,type;
 if(table.size===1){let key=[...table.keys()][0],w=key.split("").map(Number),covered=new Set(),off=new Set(),on=new Set();for(let j=0;j<2;j++){let e=E[j];if(K.has(e.u)){(w[j]?on:off).add(e.i)}else if(w[j]){if(covered.has(e.r))return {no:true,table};covered.add(e.r)}}for(const i of on){if(off.has(i))return {no:true,table};let t=Q.T.find(t=>t.i===i);for(const r of t.a.filter(r=>Q.R.includes(r))){if(covered.has(r))return {no:true,table};covered.add(r)}fixed.push(i)}Q.T=Q.T.filter(t=>!on.has(t.i)&&!off.has(t.i)&&!t.a.some(r=>covered.has(r)));Q.R=Q.R.filter(r=>!covered.has(r));decode=()=>key;type="singleton";
 }else{assert(E[0].c===E[1].c,"different colors with two states");let c=E[0].c,o=E.map(e=>K.has(e.u)),row=()=>c+":g"+fresh++;
 if(o[0]!==o[1]){let j=o[0]?0:1,k=1-j;let t=Q.T.find(t=>t.i===E[j].i);t.a[c]=E[k].r;decode=L=>L.includes(E[j].i)?"11":"00";type="equal";
 }else if(o[0]){let r=row();Q.R.push(r);for(const e of E)Q.T.find(t=>t.i===e.i).a[c]=r;decode=L=>E.map(e=>+L.includes(e.i)).join("");type="out-complement";
 }else{let r=[0,1,2].map(d=>d===c?null:d+":g"+fresh++);Q.R.push(...r.filter(Boolean));let ids=E.map(e=>{let a=[...r];a[c]=e.r;let i=next++;Q.T.push({i,a});return i});decode=L=>ids.map(i=>+L.includes(i)).join("");type="in-complement"}
 }
 if(!balanced(Q))return {no:true,table};
 assert(Q.T.every(t=>t.a.every(r=>Q.R.includes(r))),"dangling edge");
 return {Q,table,type,liftAll:L=>{let key=decode(L),z=table.get(key);assert(z,"invalid decoded word");return z.map(S=>[...L.filter(i=>old.has(i)),...fixed,...S])}};
 }
 function projected(P,c,d,forced){let R=P.R.filter(r=>col(r)===c),used=new Set(),M=new Map(),u0=forced?.a[c],v0=forced?.a[d];if(forced)used.add(v0);let A=new Map(R.map(r=>[r,[]]));for(const t of P.T)if(t.a[c]!==u0&&!used.has(t.a[d]))A.get(t.a[c]).push(t.a[d]);function aug(u,seen){for(const v of A.get(u)){if(seen.has(v))continue;seen.add(v);if(!M.has(v)||aug(M.get(v),seen)){M.set(v,u);return true}}return false}return R.every(u=>u===u0||aug(u,new Set()))}
 function closure(P,stats){P=cp(P);let fixed=[];for(;;){if(!balanced(P))return {no:true};let row=new Map(P.R.map(r=>[r,[]]));for(const t of P.T)for(const r of t.a)row.get(r).push(t);if([...row.values()].some(a=>!a.length))return {no:true};let one=[...row.values()].find(a=>a.length===1);if(one){let t=one[0],S=new Set(t.a);fixed.push(t.i);P.T=P.T.filter(u=>!u.a.some(r=>S.has(r)));P.R=P.R.filter(r=>!S.has(r));continue}let del=new Set();for(const [c,d]of [[0,1],[0,2],[1,2]]){stats.pm++;if(!projected(P,c,d))return {no:true};let seen=new Map();for(const t of P.T){let k=t.a[c]+"|"+t.a[d];if(!seen.has(k)){stats.pm++;seen.set(k,projected(P,c,d,t))}if(!seen.get(k))del.add(t.i)}}if(!del.size)return {P,fixed};P.T=P.T.filter(t=>!del.has(t.i))}}
 function solve(P,stats,depth=0){stats.nodes++;let C=closure(P,stats);if(C.no)return {status:"NO"};let Q=C.P;if(Q.T.length<=12){let z=all(Q);return z.length?{status:"YES",w:[...C.fixed,...z[0]]}:{status:"NO"}}let cc=components(graph(Q));if(cc.length>1){let w=[...C.fixed],unknown=false;for(const S of cc){let R={T:Q.T.filter(t=>S.has("t"+t.i)),R:Q.R.filter(r=>S.has("r"+r))},z=solve(R,stats,depth+1);if(z.status==="NO")return z;if(z.status==="UNKNOWN")unknown=true;else w.push(...z.w)}return unknown?{status:"UNKNOWN"}:{status:"YES",w}}
 for(const cut of cuts(Q)){if(cut.S.size<=4)continue;let a=patch(Q,cut);stats.attempt++;if(a.no)return {status:"NO"};if(sz(a.Q)>=sz(Q))continue;stats.types[a.type]=(stats.types[a.type]||0)+1;let z=solve(a.Q,stats,depth+1);if(z.status!=="YES")return z;return {status:"YES",w:[...C.fixed,...a.liftAll(z.w)[0]]}}return {status:"UNKNOWN"}}
 const base=[[0,0,0],[1,1,1],[0,0,1],[1,1,0]];
 function chain(k){let T=Array.from({length:k},(_,i)=>base.map(t=>t.map(x=>x+2*i))).flat();for(let i=0;i<k-1;i++){let [d,r]=i%2===0?[i,i+1]:[i+1,i],row=d===i?0:1,rr=r===i+1?1:0,D=[],R=[];for(let j=0;j<4;j++){if(T[4*d+j][1]===2*d+row)D.push(4*d+j);if(T[4*r+j][1]===2*r+rr)R.push(4*r+j)}assert(D.length===2&&R.length===2,"chain");T[R[1]][1]=2*k+i;T[D[0]][1]=2*r+rr;T[D[1]][1]=2*k+i}return T}
 const B=["001","002","010","020","101","110","111","202","220","222"].map(s=>s.split("").map(Number));
 function ring(k){let T=Array.from({length:k},(_,i)=>B.map(t=>t.map(x=>x+3*i))).flat();for(let i=0;i<k;i++)T[i*10][1]=3*((i+1)%k);return T}
 let result={exactCuts:0,sourceCases:0,types:{},scales:[],neighbors:[],smallSources:[]};
 function cutAudit(P){let orig=all(P),key=z=>z.slice().sort((a,b)=>a-b).join(","),ref=orig.map(key).sort().join("|");for(const cut of cuts(P,12)){let a=patch(P,cut);let lift=a.no?[]:all(a.Q).flatMap(z=>a.liftAll(z));assert(lift.every(z=>valid(P,z)),"cut witness");assert(lift.map(key).sort().join("|")===ref,"exact full support");result.exactCuts++;let type=a.no?"empty":a.type;result.types[type]=(result.types[type]||0)+1}result.sourceCases++}
 for(let k of [2,3,4,5])cutAudit(make(chain(k)));
 cutAudit(make(ring(2)));
 // All eight tuple subinstances on the 2x2x2 cube (all subsets), preserving empty owner rows.
 const cube=Array.from({length:8},(_,i)=>[i>>2&1,i>>1&1,i&1]);
 for(let mask=0;mask<256;mask++){let P=make(cube.filter((_,j)=>mask>>j&1));P.R=["0:0","0:1","1:0","1:1","2:0","2:1"];let z=all(P),stats={nodes:0,pm:0,attempt:0,types:{}},q=solve(P,stats);assert((q.status==="YES")===!!z.length,"small cube");if(q.status==="YES")assert(valid(P,q.w),"small witness");result.smallSources.push({mask,status:q.status});if(components(graph(P)).length===1)cutAudit(P)}
 function trial(T,label){let P=make(T),stats={nodes:0,pm:0,attempt:0,types:{}},z=solve(P,stats);if(z.status==="YES")assert(valid(P,z.w),"scale witness");return {label,m:T.length,status:z.status,stats,w:z.w}}
 for(const k of [2,4,8,16,32])result.scales.push(trial(chain(k),"complement chain "+k));
 for(const k of [2,4,8,16])result.scales.push(trial(ring(k),"prior series ring "+k));
 // Neighbors: force phase 0 in block 0; then forbid required opposite phase in block 1.
 for(const k of [2,4,8,16]){let T=chain(k);let A=T.filter((_,i)=>i!==2);let D=T.filter((_,i)=>i!==2&&i!==6);let y=trial(A,"SAT "+k),n=trial(D,"UNSAT "+k);assert(y.status==="YES"&&n.status==="NO","neighbor");result.neighbors.push(y,n)}
 return result;
}
console.log(JSON.stringify(audit(),null,2));
