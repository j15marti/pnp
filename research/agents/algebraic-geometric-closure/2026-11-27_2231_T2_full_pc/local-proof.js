function checkAndDiscover(peer,sha,compile){
const enc=x=>JSON.stringify(x)+"\n",parse=s=>s.trimEnd().split("\n").slice(1).map(x=>x.trim().split(/\s+/).map(Number).slice(0,-1));
const x=peer.proof,F=parse(x.dimacs);if(sha(x.dimacs)!==peer.instance_id.split(":").at(-1)||x.dimacs.length*8!==peer.original_N_bits)throw Error("source");
let P=new Map(),pairChecks=0;function key(c){return c.slice().sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b).join(",")}
for(let i=0;i<F.length;i++){let k=key(F[i]);if(P.has(k))throw Error("duplicate");P.set(k,i)}
let triples=[],deg=new Map(),pair=new Set();
for(let i=0;i<F.length;i++){let c=F[i],j=P.get(key(c.map(l=>-l)));if(j===undefined)throw Error("pair");if(j<i)continue;let v=c.map(Math.abs).sort((a,b)=>a-b);for(let a of v)deg.set(a,(deg.get(a)||0)+1);for(let a=0;a<3;a++)for(let b=a+1;b<3;b++){let k=v[a]+","+v[b];if(pair.has(k))throw Error("shared pair");pair.add(k);pairChecks++}triples.push({v,ids:[i,j]})}
let internal=[...deg].filter(([v,d])=>d<4).map(([v])=>v),I=new Set(internal),adj=new Map(internal.map(v=>[v,new Set()]));
for(let t of triples)for(let a of t.v.filter(v=>I.has(v)))for(let b of t.v.filter(v=>I.has(v)))adj.get(a).add(b);
let seen=new Set(),groups=[];
for(let v of internal){if(seen.has(v))continue;let q=[v];seen.add(v);for(let i=0;i<q.length;i++)for(let b of adj.get(q[i]))if(!seen.has(b)){seen.add(b);q.push(b)}let S=new Set(q),T=triples.filter(t=>t.v.some(v=>S.has(v))),vs=[...new Set(T.flatMap(t=>t.v))].sort((a,b)=>a-b),shared=vs.filter(v=>!I.has(v)),ids=T.flatMap(t=>t.ids).sort((a,b)=>a-b);if(T.length!==6||vs.length!==7||shared.length!==2)throw Error("group");groups.push({ids,vs,shared})}
if(groups.flatMap(g=>g.ids).sort((a,b)=>a-b).join()!==F.map((_,i)=>i).join())throw Error("partition");
const pop=m=>{let k=0;while(m){m&=m-1;k++}return k};
function local(g){
let {vs,shared,ids}=g,rows=ids.map(i=>F[i]),good=[],parity=new Set(),checks=0;
for(let w=0;w<128;w++){const val=v=>(w>>vs.indexOf(v))&1;let ok=true;for(let c of rows){checks++;if(!c.some(l=>val(Math.abs(l))===Number(l>0))){ok=false;break}}if(ok){good.push(w);parity.add(val(shared[0])^val(shared[1]))}}
if(parity.size!==1)throw Error("boundary parity");let b=[...parity][0],target=[...shared.map(v=>1<<vs.indexOf(v)),...(b?[0]:[])];
const ms=Array.from({length:128},(_,i)=>i).filter(i=>pop(i)<=3),idx=new Map(ms.map((m,i)=>[m,i])),one=m=>1n<<BigInt(idx.get(m));
let lines=[],B=new Map(),events=0;function record(r,op){let i=lines.length;lines.push({r,op});return i}function add(i){let r=lines[i].r;while(r){events++;let k=r&-r;if(!B.has(k)){B.set(k,i);return true}let j=B.get(k);r^=lines[j].r;i=record(r,["xor",i,j])}return false}
function clause(c){let P=new Set([0]);for(let l of c){let Q=new Set(),v=1<<vs.indexOf(Math.abs(l));function tog(m){if(Q.has(m))Q.delete(m);else Q.add(m)}for(let m of P){tog(m|v);if(l>0)tog(m)}P=Q}let r=0n;for(let m of P)r^=one(m);return r}
for(let i of ids)add(record(clause(F[i]),["axiom",i+1]));
let goal=target.reduce((r,m)=>r^one(m),0n);
function proveGoal(){let r=goal,ls=[];while(r){let k=r&-r;if(!B.has(k))return -1;let j=B.get(k);ls.push(j);r^=lines[j].r}let i=ls[0];for(let j of ls.slice(1))i=record(lines[i].r^lines[j].r,["xor",i,j]);return i}
let end=proveGoal(),sweeps=0;
while(end<0){let old=B.size;sweeps++;for(let v=0;v<7;v++){let high=0n,mp=new Map(),H=new Map();for(let m of ms){let q=m|(1<<v);if(pop(q)>3)high|=one(m);else mp.set(one(m),one(q))}
for(let j of [...B.values()]){let r=lines[j].r,h=r&high;while(h){let k=h&-h;events++;if(!H.has(k)){H.set(k,j);break}let z=H.get(k);r^=lines[z].r;j=record(r,["xor",j,z]);h=r&high}if(!h&&r){let y=0n;while(r){let k=r&-r;r^=k;y^=mp.get(k);events++}add(record(y,["mul",j,vs[v]]))}}
end=proveGoal();if(end>=0)break}if(end<0&&old===B.size)throw Error("degree3 stall")}
let keep=new Set();function visit(i){if(keep.has(i))return;keep.add(i);let o=lines[i].op;if(o[0]==="xor"){visit(o[1]);visit(o[2])}if(o[0]==="mul")visit(o[1])}visit(end);let order=[...keep].sort((a,b)=>a-b),ren=new Map(order.map((x,i)=>[x,i])),proof=order.map(i=>{let o=lines[i].op.slice();if(o[0]==="xor"){o[1]=ren.get(o[1]);o[2]=ren.get(o[2])}if(o[0]==="mul")o[1]=ren.get(o[1]);return o});
// Independent set-of-monomials verifier; degree tested at every proof line.
let vals=[],replay=0;function tog(S,m){replay++;if(S.has(m))S.delete(m);else S.add(m)}
for(let o of proof){let R=new Set();if(o[0]==="axiom"){if(!ids.includes(o[1]-1))throw Error("bad axiom");R.add(0);for(let l of F[o[1]-1]){let Q=new Set();for(let m of R){tog(Q,m|(1<<vs.indexOf(Math.abs(l))));if(l>0)tog(Q,m)}R=Q}}else if(o[0]==="xor"){for(let m of vals[o[1]])tog(R,m);for(let m of vals[o[2]])tog(R,m)}else if(o[0]==="mul"){for(let m of vals[o[1]])tog(R,m|(1<<vs.indexOf(o[2])))}else throw Error("op");if([...R].some(m=>pop(m)>3))throw Error("degree");vals.push(R)}
if([...vals.at(-1)].sort((a,b)=>a-b).join()!==target.sort((a,b)=>a-b).join())throw Error("target replay");
return {ids:ids.map(i=>i+1),vs,shared,b,good,checks,rank:B.size,sweeps,generated:lines.length,events,proof,replay}
}
let localCerts=groups.map(local),boundary=new Map(),twist=0;for(let c of localCerts){twist^=c.b;for(let v of c.shared)boundary.set(v,(boundary.get(v)||0)^1)}if(twist!==1||[...boundary.values()].some(x=>x))throw Error("global XOR");
let ring={problem_id:peer.problem_id,instance:peer.instance,instance_id:peer.instance_id,original_N_bits:peer.original_N_bits,source_pin:peer.source_pin,guard_id:"EMPTY",residual_id:"ROOT",original_ids:peer.original_ids,parents:["CERT-v1:sha256:951e49b1862186fa31f7ff336a752949c6f9a04521b56ff28529d421a7efa9b9"],pairChecks,groups:localCerts,twist,claim:"Full square-free Boolean PC degree3 derives each boundary parity, whose XOR is 1; degree2 grouped span is globally closed under admissible multiplication and has no affine identity."};
let hostile=[];
for(let n of [8,16,32,64]){let E=[],T=new Set(),pairs=0;for(let a=0;a<n;a++)for(let b=a+1;b<n;b++)for(let c=b+1;c<n;c++){let e=a^b^c;if(e>c)E.push([a,b,c,e])}
for(let e of E)for(let j=0;j<4;j++){let t=e.filter((_,i)=>i!==j).join(",");if(T.has(t))throw Error("shared triple");T.add(t);pairs++}
if(T.size!==n*(n-1)*(n-2)/6)throw Error("triple cover");let C=E.flatMap(e=>[e.map(v=>v+1),e.map(v=>-v-1)]),dimacs="p cnf "+n+" "+C.length+"\n"+C.map(c=>c.join(" ")+" 0\n").join(""),hash=sha(dimacs),N=8*dimacs.length,majority=n/2,pigeon=majority*(majority-1)/2>n-1;
let yes=null,count=null,checks=0;if(n<=16){count=0;for(let w=0;w<2**n;w++){let ok=true;for(let e of E){checks++;let b=e.map(v=>(w>>v)&1);if(b.every(x=>x===b[0])){ok=false;break}}if(ok){count++;if(yes===null)yes=w}}if(pigeon&&count!==0)throw Error("count")}
let native=null;if(n===16){let G=compile({id:"AG4-"+n,nvars:n,dimacs});let s=enc(G.network);native={instance_id:"STRICT-EB4-v1:sha256:"+sha(s),N_bits:s.length*8,vertices:G.network.types.length,edges:G.network.edges.length,map_sha256:sha(enc(G.source_map))}}
hostile.push({problem_id:"DIMACS-CNF-v1",instance:"AG4-"+n+"@"+hash.slice(0,12),instance_id:"DIMACS-CNF-v1:sha256:"+hash,original_N_bits:N,guard_id:"EMPTY",residual_id:"ROOT",original_ids:{variables:[1,n],clauses:[1,C.length]},parents:[],n,blocks:E.length,tripleChecks:pairs,pigeon,majorityPairs:majority*(majority-1)/2,availableSums:n-1,exhaustiveCount:count,exhaustiveChecks:checks,yesWord:yes,native,dimacs:n<=16?dimacs:null});
}
return {ring,hostile}
}
module.exports={checkAndDiscover};
