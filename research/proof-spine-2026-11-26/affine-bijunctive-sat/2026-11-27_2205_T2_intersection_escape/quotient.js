const key=c=>c.slice().sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b).join(",");
function up(F,n,g,st){let A=new Int8Array(n+1),ch=true;for(let l of g){let i=Math.abs(l),v=Math.sign(l);if(A[i]===-v)return {A,bad:true};A[i]=v}while(ch){ch=false;for(let c of F){let u=0,k=0,hit=false;for(let l of c){st.reads++;let a=A[Math.abs(l)];if(a===Math.sign(l)){hit=true;break}if(!a){k++;u=l}}if(hit)continue;if(!k)return {A,bad:true};if(k===1){A[Math.abs(u)]=Math.sign(u);ch=true}}}return{A,bad:false}}
function replay(F,n,P){let rows=F.slice(),ix=new Map(),units=[],reads=0;function add(c){let j=rows.length;rows.push(c);if(c.length<=1)units.push(j);for(let l of c){if(!ix.has(l))ix.set(l,[]);ix.get(l).push(j)}}rows=[];F.forEach(add);for(let p of P){let A=new Int8Array(n+1),q=[],bad=false;function set(l){let i=Math.abs(l),s=Math.sign(l);if(A[i]===-s)bad=true;else if(!A[i]){A[i]=s;q.push(l)}}for(let l of p)set(-l);for(let j of units){if(!rows[j].length){bad=true;break}set(rows[j][0])}for(let k=0;k<q.length&&!bad;k++)for(let j of ix.get(-q[k])||[]){let u=0,z=0,hit=false;for(let l of rows[j]){reads++;let a=A[Math.abs(l)];if(a===Math.sign(l)){hit=true;break}if(!a){z++;u=l}}if(hit)continue;if(!z){bad=true;break}if(z===1)set(u);if(bad)break}if(!bad)throw Error("RUP replay");add(p)}return {reads,steps:P.length,empty:P.at(-1)?.length===0}}
function rup(F,n,cap=20000000){let rows=F.slice(),seen=new Set(F.map(key)),P=[],st={reads:0},tries=0,epochs=0,C=[[]],start=Date.now();for(let i=1;i<=n;i++)for(let s of [-1,1])C.push([s*i]);for(let i=1;i<=n;i++)for(let j=i+1;j<=n;j++)for(let s of [-1,1])for(let t of [-1,1])C.push([s*i,t*j]);while(true){epochs++;let ch=false;for(let c of C){if(seen.has(key(c)))continue;if(st.reads>cap)return{status:"UNKNOWN_CAP",P,tries,epochs,reads:st.reads,ms:Date.now()-start};tries++;if(up(rows,n,c.map(l=>-l),st).bad){rows.push(c);P.push(c);seen.add(key(c));ch=true;if(!c.length)return{status:"UNSAT",P,tries,epochs,reads:st.reads,ms:Date.now()-start}}}if(!ch)return{status:"UNKNOWN_FIXED",P,tries,epochs,reads:st.reads,ms:Date.now()-start}}}
function dpll(F,n){let rows=F.slice(),P=[],st={reads:0},nodes=0;function go(g){nodes++;if(st.reads>1e7)throw Error("DPLL cap");let z=up(rows,n,g,st);if(z.bad){let c=g.map(l=>-l);P.push(c);rows.push(c);return true}let f=new Int32Array(n+1);for(let c of rows)if(!c.some(l=>z.A[Math.abs(l)]===Math.sign(l)))for(let l of c)if(!z.A[Math.abs(l)])f[Math.abs(l)]++;let v=0;for(let i=1;i<=n;i++)if(f[i]>f[v])v=i;if(!v)return false;if(!go([...g,-v])||!go([...g,v]))return false;if(!up(rows,n,g,st).bad)throw Error("join");let c=g.map(l=>-l);P.push(c);rows.push(c);return true}let start=Date.now(),no=go([]);return{status:no?"UNSAT":"SAT",nodes,P,reads:st.reads,ms:Date.now()-start}}
function compress(F,n){let start=Date.now(),B=F.filter(c=>c.length<=2),P=F.filter(c=>c.length>2),st={reads:0},pins=[];for(let i=1;i<=n;i++)pins.push(up(B,n,[...pins,-i],st).bad?i:-i);let a=new Int8Array(n+1);for(let l of pins)a[Math.abs(l)]=Math.sign(l);if(!B.every(c=>c.some(l=>a[Math.abs(l)]===Math.sign(l))))return{status:"OUTER_UNRESOLVED",keep:F};let edges=Array.from({length:n+1},()=>[]),neg=[];for(let c of B){let d=c.map(l=>a[Math.abs(l)]===1?-l:l);if(d.some(l=>l>0)){let p=d.find(l=>l>0),q=-d.find(l=>l<0);edges[q].push(p)}else neg.push(d.map(l=>-l))}
let cache=new Map(),clVisits=0;function cl(seed){let k=seed.join(",");if(cache.has(k))return cache.get(k);let q=seed.slice(),S=new Set(q);for(let i=0;i<q.length;i++)for(let u of edges[q[i]]){clVisits++;if(!S.has(u)){q.push(u);S.add(u)}}for(let c of neg){clVisits++;if(c.every(x=>S.has(x))){cache.set(k,null);return null}}let s=[...S].sort((a,b)=>a-b).join(",");cache.set(k,s);return s}
let K=new Map(),keys=[],vec=[];function id(s){if(!K.has(s)){K.set(s,keys.length);keys.push(s)}return K.get(s)}let one=id(cl([]));for(let c of P){if(c.length>10)return{status:"DEGREE_CAP",keep:F,degree:c.length};let terms=[[]];for(let l of c){let i=Math.abs(l),b=Number(a[i]!==Math.sign(l));terms=terms.flatMap(s=>[...(b?[s]:[]),[...new Set([...s,i])].sort((a,b)=>a-b)])}let v=0n;for(let s of terms){let q=cl(s);if(q!==null)v^=1n<<BigInt(id(q))}vec.push(v)}
let D=new Map(),keep=[],deps=[],xors=0;function reduce(v,p){while(v){let j=v.toString(2).length-1,q=D.get(j);if(!q)return{v,p,j};v^=q.v;p^=q.p;xors++}return{v,p,j:-1}}for(let i=0;i<vec.length;i++){let q=reduce(vec[i],1n<<BigInt(i));if(q.v){D.set(q.j,q);keep.push(i)}else deps.push([i,q.p.toString(16)])}let q=reduce(1n<<BigInt(one),0n),contradiction=!q.v,checks=0,evalXors=0;for(let k of keys){let S=new Set(k?k.split(",").map(Number):[]),vals=P.map(c=>{checks+=c.length;return Number(c.every(l=>((a[Math.abs(l)]===1)^S.has(Math.abs(l)))!==Number(l>0)))});function sum(mask){let v=0;while(mask){let low=mask&-mask;v^=vals[low.toString(2).length-1];mask^=low;evalXors++}return v}for(let [i,h] of deps)if(sum(BigInt("0x"+h)))throw Error("dep");if(contradiction&&sum(q.p)!==1)throw Error("constant")}
return{status:contradiction?"UNSAT":"EQUIVALENT",keep:[...B,...keep.map(i=>P[i])],packets:P.length,rank:D.size,binary:B.length,keys:keys.length,degree:Math.max(0,...P.map(c=>c.length)),proof:{pins,keys,kept:keep,deps,constant:contradiction?q.p.toString(16):null},reads:st.reads,clVisits,xors,checks,evalXors,ms:Date.now()-start}}
function parity(F){let M=new Map(),reads=0,eq=[],piv=new Map(),xors=0;for(let c of F){let s=[...new Set(c.map(Math.abs))].sort((a,b)=>a-b),k=s.join(",");if(!M.has(k))M.set(k,{s,C:[]});M.get(k).C.push(c)}for(let {s,C} of M.values()){if(s.length>10)continue;let good=[];for(let m=0;m<2**s.length;m++)if(C.every(c=>c.some(l=>{reads++;return Boolean((m>>s.indexOf(Math.abs(l)))&1)===(l>0)})))good.push(m);if(!good.length)return{status:"UNSAT",eq,reads,xors,rank:piv.size};for(let mask=1;mask<2**s.length;mask++){let p=m=>{let a=m&mask,b=0;while(a){a&=a-1;b^=1}return b},b=p(good[0]);if(good.every(m=>p(m)===b)){let v=0n;for(let i=0;i<s.length;i++)if(mask&(1<<i))v|=1n<<BigInt(s[i]-1);eq.push({v:v.toString(16),b,scope:s});while(v){let k=v.toString(2).length-1;if(!piv.has(k)){piv.set(k,[v,b]);break}let z=piv.get(k);v^=z[0];b^=z[1];xors++}if(!v&&b)return{status:"UNSAT",eq,reads,xors,rank:piv.size}}}}return{status:"UNKNOWN",eq,reads,xors,rank:piv.size}}
function fusion(F,n,width=3,cap=128){let seen=new Set(F.map(key)),P=[],pairs=0;outer:for(let i=0;i<F.length;i++)for(let j=i+1;j<F.length;j++){pairs++;for(let l of F[i])if(F[j].includes(-l)){let c=[...new Set([...F[i].filter(x=>x!==l),...F[j].filter(x=>x!==-l)])];if(c.length>width||c.some(x=>c.includes(-x))||seen.has(key(c)))continue;P.push(c);seen.add(key(c));if(P.length>=cap)break outer}}return{P,pairs,replay:replay(F,n,P)}}
function feedback(F,n){let out=[];for(let width of [2,4])for(let mode of ["baseline","flips","deductions","table","residue"]){let rows=F.slice(),P=[],reads=0,flips=0,ties=0,ro=0,pairs=0,a=new Uint8Array(n+1),start=Date.now();function score(){let bad=0,z=0;for(let c of rows){let k=0,s=0;for(let l of c){reads++;if(Boolean(a[Math.abs(l)])===(l>0)){k++;s+=Math.sign(l)}}if(!k)bad++;let kr=k%3,sr=((s%3)+3)%3;ro+=2;if(k&&sr===0)z++;if(kr<0)throw Error("residue")}return[bad,z]}function hill(){for(let t=0;t<n;t++){let [orig]=score(),best=orig,bz=Infinity,v=0,plain=0;for(let i=1;i<=n;i++){a[i]^=1;let [b,z]=score();a[i]^=1;if(b<best){best=b;v=plain=i;bz=z}else if(b===best&&b<orig&&mode==="residue"&&z<bz){v=i;bz=z}}if(!v)break;if(v!==plain)ties++;a[v]^=1;flips++}}if(["flips","table","residue"].includes(mode))hill();if(["deductions","table","residue"].includes(mode)){let f=fusion(F,n,width);P=f.P;pairs=f.pairs;rows.push(...P);if(mode!=="deductions")hill()}out.push({mode,width,flips,ties,learn:P.length,pairs,reads,ro,replay:replay(F,n,P),peakRows:rows.length,ms:Date.now()-start})}return out}


