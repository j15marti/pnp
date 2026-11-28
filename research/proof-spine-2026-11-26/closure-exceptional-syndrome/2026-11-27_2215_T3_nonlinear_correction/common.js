function sha(s){let k=[],h=[],p=2;while(k.length<64){if(!Array.from({length:Math.floor(Math.sqrt(p))-1},(_,i)=>i+2).some(i=>p%i===0)){if(h.length<8)h.push((Math.sqrt(p)%1*4294967296)|0);k.push((Math.cbrt(p)%1*4294967296)|0)}p++}const a=Array.from(s,ch=>ch.charCodeAt(0));if(a.some(x=>x>127)||a.length*8>=2**32)throw Error("hash input cap");const n=a.length*8;a.push(128);while(a.length%64!==56)a.push(0);a.push(0,0,0,0,(n>>>24)&255,(n>>>16)&255,(n>>>8)&255,n&255);const rr=(v,n)=>(v>>>n)|(v<<(32-n));for(let i=0;i<a.length;i+=64){let w=[];for(let j=0;j<16;j++)w[j]=(a[i+4*j]<<24)|(a[i+4*j+1]<<16)|(a[i+4*j+2]<<8)|a[i+4*j+3];for(let j=16;j<64;j++){let x=w[j-15],y=w[j-2];w[j]=(w[j-16]+(rr(x,7)^rr(x,18)^(x>>>3))+w[j-7]+(rr(y,17)^rr(y,19)^(y>>>10)))|0}let [A,B,C,D,E,F,G,H]=h;for(let j=0;j<64;j++){let t=(H+(rr(E,6)^rr(E,11)^rr(E,25))+((E&F)^(~E&G))+k[j]+w[j])|0,u=((rr(A,2)^rr(A,13)^rr(A,22))+((A&B)^(A&C)^(B&C)))|0;[A,B,C,D,E,F,G,H]=[(t+u)|0,A,B,C,(D+t)|0,E,F,G]}h=h.map((v,j)=>(v+[A,B,C,D,E,F,G,H][j])|0)}return h.map(v=>(v>>>0).toString(16).padStart(8,"0")).join("")}
function compile(instance){
const lines=instance.dimacs.trimEnd().split("\n"),h=lines.shift().split(" ").map((s,i)=>i>=2?Number(s):s);if(h[0]!=="p"||h[1]!=="cnf"||h[2]!==instance.nvars||h[3]!==lines.length)throw Error("header");
const n=instance.nvars,F=[],parents=[];let next=n;const add=(a,id)=>{F.push(a);parents.push(id)};
lines.forEach((line,i)=>{const a=line.split(/\s+/).map(Number);if(a.pop()!==0||a.some(l=>!Number.isInteger(l)||!l||Math.abs(l)>n))throw Error("clause");const id=i+1;if(a.length===0){let v=++next;add([v,v,v],id);add([-v,-v,-v],id)}else if(a.length<=3){while(a.length<3)a.push(a[a.length-1]);add(a,id)}else{let prev=++next;add([a[0],a[1],prev],id);for(let j=2;j<a.length-2;j++){let t=++next;add([-prev,a[j],t],id);prev=t}add([-prev,a[a.length-2],a[a.length-1]],id)}});
const types=[],used=[],edges=[],groups=new Map(),reps={},owners=[];const V=(t,owner)=>{types.push(t);used.push(0);owners.push(owner);return types.length-1};const P=v=>{if(used[v]>=4)throw Error("port");return 4*v+used[v]++};const E=(a,b,s=0)=>edges.push([a,b,s]);const wire=(a,b,s)=>{const v=Array.from({length:5},()=>V("E",["wire",a,b]));for(let i=0;i<5;i++)for(let j=i+1;j<5;j++)if(i!==0||j!==1)E(P(v[i]),P(v[j]));E(a,P(v[0]),s);E(b,P(v[1]),0)};const occ=(id,s,p)=>{if(!groups.has(id))groups.set(id,[]);groups.get(id).push([p,s])};
F.forEach(([a,b,c],i)=>{const L=x=>["x"+Math.abs(x),Number(x<0)],z="z"+i,T=[[L(a),L(b),[z,0]],[[z,1],L(c),["f",0]]];for(let j=0;j<2;j++)for(let k=0;k<2;k++){let v=V("B",["clause",parents[i],i,j,k]);for(const [id,s] of T[j])occ(id,s,P(v));occ("w"+i+"_"+j,0,P(v))}});
for(const [id,O] of groups){if(O.length%2||O.length<2)throw Error("parity");reps[id]=O[0];if(O.length===2){wire(O[0][0],O[1][0],O[0][1]^O[1][1]);continue}const a=Array.from({length:(O.length-2)/2},()=>V("E",["carrier",id]));for(let i=1;i<a.length;i++)wire(P(a[i-1]),P(a[i]),0);let k=0;for(const v of a)while(used[v]<4){const [p,s]=O[k++];wire(P(v),p,s)}if(k!==O.length)throw Error("fanout")}
return{network:{format:"STRICT-EB4-v1",types,edges},source_map:{original_n:n,ternary_clauses:F,original_clause_ids:parents,representative_ports:reps,vertex_provenance:owners}}
}
function run(corpus,registry,peers){
const ck=(x,s)=>{if(!x)throw Error(s||"check")};ck(sha("")==="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855");ck(sha("abc")==="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad");
const sort=a=>[...new Set(a)].sort((a,b)=>a-b),cap=1000000,tick=(m,k=1)=>{m.events+=k;if(m.events>cap)throw Error("cap")};
function normal(G){
let n=4*G.types.length,A=Array.from({length:n},()=>[]),R=new Int32Array(n).fill(-1),P=new Uint8Array(n),seen=new Set(),edges=new Set(),arcs=0;const add=(a,b,s)=>{A[a].push([b,s]);A[b].push([a,s]);arcs+=2};
for(const [a,b,s] of G.edges){let u=a>>2,v=b>>2,k=[Math.min(u,v),Math.max(u,v)].join(":");ck(a>=0&&a<n&&b>=0&&b<n&&u!==v&&!edges.has(k)&&!seen.has(a)&&!seen.has(b)&&[0,1].includes(s));edges.add(k);seen.add(a);seen.add(b);add(a,b,s)}ck(seen.size===n);
G.types.forEach((t,v)=>{ck(t==="E"||t==="B");if(t==="E")for(let j=1;j<4;j++)add(4*v,4*v+j,0)});
for(let i=0;i<n;i++)if(R[i]<0){R[i]=i;let q=[i];for(let j=0;j<q.length;j++)for(let [v,s] of A[q[j]]){let b=P[q[j]]^s;if(R[v]<0){R[v]=i;P[v]=b;q.push(v)}else ck(R[v]===i&&P[v]===b)}}
let D=new Map();G.types.forEach((t,v)=>{if(t!=="B")return;let l=Array.from({length:4},(_,j)=>(R[4*v+j]+1)*(P[4*v+j]?-1:1)).sort((a,b)=>a-b),r=l.map(x=>-x).reverse();if(r.join(",")<l.join(","))l=r;let k=l.join(",");if(!D.has(k))D.set(k,{l,ids:[]});D.get(k).ids.push(v)});
let F=[...D.values()].map(({l,ids},id)=>{let vs=sort(l.map(Math.abs)),ok=[];for(let w=0;w<2**vs.length;w++)if(l.reduce((s,x)=>s+((w>>vs.indexOf(Math.abs(x))&1)^+(x<0)),0)===2)ok.push(w);return{id,vs,ok,ids}});
for(const [a,b,s] of G.edges)ck(R[a]===R[b]&&(P[a]^P[b])===s);
for(const f of F)for(const v of f.ids){let S=[];for(let w=0;w<2**f.vs.length;w++){let sum=0;for(let j=0;j<4;j++)sum+=(w>>f.vs.indexOf(R[4*v+j]+1)&1)^P[4*v+j];if(sum===2)S.push(w)}ck(JSON.stringify(S)===JSON.stringify(f.ok))}
return{F,R,P,arcs}
}
const pr=(w,U,V)=>V.reduce((s,v,i)=>s|((w>>U.indexOf(v)&1)<<i),0);
function project(F){let Q=F.slice(),seq=F.length,trace=[],scans=0,tests=0,checkTests=0;for(;;){let O=new Map();for(let f of Q)for(let v of f.vs){scans++;if(!O.has(v))O.set(v,[]);O.get(v).push(f)}let c=[...O].filter(([v,L])=>L.length<=2&&sort(L.flatMap(f=>f.vs)).length<=7).sort((a,b)=>a[1].length-b[1].length||a[0]-b[0]);if(!c.length)break;let [v,L]=c[0],U=sort(L.flatMap(f=>f.vs)),W=U.filter(x=>x!==v),S=new Set();for(let w=0;w<2**U.length;w++)if(L.every(f=>{tests++;return f.ok.includes(pr(w,U,f.vs))}))S.add(pr(w,U,W));let ok=sort([...S]),V=[];for(let w=0;w<2**W.length;w++){let a=new Map(W.map((x,i)=>[x,w>>i&1]));let yes=false;for(let b=0;b<2;b++){a.set(v,b);if(L.every(f=>{checkTests++;return f.ok.includes(f.vs.reduce((s,x,i)=>s|(a.get(x)<<i),0))}))yes=true}if(yes)V.push(w)}ck(V.join()===ok.join(),"projection");let t={v,in:L.map(f=>f.id),out:seq,vs:W,ok,ids:sort(L.flatMap(f=>f.ids))};trace.push(t);Q=Q.filter(f=>!L.includes(f));if(ok.length!==2**W.length)Q.push({id:seq,vs:W,ok,ids:t.ids});seq++}return{Q,trace,scans,tests,checkTests}}
function clauses(F){let C=[];for(let f of F)for(let w=0;w<2**f.vs.length;w++)if(!f.ok.includes(w))C.push(f.vs.map((v,i)=>(w>>i&1)?-v:v));return C}
function up(C,g,m,rev=false){let a=new Map();for(let l of g){if(a.has(Math.abs(l))&&a.get(Math.abs(l))!==+(l>0))return null;a.set(Math.abs(l),+(l>0))}for(;;){let ch=false;for(let i=0;i<C.length;i++){tick(m);let c=C[rev?C.length-i-1:i];if(c.some(l=>a.get(Math.abs(l))===+(l>0)))continue;let u=c.filter(l=>!a.has(Math.abs(l)));if(!u.length)return null;if(u.length===1){a.set(Math.abs(u[0]),+(u[0]>0));ch=true;if(rev)break}}if(!ch)return a}}
function tree(C,g,m){m.nodes=(m.nodes||0)+1;let a=up(C,g,m);if(!a)return 0;let f=new Map();for(let c of C){tick(m);if(!c.some(l=>a.get(Math.abs(l))===+(l>0)))for(let l of c)if(!a.has(Math.abs(l)))f.set(Math.abs(l),(f.get(Math.abs(l))||0)+1)}if(!f.size)return null;let v=[...f].sort((a,b)=>b[1]-a[1]||a[0]-b[0])[0][0],L=tree(C,g.concat(-v),m);if(L===null)return null;let H=tree(C,g.concat(v),m);return H===null?null:[v,L,H]}
function replay(C,g,t,m){if(t===0){ck(up(C,g,m,true)===null,"bad leaf");return}ck(Array.isArray(t)&&t.length===3&&!g.some(l=>Math.abs(l)===t[0]));replay(C,g.concat(-t[0]),t[1],m);replay(C,g.concat(t[0]),t[2],m)}
function solve(C,g){let m={events:0},t=null;try{t=tree(C,g,m)}catch(e){if(e.message!=="cap")throw e}let check={events:0};if(t!==null)replay(C,g,t,check);return{status:t===null?"UNKNOWN":"NO",m,check,t}}
const pins=g=>new Map(g.map(l=>[Math.abs(l),+(l>0)])),filter=(f,a)=>f.ok.filter(w=>f.vs.every((v,i)=>!a.has(v)||a.get(v)===(w>>i&1)));
function gac(F,g,m){let a=pins(g);for(;;){let ch=false;for(let f of F){tick(m,f.ok.length);let S=filter(f,a);if(!S.length)return true;for(let i=0;i<f.vs.length;i++){let v=f.vs[i],b=S[0]>>i&1;if(!a.has(v)&&S.every(w=>(w>>i&1)===b)){a.set(v,b);ch=true}}}if(!ch)return false}}
function ge(F,g,m,V){let a=pins(g),I=new Map(V.map((v,i)=>[v,i])),basis=new Map(),add=(w,b)=>{while(w){tick(m);let j=w.toString(2).length-1;if(!basis.has(j)){basis.set(j,[w,b]);return true}let [z,c]=basis.get(j);w^=z;b^=c}return b===0};for(let [v,b] of a)if(!add(1n<<BigInt(I.get(v)),b))return true;let par=x=>{let p=0;while(x){p^=1;x&=x-1}return p};for(let f of F){let S=filter(f,a);if(!S.length)return true;for(let mask=1;mask<2**f.vs.length;mask++){tick(m,S.length);let b=par(S[0]&mask);if(S.every(w=>par(w&mask)===b)){let z=0n;f.vs.forEach((v,i)=>{if(mask>>i&1)z|=1n<<BigInt(I.get(v))});if(!add(z,b))return true}}}return false}
function binary(F,g,m,V){let A=new Map(V.flatMap(v=>[[v,[]],[-v,[]]])),a=pins(g);const e=(u,v)=>A.get(u).push(v);g.forEach(l=>e(-l,l));for(let f of F){let S=filter(f,a);if(!S.length)return true;for(let i=0;i<f.vs.length;i++)for(let j=i;j<f.vs.length;j++)for(let b=0;b<2;b++)for(let c=0;c<2;c++){if(i===j&&b!==c)continue;tick(m,S.length);if(!S.some(w=>(w>>i&1)===b&&(w>>j&1)===c)){let x=f.vs[i]*(b?1:-1),y=f.vs[j]*(c?1:-1);e(x,-y);e(y,-x)}}}function reach(u,v){let q=[u],S=new Set(q);for(let j=0;j<q.length;j++)for(let z of A.get(q[j])){tick(m);if(z===v)return true;if(!S.has(z)){S.add(z);q.push(z)}}return false}return V.some(v=>reach(v,-v)&&reach(-v,v))}
function join(F,g,m){let a=pins(g),Q=F.map(f=>{let V=f.vs.filter(v=>!a.has(v));return{vs:V,ok:sort(filter(f,a).map(w=>pr(w,f.vs,V)))}});if(Q.some(f=>!f.ok.length))return true;Q=Q.filter(f=>f.ok.length!==2**f.vs.length);for(;;){let O=new Map();for(let f of Q)for(let v of f.vs){tick(m);if(!O.has(v))O.set(v,[]);O.get(v).push(f)}let L=[...O].map(([v,F])=>({v,F,U:sort(F.flatMap(f=>f.vs))})).filter(x=>x.U.length<=9).sort((a,b)=>a.U.length-b.U.length||a.v-b.v);if(!L.length)return false;let {v,F,U}=L[0],W=U.filter(x=>x!==v),S=new Set();for(let w=0;w<2**U.length;w++)if(F.every(f=>{tick(m);return f.ok.includes(pr(w,U,f.vs))}))S.add(pr(w,U,W));if(!S.size)return true;Q=Q.filter(f=>!F.includes(f));if(S.size!==2**W.length)Q.push({vs:W,ok:[...S]})}}
function mass(V,L,extra,M){let ans=0n;for(let s=0;s<2**L.length;s++){M.terms++;let a=new Map(),ok=true,par=0;const ins=l=>{let v=Math.abs(l),b=+(l>0);if(a.has(v)&&a.get(v)!==b)ok=false;a.set(v,b)};extra.forEach(ins);for(let i=0;i<L.length;i++)if(s>>i&1){par^=1;L[i].forEach(ins)}if(ok)ans+=(par?-1n:1n)*(1n<<BigInt(V.length-a.size))}return ans}
function greedy(V,pool){let L=[],M={terms:0},rows=[];for(let k=0;k<5;k++){let before=mass(V,L,[],M);if(!before)break;let best=null;for(let x of pool){let q=mass(V,L,x.g,M);if(best===null||q>best.q)best={...x,q}}if(!best||!best.q)break;L.push(best.g);let after=mass(V,L,[],M);ck(before-after===best.q);rows.push({...best,q:String(best.q),before:String(before),after:String(after)})}return{L,rows,terms:M.terms,remaining:String(mass(V,L,[],M))}}
function sample(V,L,C,seed){let M={terms:0},R=mass(V,L,[],M),samples=[],attempts=0;const next=()=>{seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return seed>>>0};if(!R)return{samples,terms:M.terms,attempts};let bits=(R-1n).toString(2).length;for(let t=0;t<32;t++){let r;do{attempts++;r=0n;for(let j=0;j<bits;j+=32)r=(r<<32n)|BigInt(next());r&=(1n<<BigInt(bits))-1n}while(r>=R);let p=[];for(let v of V){let q=mass(V,L,p.concat(-v),M);if(r<q)p.push(-v);else{p.push(v);r-=q}}ck(r===0n&&!L.some(g=>g.every(l=>p.includes(l))));let S=new Set(p),bad=C.map((c,i)=>c.every(l=>!S.has(l))?i:-1).filter(i=>i>=0);ck(bad.length>0,"candidate SAT");samples.push({word:p,bad:bad.length,firstBad:bad[0]})}return{samples,terms:M.terms,attempts}}
function peerReproof(peer,e,V,anchor,D,C,broad,local){
 const ch=peer.children[0],a=ch.artifact;ck(peer.instance_id===e.instance_id&&peer.original_N_bits===e.N_bits&&peer.guard_id==="EMPTY"&&peer.residual_id==="ROOT");let peerId="GUARD-v1:sha256:"+sha(JSON.stringify(["PNP-GUARD-v1",e.instance_id,a.schema,sha(JSON.stringify(a)+"\n")])+"\n");ck(peerId===ch.guard_id,"peer guard ID");
 if(a.anchor!==anchor-1||a.equations.length!==1||a.equations[0].ports.length!==2)return{status:"UNKNOWN map"};
 let eq=a.equations[0],uv=eq.ports.map(v=>v+1);if(!uv.every(v=>V.includes(v)&&D.R[v-1]===v-1&&D.P[v-1]===0))return{status:"UNKNOWN coordinates"};
 let split=[];for(let b=0;b<2;b++){let g=[(b?1:-1)*uv[0],((b^eq.b)?1:-1)*uv[1]],q=solve(C,g);split.push({g,proof:q})}
 if(!split.every(z=>z.proof.status==="NO"))return{status:"UNKNOWN reproof",split};
 let extra=split.map(z=>z.g.map(l=>-l));return{status:"NO guard",guard_id:peerId,artifact:a,split,hybrid:solve(C.concat(broad.map(z=>z.g.map(l=>-l)),extra),[]),greedy:greedy(V,broad.concat(split.map(z=>({kind:"peer-reproved",g:z.g,proof:z.proof})),local))}
}

function plateauProjection(C,V,mode,start){
 const t0=Date.now(),a=new Map(V.map(v=>[v,start])),mod=x=>(x%3+3)%3,occ=new Map(V.map(v=>[v,[]])),edges=new Map(V.map(v=>[v,new Set()]));
 C.forEach((c,i)=>{let vs=c.map(Math.abs);for(let v of vs){occ.get(v).push(i);for(let u of vs)if(u!==v)edges.get(v).add(u)}});
 let visits=0,audit=0,checks=0,changed=0,path=[],stalls=[],peak=0,firstPairAudit=null;
 const val=(c,flip)=>{let k=0,h=0;for(let l of c){visits++;if((a.get(Math.abs(l))^+flip.has(Math.abs(l)))===+(l>0)){k++;h+=l>0?1:-1}}return{k,km:mod(k),sm:mod(h)}};
 const bad=x=>+(x.k===0),tie=x=>+(x.k>0&&x.sm===0),key=x=>x.join(",");
 const exact=(S)=>{let f=new Set(S),b=0,z=0;for(let c of C){let k=0,h=0;for(let l of c){audit++;let v=Math.abs(l);if((a.get(v)^+f.has(v))===+(l>0)){k++;h+=l>0?1:-1}}b+=+(k===0);z+=+(k>0&&mod(h)===0)}return[b,z]};
 const pairs=[];for(let v of V)for(let u of edges.get(v))if(v<u)pairs.push([v,u]);pairs.sort((a,b)=>a[0]-b[0]||a[1]-b[1]);
 const triples=new Map();for(let p of pairs)for(let v of new Set([...edges.get(p[0]),...edges.get(p[1])]))if(!p.includes(v)){let S=[...p,v].sort((a,b)=>a-b);triples.set(key(S),S)}let T3=[...triples.values()].sort((a,b)=>a[0]-b[0]||a[1]-b[1]||a[2]-b[2]);
 const slots=V.length+2*pairs.length+3*T3.length+C.reduce((s,c)=>s+4*c.length,0)+3*C.length;peak=Math.max(peak,slots);
 for(let step=0;step<=C.length;step++){
  let T=C.map(c=>val(c,new Set())),base=T.reduce((s,x)=>s+bad(x),0),z0=T.reduce((s,x)=>s+tie(x),0);if(!base)return{status:"SAT candidate",word:[...a],path,stalls,visits,audit,checks,changed,peak,elapsedMs:Date.now()-t0};
  const score=S=>{checks++;let touched=new Set(S.flatMap(v=>occ.get(v))),gain=0,tieDelta=0,f=new Set(S);for(let i of touched){let q=val(C[i],f);gain+=bad(T[i])-bad(q);tieDelta+=tie(q)-tie(T[i])}return{S,gain,tie:z0+tieDelta}};
  let choose=null,plain=null;const search=L=>{let best=null,first=null;for(let S of L){let q=score(S);if(q.gain<=0)continue;if(!best||q.gain>best.gain){best=q;first=q}else if(q.gain===best.gain&&mode==="residue"&&q.tie<best.tie)best=q}return[best,first]};
  [choose,plain]=search(V.map(v=>[v]));
  if(!choose){let p=search(pairs),q=search(T3);let outside=0,positive=0; // independent exhaustive all-pairs check at first singleton plateau
   if(firstPairAudit===null){for(let i=0;i<V.length;i++)for(let j=i+1;j<V.length;j++){let S=[V[i],V[j]],ex=exact(S),d=base-ex[0];if(d>0){positive++;if(!edges.get(S[0]).has(S[1]))outside++}let m=score(S);if(m.gain!==d||m.tie!==ex[1])throw Error("pair score mismatch")}if(outside)throw Error("disconnected improving pair");firstPairAudit={positive,outside,total:V.length*(V.length-1)/2}}
   stalls.push({bad:base,bestPair:p[0]?.gain||0,bestTriple:q[0]?.gain||0,word:[...a]});
   [choose,plain]=p[0]?p:q;
  }
  if(!choose)return{status:"UNKNOWN plateau",bad:base,word:[...a],path,stalls,firstPairAudit,visits,audit,checks,changed,peak,pairs:pairs.length,triples:T3.length,elapsedMs:Date.now()-t0};
  let ex=exact(choose.S);if(base-ex[0]!==choose.gain||ex[1]!==choose.tie||choose.gain<=0)throw Error("accepted move");if(key(choose.S)!==key(plain.S))changed++;for(let v of choose.S)a.set(v,1-a.get(v));path.push({S:choose.S,plain:plain.S,gain:choose.gain,before:base,after:ex[0],tie:choose.tie});
 }
 throw Error("strict descent bound");
}
function retirement(C,V,width=4){
 const start=Date.now(),canon=c=>{let s=new Set(c);if([...s].some(l=>s.has(-l)))return null;return [...s].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b)},key=c=>c.join(","),sub=(a,b)=>a.every(l=>b.includes(l));
 let Q=[...new Map(C.map(c=>canon(c)).filter(c=>c!==null).map(c=>[key(c),c])).values()],W=V.slice(),trace=[],events=0,replay=0,peak=Q.reduce((s,c)=>s+c.length,0),cap=2000000,refusal=[];
 const tick=(n=1)=>{events+=n;if(events>cap)throw Error("cap")};
 function candidate(v){let A=Q.filter(c=>c.includes(v)),B=Q.filter(c=>c.includes(-v)),U=Q.filter(c=>!c.includes(v)&&!c.includes(-v)),R=new Map();if(!A.length&&!B.length)return{v,A,B,U,R:[],pairs:0};for(let a of A)for(let b of B){tick();let c=canon(a.filter(l=>l!==v).concat(b.filter(l=>l!==-v)));if(c===null)continue;if(U.some(d=>{tick();return d.length<=c.length&&sub(d,c)}))continue;if(c.length>width)return{v,reason:"width",witness:{a,b,c}};R.set(key(c),c);if(R.size>A.length+B.length)return{v,reason:"fill",count:R.size,removed:A.length+B.length}}let rr=[...R.values()];return{v,A,B,U,R:rr,pairs:A.length*B.length}}
 try{while(W.length&&!Q.some(c=>!c.length)){refusal=[];let best=null;for(let v of W){let t=candidate(v);if(t.reason){refusal.push(t);continue}if(!best||t.R.length-t.A.length-t.B.length<best.R.length-best.A.length-best.B.length||t.R.length-t.A.length-t.B.length===best.R.length-best.A.length-best.B.length&&t.pairs<best.pairs)best=t}if(!best)break;
 let {v,A,B,U,R}=best;
 // independently rederive complete pair set by complement check and verify each non-tautological resolvent is implied by a surviving or new clause.
 let check=new Set();for(let a of A)for(let b of B){let s=new Set([...a.filter(l=>l!==v),...b.filter(l=>l!==-v)]);replay++;if([...s].some(l=>s.has(-l)))continue;let c=canon([...s]);if(!U.concat(R).some(d=>{replay++;return sub(d,c)}))throw Error("missing projected resolvent");check.add(key(c))}
 for(let c of R)if(!check.has(key(c)))throw Error("invented resolvent");
 let next=U.concat(R);if(next.length>Q.length)throw Error("fill");trace.push({v,removed:A.concat(B),added:R,before:Q.length,after:next.length});Q=next;W=W.filter(w=>w!==v);peak=Math.max(peak,Q.reduce((s,c)=>s+c.length,0))}
 }catch(e){if(e.message!=="cap")throw e;return{status:"UNKNOWN cap",Q,W,trace,events,replay,peak,elapsedMs:Date.now()-start}}
 return{status:Q.some(c=>!c.length)?"NO empty":"UNKNOWN residual",Q,W,trace,refusal,events,replay,peak,elapsedMs:Date.now()-start}
}

