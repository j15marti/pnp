function crossScope(src){
const C=Function(src.compiler.slice(src.compiler.indexOf("function compile("),src.compiler.indexOf("function auditLocal("))+";return compile")(),H=Function(src.hybrid.split('if(typeof require==="function"')[0]+";return {sha,norm,closure,affine,compact,reduce,solve,canon,unique}")(),B=JSON.parse(src.corpus),R=JSON.parse(src.registry);
const assert=(x,m)=>{if(!x)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b),V=F=>[...new Set(F.flat().map(Math.abs))].sort((a,b)=>a-b),mod=x=>(x%3+3)%3;
function up(F,g=[]){let p=new Map(g),reads=0;for(;;){let ch=false;for(let c of F){let a=[],hit=false;for(let l of c){reads++;let v=Math.abs(l);if(p.has(v)){if(p.get(v)===+(l>0)){hit=true;break}}else a.push(l)}if(hit)continue;if(!a.length)return {bad:true,p,reads};if(a.length===1){p.set(Math.abs(a[0]),+(a[0]>0));ch=true}}if(!ch)return {bad:false,p,reads}}}
function restrict(F,p){return H.unique(F.filter(c=>!c.some(l=>p.has(Math.abs(l))&&p.get(Math.abs(l))===+(l>0))).map(c=>c.filter(l=>!p.has(Math.abs(l)))))}
function scope(c){return c.map(Math.abs).sort((a,b)=>a-b).join(",")}
function res(F,width,same,order=null,cap=40000,maxNew=120){
 let D=F.slice(),S=new Set(D.map(c=>c.join(","))),steps=[],work=0,failed=0;
 let ord=order?F.map((_,i)=>i).sort((a,b)=>order[a]-order[b]||a-b):F.map((_,i)=>i);
 outer:for(let ii=0;ii<ord.length;ii++)for(let jj=ii+1;jj<ord.length;jj++){let i=ord[ii],j=ord[jj],a=D[i],b=D[j];if(++work>cap)break outer;if(same&&scope(a)!==scope(b))continue;if(!same&&scope(a)===scope(b))continue;
 for(let l of a)if(b.includes(-l)){work++;let q=H.canon(a.filter(x=>x!==l).concat(b.filter(x=>x!==-l)));if(!q||q.length>width||S.has(q.join(","))){failed++;continue}S.add(q.join(","));steps.push({i,j,l,q});D.push(q);if(steps.length>=maxNew)break outer}}
 return {D,steps,work,failed}
}
function replay(F,steps){let D=F.slice(),checks=0;for(let t of steps){let a=D[t.i],b=D[t.j];assert(a&&b&&a.includes(t.l)&&b.includes(-t.l),"resolution parents");let q=H.canon(a.filter(x=>x!==t.l).concat(b.filter(x=>x!==-t.l)));assert(eq(q,t.q),"resolvent");D.push(q);checks+=a.length+b.length}return {D,checks}}
function polynomial(F,same,D=3){
 // Each generator is a false-clause indicator times a monomial of degree <=D-width.
 // Restrict to original clause scopes in identical-scope baseline; global cancellation only in cross mode.
 let vars=V(F),n=vars.length,index=new Map(vars.map((v,i)=>[v,i])),mons=[0n],mi=new Map([["0",0]]);let ops=0,cap=2000000;
 function combinations(start,left,mask,cb){if(!left){cb(mask);return}for(let j=start;j<=n-left;j++)combinations(j+1,left-1,mask|(1n<<BigInt(j)),cb)}
 for(let d=1;d<=D;d++)combinations(0,d,0n,a=>{mi.set(a.toString(),mons.length);mons.push(a)});
 const deg=a=>{let z=0;while(a){z++;a&=a-1n}return z};
 function cp(c){let S=new Set([0n]);for(let l of c){let b=1n<<BigInt(index.get(Math.abs(l))),T=new Set();const add=x=>T.has(x)?T.delete(x):T.add(x);for(let a of S){if(l>0)add(a);add(a|b)}S=T}return [...S]}
 function encode(p){let r=0n;for(let a of p){let j=mi.get(a.toString());assert(j!==undefined,"degree");r^=1n<<BigInt(j)}return r}
 function gen(c,mask){let a=cp(c).map(x=>x|mask);let S=new Set();for(let x of a)S.has(x)?S.delete(x):S.add(x);return encode(S)}
 let G=[],groups=new Map();
 for(let [i,c] of F.entries()){if(c.length>D)continue;let masks=[0n];if(c.length<D&&!same)for(let d=1;d<=D-c.length;d++)combinations(0,d,0n,a=>masks.push(a));for(let mask of masks){let row=gen(c,mask);if(row)G.push({i,mask:mask.toString(),row})}}
 let identities=[],rank=0,peak=0,contradiction=false;
 for(let [j,g] of G.entries()){let key=same?scope(F[g.i]):"*";if(!groups.has(key))groups.set(key,new Map());let A=groups.get(key),r=g.row,w=1n<<BigInt(j);
 while(r){if(++ops>cap)throw Error("poly cap");let i=r.toString(2).length-1;if(!A.has(i)){A.set(i,[r,w]);rank++;peak=Math.max(peak,A.size);break}let [a,b]=A.get(i);r^=a;w^=b}
 }
 // Extract all constant/linear basis rows, and replay using independent direct clause expansion.
 let check=0;for(let A of groups.values())for(let [i,[r,w]] of A){if(i>n)continue;let ids=[],sum=new Set();for(let j=0;j<G.length;j++)if((w>>BigInt(j))&1n){let g=G[j],mask=BigInt(g.mask),c=F[g.i];ids.push({clause:g.i,multiplier:vars.filter((v,i)=>(mask>>BigInt(i))&1n)});let terms=[mask];for(let l of c){let b=1n<<BigInt(index.get(Math.abs(l)));terms=l>0?terms.concat(terms.map(t=>t|b)):terms.map(t=>t|b)}for(let a of terms){check++;sum.has(a)?sum.delete(a):sum.add(a)}}
 assert(encode(sum)===r,"independent polynomial combination");let row={constant:Number(r&1n),vars:vars.filter((v,j)=>(r>>BigInt(j+1))&1n),parents:ids};identities.push(row);if(!row.vars.length&&row.constant)contradiction=true}
 return {rank,generated:G.length,monomials:mons.length,ops,check,peak,identities,contradiction}
}
function affinePins(A){let F=[];for(let a of A.identities){if(a.vars.length===0&&a.constant)F.push([]);else if(a.vars.length===1)F.push([a.constant?a.vars[0]:-a.vars[0]]);else if(a.vars.length===2){let [x,y]=a.vars;F.push(a.constant?[x,y]:[-x,y],a.constant?[-x,-y]:[x,-y])}}return H.unique(F)}
function fields(F,p){return F.map(c=>{let k=0,t=0;for(let l of c)if(p.get(Math.abs(l))===+(l>0)){k++;t+=l>0?1:-1}return {k,k3:k%3,t3:mod(t)}})}
function feedback(F,residue){
 let vars=V(F),p=new Map(vars.map(v=>[v,0])),flips=0,ties=0,work=0;let a=fields(F,p);work+=F.flat().length;
 const bad=A=>A.filter(x=>x.k===0).length,zero=A=>A.filter(x=>x.k>0&&x.t3===0).length;
 let history=[],init=bad(a);for(let j=0;j<=F.length;j++){let old=bad(a),best=old,choices=[];
 for(let v of vars){p.set(v,1-p.get(v));let b=fields(F,p);work+=F.flat().length;p.set(v,1-p.get(v));let d=bad(b);if(d<best){best=d;choices=[]}if(d===best&&d<old)choices.push({v,z:zero(b),b})}
 if(!choices.length)break;let first=choices[0],q=residue?choices.slice().sort((x,y)=>x.z-y.z||x.v-y.v)[0]:first;if(q.v!==first.v)ties++;p.set(q.v,1-p.get(q.v));a=q.b;flips++;history.push(q.v)}
 let final=bad(a);return {p:[...p],flips,ties,work,init,final,history,fields:a}
}
function tree(F){try{let t=H.solve(F,500000);return {status:"UNSAT",nodes:t.nodes,reads:t.scans,tree:t.tree}}catch(e){return {status:"UNKNOWN",error:String(e)}}}
function verifyTree(F,t){if(t.status!=="UNSAT")return 0;let reads=0,nodes=0;function rec(q,g){nodes++;let u=up(F,g);reads+=u.reads;if(u.bad){assert(q===0,"tree leaf");return}assert(Array.isArray(q)&&q.length===3&&!u.p.has(q[0])&&V(F).includes(q[0]),"tree split");rec(q[1],[...u.p,[q[0],0]]);rec(q[2],[...u.p,[q[0],1]])}rec(t.tree,[]);assert(nodes===t.nodes,"nodes");return reads}
function bij(F){let vs=V(F),adj=new Map(vs.flatMap(v=>[[v,[]],[-v,[]]]));for(let c of F)if(c.length===2){adj.get(-c[0]).push(c[1]);adj.get(-c[1]).push(c[0])}let scans=0;function reach(a,b){let q=[a],s=new Set(q);for(let i=0;i<q.length;i++)for(let v of adj.get(q[i])){scans++;if(v===b)return true;if(!s.has(v)){q.push(v);s.add(v)}}return false}let bad=vs.some(v=>reach(v,-v)&&reach(-v,v));return {bad,scans}}
function join(F,same,cap=100000){let count=0,attempts=0,conflict=null,units=[],pairs=[];let groups=new Map();for(let [i,c] of F.entries()){let k=scope(c);if(!groups.has(k))groups.set(k,{v:V([c]),ids:[]});groups.get(k).ids.push(i)}let G=[...groups.values()];outer:for(let i=0;i<G.length;i++)for(let j=i+(same?0:1);j<G.length;j++){let a=G[i],b=G[j];if(same&&i!==j)continue;if(!a.v.some(v=>b.v.includes(v)))continue;let U=[...new Set(a.v.concat(b.v))].sort((a,b)=>a-b);if(U.length>6)continue;attempts++;let ids=[...new Set(a.ids.concat(b.ids))],ok=[];for(let w=0;w<2**U.length;w++){if(++count>cap)break outer;if(ids.every(id=>F[id].some(l=>(w>>U.indexOf(Math.abs(l))&1)===+(l>0))))ok.push(w)}if(!ok.length){conflict={ids,U};break outer}for(let [k,v] of U.entries())if(ok.every(w=>(w>>k&1)===(ok[0]>>k&1))){let l=(ok[0]>>k&1)?v:-v;units.push({l,ids,U});} }
 let unique=[...new Map(units.map(x=>[x.l,x])).values()];for(let x of unique.concat(conflict?[conflict]:[])){for(let w=0;w<2**x.U.length;w++)if(x.ids.every(i=>F[i].some(l=>(w>>x.U.indexOf(Math.abs(l))&1)===+(l>0))))assert(x.l!==undefined&&(w>>x.U.indexOf(Math.abs(x.l))&1)===+(x.l>0),"join replay")}
 return {attempts,count,units:unique,conflict}}
function guards(F){let occ=new Map();for(let c of F)for(let l of c)occ.set(Math.abs(l),(occ.get(Math.abs(l))||0)+1);let v=[...occ].sort((a,b)=>b[1]-a[1]||a[0]-b[0]).slice(0,4).map(x=>x[0]);return [...v.map((x,i)=>v.slice(0,i).map(y=>[y,1]).concat([[x,0]])),v.map(x=>[x,1])]}
function cover(gs,n){let sum=0n,counts=[];for(let mask=1;mask<32;mask++){let p=new Map(),bad=false,k=0;for(let i=0;i<5;i++)if(mask>>i&1){k++;for(let [v,b] of gs[i]){if(p.has(v)&&p.get(v)!==b)bad=true;p.set(v,b)}}let a=bad?0n:1n<<BigInt(n-p.size);counts.push(a.toString());sum+=(k%2?1n:-1n)*a}assert(sum===1n<<BigInt(n),"cover");return counts}
function process(F,gs){
 let out=[],cert=[];
 for(let g of gs){let U=up(F,g);if(U.bad){out.push({g,early:"UNSAT",pins:U.p.size,reads:U.reads});cert.push({g,early:true});continue}
 let E=restrict(F,U.p),same=polynomial(E,true),cross=polynomial(E,false),J0=join(E,true),J=join(E,false),bi=bij(E);
 let importRows=H.unique(affinePins(cross).concat(J.units.map(x=>[x.l]),J.conflict?[[]]:[])),E1=H.unique(E.concat(importRows)),post=up(E1),A=[];
 // feedback controls on same E1, inside guard, with checked resolution learned rows
 for(let [name,width,fb] of [["baseline",0,-1],["flips",0,0],["deductions2",2,-1],["table2",2,0],["residue2",2,1],["deductions4",4,-1],["table4",4,0],["residue4",4,1]]){
  let f=fb<0?null:feedback(E1,!!fb),ord=f?f.fields.map(x=>x.k):null,L=width?res(E1,width,false,ord):{D:E1,steps:[],work:0,failed:0},r=replay(E1,L.steps);assert(eq(r.D,L.D),"resolution replay");let next=f&&width?feedback(L.D,!!fb):null,t=tree(L.D),vr=verifyTree(L.D,t);
  A.push({name,learned:L.steps.length,attempts:L.work,failed:L.failed,verify:r.checks,flips:(f?.flips||0)+(next?.flips||0),ties:(f?.ties||0)+(next?.ties||0),feedbackReads:(f?.work||0)+(next?.work||0),status:t.status,nodes:t.nodes,reads:t.reads,treeVerify:vr,peakStoredLiterals:L.D.flat().length});
  if(name==="baseline")cert.push({g,early:false,restricted:E,polynomial:cross.identities,joinUnits:J.units,joinConflict:J.conflict,importRows,tree:t});
 }
 out.push({g,early:"UNKNOWN",pins:U.p.size,reads:U.reads,rows:E.length,vars:V(E).length,same:{rank:same.rank,generated:same.generated,identities:same.identities.length,ops:same.ops},cross:{rank:cross.rank,generated:cross.generated,identities:cross.identities.length,ops:cross.ops,verify:cross.check,monomials:cross.monomials,peak:cross.peak,contradiction:cross.contradiction},sameJoin:{attempts:J0.attempts,words:J0.count,units:J0.units.length},crossJoin:{attempts:J.attempts,words:J.count,units:J.units.length,conflict:!!J.conflict},bij:bi,importRows:importRows.length,reclosure:{bad:post.bad,pins:post.p.size,reads:post.reads},arms:A})
 }return {out,cert}
}
let results=[],certs=[];
for(let id of ["JOINT-24","RANDOM-3CNF-40"]){let x=B.instances.find(z=>z.id===id),e=R.instances.find(z=>z.alias==="EB-"+id),G=C(x),raw=JSON.stringify(G.network)+"\n";assert(H.sha(raw)===e.sha256&&raw.length*8===e.N_bits&&H.sha(x.dimacs)===e.source_cnf.sha256&&x.dimacs.length*8===e.source_cnf.N_bits,"identity");let S=H.norm(G.network),m={n:0,cap:2e6},p=new Map(),cl=H.closure(S.factors,p,m),ge=H.affine(S),K=H.compact(S,2e6),D=H.reduce(K.F,2e6),F=D.F,gs=guards(F),cov=cover(gs,V(F).length),P=process(F,gs),Q=x.dimacs.trimEnd().split("\n").slice(1).map(l=>l.trim().split(/\s+/).map(Number).slice(0,-1)),cq=process(Q,guards(Q));let chart=JSON.stringify({gauge:S.gauge,F})+"\n",map=JSON.stringify({private:K.trace,dp:D.trace,normalizer:"08f5d87b1534442cf0b8225761ba1a954a455e6c"})+"\n";
let guardInfo=gs.map(g=>{let schema="T3-relative-carrier-v1",a=JSON.stringify({gaugePort:S.gauge-1,relativePortBits:g.map(([v,b])=>[v-1,b]).sort((a,b)=>a[0]-b[0])})+"\n",gid="GUARD-v1:sha256:"+H.sha(JSON.stringify(["PNP-GUARD-v1",e.instance_id,schema,H.sha(a)])+"\n");return {schema,a,gid,rid:"RESIDUAL-v1:sha256:"+H.sha(JSON.stringify(["PNP-RESIDUAL-v1",e.instance_id,gid,"T3-CNF-chart-v1",H.sha(chart),H.sha(map)])+"\n")}});
let cert={problem_id:"STRICT-EB4-v1",instance:e.short_id,instance_id:e.instance_id,original_N_bits:e.N_bits,source_pin:"registry 0c14cdc57925788cf7a451dcd5aa171dce860f2c; compiler 21b9d53fb8166c819b24e708656c742cd3c24f10; corpus e315349cd6c1fe3fa696504859f28312f6aab69a",guard_id:"EMPTY",residual_id:"ROOT",original_ids:{vertices:[0,G.network.types.length-1],ports:[0,4*G.network.types.length-1],edges:[0,G.network.edges.length-1]},parents:[],chart,map,guardInfo,cover:cov,proof:P.cert};let s=JSON.stringify(cert)+"\n";certs.push({id,s,sha:H.sha(s)});
results.push({id,instance:e.instance_id,N:e.N_bits,early:{roots:S.roots,factors:S.factors.length,forced:p.size,local:cl,checks:m.n,ge,private:K.trace.length,dp:D.trace.length,rows:F.length,vars:V(F).length},native:P.out,companion:cq.out,certificateSha:H.sha(s),certificateBytes:s.length})}
const fano=[[1,2,3],[1,4,5],[1,6,7],[2,4,6],[2,5,7],[3,4,7],[3,5,6]].flatMap(c=>[c,c.map(x=>-x)]);let fc=process(fano,guards(fano));return {results,certs,fano:fc.out}
}
if(typeof require==='function'){const fs=require('fs');const k=['compiler','corpus','registry','hybrid'];const s=Object.fromEntries(k.map((x,i)=>[x,fs.readFileSync(process.argv[i+2],'utf8')]));console.log(JSON.stringify(crossScope(s),null,2));}
