// node shared.js; only Node built-ins. Exact signed monomial quotient; no reference SAT labels used by checker.
function run(sha){
const A=(x,m)=>{if(!x)throw Error(m)},enc=x=>JSON.stringify(x)+"\n",key=c=>[...c].sort((a,b)=>a-b).join(","),dimacs=(n,F)=>"p cnf "+n+" "+F.length+"\n"+F.map(c=>c.join(" ")+" 0").join("\n")+"\n";
function gen(m,k,yes){let B=Array.from({length:m},(_,i)=>Array.from({length:k},(_,j)=>i*k+j+1));for(let i=0;i<m;i++){let s=m*k+i+1,j=(i+2)%m;B[i].push(s);B[j].push(yes&&i%2===1?s:-s)}let E=Array.from({length:m},(_,i)=>[i,(i+1)%m]),F=[];for(let [i,j] of E){for(let a of B[i])for(let b of B[j])F.push([a,b]);F.push([...B[i],...B[j]].map(x=>-x))}return {m,k,n:m*(k+1),F,B,E}}
function blind(F){let H=new Map(),long=[];for(let c of F)if(c.length>2){let id=long.length;long.push(c);for(let l of c){let s=-l;if(!H.has(s))H.set(s,[]);H.get(s).push(id)}}let G=new Map();for(let [l,ids] of H){if(ids.length!==2)return null;let k=ids.join(",");if(!G.has(k))G.set(k,[]);G.get(k).push(l)}let B=[...G.values()],E=[];for(let i=0;i<long.length;i++){let ix=[...G.keys()].map((k,j)=>k.split(",").map(Number).includes(i)?j:-1).filter(x=>x>=0);if(ix.length!==2)return null;E.push(ix)}return {B,E}}
function audit(n,F,B,E){let stock=new Map(),vis=0,counts=new Map(),owners=new Map();for(let c of F){let z=key(c);stock.set(z,(stock.get(z)||0)+1);vis+=c.length;A(c.every(l=>Number.isInteger(l)&&l!==0&&Math.abs(l)<=n),"source ids")}
for(let [i,b] of B.entries()){let s=new Set(b.map(Math.abs));A(s.size===b.length&&b.length>=1,"monomial");for(let l of b){let v=Math.abs(l);counts.set(v,(counts.get(v)||0)+1);if(!owners.has(v))owners.set(v,[]);owners.get(v).push([i,l])}}
const privateBits=B.map(b=>b.filter(l=>counts.get(Math.abs(l))===1));A(privateBits.every(b=>b.length>0),"no private slack");
function take(c){vis+=c.length;let z=key(c),t=stock.get(z)||0;A(t>0,"missing source clause");stock.set(z,t-1)}
for(let [i,j] of E){A(i!==j&&B[i]&&B[j],"edge");for(let a of B[i])for(let b of B[j])take([a,b]);take([...B[i],...B[j]].map(x=>-x))}
A([...stock.values()].every(x=>x===0),"uncovered source rows");let Q=[],C=[],seen=new Set(),pairs=0;
for(let [i,j] of E)Q.push([i+1,j+1],[-i-1,-j-1]);for(let [v,O] of owners){for(let a=0;a<O.length;a++)for(let b=a+1;b<O.length;b++){pairs++;let [i,l]=O[a],[j,r]=O[b];if(l!==-r)continue;let c=[-i-1,-j-1],z=key(c);if(!seen.has(z)){seen.add(z);C.push({c,v,owners:[i,j]});Q.push(c)}}}
return {Q,C,privateBits,vis,pairs}}
function checkWord(F,w){let vis=0;for(let c of F){let sat=false;for(let l of c){vis++;if(w[Math.abs(l)-1]===+(l>0))sat=true}if(!sat)return {sat:false,vis}}return {sat:true,vis}}
function lift(n,B,priv,w){let x=Array(n).fill(-1);for(let i=0;i<B.length;i++)if(w[i])for(let l of B[i]){let v=Math.abs(l)-1,b=+(l>0);if(x[v]!==-1&&x[v]!==b)return null;x[v]=b}
for(let i=0;i<B.length;i++)if(!w[i]){let l=priv[i][0],v=Math.abs(l)-1;A(x[v]===-1,"private");x[v]=+(l<0)}return x.map(b=>Math.max(0,b))}
function phase(B,x){return B.map(b=>+b.every(l=>x[Math.abs(l)-1]===+(l>0)))}
function paths(Q,m){let adj=new Map(),vis=0;function add(a,b,row){if(!adj.has(a))adj.set(a,[]);adj.get(a).push([b,row])}for(let [i,c] of Q.entries()){A(c.length===2,"binary");add(-c[0],c[1],i);add(-c[1],c[0],i)}
function walk(s,t){let queue=[s],P=new Map([[s,null]]);for(let k=0;k<queue.length;k++){let u=queue[k];if(u===t){let p=[];while(P.get(u)!==null){let [v,row]=P.get(u);p.push([v,u,row]);u=v}return p.reverse()}for(let [v,r] of adj.get(u)||[]){vis++;if(!P.has(v)){P.set(v,[u,r]);queue.push(v)}}}return null}
for(let v=1;v<=m;v++){let a=walk(v,-v),b=walk(-v,v);if(a&&b)return {conflict:true,paths:[a,b],v,vis}}return {conflict:false,vis}}
function replay(Q,p){A(p.conflict,"expected contradiction");let count=0;for(let [i,P] of p.paths.entries()){let s=i?-p.v:p.v,t=-s;for(let [u,v,r] of P){A(u===s,"path gap");let c=Q[r];A(c&&((c[0]===-u&&c[1]===v)||(c[1]===-u&&c[0]===v)),"invalid implication");s=v;count+=2}A(s===t,"wrong path end")}return count}
function orientation(m,b){return Array.from({length:m},(_,i)=>(i%2)^b)}
let instances=[];for(let [m,k] of [[6,1],[10,2],[18,3],[34,4],[66,5]])for(let yes of [false,true]){
let g=gen(m,k,yes),d=dimacs(g.n,g.F),b=blind(g.F),map=b||{B:g.B,E:g.E};let R=audit(g.n,g.F,map.B,map.E),p=paths(R.Q,m),witness=null,checks=0;A(p.conflict===!yes,"label");
if(p.conflict)checks=replay(R.Q,p);else {for(let bit=0;bit<2;bit++){let w=orientation(m,bit); // mapped YES ordering is original ring
if(!checkWord(R.Q,w).sat)continue;let x=lift(g.n,map.B,R.privateBits,w);A(x&&phase(map.B,x).join()===w.join(),"lift");let v=checkWord(g.F,x);A(v.sat,"source witness");checks+=v.vis;witness=x;break}A(witness!==null,"missing lift")}
let relaxed=paths(R.Q.slice(0,2*m),m);A(!relaxed.conflict,"phase only should be consistent");
let ablation=[];if(!yes){ // remove overlap constraints involving either parity class (in original block indexing via source map)
let src=audit(g.n,g.F,g.B,g.E);for(let side=0;side<2;side++){let Q=[...src.Q.slice(0,2*m),...src.C.filter(z=>z.owners[0]%2!==side).map(z=>z.c)];let w=orientation(m,side===0?1:0);A(checkWord(Q,w).sat,"parent removal control");ablation.push({side,rows:Q.length,phaseWitness:w})}}
let exhaustive=null;if(m===6&&k===1){let support=new Set(),originalSat=0,vis=0;for(let bits=0;bits<2**g.n;bits++){let x=Array.from({length:g.n},(_,i)=>bits>>i&1),w=phase(map.B,x);support.add(w.join());let z=checkWord(g.F,x);vis+=z.vis;originalSat+=+z.sat}let predicted=0;for(let bits=0;bits<2**m;bits++){let w=Array.from({length:m},(_,i)=>bits>>i&1),allowed=R.C.every(z=>checkWord([z.c],w).sat);A(allowed===support.has(w.join()),"fiber equivalence");if(checkWord(R.Q,w).sat)predicted++}A((originalSat>0)===(predicted>0),"source exhaustive");exhaustive={originalWords:2**g.n,phaseWords:2**m,support:support.size,originalSat,predicted,vis}}
let name="SIGNED-SLACK-SEAM-"+m+"-"+k+"-"+(yes?"YES":"NO"),cert={model:"DIMACS-CNF-v1",guard_id:"EMPTY",residual_id:"ROOT",source_sha256:sha(d),original_N_bits:d.length*8,original_ids:{variables:[1,g.n],clauses:[1,g.F.length]},source_parameters:{m,k,yes},map,quotient:R.Q,conflictOrigins:R.C,privateBits:R.privateBits,pathProof:p.conflict?p:null,witness};
instances.push({instance:name+"@"+sha(d).slice(0,12),instance_id:"DIMACS-CNF-v1:sha256:"+sha(d),N:d.length*8,n:g.n,clauses:g.F.length,privateCount:m*k,sharedCount:m,phaseCount:m,overlapClauses:R.C.length,blind:!!b,status:p.conflict?"UNSAT":"SAT",work:{sourceAuditLiteralVisits:R.vis,overlapPairChecks:R.pairs,implicationArcVisits:p.vis,replayLiteralVisits:checks},phaseOnly:"SAT",ablation,exhaustive,certificate_id:"CERT-v1:sha256:"+sha(enc(cert)),certificate:cert});
}
return {schema:"SIGNED-PRIVATE-SLACK-SEAMS-v1",instances}}
if(typeof require!=="undefined"&&require.main===module){let sha=s=>require("node:crypto").createHash("sha256").update(s,"utf8").digest("hex");console.log(JSON.stringify(run(sha)));}