function gaugeFactors(F,anchor){return F.map(f=>{let i=f.vs.indexOf(anchor);return i<0?f:{...f,vs:f.vs.filter(v=>v!==anchor),ok:f.ok.filter(w=>!(w>>i&1)).map(w=>(w&((1<<i)-1))|((w>>(i+1))<<i))}})}
function early(F,V,C){let a=new Map(),basis=new Map(),eqs=[],rowTests=0,affineOps=0,binaryArcs=0,binaryVisits=0,checks=0,iterations=0,history=[],I=new Map(V.map((v,i)=>[v,i]));let conflict=false;let bit=v=>1n<<BigInt(I.get(v));const par=x=>{let p=0;while(x){x&=x-1;p^=1}return p};function add(w,b){while(w){affineOps++;let j=w.toString(2).length-1;if(!basis.has(j)){basis.set(j,[w,b]);return true}let[z,c]=basis.get(j);w^=z;b^=c}return !b}function reduce(w,b){while(w){affineOps++;let j=w.toString(2).length-1;if(!basis.has(j))return false;let[z,c]=basis.get(j);w^=z;b^=c}return !b}
function set(v,b,reason){if(a.has(v)){if(a.get(v)!==b)conflict=true;return false}a.set(v,b);history.push({v,b,reason});return true}
for(;;){iterations++;let change=false;for(let c of C){rowTests++;if(c.some(l=>a.get(Math.abs(l))===+(l>0)))continue;let u=c.filter(l=>!a.has(Math.abs(l)));if(!u.length){conflict=true;break}if(u.length===1)change=set(Math.abs(u[0]),+(u[0]>0),"unit")||change}if(conflict)break;
let E=new Map(V.flatMap(v=>[[v,[]],[-v,[]]]));const edge=(u,v)=>{E.get(u).push(v);binaryArcs++};basis=new Map();eqs=[];for(let[v,b]of a)if(!add(bit(v),b)){conflict=true;break}
for(let f of F){let S=filter(f,a);rowTests+=f.ok.length;if(!S.length){conflict=true;break}
for(let i=0;i<f.vs.length;i++){let v=f.vs[i],b=S[0]>>i&1;if(S.every(w=>(w>>i&1)===b))change=set(v,b,"support")||change}
for(let mask=1;mask<2**f.vs.length;mask++){rowTests+=S.length;let b=par(S[0]&mask);if(S.every(w=>par(w&mask)===b)){let w=0n;f.vs.forEach((v,i)=>{if(mask>>i&1)w|=bit(v)});eqs.push({factor:f.id,mask,b});if(!add(w,b)){conflict=true;break}}}if(conflict)break;
for(let i=0;i<f.vs.length;i++)for(let j=i;j<f.vs.length;j++)for(let b=0;b<2;b++)for(let c=0;c<2;c++){if(i===j&&b!==c)continue;rowTests+=S.length;if(!S.some(w=>(w>>i&1)===b&&(w>>j&1)===c)){let u=f.vs[i]*(b?1:-1),v=f.vs[j]*(c?1:-1);edge(u,-v);edge(v,-u)}}}if(conflict)break;
for(let v of V)if(!a.has(v)){if(reduce(bit(v),0))change=set(v,0,"affine")||change;else if(reduce(bit(v),1))change=set(v,1,"affine")||change}
function reach(u,v){let q=[u],S=new Set(q);for(let i=0;i<q.length;i++)for(let z of E.get(q[i])){binaryVisits++;if(z===v)return true;if(!S.has(z)){S.add(z);q.push(z)}}return false}
for(let v of V)if(!a.has(v)){let p=reach(v,-v),n=reach(-v,v);if(p&&n){conflict=true;break}if(p)change=set(v,0,"binary")||change;if(n)change=set(v,1,"binary")||change}
if(conflict||!change)break}
return{pins:[...a].sort((a,b)=>a[0]-b[0]),history,rank:basis.size,eqs,rowTests,affineOps,binaryArcs,binaryVisits,iterations,conflict,checks}}
function canon(c){let s=new Set(c);if([...s].some(l=>s.has(-l)))return null;return [...s].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b)}
function simplify(C,pins){let a=new Map(pins);return C.map((c,i)=>({c:canon(c),id:i+1})).filter(r=>r.c!==null&&!r.c.some(l=>a.get(Math.abs(l))===+(l>0))).map(r=>({...r,c:r.c.filter(l=>!a.has(Math.abs(l)))}))}
function feedback(base,V,mode,width){
const start=Date.now(),maxPairs=6000,maxRows=48,maxRounds=3,maxScore=4000000;
let rows=base.map(r=>({...r,c:r.c.slice()})),next=Math.max(0,...rows.map(r=>r.id))+1,keys=new Set(rows.map(r=>r.c.join(","))),learned=[],pairs=0,score=0,residueOps=0,flips=0,changed=0,checks=0,proofChecks=0,phaseHistory=[],peakSlots=0,phases=[],capHit=false;
const mod=x=>(x%3+3)%3;
function fields(c,a,res){let k=0,s=0;for(let l of c){score++;if(a.get(Math.abs(l))===+(l>0)){k++;s+=l>0?1:-1}if(res)residueOps++}return{k,km:mod(k),sm:mod(s)}}
function runPhase(initial){let a=new Map(V.map(v=>[v,initial])),stalled=false,path=[],before=flips;for(;;){let T=rows.map(r=>fields(r.c,a,mode==="residue")),bad=T.filter(t=>!t.k).length;let best=0,chosen=null,plain=null,bestTie=Infinity;peakSlots=Math.max(peakSlots,rows.reduce((s,r)=>s+r.c.length+4,0)+2*V.length+3*T.length);
if(score>maxScore){capHit=true;return{a,T,bad,path,stalled:false}}
for(let v of V){a.set(v,1-a.get(v));let Q=rows.map(r=>fields(r.c,a,mode==="residue"));a.set(v,1-a.get(v));let gain=bad-Q.filter(t=>!t.k).length,tie=Q.filter(t=>t.k>0&&t.sm===0).length;if(gain>best){best=gain;chosen=v;plain=v;bestTie=tie}else if(gain===best&&gain>0&&mode==="residue"&&tie<bestTie){chosen=v;bestTie=tie}}
if(score>maxScore){capHit=true;return{a,T,bad,path,stalled:false}}
if(!chosen){stalled=true;return{a,T,bad,path,stalled}}
if(chosen!==plain)changed++;a.set(chosen,1-a.get(chosen));flips++;path.push({v:chosen,plain,gain:best,residueTieChanged:chosen!==plain});}}
function resolvent(a,b,p){if(!a.includes(p)||!b.includes(-p))return null;return canon(a.filter(l=>l!==p).concat(b.filter(l=>l!==-p)))}
function learn(prior){let n=rows.length,order=Array.from({length:n},(_,i)=>i);if(prior)order.sort((i,j)=>Number(prior[i].k!==0)-Number(prior[j].k!==0)||i-j);let gained=0;
outer:for(let i of order)for(let j=0;j<n;j++){if(i===j)continue;if(++pairs>maxPairs){capHit=true;break outer}for(let p of rows[i].c){if(!rows[j].c.includes(-p))continue;let c=resolvent(rows[i].c,rows[j].c,p);if(!c||c.length>width||keys.has(c.join(",")))continue;let id=next++,r={id,c,parents:[rows[i].id,rows[j].id],pivot:p};rows.push(r);learned.push(r);keys.add(c.join(","));gained++;if(learned.length>=maxRows||gained>=16||!c.length)break outer}}
return gained}
let firstRows=base.map(r=>({id:r.id,literals:r.c,allFalse:{k:r.c.filter(l=>l<0).length,km:r.c.filter(l=>l<0).length%3,sm:mod(-r.c.filter(l=>l<0).length)},allTrue:{k:r.c.filter(l=>l>0).length,km:r.c.filter(l=>l>0).length%3,sm:r.c.filter(l=>l>0).length%3}}));
if(mode!=="baseline"){for(let round=0;round<maxRounds;round++){let phase=null;if(mode!=="deductions"){let p0=runPhase(0),p1=runPhase(1);for(let p of [p0,p1])phases.push({round,bad:p.bad,path:p.path,stalled:p.stalled,word:[...p.a],fields:p.T});phase=p0.bad<=p1.bad?p0:p1;if(mode==="flips"||capHit)break}
let gained=learn(mode==="deductions"?null:phase.T);if(!gained||capHit||rows.some(r=>!r.c.length)||learned.length>=maxRows)break}}
let by=new Map(base.map(r=>[r.id,r.c]));for(let r of learned){let a=by.get(r.parents[0]),b=by.get(r.parents[1]);ck(a&&b,"parents");let p=r.pivot;let x=new Set(a.filter(l=>l!==p));for(let l of b)if(l!==-p)x.add(l);proofChecks+=a.length+b.length;ck(a.includes(p)&&b.includes(-p)&&![...x].some(l=>x.has(-l))&&canon([...x]).join(",")===r.c.join(","),"resolution replay");by.set(r.id,r.c)}
let result=solve(rows.map(r=>r.c),[]);return{mode,width,stage:"reached",firstRows,learned,pairs,score,residueOps,flips,changed,phases,capHit,peakSlots,proofChecks,result,elapsedMs:Date.now()-start}}
function tableFromCNF(C){return C.map((c,id)=>{c=canon(c);if(!c)return null;let vs=sort(c.map(Math.abs));if(vs.length>8)return null;let ok=[];for(let w=0;w<2**vs.length;w++)if(c.some(l=>(w>>vs.indexOf(Math.abs(l))&1)===+(l>0)))ok.push(w);return{id,vs,ok,ids:[id+1]}}).filter(Boolean)}
function experiment(C,V,F){let E=early(F,V,C);if(E.conflict)return{early:E,stage:"unreachable"};let base=simplify(C,E.pins),W=V.filter(v=>!E.pins.some(p=>p[0]===v));let arms=[];for(let width of [2,4])for(let mode of ["baseline","flips","deductions","table","residue"])arms.push(feedback(base,W,mode,width));return{early:E,base,W,arms}}
function guardIdentity(e,anchor,g){let artifact={schema:"EB-RELATIVE-PORT-PINS-v1",anchor:anchor-1,pins:g.map(l=>[Math.abs(l)-1,+(l>0)]).sort((a,b)=>a[0]-b[0])};return{artifact,guard_id:"GUARD-v1:sha256:"+sha(JSON.stringify(["PNP-GUARD-v1",e.instance_id,artifact.schema,sha(JSON.stringify(artifact)+"\n")])+"\n")}}

  // This function is inserted inside the prior audit's run, reusing its verified normalization and exact feedback methods.
  const result=[];
  for(const name of ["JOINT-24","RANDOM-3CNF-40"]){
   let x=corpus.instances.find(z=>z.id===name),e=registry.instances.find(z=>z.alias==="EB-"+name),G=compile(x),s=JSON.stringify(G.network)+"\n",mp=JSON.stringify(G.source_map)+"\n";
   ck(sha(s)===e.sha256&&s.length*8===e.N_bits&&sha(x.dimacs)===e.source_cnf.sha256&&x.dimacs.length*8===e.source_cnf.N_bits&&sha(mp)===e.source_map_sha256,"auth");
   let D=normal(G.network),rawV=sort(D.F.flatMap(f=>f.vs)),raw=early(D.F,rawV,clauses(D.F));ck(!raw.conflict&&!raw.pins.length);
   let P=project(D.F),freq=new Map();for(let f of P.Q)for(let v of f.vs)freq.set(v,(freq.get(v)||0)+1);
   let anchor=[...freq].sort((a,b)=>b[1]-a[1]||a[0]-b[0])[0][0];ck(P.Q.every(f=>f.ok.every(w=>f.ok.includes(w^(2**f.vs.length-1)))));
   let F=gaugeFactors(P.Q,anchor),V=sort(F.flatMap(f=>f.vs)),C=clauses(F),native=experiment(C,V,F);
   let directC=x.dimacs.trimEnd().split("\n").slice(1).map(l=>l.split(/\s+/).map(Number).slice(0,-1)),direct=experiment(directC,Array.from({length:x.nvars},(_,i)=>i+1),tableFromCNF(directC));
   let [a,b,c,d]=V.map(v=>[v,F.filter(f=>f.vs.includes(v)).length]).sort((a,b)=>b[1]-a[1]||a[0]-b[0]).slice(0,4).map(z=>z[0]),guards=[[-a],[a,-b],[a,b,-c],[a,b,c,-d],[a,b,c,d]],lanes=[];
   for(let [label,fn] of [["occupancy",(g,m)=>gac(F,g,m)],["affine",(g,m)=>ge(F,g,m,V)],["binary",(g,m)=>binary(F,g,m,V)],["separator",(g,m)=>join(F,g,m)],["DAG",(g,m)=>tree(C,g,m)!==null]]){let m={events:0},status=[];for(let g of guards){try{status.push(fn(g,m)?"NO":"UNKNOWN")}catch(e){if(e.message!=="cap")throw e;status.push("UNKNOWN cap")}}lanes.push({label,status,m})}
   let proofs=guards.map(g=>({g,...solve(C,g)}));ck(proofs.every(p=>p.status==="NO"));ck(mass(V,guards,[],{terms:0})===0n);
   let baseline=solve(C,[]),pc=peers[name];ck(pc.instance_id===e.instance_id&&pc.N===e.N_bits&&anchor===11&&pc.guard[0][0]===10&&pc.guard[0][1]===0);
   // Distinct peer chart: no raw residual identity transfer. Only rederive candidate clauses using own chart and same original-port coordinates.
   let Q=C.slice(),imports=[],rejected=[],vis=0;
   for(let l of pc.proof.slice(0,8)){if(!l.length||!l.every(v=>V.includes(Math.abs(v)))){rejected.push({l,why:"scope or empty"});continue}let m={events:0};if(up(Q,l.map(x=>-x),m,true)===null){imports.push({l,checks:m.events});Q.push(l)}else rejected.push({l,why:"not RUP",checks:m.events});vis+=m.events;}
   let hybrid=solve(Q,[]),remove=[];for(let i=0;i<imports.length;i++){let R=C.slice(),admitted=0;for(let j=0;j<imports.length;j++)if(i!==j){let l=imports[j].l,m={events:0};if(up(R,l.map(x=>-x),m,true)===null){R.push(l);admitted++}}remove.push({removed:imports[i].l,admitted,refutation:solve(R,[]).status})}
   let chart={anchor,V,F,trace:P.trace},map={coordinate:"relative original representative port v-1 XOR anchor",anchor,reverse:"reverse full incident elimination then signed equality BFS and gauge"};let chartSha=sha(JSON.stringify(chart)+"\n"),mapSha=sha(JSON.stringify(map)+"\n"),chartId="RESIDUAL-v1:sha256:"+sha(JSON.stringify(["PNP-RESIDUAL-v1",e.instance_id,"EMPTY","T3-NONLINEAR-CORRECTION-CHART-v1",chartSha,mapSha])+"\n");
   function pol(cl){let p=new Set([0n]);for(let l of cl){let z=1n<<BigInt(V.indexOf(Math.abs(l))),n=new Set();for(let x of p){let add=y=>n.has(y)?n.delete(y):n.add(y);if(l>0)add(x);add(x|z)}p=n}return p}
   function span(rows){let b=new Map();for(let p of rows){let s=new Set(p);while(s.size){let k=[...s].reduce((a,b)=>a>b?a:b);if(!b.has(k)){b.set(k,s);break}for(let x of b.get(k))s.has(x)?s.delete(x):s.add(x)}}return{rank:b.size,one:b.has(0n)}}
   const rows=C.map(pol),m=rows.length,sketch=[];let fieldMul=(a,b)=>{let r=0;while(b){if(b&1)r^=a;b>>=1;a<<=1;if(a&256)a^=285}return r};
   for(let bit=0;bit<17;bit++){let p=new Set();for(let i=0;i<m;i++){let a=i+1,label=1|(a<<1)|(fieldMul(fieldMul(a,a),a)<<9);if(label>>bit&1)for(let z of rows[i])p.has(z)?p.delete(z):p.add(z)}sketch.push(p)}
   let full=span(rows),small=span(sketch),corrected=span(sketch.concat(imports.map(x=>pol(x.l)))),allHybrid=span(rows.concat(imports.map(x=>pol(x.l))));
   result.push({entry:e,chart,chartId,chartSha,mapSha,map,raw:{variables:rawV.length,early:raw},projection:{steps:P.trace.length,scans:P.scans,tests:P.tests,checkTests:P.checkTests},native,direct,lanes,guards,proofs,baseline,imports,rejected,vis,hybrid,remove,compression:{full,small,corrected,allHybrid,correctionRows:full.rank-small.rank}});
  }
  let fano=[[1,2,3],[1,4,5],[1,6,7],[2,4,6],[2,5,7],[3,4,7],[3,5,6]].flatMap(c=>[c,c.map(l=>-l)]);
  return {cases:result,fano:experiment(fano,[1,2,3,4,5,6,7],tableFromCNF(fano))};

}

const fs=require('node:fs');const [b,r,j,k]=process.argv.slice(2).map(x=>JSON.parse(fs.readFileSync(x,'utf8')));console.log(JSON.stringify(run(b,r,{'JOINT-24':j,'RANDOM-3CNF-40':k}),null,2));
