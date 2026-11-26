// node gate_audit.js
function gateAudit(){
let checks=0,seed=20261126;const ok=(v,m)=>{checks++;if(!v)throw Error(m||"check "+checks)};const rnd=n=>{seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return(seed>>>0)%n};function shuffle(a){for(let i=a.length-1;i;i--){let j=rnd(i+1);[a[i],a[j]]=[a[j],a[i]]}return a}
const AG=[[[0,1,2],[3,4,5],[6,7,8]],[[0,3,6],[1,4,7],[2,5,8]],[[0,4,8],[1,5,6],[2,3,7]],[[0,5,7],[1,3,8],[2,4,6]]],P=[[[4,11,14],[5,9,12],[3,7,10],[2,6,13],[0,1,8]],[[8,9,14],[0,2,11],[4,6,10],[5,7,13],[1,3,12]],[[2,3,9],[1,5,6],[4,7,12],[8,10,11],[0,13,14]],[[4,8,13],[3,5,14],[1,2,7],[0,9,10],[6,11,12]]];
const nae=a=>a.some(b=>b!==a[0]),bit=(w,i)=>(w>>>i)&1, bad=(c,x)=>!nae(c.map(v=>x[v])), count=(F,x)=>F.flat().filter(c=>bad(c,x)).length;
function auth(F,n){ok(F.length===4);let seen=new Set,par=Array.from({length:n},(_,i)=>i);function find(x){while(x!==par[x]){par[x]=par[par[x]];x=par[x]}return x}
for(let p of F){let a=new Uint8Array(n);for(let c of p){ok(c.length===3&&new Set(c).size===3);for(let v of c){ok(v>=0&&v<n);a[v]++;par[find(v)]=find(c[0])}for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){let s=Math.min(c[i],c[j])*n+Math.max(c[i],c[j]);ok(!seen.has(s),"linearity");seen.add(s)}}ok(a.every(x=>x===1),"partition")}ok(par.every((_,i)=>find(i)===find(0)),"connected")}
function split(a){for(let u=0;u<2;u++)for(let v=0;v<2;v++)if(nae([a[0],a[1],u])&&nae([1^u,a[2],v])&&nae([1^v,a[3],a[4]]))return[u,v];return null}
for(let w=0;w<32;w++){let a=Array.from({length:5},(_,i)=>bit(w,i));ok((split(a)!==null)===nae(a))}
const literal=(v,s=0)=>[v,s],val=(l,x)=>x[l[0]]^l[1];
function guarded(F,n){let m=4*n/3,s=n,t=n+1,d=n+2,C=[],chains=[];
for(let c of F.flat())for(let sign of [0,1]){let a=[literal(s,1),...c.map(v=>literal(v,sign)),literal(t)],u=d++,v=d++;C.push([a[0],a[1],literal(u)],[literal(u,1),a[2],literal(v)],[literal(v,1),a[3],a[4]]);chains.push({a,u,v})}
let counts=Array.from({length:d},()=>[0,0]);for(let c of C)for(let [v,z] of c)counts[v][z]++;counts[s][0]++;counts[t][0]++;let h=d++;for(let v=0;v<counts.length;v++){let [p,q]=counts[v];for(let j=0;j<Math.abs(p-q);j++)C.push([literal(h),literal(h,1),literal(v,p>q?1:0)])}ok(C.length===10*m);
function extend(x,S,T){let z=Array(d).fill(0);for(let i=0;i<n;i++)z[i]=x[i];z[s]=S;z[t]=T;for(let {a,u,v} of chains){let p=split(a.map(l=>val(l,z)));ok(p!==null,"guarded model");[z[u],z[v]]=p}ok(C.every(c=>nae(c.map(l=>val(l,z)))));return z}
return{C,d,s,t,extend}}
function compile(F,n){let m=4*n/3,{C,d,s,t,extend}=guarded(F,n),occ=Array.from({length:d},()=>[[],[]]),positions=C.map(c=>c.map(([v,sign])=>{let o={v,sign,w:-1};occ[v][sign].push(o);return o})),sp={v:s,sign:0,w:-1},tp={v:t,sign:0,w:-1};occ[s][0].push(sp);occ[t][0].push(tp);
let wire=[],succ=new Map;const token=(b,row)=>3*b+row;
for(let v=0;v<d;v++){let [p,q]=occ[v];ok(p.length===q.length&&p.length>0);let a=[];for(let i=0;i<p.length;i++)for(let o of [p[i],q[i]]){o.w=wire.length;wire.push(o);a.push(o.w)}for(let i=0;i<a.length;i++){let b=a[i];succ.set(token(b,0),token(b,0));succ.set(token(b,1),token(a[(i+1)%a.length],1))}}
let B=wire.length+C.length,off=9*B,N=off+15,H=[[],[],[],[]],gateA=token(sp.w,2),gateB=token(tp.w,2);ok(wire.length===30*m+2&&N===480*n+33);
for(let j=0;j<C.length;j++)for(let r=0;r<3;r++){let a=token(positions[j][r].w,2),b=token(wire.length+j,r);succ.set(a,b);succ.set(b,a)}
for(let i=0;i<3*B;i++){let a=3*i;if(i===gateA)H[0].push([a,a+1,3*gateB+2]);else if(i===gateB)H[0].push([a,a+1,off+4]);else{ok(succ.has(i));H[0].push([a,a+1,3*succ.get(i)+2])}}
H[0].push([off+11,off+14,3*gateA+2]);for(let j=0;j<4;j++)for(let i=0;i<P[j].length;i++)if(j!==0||i!==0)H[j].push(P[j][i].map(v=>v+off));
for(let b=0;b<B;b++)for(let j=1;j<4;j++)for(let c of AG[j])H[j].push(c.map(v=>v+9*b));
function lift(z){let x=Array(N);function mono(T,b){for(let i=0;i<3;i++)x[3*T+i]=b}function free(T,b){x[3*T]=0;x[3*T+1]=1;x[3*T+2]=b}
for(let w=0;w<wire.length;w++){let o=wire[w],b=z[o.v]^o.sign;free(token(w,0),0);mono(token(w,1),b);mono(token(w,2),1^b)}
for(let j=0;j<C.length;j++){let a=C[j].map(l=>val(l,z)),i0=a.indexOf(0),i1=a.indexOf(1);ok(i0>=0&&i1>=0);for(let r=0;r<3;r++){let T=token(wire.length+j,r);if(r===i0||r===i1)mono(T,a[r]);else free(T,a[r])}}
let base=20933;for(let i=0;i<15;i++)x[off+i]=bit(base,i)^z[t];ok(x[off+4]===z[t]&&x[off+11]!==x[off+14]);ok(x.every(v=>v===0||v===1));return x}
function project(x){ok(count(H,x)===0);let z=Array(d).fill(-1);for(let w=0;w<wire.length;w++){let o=wire[w],b=x[9*w+3]^o.sign;ok(z[o.v]===-1||z[o.v]===b);z[o.v]=b}ok(z[s]!==z[t]);ok(C.every(c=>nae(c.map(l=>val(l,z)))));let y=z.slice(0,n).map(v=>v^z[t]);ok(count(F,y)===0);return y}
return{H,N,base:lift(extend(Array(n).fill(0),0,0)),sat:x=>lift(extend(x,1,0)),project,wireBlocks:wire.length,clauseBlocks:C.length}}
function ring(k,no){let F=[[],[],[],[]];for(let b=0;b<k;b++)for(let j=0;j<4;j++)for(let i=0;i<3;i++){let c=AG[j][i].map(v=>9*b+v);if(j===0&&(i===0||(!no&&i===1)))c[2]=9*((b+1)%k)+AG[j][i][2];F[j].push(c)}let x=Array.from({length:9*k},(_,i)=>{let t=Math.floor(i/9),r=i%9;return r<3?t%2:r<6?1^(t%2):r===8?1:0});return{F,n:9*k,x}}
function brute(F,n){for(let w=0;w<2**n;w++)if(F.flat().every(c=>{let a=bit(w,c[0]),b=bit(w,c[1]),d=bit(w,c[2]);return a!==b||b!==d}))return w;return null}
let cases=[];for(let k of [2,4,16,32])for(let no of [false,true]){let{F,n,x}=ring(k,no);auth(F,n);let ref=n<=18?brute(F,n):undefined;if(ref!==undefined)ok((ref===null)===no);if(no){let L=F.flat().filter(c=>c.every(v=>v<9));ok(L.length===11);ok(brute([L],9)===null)}else ok(count(F,x)===0);let Q=compile(F,n);auth(Q.H,Q.N);ok(count(Q.H,Q.base)===1,"exact one defect");let defect=Q.H.flat().find(c=>bad(c,Q.base));ok(defect!==undefined);if(!no){let y=Q.sat(x);ok(count(Q.H,y)===0);ok(Q.project(y).every((v,i)=>v===x[i]))}
let p=shuffle(Array.from({length:Q.N},(_,i)=>i)),G=Q.H.map(part=>shuffle(part.map(c=>shuffle(c.map(v=>p[v]))))),b=Array(Q.N);Q.base.forEach((v,i)=>b[p[i]]=v);auth(G,Q.N);ok(count(G,b)===1);cases.push({k,n,physical:Q.N,physicalClauses:4*Q.N/3,status:no?"UNSAT":"SAT",suppliedDefects:1,reference:n<=18?"exhaustive original":no?"11-line contradiction in original":"explicit original witness",wireBlocks:Q.wireBlocks,clauseBlocks:Q.clauseBlocks})}
return{seed:20261126,checks,guardTruthTable:32,cases}
}
console.log(JSON.stringify(gateAudit(),null,2));
