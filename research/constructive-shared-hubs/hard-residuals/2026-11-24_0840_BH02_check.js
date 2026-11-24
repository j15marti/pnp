function BH02(){
 const assert=(p,s)=>{if(!p)throw Error(s)};
 const E=(a,b,c,lo=1,hi=2)=>({v:[a,b,c],lo,hi});
 const F=[E(0,1,2),E(0,3,4),E(0,5,6),E(1,3,5),E(1,4,6),E(2,3,6),E(2,4,5)];
 const valid=(F,x)=>F.every(e=>{let s=e.v.reduce((a,v)=>a+x[v],0);return s>=e.lo&&s<=e.hi});
 function brute(n,F){let count=0,w=null;for(let k=0;k<2**n;k++){let x=Array.from({length:n},(_,i)=>(k>>i)&1);if(valid(F,x)){count++;w=x}}return {count,w}}
 function ledger(){return {closureScans:0,localRows:0,localUnions:0,cycleUnions:0,discoverySweeps:0,anchorEntries:0,neighborPairVisits:0,anchorPairs:0,pairEdgeVisits:0,cycleVertices:0,cycleCertificates:0,certificateEdgeChecks:0,chordChecks:0,terminalGuards:0,implicationEdges:0,implicationVisits:0,sourceChecks:0,peakPairGraphVertices:0,peakAnchorKeys:0,retainedCertificateIds:0}}
 function state(n){let p=Array.from({length:n+1},(_,i)=>i),q=Array(n+1).fill(0);return {p,q,n}}
 function root(D,x){let b=0;while(D.p[x]!==x){b^=D.q[x];x=D.p[x]}return [x,b]}
 function join(D,x,y,b){let [a,i]=root(D,x),[c,j]=root(D,y);if(a===c)return (i^j)===b?0:-1;if(a===D.n){[a,c]=[c,a];[i,j]=[j,i]}D.p[a]=c;D.q[a]=b^i^j;return 1}
 function copy(D){return {n:D.n,p:D.p.slice(),q:D.q.slice()}}
 function close(D,F,L){for(;;){let moved=false;for(let e of F){L.closureScans++;let a=e.v.map(v=>root(D,v)),u=[...new Set(a.map(t=>t[0]).filter(v=>v!==D.n))],idx=new Map(u.map((v,i)=>[v,i])),rows=[];for(let m=0;m<2**u.length;m++){L.localRows++;let s=a.reduce((z,[v,b])=>z+(b^(v===D.n?0:((m>>idx.get(v))&1))),0);if(s>=e.lo&&s<=e.hi)rows.push(m)}if(!rows.length)return false;
 for(let i=0;i<u.length&&!moved;i++){let t=(rows[0]>>i)&1;if(rows.every(m=>((m>>i)&1)===t)){assert(join(D,u[i],D.n,t)===1,"local pin");L.localUnions++;moved=true;break}
 for(let j=i+1;j<u.length;j++){let t=((rows[0]>>i)^(rows[0]>>j))&1;if(rows.every(m=>(((m>>i)^(m>>j))&1)===t)){assert(join(D,u[i],u[j],t)===1,"local parity");L.localUnions++;moved=true;break}}}
 if(moved)break}if(!moved)return true}}
 function discover(D,F,L){
 L.discoverySweeps++;let n=D.n,A=Array.from({length:n},()=>[]),N=Array.from({length:n},()=>new Set()),T=[];
 for(let id=0;id<F.length;id++){let e=F[id];if(e.lo!==1||e.hi!==2)continue;let r=e.v.map(v=>root(D,v));if(r.some(t=>t[0]===n||t[1]!==r[0][1])||new Set(r.map(t=>t[0])).size!==3)continue;let v=r.map(t=>t[0]);T.push({v,id});for(let i=0;i<3;i++){let a=v[i],b=v[(i+1)%3],c=v[(i+2)%3];A[a].push({b,c,id});N[b].add(a);N[c].add(a);L.anchorEntries++}}
 let P=new Map;for(let ns of N){let a=[...ns].sort((a,b)=>a-b);for(let i=0;i<a.length;i++)for(let j=i+1;j<a.length;j++){L.neighborPairVisits++;let k=a[i]*n+a[j];P.set(k,(P.get(k)||0)+1)}}L.peakAnchorKeys=Math.max(L.peakAnchorKeys,P.size);
 let out=[];for(let [k,z] of P){if(z<4)continue;let a=Math.floor(k/n),b=k%n;L.anchorPairs++;let G=new Map;
 function add(u,v,col,id){if(!G.has(u))G.set(u,[]);G.get(u).push({v,col,id})}
 for(let col=0;col<2;col++)for(let e of A[col?b:a]){L.pairEdgeVisits++;if([e.b,e.c].includes(a)||[e.b,e.c].includes(b))continue;add(e.b,e.c,col,e.id);add(e.c,e.b,col,e.id)}
 L.peakPairGraphVertices=Math.max(L.peakPairGraphVertices,G.size);let seen=new Set,found=false;
 for(let start of G.keys()){if(found)break;if(seen.has(start))continue;let Q=[start],part=new Map([[start,0]]),ids=new Set,ok=true;seen.add(start);
 for(let i=0;i<Q.length;i++){let u=Q[i],es=G.get(u);L.cycleVertices++;if(es.length!==2||es[0].col===es[1].col)ok=false;
 for(let e of es){ids.add(e.id);if(!part.has(e.v)){part.set(e.v,part.get(u)^1);seen.add(e.v);Q.push(e.v)}else if(part.get(e.v)===part.get(u))ok=false}}
 if(!ok||Q.length<4)continue;
 let chords=new Map;for(let e of T){L.chordChecks++;for(let i=0;i<3;i++){let c=e.v[i],u=e.v[(i+1)%3],v=e.v[(i+2)%3];if(!part.has(u)||!part.has(v)||part.get(u)!==part.get(v))continue;let s=part.get(u);if(!chords.has(c))chords.set(c,[null,null]);chords.get(c)[s]={id:e.id,u,v};}}
 for(let [c,rr] of chords){if(!rr[0]||!rr[1])continue;
 // Independent structural certificate check against the current mapped source, including signed-root orientation.
 let cert=[...ids],Dg=new Map(Q.map(v=>[v,[0,0]]));
 for(let id of cert){L.certificateEdgeChecks++;let e=F[id],r=e.v.map(v=>root(D,v));assert(e.lo===1&&e.hi===2&&r.every(t=>t[1]===r[0][1]),"source cycle");let v=r.map(t=>t[0]),col=v.includes(a)?0:1,anchor=col?b:a;assert(v.includes(anchor)&&!v.includes(col?a:b),"anchor");let uv=v.filter(x=>x!==anchor);assert(uv.length===2&&Dg.has(uv[0])&&Dg.has(uv[1])&&part.get(uv[0])!==part.get(uv[1]),"alternating pair");for(let u of uv)Dg.get(u)[col]++}
 assert([...Dg.values()].every(d=>d[0]===1&&d[1]===1),"perfect matchings");
 for(let s=0;s<2;s++){L.certificateEdgeChecks++;let e=F[rr[s].id],r=e.v.map(v=>root(D,v));assert(e.lo===1&&e.hi===2&&r.every(t=>t[1]===r[0][1])&&r.map(t=>t[0]).includes(c)&&part.get(rr[s].u)===s&&part.get(rr[s].v)===s,"chord")}
 L.cycleCertificates++;L.retainedCertificateIds+=cert.length+2;out.push({a,b,ids:cert,rr,c});found=true;break}
 }}return out}
 function normalize(D,F,L){if(!close(D,F,L))return false;for(;;){let facts=discover(D,F,L),moved=false;for(let {a,b} of facts){let k=join(D,a,b,0);if(k<0)return false;if(k===1){L.cycleUnions++;moved=true;if(!close(D,F,L))return false}}if(!moved)return true}}
 function twoCNF(D,F,L){
 let clauses=[];for(let e of F){for(let sign of [0,1]){if((sign===0&&e.lo===0)||(sign===1&&e.hi===3))continue;let S=new Map,taut=false;for(let v of e.v){let [r,b]=root(D,v);let want=1^sign^b;if(r===D.n){if(want===0)taut=true;continue}if(S.has(r)&&S.get(r)!==want)taut=true;S.set(r,want)}if(taut)continue;let z=[...S].map(([r,b])=>2*r+b);if(z.length===0)return {answer:"UNSAT"};clauses.push(z)}}
 let triples=clauses.filter(c=>c.length>2);if(triples.length){let common=triples[0].map(x=>x>>1).filter(r=>triples.every(c=>c.some(x=>(x>>1)===r)));return {answer:"UNKNOWN",common}}
 let n=D.n*2,G=Array.from({length:n},()=>[]),R=Array.from({length:n},()=>[]);function add(u,v){G[u].push(v);R[v].push(u);L.implicationEdges++}
 for(let c of clauses){let a=c[0],b=c[1]??a;add(a^1,b);add(b^1,a)}
 let seen=new Set,order=[];function dfs(v){seen.add(v);for(let w of G[v]){L.implicationVisits++;if(!seen.has(w))dfs(w)}order.push(v)}
 for(let i=0;i<n;i++)if(!seen.has(i))dfs(i);let cc=Array(n).fill(-1),k=0;function rev(v){cc[v]=k;for(let w of R[v]){L.implicationVisits++;if(cc[w]<0)rev(w)}}
 for(let i=order.length-1;i>=0;i--)if(cc[order[i]]<0){rev(order[i]);k++}
 for(let i=0;i<D.n;i++)if(cc[2*i]===cc[2*i+1])return {answer:"UNSAT"};
 let x=Array.from({length:D.n},(_,i)=>{let [r,b]=root(D,i);return b^(r===D.n?0:Number(cc[2*r+1]>cc[2*r]))});L.sourceChecks+=F.length;assert(valid(F,x),"2SAT source lift");return {answer:"SAT",x}}
 function solve(n,F){let L=ledger(),D=state(n);if(!normalize(D,F,L))return {answer:"UNSAT",L};let t=twoCNF(D,F,L);if(t.answer!=="UNKNOWN")return {...t,L};
 if(t.common.length){let r=t.common[0],unknown=false;for(let b=0;b<2;b++){L.terminalGuards++;let C=copy(D);assert(join(C,r,n,b)===1,"guard");if(!normalize(C,F,L))continue;let t=twoCNF(C,F,L);if(t.answer==="SAT")return {...t,L};if(t.answer==="UNKNOWN")unknown=true}return {answer:unknown?"UNKNOWN":"UNSAT",L}}
 return {answer:"UNKNOWN",L}}
 const relax=(F,i,b)=>F.map((e,j)=>j===i?{...e,lo:b===0?0:e.lo,hi:b===1?3:e.hi}:e);
 let fano=[];for(let i=-1;i<7;i++)for(let b of i<0?[0]:[0,1]){let f=i<0?F:relax(F,i,b),r=solve(7,f),ref=brute(7,f);assert(ref.count===(i<0?0:5)&&r.answer===(i<0?"UNSAT":"SAT"),"Fano");fano.push({i,b,count:ref.count,...r})}
 function graph(n=1){return {n,F:[]}}
 function wire(G,a,b){let ids=[a,b,...Array.from({length:5},()=>G.n++)];for(let e of F.slice(1))G.F.push(E(...e.v.map(i=>ids[i])))}
 function base(){let G=graph();let ends=[];for(let j=0;j<2;j++){let a=0;for(let i=0;i<4;i++){let b=G.n++;wire(G,a,b);a=b}ends.push(a)}G.F.push(E(0,...ends));return G}
 function stretch(G){let H=graph(G.n);for(let e of G.F){let p=e.v.map(a=>{let b=H.n++;wire(H,a,b);return b});H.F.push(E(...p))}return H}
 function rng(s){return ()=>{s^=s<<13;s^=s>>>17;s^=s<<5;return (s>>>0)/4294967296}}
 let R=rng(208240);function shuffle(G){let p=Array.from({length:G.n},(_,i)=>i);for(let i=p.length-1;i;i--){let j=Math.floor(R()*(i+1));[p[i],p[j]]=[p[j],p[i]]}return {n:G.n,F:G.F.map(e=>({...e,v:e.v.map(v=>p[v])}))}}
 let B=base(),H=stretch(B),do02=[];for(let G of [B,H]){let r=solve(G.n,shuffle(G).F);assert(r.answer==="UNSAT","DO02");do02.push({n:G.n,m:G.F.length,...r})}
 // Two arbitrarily long alternating cycles with a shared third anchor; only final owner changed.
 function ring(k){let G=graph(3),x=[0,0,0];function gadget(a,b,c){let v=Array.from({length:2*k},()=>{x.push(1);return G.n++});for(let i=0;i<2*k;i++)G.F.push(E(i%2?b:a,v[i],v[(i+1)%(2*k)]));let t=2*Math.floor(k/2);G.F.push(E(c,v[0],v[t]),E(c,v[1],v[t+1]))}gadget(0,1,2);gadget(1,2,0);G.F.push(E(0,1,2));return {...G,x}}
 let scaling=[];for(let k of [2,4,8,16,32,64,128,256]){let G=ring(k),f=G.F,rs=solve(G.n,f),sat=solve(G.n,relax(f,f.length-1,0)),sat1=solve(G.n,relax(f,f.length-1,1));assert(rs.answer==="UNSAT"&&sat.answer==="SAT"&&sat1.answer==="SAT","ring "+k);assert(valid(relax(f,f.length-1,0),G.x),"reference ring");scaling.push({k,n:G.n,m:f.length,unsat:rs.L,sat0:sat.L,sat1:sat1.L})}
 let random={cases:0,sat:0,unsat:0,decidedSAT:0,decidedUNSAT:0,unknown:0,referenceAssignments:0,ledger:ledger()};for(let k=0;k<160;k++){let n=4+Math.floor(R()*6),m=3+Math.floor(R()*18),f=[];for(let j=0;j<m;j++){let v=[];while(v.length<3){let a=Math.floor(R()*n);if(!v.includes(a))v.push(a)}let t=R();f.push(E(...v,t<.15?0:1,t>.85?3:2))}let ref=brute(n,f),a=solve(n,f);assert(a.answer==="UNKNOWN"||(a.answer==="SAT")===(ref.count>0),"random mismatch");random.cases++;random.referenceAssignments+=2**n;random[ref.count?"sat":"unsat"]++;random[a.answer==="UNKNOWN"?"unknown":a.answer==="SAT"?"decidedSAT":"decidedUNSAT"]++;for(let k of Object.keys(a.L))random.ledger[k]+=a.L[k]}
 // Reproduce BH01's exact deterministic high-girth precursor source; labels from prior spectral certificate and planted witness.
 function gen(n){let R=rng(1234567),A=Array(n).fill(0n),F=[],fail=0;while(fail<20000){let a=Math.floor(R()*n),b=Math.floor(R()*n),c=Math.floor(R()*n);if(a===b||a===c||b===c){fail++;continue}let aa=1n<<BigInt(a),bb=1n<<BigInt(b),cc=1n<<BigInt(c);if((A[a]&bb)||(A[a]&cc)||(A[b]&cc)||(A[a]&A[b])||(A[a]&A[c])||(A[b]&A[c])){fail++;continue}A[a]|=bb|cc;A[b]|=aa|cc;A[c]|=aa|bb;F.push(E(...[a,b,c].sort((x,y)=>x-y)));fail=0}return F}
 function girth3(n,F){let A=Array(n).fill(0n),p=new Set;for(let {v:e} of F)for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){let a=e[i],b=e[j],k=a*n+b;assert(!p.has(k),"pair");p.add(k);A[a]|=1n<<BigInt(b);A[b]|=1n<<BigInt(a)}for(let {v:e} of F)for(let i=0;i<3;i++)for(let j=i+1;j<3;j++)assert((A[e[i]]&A[e[j]])===(1n<<BigInt(e[3-i-j])),"triangle");return p.size}
 let hg=gen(600),px=Array.from({length:600},(_,i)=>i%2),hp=hg.filter(e=>valid([e],px));assert(hg.length===3808&&hp.length===2845,"BH01 source size");let high=[];for(let f of [hg,hp]){let p=girth3(600,f),r=solve(600,f);assert(r.L.cycleCertificates===0&&r.answer==="UNKNOWN","girth terminal");high.push({n:600,m:f.length,pairs:p,...r})}assert(valid(hp,px),"high planted");
 return {seed:208240,fano,do02,scaling,random,high,notes:"BH01 high-girth labels from prior integer certificate and actual planted assignment; not independently rechecking certificate here. No full strict physical compiler, all-channel closure or global search. Counts are logical operation counters, not timings."}
}
console.log(JSON.stringify(BH02(),null,2));
