// C08-05 source-only exact quotient and fixed-width elimination audit.
function contract(F,n,ok){
const bit=(w,i)=>(w>>>i)&1, nae=a=>a.some(b=>b!==a[0]), valid=x=>F.flat().every(c=>nae(c.map(v=>x[v])));
let p=Array.from({length:n},(_,i)=>i);function find(i){while(p[i]!==i){p[i]=p[p[i]];i=p[i]}return i}
let adj=Array.from({length:n},()=>new Set);
for(let c of F.slice(1).flat())for(let v of c){p[find(v)]=find(c[0]);for(let u of c)if(u!==v)adj[v].add(u)}
let groups=new Map;for(let i=0;i<n;i++){let k=find(i);if(!groups.has(k))groups.set(k,[]);groups.get(k).push(i)}
let R=[...groups.values()].filter(v=>v.length===15);ok(R.length===1);R=R[0];let rid=new Map(R.map((v,i)=>[v,i])),Rlocal=F.slice(1).flat().filter(c=>rid.has(c[0]));let rowOf=Array(n).fill(-1),rows=[],blocks=[];
for(let V of groups.values()){if(V===R)continue;ok(V.length===9);let b=[];for(let v of V)if(rowOf[v]===-1){let a=V.filter(u=>u===v||!adj[v].has(u));ok(a.length===3&&a.every(u=>rowOf[u]===-1));let id=rows.length;a.forEach(u=>rowOf[u]=id);rows.push({a,pair:null,single:null,succ:-1,pred:-1});b.push(id)}ok(b.length===3);blocks.push(b)}
let rt=rows.length;R.forEach(v=>rowOf[v]=rt);rows.push({a:R,pair:null,single:null,succ:-1,pred:-1});
for(let c of F[0]){let z=c.map(v=>rowOf[v]);if(z.every(t=>t===rt)){Rlocal.push(c);continue}
let t=z.find(t=>z.filter(u=>u===t).length>=2);ok(t!==undefined);let i=z.findIndex(u=>u!==t);if(i<0)i=2;let u=z[i],A=rows[t],B=rows[u];ok(A.pair===null&&B.single===null);A.pair=c.filter((_,j)=>j!==i);A.succ=u;B.single=c[i];B.pred=t}
ok(rows.every(t=>t.pair&&t.single!==null&&t.succ>=0&&t.pred>=0));let forced=Array(rows.length).fill(false),Q=[],wire=0,edges=Array.from({length:rows.length},()=>[]);
function edge(t,u){edges[t].push(u);edges[u].push(t)}
for(let b of blocks){let self=b.filter(t=>rows[t].succ===t);ok(self.length<=1);if(!self.length){Q.push(b);continue}wire++;let kept=b.filter(t=>t!==self[0]);kept.forEach(t=>forced[t]=true);edge(...kept)}
for(let t=0;t<rt;t++)if(forced[t]&&forced[rows[t].succ])edge(t,rows[t].succ);
for(let b of Q)for(let t of b){let u=rows[t].succ;ok(forced[u]&&rows[u].succ===t&&rows[t].pred===u)}
ok(forced[rows[rt].succ]&&forced[rows[rt].pred]);
let rWitness=[null,null],rw=rows[rt];for(let w=0;w<32768&&rWitness.some(a=>a===null);w++){if(bit(w,rid.get(rw.pair[0]))===bit(w,rid.get(rw.pair[1])))continue;if(!Rlocal.every(c=>nae(c.map(v=>bit(w,rid.get(v))))))continue;rWitness[bit(w,rid.get(rw.single))]=w}
ok(rWitness.every(w=>w!==null));
let phase=Array(rows.length).fill(-1),color=Array(rows.length).fill(-1),q=0;
for(let t=0;t<rt;t++)if(forced[t]&&phase[t]<0){let queue=[t];phase[t]=q;color[t]=0;for(let i=0;i<queue.length;i++)for(let u of edges[queue[i]]){let v=queue[i];if(phase[u]<0){phase[u]=q;color[u]=1^color[v];queue.push(u)}else if(color[u]===color[v])return{status:"UNSAT",reason:"wire parity"}}q++}
let C=Q.map(b=>b.map(t=>{let u=rows[t].pred;return [phase[u],1^color[u]]}));
let uf=Array.from({length:q},(_,i)=>i),sign=Array(q).fill(0);function root(i){let t=i,s=0;while(uf[t]!==t){s^=sign[t];t=uf[t]}return[t,s]}function join(a,b,d){let [u,s]=root(a),[v,t]=root(b);if(u===v)return (s^t)===d;uf[u]=v;sign[u]=s^t^d;return true}
let clauses=C.slice(),taut=0,equations=0;for(;;){let next=[],change=false;for(let c of clauses){let a=c.map(([v,s])=>{let [u,t]=root(v);return[u,s^t]});if(a.some(([v,s],i)=>a.some(([u,t],j)=>i!==j&&v===u&&s!==t))){taut++;continue}let M=new Map(a);if(M.size===1)return{status:"UNSAT",reason:"constant NAE"};if(M.size===2){let [[v,s],[u,t]]=[...M];if(!join(v,u,1^s^t))return{status:"UNSAT",reason:"affine closure"};equations++;change=true;continue}next.push(a)}clauses=next;if(!change)break}
let ids=[...new Set(Array.from({length:q},(_,i)=>root(i)[0]))],ix=new Map(ids.map((v,i)=>[v,i])),d=ids.length;
let factors=clauses.map(c=>{let vars=c.map(([v])=>ix.get(v)),tab=new Uint8Array(8);for(let w=0;w<8;w++)tab[w]=Number(nae(c.map(([v,s],i)=>bit(w,i)^s)));return{vars,tab}});
let dom=Array(d).fill(3),alive=new Set(Array.from({length:d},(_,i)=>i)),records=[],width=0,ops=0,rounds=0;
function close(){for(;;){rounds++;let changed=false;for(let f of factors){let sup=Array(f.vars.length).fill(0),any=false;for(let w=0;w<f.tab.length;w++)if(f.tab[w]){ops++;if(!f.vars.every((v,i)=>dom[v]&(1<<bit(w,i)))){f.tab[w]=0;changed=true;continue}any=true;f.vars.forEach((v,i)=>sup[i]|=1<<bit(w,i))}if(!any)return false;for(let i=0;i<f.vars.length;i++){let v=f.vars[i],t=dom[v]&sup[i];if(t!==dom[v]){dom[v]=t;changed=true}if(!t)return false}}if(!changed)return true}}
let initial=clauses.length;
while(alive.size){if(!close())return{status:"UNSAT",wire,clauseBlocks:Q.length,phases:q,taut,equations,remaining:initial,width,ops,rounds};
let nei=Array.from({length:d},()=>new Set);for(let f of factors)for(let v of f.vars)for(let u of f.vars)if(u!==v)nei[v].add(u);
let v=-1;for(let u of alive)if(v<0||nei[u].size<nei[v].size)v=u;let B=[...nei[v]],w=B.length;width=Math.max(width,w);if(w>16)return{status:"UNKNOWN",width,phases:q,taut,equations,remaining:initial};
let hit=factors.filter(f=>f.vars.includes(v)),rest=factors.filter(f=>!f.vars.includes(v)),pos=new Map(B.map((u,i)=>[u,i]));
let enc=hit.map(f=>f.vars.map(u=>u===v?-1:pos.get(u))),tab=new Uint8Array(2**w),choice=new Int8Array(2**w).fill(-1);
for(let z=0;z<tab.length;z++){if(!B.every((u,i)=>dom[u]&(1<<bit(z,i))))continue;for(let b=0;b<2;b++)if(dom[v]&(1<<b)){let good=true;for(let i=0;i<hit.length;i++){let a=0;enc[i].forEach((j,k)=>a|=(j<0?b:bit(z,j))<<k);ops++;if(!hit[i].tab[a]){good=false;break}}if(good){tab[z]=1;choice[z]=b;break}}}
if(!tab.some(x=>x))return{status:"UNSAT",wire,clauseBlocks:Q.length,phases:q,taut,equations,remaining:initial,width,ops,rounds};
if(B.length)rest.push({vars:B,tab});records.push({v,B,choice});factors=rest;alive.delete(v)}
let model=Array(d);for(let i=records.length-1;i>=0;i--){let {v,B,choice}=records[i],z=B.reduce((a,u,j)=>a|(model[u]<<j),0);model[v]=choice[z];ok(model[v]>=0)}
let z=Array.from({length:q},(_,i)=>{let[u,s]=root(i);return model[ix.get(u)]^s});
ok(C.every(c=>nae(c.map(([v,s])=>z[v]^s))));
let x=Array(n);function mono(t,b){rows[t].a.forEach(v=>x[v]=b)}function free(t,b){let a=rows[t];x[a.pair[0]]=0;x[a.pair[1]]=1;x[a.single]=b}
for(let t=0;t<rt;t++)if(forced[t])mono(t,z[phase[t]]^color[t]);else if(rows[t].succ===t)free(t,0);
for(let b of Q){let a=b.map(t=>{let u=rows[t].pred;return 1^z[phase[u]]^color[u]}),i0=a.indexOf(0),i1=a.indexOf(1);ok(i0>=0&&i1>=0);b.forEach((t,i)=>{if(i===i0||i===i1)mono(t,a[i]);else free(t,a[i])})}
let u=rw.pred,word=rWitness[1^z[phase[u]]^color[u]];R.forEach((v,i)=>x[v]=bit(word,i));ok(x.every(v=>v===0||v===1)&&valid(x),"actual witness lift");
return{status:"SAT",wire,clauseBlocks:Q.length,phases:q,taut,equations,remaining:initial,width,ops,rounds};
}
// node audit.js; C08-05 standalone monitor amplification, adapted from FN13 gate_audit.js
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
let monitorStart=C.length; for(let i=0;i<n;i++){C.push([literal(s),literal(t,1),literal(s,1)],[literal(s,1),literal(t),literal(s)]);} let monitorEnd=C.length; let counts=Array.from({length:d},()=>[0,0]);for(let c of C)for(let [v,z] of c)counts[v][z]++;counts[s][0]++;counts[t][0]++;let h=d++;for(let v=0;v<counts.length;v++){let [p,q]=counts[v];for(let j=0;j<Math.abs(p-q);j++)C.push([literal(h),literal(h,1),literal(v,p>q?1:0)])}ok(C.length===10*m+2*n);
function extend(x,S,T){let z=Array(d).fill(0);for(let i=0;i<n;i++)z[i]=x[i];z[s]=S;z[t]=T;for(let {a,u,v} of chains){let p=split(a.map(l=>val(l,z)));ok(p!==null,"guarded model");[z[u],z[v]]=p}ok(C.every(c=>nae(c.map(l=>val(l,z)))));return z}
return{C,d,s,t,extend,monitorStart,monitorEnd}}
function compile(F,n){let m=4*n/3,{C,d,s,t,extend,monitorStart,monitorEnd}=guarded(F,n),occ=Array.from({length:d},()=>[[],[]]),positions=C.map(c=>c.map(([v,sign])=>{let o={v,sign,w:-1};occ[v][sign].push(o);return o})),sp={v:s,sign:0,w:-1},tp={v:t,sign:0,w:-1};occ[s][0].push(sp);occ[t][0].push(tp);
let wire=[],succ=new Map;const token=(b,row)=>3*b+row;
for(let v=0;v<d;v++){let [p,q]=occ[v];ok(p.length===q.length&&p.length>0);let a=[];for(let i=0;i<p.length;i++)for(let o of [p[i],q[i]]){o.w=wire.length;wire.push(o);a.push(o.w)}for(let i=0;i<a.length;i++){let b=a[i];succ.set(token(b,0),token(b,0));succ.set(token(b,1),token(a[(i+1)%a.length],1))}}
let B=wire.length+C.length,off=9*B,N=off+15,H=[[],[],[],[]],gateA=token(sp.w,2),gateB=token(tp.w,2);ok(wire.length===30*m+6*n+2&&N===552*n+33);
for(let j=0;j<C.length;j++)for(let r=0;r<3;r++){let a=token(positions[j][r].w,2),b=token(wire.length+j,r);succ.set(a,b);succ.set(b,a)}
for(let i=0;i<3*B;i++){let a=3*i;if(i===gateA)H[0].push([a,a+1,3*gateB+2]);else if(i===gateB)H[0].push([a,a+1,off+4]);else{ok(succ.has(i));H[0].push([a,a+1,3*succ.get(i)+2])}}
H[0].push([off+11,off+14,3*gateA+2]);for(let j=0;j<4;j++)for(let i=0;i<P[j].length;i++)if(j!==0||i!==0)H[j].push(P[j][i].map(v=>v+off));
for(let b=0;b<B;b++)for(let j=1;j<4;j++)for(let c of AG[j])H[j].push(c.map(v=>v+9*b));
function lift(z){let x=Array(N);function mono(T,b){for(let i=0;i<3;i++)x[3*T+i]=b}function free(T,b){x[3*T]=0;x[3*T+1]=1;x[3*T+2]=b}
for(let w=0;w<wire.length;w++){let o=wire[w],b=z[o.v]^o.sign;free(token(w,0),0);mono(token(w,1),b);mono(token(w,2),1^b)}
for(let j=0;j<C.length;j++){let a=C[j].map(l=>val(l,z)),i0=a.indexOf(0),i1=a.indexOf(1);ok(i0>=0&&i1>=0);for(let r=0;r<3;r++){let T=token(wire.length+j,r);if(r===i0||r===i1)mono(T,a[r]);else free(T,a[r])}}
let base=20933;for(let i=0;i<15;i++)x[off+i]=bit(base,i)^z[t];ok(x[off+4]===z[t]&&x[off+11]!==x[off+14]);ok(x.every(v=>v===0||v===1));return x}
function project(x){ok(count(H,x)===0);let z=Array(d).fill(-1);for(let w=0;w<wire.length;w++){let o=wire[w],b=x[9*w+3]^o.sign;ok(z[o.v]===-1||z[o.v]===b);z[o.v]=b}ok(z[s]!==z[t]);ok(C.every(c=>nae(c.map(l=>val(l,z)))));let y=z.slice(0,n).map(v=>v^z[t]);ok(count(F,y)===0);return y}
return{H,N,base:lift(extend(Array(n).fill(0),0,0)),sat:x=>lift(extend(x,1,0)),project,wireBlocks:wire.length,clauseBlocks:C.length,monitorStart:wire.length+monitorStart,monitorEnd:wire.length+monitorEnd}}
function ring(k,no){let F=[[],[],[],[]];for(let b=0;b<k;b++)for(let j=0;j<4;j++)for(let i=0;i<3;i++){let c=AG[j][i].map(v=>9*b+v);if(j===0&&(i===0||(!no&&i===1)))c[2]=9*((b+1)%k)+AG[j][i][2];F[j].push(c)}let x=Array.from({length:9*k},(_,i)=>{let t=Math.floor(i/9),r=i%9;return r<3?t%2:r<6?1^(t%2):r===8?1:0});return{F,n:9*k,x}}
function brute(F,n){for(let w=0;w<2**n;w++)if(F.flat().every(c=>{let a=bit(w,c[0]),b=bit(w,c[1]),d=bit(w,c[2]);return a!==b||b!==d}))return w;return null}
let local=[]; for(let polarity of [0,1]){let w=Array(9).fill(0);for(let i=0;i<3;i++)w[i]=polarity;for(let i=3;i<6;i++)w[i]=1^polarity;w[6]=0;w[7]=1;w[8]=1^polarity;for(let S of [0,1]){let T=1^S;let l=[S^polarity,T^1^polarity,S^1^polarity],num=0,min=[3,3,3,3];for(let b=0;b<512;b++){let y=Array.from({length:9},(_,i)=>bit(b,i));if(![2,5,8].every((i,j)=>y[i]===l[j])||!AG.slice(1).flat().every(c=>!bad(c,y)))continue;num++;let d=[Number((y[6]^y[7])!==(w[6]^w[7]))];for(let j=1;j<4;j++)d.push(AG[j].filter(c=>!c.every(v=>(y[v]^w[v])===(y[c[0]]^w[c[0]]))).length);ok(d.every(x=>x>=1),'monitor obstruction');min=min.map((x,i)=>Math.min(x,d[i]));}ok(num>0);local.push({polarity,S,T,num,min});}} let cases=[];for(let k of [2,4,8,16])for(let no of [false,true]){let{F,n,x}=ring(k,no);auth(F,n);let ref=n<=18?brute(F,n):undefined;if(ref!==undefined)ok((ref===null)===no);if(no){let L=F.flat().filter(c=>c.every(v=>v<9));ok(L.length===11);ok(brute([L],9)===null)}else ok(count(F,x)===0);let Q=compile(F,n);auth(Q.H,Q.N);ok(count(Q.H,Q.base)===1,"exact one defect");let defect=Q.H.flat().find(c=>bad(c,Q.base));ok(defect!==undefined);let release=null;if(!no){let y=Q.sat(x);ok(count(Q.H,y)===0);ok(Q.project(y).every((v,i)=>v===x[i]));release=Q.H.map(part=>part.filter(c=>!c.every(v=>(y[v]^Q.base[v])===(y[c[0]]^Q.base[c[0]]))).length);ok(release.every(d=>d>=2*n));for(let b=Q.monitorStart;b<Q.monitorEnd;b++){let a=9*b;ok((y[a+6]^y[a+7])!==(Q.base[a+6]^Q.base[a+7]));for(let j=1;j<4;j++)ok(AG[j].some(c=>!c.every(v=>(y[a+v]^Q.base[a+v])===(y[a+c[0]]^Q.base[a+c[0]]))));}}
let p=shuffle(Array.from({length:Q.N},(_,i)=>i)),G=Q.H.map(part=>shuffle(part.map(c=>shuffle(c.map(v=>p[v]))))),b=Array(Q.N);Q.base.forEach((v,i)=>b[p[i]]=v);auth(G,Q.N);ok(count(G,b)===1);let acquired=contract(G,Q.N,ok);ok(acquired.status===(no?'UNSAT':'SAT'),'source-only decision');cases.push({k,n,physical:Q.N,physicalClauses:4*Q.N/3,status:no?"UNSAT":"SAT",suppliedDefects:1,reference:n<=18?"exhaustive original":no?"11-line contradiction in original":"explicit original witness",wireBlocks:Q.wireBlocks,clauseBlocks:Q.clauseBlocks,monitorBlocks:2*n,release,acquired})}
return{seed:20261126,checks,guardTruthTable:32,local,cases}
}




console.log(JSON.stringify(gateAudit(),null,2));
