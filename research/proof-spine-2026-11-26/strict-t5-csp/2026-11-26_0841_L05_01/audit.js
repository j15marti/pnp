function assert(x,m){if(!x)throw Error(m)}
const C=(x,y,z)=>new Set([x,y,z]).size===3&&[0,1,2,3,4].some(i=>[x,y,z].every(v=>[i,(i+1)%5,(i+2)%5].includes(v)));
const beats=(x,y)=>[1,3].includes((y-x+5)%5);
const R=(x,y,z)=>new Set([x,y,z]).size===3&&beats(x,y)!==beats(x,z);
const bits=w=>[w&1,(w>>1)&1,(w>>2)&1,(w>>3)&1];
function build(n,F){
 const k=Math.max(1,n,F.length), H=(i,j)=>i*(k+1)+j, V=(i,j)=>k*(k+1)+i*k+j, p=2*k*(k+1),T=[],D=Array(p).fill(3);
 for(let i=0;i<k;i++){if(i>=n)D[H(i,0)]=1;for(let j=0;j<k;j++){let mask=0;for(let w=0;w<16;w++){const [a,b,c,d]=bits(w);const lit=(F[j]||[]).some(l=>Math.abs(l)===i+1&&(l>0?a===1:a===0));if(a===b&&d===Number(!!c||lit))mask|=1<<w}T.push({ids:[H(i,j),H(i,j+1),V(i,j),V(i+1,j)],mask})}}
 for(let j=0;j<k;j++){D[V(0,j)]=1;D[V(k,j)]=j<F.length?2:1}
 return {k,p,T,D,n,F};
}
function check(G,x){return x.length===G.p&&G.D.every((d,i)=>d&(1<<x[i]))&&G.T.every(t=>t.mask&(1<<t.ids.reduce((s,e,i)=>s+(x[e]<<i),0)))}
function lift(G,a){const {k,n,F}=G,x=Array(G.p).fill(0);for(let i=0;i<k;i++)for(let j=0;j<=k;j++)x[i*(k+1)+j]=i<n?a[i]:0;let off=k*(k+1);for(let j=0;j<k;j++)for(let i=0;i<k;i++)x[off+(i+1)*k+j]=Number(!!x[off+i*k+j]||(F[j]||[]).some(l=>Math.abs(l)===i+1&&(l>0?a[i]===1:a[i]===0)));return x}
function evalF(F,a){return F.every(c=>c.some(l=>l>0?a[l-1]===1:a[-l-1]===0))}
function gridDP(G){ // exact count, general local tables, no source metadata used
 const {k,T,D}=G,off=k*(k+1);let dp=new Map();
 for(let u=0;u<2**k;u++)if(Array.from({length:k},(_,j)=>D[off+j]&(1<<((u>>j)&1))).every(Boolean))dp.set(u,1n);
 for(let i=0;i<k;i++){let next=new Map();for(const [u,count] of dp)for(let a=0;a<2;a++){if(!(D[i*(k+1)]&(1<<a)))continue;
 function rec(j,w,v){if(j===k){next.set(v,(next.get(v)||0n)+count);return}let t=T[i*k+j];for(let e=0;e<2;e++)for(let s=0;s<2;s++){let z=w+2*e+4*((u>>j)&1)+8*s;if((t.mask&(1<<z))&&(D[t.ids[1]]&(1<<e))&&(D[t.ids[3]]&(1<<s)))rec(j+1,e,v+(s<<j))}}
 rec(0,a,0)}dp=next}
 return [...dp.values()].reduce((a,b)=>a+b,0n);
}
function parity(x){let y=0;while(x){x&=x-1;y^=1}return y}
function close(G){const D=G.D.slice(),T=G.T.map(t=>({...t}));let rounds=0,changes=true;
 while(changes){changes=false;rounds++;for(let t of T){let m=0;for(let z=0;z<16;z++)if((t.mask&(1<<z))&&t.ids.every((e,j)=>D[e]&(1<<((z>>j)&1))))m|=1<<z;if(!m)return {no:true,rounds};if(m!==t.mask){t.mask=m;changes=true}for(let j=0;j<4;j++){let d=0;for(let z=0;z<16;z++)if(m&(1<<z))d|=1<<((z>>j)&1);if(d!==D[t.ids[j]]){D[t.ids[j]]=d;changes=true}}}
 const piv=new Map();function add(m,r){while(m){let i=m.toString(2).length-1;if(!piv.has(i)){piv.set(i,[m,r]);return true}let [u,v]=piv.get(i);m^=u;r^=v}return r===0}
 for(let i=0;i<G.p;i++)if(D[i]!==3&&!add(1n<<BigInt(i),D[i]===2?1:0))return {no:true,rounds};
 for(let t of T)for(let a=1;a<16;a++){let s=-1,ok=true,m=0n;for(let z=0;z<16;z++)if(t.mask&(1<<z)){let r=parity(z&a);if(s<0)s=r;else if(s!==r){ok=false;break}}if(ok){for(let j=0;j<4;j++)if(a&(1<<j))m^=1n<<BigInt(t.ids[j]);if(!add(m,s))return {no:true,rounds}}}
 let dir=[],off=[];for(let i=0;i<G.p;i++){if(!piv.has(i)){dir.push(1n<<BigInt(i));off.push(0);continue}let [m,r]=piv.get(i);m^=1n<<BigInt(i);let v=0n;while(m){let j=m.toString(2).length-1;v^=dir[j];r^=off[j];m^=1n<<BigInt(j)}dir.push(v);off.push(r);if(v===0n&&D[i]!==1<<r){D[i]=1<<r;changes=true}}
 for(let t of T){let m=t.mask;for(let a=1;a<16;a++){let v=0n,r=0;for(let j=0;j<4;j++)if(a&(1<<j)){v^=dir[t.ids[j]];r^=off[t.ids[j]]}if(v===0n)for(let z=0;z<16;z++)if(parity(z&a)!==r)m&=~(1<<z)}if(!m)return {no:true,rounds};if(m!==t.mask){t.mask=m;changes=true}}
 }
 return {no:false,rounds,free:D.filter(d=>d===3).length,freeWest:Array.from({length:G.n},(_,i)=>D[i*(G.k+1)]===3).filter(Boolean).length};
}
function circuit(G){let b=G.p,g=[];const NOT=a=>{g.push(["N",a]);return b++},OR=(a,c)=>{g.push(["O",a,c]);return b++},AND=(a,c)=>NOT(OR(NOT(a),NOT(c)));const one=OR(0,NOT(0)),zero=NOT(one);let out=one;
 for(const t of G.T){let v=zero;for(let w=0;w<16;w++)if(t.mask&(1<<w)){let u=one;for(let j=0;j<4;j++)u=AND(u,(w&(1<<j))?t.ids[j]:NOT(t.ids[j]));v=OR(v,u)}out=AND(out,v)}
 for(let i=0;i<G.p;i++)if(G.D[i]!==3)out=AND(out,G.D[i]===2?i:G.D[i]===1?NOT(i):zero);
 return {p:G.p,b,g,out};
}
function compile(B){let vars=5,clauses=[],w=[],helpers=[];const add=(...c)=>{assert(new Set(c).size===3,"distinct names");clauses.push(c)};
 for(let i=0;i<5;i++)add(i,(i+1)%5,(i+2)%5);
 for(let i=0;i<B.b;i++){let t=vars++;w.push(t);let u=[];for(let j=2;j<=4;j++){u.push(vars);add(j,t,vars++)}helpers.push(u)}
 let oh=[];for(let i=0;i<B.g.length;i++){let [op,a,b]=B.g[i],o=w[B.p+i];if(op==="N")add(2,w[a],o);else{let y=vars++,z=vars++;add(1,2,y);add(0,1,z);add(4,w[a],y);add(3,w[b],z);add(o,y,z);oh.push([i,y,z])}}
 add(0,2,w[B.out]);return {vars,clauses,w,helpers,oh};
}
function t5Lift(B,T,a){let v=a.slice();for(let [op,p,q] of B.g)v.push(op==="N"?1-v[p]:v[p]|v[q]);let x=Array(T.vars).fill(-1);for(let i=0;i<5;i++)x[i]=i;for(let i=0;i<v.length;i++){x[T.w[i]]=v[i];for(let j=2;j<=4;j++)x[T.helpers[i][j-2]]=[0,1,2,3,4].find(u=>C(j,v[i],u))}
 for(let [i,y,z] of T.oh){let [,p,q]=B.g[i];x[y]=v[p]?0:3;x[z]=v[q]?2:4}
 assert(x.every(y=>y>=0),"full lift");assert(T.clauses.slice(0,-1).every(c=>C(...c.map(j=>x[j]))),"gate lift");return {accept:T.clauses.every(c=>C(...c.map(j=>x[j]))),r:T.clauses.every(c=>R(x[c[0]],x[c[1]],x[c[2]])&&R(x[c[1]],x[c[0]],x[c[2]]))};
}
function clauses(t,bad){let F=[];for(let g=0;g<t;g++)for(let a=0;a<8;a++){let z=a===7&&!(bad&&g===t-1)?6:a;F.push(Array.from({length:3},(_,j)=>(3*g+j+1)*((z>>j)&1?-1:1)))}return F}
function singleton(k){const p=2*k*(k+1),D=Array(p).fill(3),T=[];for(let i=0;i<k;i++)for(let j=0;j<k;j++)T.push({ids:[i*(k+1)+j,i*(k+1)+j+1,k*(k+1)+i*k+j,k*(k+1)+(i+1)*k+j],mask:1});return {k,p,D,T}}
function audit(){let c=0,r=0,frames=0,gateChecks=0;for(let x=0;x<5;x++)for(let y=0;y<5;y++)for(let z=0;z<5;z++){c+=Number(C(x,y,z));r+=Number(R(x,y,z));assert(C(x,y,z)===(R(x,y,z)&&R(y,x,z)),"C/R")}
 for(let a=0;a<3125;a++){let x=Array.from({length:5},(_,i)=>Math.floor(a/5**i)%5);if(x.every((v,i)=>C(v,x[(i+1)%5],x[(i+2)%5])))frames++}assert(frames===10,"frames");
 for(let b=0;b<5;b++){let p=[2,3,4].map(j=>[0,1,2,3,4].filter(u=>C(j,b,u)).length).reduce((a,b)=>a*b,1);assert(p===(b<2?2:0),"domain")}
 for(let p=0;p<2;p++)for(let q=0;q<2;q++)for(let o=0;o<2;o++){let count=0;for(let y=0;y<5;y++)for(let z=0;z<5;z++)count+=Number(C(1,2,y)&&C(0,1,z)&&C(4,p,y)&&C(3,q,z)&&C(o,y,z));assert(count===Number(o===(p|q)),"OR");assert(C(2,p,o)===(o===1-p),"NOT");gateChecks++}
 let formulaTests=0,lifts=0,dpTests=0,t5Tests=0;const all=clauses(1,true);
 for(let mask=0;mask<256;mask++){let F=all.filter((_,j)=>mask&(1<<j)),G=build(3,F),cnt=0;for(let a=0;a<8;a++){let x=[a&1,(a>>1)&1,(a>>2)&1],ok=evalF(F,x);cnt+=Number(ok);assert(check(G,lift(G,x))===ok,"grid lift");lifts++}assert(gridDP(G)===BigInt(cnt),"independent frontier count");dpTests++;formulaTests++}
 for(const F of [[],[[1,1,-1]],[[1],[-1]],[[1,2,-1],[2,-3,3]],clauses(1,false),clauses(1,true)]){let G=build(3,F),B=circuit(G),T=compile(B);for(let a=0;a<8;a++){let x=[a&1,(a>>1)&1,(a>>2)&1],y=t5Lift(B,T,lift(G,x));assert(y.accept===evalF(F,x)&&y.r===y.accept,"T5 decision");t5Tests++}}
 const neighbors=[];for(let t of [1,2,4,8,16]){let A=build(3*t,clauses(t,false)),B=build(3*t,clauses(t,true));assert(A.T.filter((x,i)=>x.mask!==B.T[i].mask).length===1,"one table neighbor");assert(check(A,lift(A,Array(3*t).fill(1)))&&!check(B,lift(B,Array(3*t).fill(1))),"SAT neighbor witness");let ca=t<=4?close(A):null,cb=t<=4?close(B):null;assert(!ca||(!ca.no&&!cb.no&&ca.freeWest===3*t&&cb.freeWest===3*t),"local closure control");neighbors.push({t,k:A.k,vertices:A.T.length,edgeVariables:A.p,gridBits:1+9*A.k+16*A.k*A.k,closureSAT:ca,closureNO:cb})}
 let cutChecks=0;for(let k of [2,3,4]){let K=k*k;for(let a=0;a<2**K;a++){let s=parity(0);for(let b=0;b<K;b++)s+=(a>>b)&1;if(3*s<K||3*s>2*K)continue;let e=0;for(let i=0;i<k;i++)for(let j=0;j<k;j++){let v=i*k+j;if(j<k-1)e+=((a>>v)^(a>>(v+1)))&1;if(i<k-1)e+=((a>>v)^(a>>(v+k)))&1}assert(3*e>=k,"grid cut");cutChecks++}}
 let singletonChecks=0;for(let k of [2,4,8,16,32]){let G=singleton(k),x=Array(G.p).fill(0);assert(check(G,x),"singleton accept");G.T[0].mask=1<<2;assert(close(G).no,"singleton mismatch");singletonChecks++}
 return {c,r,frames,gateChecks,formulaTests,lifts,dpTests,t5Tests,neighbors,cutChecks,singletonChecks};
}
console.log(JSON.stringify(audit(),null,2));