function quotient(F,n,cap=1000000,maxTerms=20000){
 let start=Date.now(),B=F.filter(c=>c.length<=2),P=F.filter(c=>c.length>2),ops=0,peak=1,depth=0;
 const bit=i=>1n<<BigInt(i),ids=l=>Math.abs(l)-1,ix=l=>2*ids(l)+Number(l<0);
 let A=Array.from({length:2*n},()=>[]),R=A.map(()=>[]);for(let c of B){if(!c.length)return{status:"UNSAT_OUTER",ops};let a=ix(c[0]),b=ix(c.at(-1));for(let [u,v] of [[a^1,b],[b^1,a]]){A[u].push(v);R[v].push(u);ops++}}
 let vis=new Uint8Array(2*n),order=[],comp=new Int32Array(2*n).fill(-1);
 function dfs(v){vis[v]=1;for(let u of A[v]){ops++;if(!vis[u])dfs(u)}order.push(v)}
 function back(v,c){comp[v]=c;for(let u of R[v]){ops++;if(comp[u]<0)back(u,c)}}
 for(let i=0;i<2*n;i++)if(!vis[i])dfs(i);let nc=0;for(let i=order.length-1;i>=0;i--)if(comp[order[i]]<0)back(order[i],nc++);
 for(let i=0;i<n;i++)if(comp[2*i]===comp[2*i+1])return{status:"UNSAT_OUTER",ops,pivot:i+1,ms:Date.now()-start};
 let a=Array.from({length:n},(_,i)=>Number(comp[2*i]>comp[2*i+1]));if(!B.every(c=>c.some(l=>a[ids(l)]===Number(l>0))))throw Error("anchor");
 let adj=Array.from({length:n},()=>[]),neg=[];
 for(let c of B){let d=c.map(l=>a[ids(l)]?-l:l),p=d.find(l=>l>0);if(p)adj[ids(d.find(l=>l<0))].push(ids(p));else neg.push(d.map(l=>ids(l)).reduce((m,i)=>m|bit(i),0n))}
 let reaches=[];for(let i=0;i<n;i++){let q=[i],m=bit(i);for(let j=0;j<q.length;j++)for(let v of adj[q[j]]){ops++;if(!(m&bit(v))){m|=bit(v);q.push(v)}}reaches.push(m)}
 let cache=new Map([[0n,true]]);
 function ok(m){if(cache.has(m))return cache.get(m);for(let f of neg){ops++;if((m&f)===f){cache.set(m,false);return false}}cache.set(m,true);return true}
 function toggle(s,m){if(s.has(m))s.delete(m);else s.add(m)}
 let Q=new Set([0n]),trace=[];
 for(let c of P){
  let R=new Set(Q),failed=false;
  for(let l of c){let v=ids(l),constant=Number(a[v]!==Number(l>0)),S=constant?new Set(R):new Set();
   for(let m of R){ops++;let z=m|reaches[v];if(ok(z))toggle(S,z);if(ops>cap||S.size>maxTerms||cache.size>maxTerms){failed=true;break}}
   peak=Math.max(peak,S.size,Q.size,R.size,cache.size);if(failed)break;R=S;
   if(!R.size)break;
  }
  if(failed)return{status:"UNKNOWN_CAP",depth,ops,peak,cache:cache.size,terms:Q.size,trace,ms:Date.now()-start};
  for(let m of R){ops++;toggle(Q,m)}
  depth++;trace.push(Q.size);peak=Math.max(peak,Q.size,cache.size);
  if(!Q.size)return{status:"UNSAT_QUOTIENT",depth,ops,peak,cache:cache.size,terms:0,trace,ms:Date.now()-start};
 }
 let best=null,pop=v=>{let k=0;while(v){v&=v-1n;k++}return k};for(let m of Q)if(best===null||pop(m)<pop(best))best=m;
 let witness=a.map((x,i)=>x^Number(Boolean(best&bit(i))));if(!F.every(c=>c.some(l=>witness[ids(l)]===Number(l>0))))throw Error("witness");
 return {status:"SAT",depth,ops,peak,cache:cache.size,terms:Q.size,trace,witness,ms:Date.now()-start}
}
function carrierReplay(F,n,cap=2000000){
 let B=F.filter(c=>c.length<=2),P=F.filter(c=>c.length>2),st={reads:0},nodes=0,leaves=0,limit=false;
 function visit(g){nodes++;if(st.reads>cap){limit=true;return false}let q=up(B,n,g,st);if(q.bad)return true;let i=1;while(i<=n&&q.A[i])i++;if(i>n){leaves++;for(let c of P){let sat=false;for(let l of c){st.reads++;if(q.A[Math.abs(l)]===Math.sign(l)){sat=true;break}}if(!sat)return true}return false}
 return visit([...g,-i])&&visit([...g,i])}
 let no=visit([]);return{status:limit?"UNKNOWN_CAP":no?"UNSAT":"SAT",nodes,leaves,reads:st.reads}
}
function imports(F,n,ids,rows,remove=-1){let R=F.slice(),P=[],st={reads:0};for(let i=0;i<rows.length;i++){if(i===remove)continue;let c=rows[i].clause.map(l=>Math.sign(l)*(ids.indexOf(Math.abs(l))+1));if(c.some((x,j)=>!x||!ids.includes(Math.abs(rows[i].clause[j])))||!up(R,n,c.map(l=>-l),st).bad)return{status:"REFUSED",at:i,admitted:P.length,reads:st.reads};P.push(c);R.push(c)}
 let check=replay(F,n,P);let root=up(R,n,[],st);let Q=quotient(R,n);let outer=R.filter(c=>c.length<=2),audit=Q.status==="UNSAT_OUTER"?dpll(outer,n):null;if(audit&&audit.status!=="UNSAT")throw Error("outer SCC mismatch");return{status:"ADMITTED",admitted:P.length,reads:st.reads,replay:check,rootConflict:root.bad,forced:[...root.A].filter(Boolean).length,Q,clauses:P,outerAudit:audit&&{reads:audit.reads,nodes:audit.nodes,replay:replay(outer,n,audit.P)}} }
function run2(data,peer){
 let out=[];for(let x of data){let F=x.F||x.dimacs.trimEnd().split("\n").slice(1).map(c=>c.trim().split(/\s+/).map(Number).slice(0,-1)),n=x.n;
 let Q=quotient(F,n),C=compress(F,n),H=quotient(C.keep,n),R=Q.status.startsWith("UNSAT")&&x.kind==="native"?carrierReplay(F,n):null;
 let rec={name:x.name,kind:x.kind,guard:x.guard_id,residual:x.residual_id,Q,H,R}; 
 if(x.kind==="native"){
 let p=peer.find(y=>y.id===x.name),rows=p.admitted;
 let A=imports(F,n,x.ids,rows.slice(0,3)),B=imports(F,n,x.ids,rows),ablation=[0,1,2].map(i=>imports(F,n,x.ids,rows.slice(0,3),i));
 rec.partner={A,B,ablation,otherResidual:p.ownResidual};
 }
 out.push(rec);
 }return out
}

const fs=require('node:fs');console.log(JSON.stringify(run2(JSON.parse(fs.readFileSync(process.argv[2],'utf8')),JSON.parse(fs.readFileSync(process.argv[3],'utf8'))),null,2));
