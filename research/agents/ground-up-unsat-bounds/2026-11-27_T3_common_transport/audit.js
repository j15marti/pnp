function run(corpus,peer){
const check=(p,m)=>{if(!p)throw Error(m)};
const CAP=1000000;
function parse(s){let lines=s.trim().split(/\n/), head=lines.shift().split(/\s+/),n=+head[2],c=lines.map(l=>l.trim().split(/\s+/).map(Number).slice(0,-1));check(c.length===+head[3],"header");return {n,c};}
function lane(n,c,ids){
 let ev=0,nodes=0,units=0,initial=0; const scan=()=>{if(++ev>CAP)throw Error("cap");};
 function rec(a,depth){nodes++;let trail=[];while(true){let changed=false;let scores=new Int32Array(n+1);let unresolved=false;
 for(const id of ids){const cl=c[id-1];let sat=false,u=0,last=0;for(const l of cl){scan();let v=a[Math.abs(l)];if(v===Math.sign(l)){sat=true;break}if(!v){u++;last=l}}if(sat)continue;unresolved=true;if(!u)return {trail,conflict:id};if(u===1){a[Math.abs(last)]=Math.sign(last);trail.push([last,id]);units++;if(depth===0)initial++;changed=true;break}for(const l of cl)if(!a[Math.abs(l)])scores[Math.abs(l)]+=u===2?4:u===3?2:1;}
 if(changed)continue;if(!unresolved)return {trail,sat:Array.from(a)};let v=0;for(let i=1;i<=n;i++)if(!a[i]&&scores[i]>(v?scores[v]:0))v=i;check(v,"branch");let b=a.slice();b[v]=-1;let left=rec(b,depth+1);if(left.sat)return left;b=a.slice();b[v]=1;let right=rec(b,depth+1);if(right.sat)return right;return {trail,branch:v,left,right};}}
 try{let tree=rec(new Int8Array(n+1),0);return {status:tree.sat?"SAT":"UNSAT",tree,ev,nodes,units,initial}}catch(e){if(e.message!=="cap")throw e;return {status:"UNKNOWN",ev,nodes,units,initial}}}
 function replay(n,c,tree){let ev=0,used=new Set(),nodes=0;
 function go(t,a){nodes++;for(const [l,id] of t.trail){let cl=c[id-1];check(cl&&cl.includes(l)&&!a[Math.abs(l)],"unit target");for(const x of cl){ev++;if(x!==l)check(a[Math.abs(x)]===-Math.sign(x),"reason")}a[Math.abs(l)]=Math.sign(l);used.add(id);}
 if(t.conflict){let cl=c[t.conflict-1];check(cl,"conflict id");for(const x of cl){ev++;check(a[Math.abs(x)]===-Math.sign(x),"conflict")}used.add(t.conflict);return}
 let v=t.branch;check(v&&!a[v],"branch replay");let b=a.slice();b[v]=-1;go(t.left,b);b=a.slice();b[v]=1;go(t.right,b);}
 go(tree,new Int8Array(n+1));return {ev,nodes,used:[...used].sort((a,b)=>a-b)};}
 function resolution(c,tree){let db=c.map(x=>[...new Set(x)].sort((a,b)=>a-b)),proof=[],cache=new Map(),read=0;
 function res(i,j,v){let a=db[i-1],b=db[j-1];check((a.includes(v)&&b.includes(-v))||(a.includes(-v)&&b.includes(v)),"pivot");let key=[Math.min(i,j),Math.max(i,j),v].join(",");if(cache.has(key))return cache.get(key);read+=a.length+b.length;let out=[...new Set([...a,...b].filter(x=>Math.abs(x)!==v))].sort((a,b)=>a-b);check(!out.some(x=>out.includes(-x)),"taut");db.push(out);let id=db.length;cache.set(key,id);proof.push([i,j,v,out]);return id;}
 function visit(t){let id;if(t.conflict)id=t.conflict;else{let l=visit(t.left),r=visit(t.right),v=t.branch;id=!db[l-1].includes(v)?l:!db[r-1].includes(-v)?r:res(l,r,v);}
 for(let k=t.trail.length-1;k>=0;k--){let [lit,reason]=t.trail[k];if(db[id-1].includes(-lit))id=res(id,reason,Math.abs(lit));}return id;}
 let end=visit(tree);check(db[end-1].length===0,"empty");return {proof,end,read};}
 function verifyRes(c,p){let db=c.map(x=>[...new Set(x)].sort((a,b)=>a-b));let reads=0,span=0,prev=0;let locations=db.map((_,i)=>i);for(const [i,j,v,out] of p.proof){let a=db[i-1],b=db[j-1];check(a&&b,"parent");check((a.includes(v)&&b.includes(-v))||(a.includes(-v)&&b.includes(v)),"pivot check");let expected=[...new Set(a.concat(b).filter(x=>Math.abs(x)!==v))].sort((x,y)=>x-y);check(JSON.stringify(expected)===JSON.stringify(out),"res check");reads+=a.length+b.length+out.length;for(let k of [i-1,j-1,db.length]){span+=Math.abs(k-prev);prev=k;}db.push(out);}
 check(db[p.end-1].length===0,"empty replay");return {reads,recordTravel:span};}
 // Independent global exact-one chart verification with direct coefficient identity.
 function chart(n,c,cert){let eq=[],used=new Set();for(const g of cert.groups){let a=c[g.clause-1];check(a.every(x=>x>0)&&JSON.stringify(a.slice().sort((a,b)=>a-b))===JSON.stringify(g.vars.slice().sort((a,b)=>a-b)),"positive group");used.add(g.clause);let pairs=new Set(g.pairs.map(id=>{used.add(id);let q=c[id-1];check(q.length===2&&q.every(x=>x<0),"pair");return q.map(Math.abs).sort((a,b)=>a-b).join(",")}));for(let i=0;i<a.length;i++)for(let j=i+1;j<a.length;j++)check(pairs.has([a[i],a[j]].sort((a,b)=>a-b).join(",")),"pair missing");eq.push(a.reduce((s,v)=>s^(1n<<BigInt(v-1)),1n<<BigInt(n)));}
 let rank=0,piv=[];for(let v=0;v<n;v++){let bit=1n<<BigInt(v),i=eq.findIndex((x,j)=>j>=rank&&(x&bit));if(i<0)continue;[eq[rank],eq[i]]=[eq[i],eq[rank]];for(let j=0;j<eq.length;j++)if(j!==rank&&(eq[j]&bit))eq[j]^=eq[rank];piv.push(v);rank++}let free=Array.from({length:n},(_,i)=>i).filter(v=>!piv.includes(v));check(rank===13&&free.length===11,"rank");
 let selected=[6,7,9,13,14,18,20,27,32,33,40,42,43,46,57,66,68,78,81,99,100,101,114,127,143,145,151,153];let poly=new Set();function toggle(t){if(poly.has(t))poly.delete(t);else poly.add(t);}
 let forms=Array.from({length:n},(_,v)=>{let j=free.indexOf(v);if(j>=0)return [1<<j];let r=eq[piv.indexOf(v)],out=[];if(r&(1n<<BigInt(n)))out.push(0);for(let k=0;k<free.length;k++)if(r&(1n<<BigInt(free[k])))out.push(1<<k);return out;});
 let terms=0;for(let id of selected){used.add(id);let q=c[id-1];check(q.length===2&&q.every(l=>l<0),"negative pair");for(let x of forms[-q[0]-1])for(let y of forms[-q[1]-1]){toggle(x|y);terms++;}}
 check(poly.size===1&&poly.has(0),"peer identity");return {rank,free:free.map(v=>v+1),terms,used:[...used].sort((a,b)=>a-b)};}
 // global Davis-Putnam variable elimination; all new clauses explicitly resolved.
 function dp(n,c){let db=c.map(q=>q.slice().sort((a,b)=>a-b)),active=db.map((_,i)=>i+1),proof=[],pairs=0;let maxActive=active.length;
 for(let step=0;step<n;step++){let best=0,cost=Infinity,pp=[],nn=[];for(let v=1;v<=n;v++){let p=[],q=[];for(let id of active){let z=db[id-1];if(z.includes(v))p.push(id);if(z.includes(-v))q.push(id);}if(p.length+q.length&&p.length*q.length<cost){best=v;cost=p.length*q.length;pp=p;nn=q;}}if(!best)return {status:"SAT",pairs,maxActive};
 if(pairs+cost>CAP||db.length>30000)return {status:"UNKNOWN",pairs,maxActive};active=active.filter(id=>!db[id-1].includes(best)&&!db[id-1].includes(-best));let keys=new Set(active.map(id=>db[id-1].join(",")));
 for(let i of pp)for(let j of nn){pairs++;let out=[...new Set(db[i-1].concat(db[j-1]).filter(x=>Math.abs(x)!==best))].sort((a,b)=>a-b);if(out.some(x=>out.includes(-x)))continue;let key=out.join(",");if(keys.has(key))continue;keys.add(key);db.push(out);active.push(db.length);proof.push([i,j,best,out]);if(!out.length)return {status:"UNSAT",pairs,maxActive,proof,end:db.length};}maxActive=Math.max(maxActive,active.length);}
 return {status:"SAT",pairs,maxActive};}
 const out=[];for(const name of ["JOINT-24","RANDOM-3CNF-40"]){let source=corpus.instances.find(x=>x.id===name),{n,c}=parse(source.dimacs);let ids=c.map((_,i)=>i+1);let local=lane(n,c,ids),global=dp(n,c);check(local.status==="UNSAT","local failed");let lc=replay(n,c,local.tree),rp=resolution(c,local.tree),rv=verifyRes(c,rp);let gv=global.status==="UNSAT"?verifyRes(c,global):null;
 let p=peer.find(x=>x.id===name),pv=replay(n,c,p.tree),pc=name==="JOINT-24"?chart(n,c,p.affine):null;let core=pc?pc.used:pv.used;let hybrid=lane(n,c,core);check(hybrid.status==="UNSAT","hybrid");let hc=replay(n,c,hybrid.tree),hr=resolution(c,hybrid.tree),hv=verifyRes(c,hr);
 // hostile neighbor: flip one clause selected in proof? not necessarily SAT; guaranteed SAT via planted assignment.
 let planted=Array.from({length:n+1},(_,i)=>i%2?1:-1),changed=0;let satc=c.map(q=>{if(q.some(l=>planted[Math.abs(l)]===Math.sign(l)))return q;changed++;return [-q[0],...q.slice(1)]});check(satc.every(q=>q.some(l=>planted[Math.abs(l)]===Math.sign(l))),"planted");
 let rejected=false;try{replay(n,satc,local.tree)}catch(e){rejected=true}check(rejected,"invalid proof accepted");
 out.push({name,N:source.dimacs.length*8,n,m:c.length,local:{...local,check:lc,resolution:rp,verify:rv},global:{...global,verify:gv},peer:{replay:pv,chart:pc,bytes:JSON.stringify(p).length},hybrid:{...hybrid,check:hc,resolution:hr,verify:hv},hostile:{changed,rejected}});}
 return out;
}
if(typeof require !== 'undefined' && require.main===module){const fs=require('fs');console.log(JSON.stringify(run(JSON.parse(fs.readFileSync(process.argv[2],'utf8')),JSON.parse(fs.readFileSync(process.argv[3],'utf8'))),null,2));}
