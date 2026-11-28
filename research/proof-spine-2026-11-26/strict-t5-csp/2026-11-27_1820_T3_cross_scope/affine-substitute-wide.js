function substitute(s){
 const C=Function(s.compiler.slice(s.compiler.indexOf("function compile("),s.compiler.indexOf("function auditLocal("))+";return compile")(),H=Function(s.hybrid.split('if(typeof require==="function"')[0]+";return {sha,norm,compact,reduce}")(),R=JSON.parse(s.registry),B=JSON.parse(s.corpus);
 const f=Function(s.run.slice(0,s.run.indexOf("\nlet results=[],certs=[];"))+";return {up,restrict,V};}return crossScope")()(s);
 const assert=(b,m)=>{if(!b)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b),D=3;
 function lane(F){
 let V=f.V(F),vindex=new Map(V.map((v,i)=>[v,i])),bits=V.map((_,i)=>1n<<BigInt(i)),active=bits.slice(),rows=[],steps=[],ops=0,checks=0,cap=2000000,peak=0;
 const tog=(s,x)=>s.has(x)?s.delete(x):s.add(x),deg=x=>{let c=0;while(x){c++;x&=x-1n}return c},key=a=>[...a].sort((a,b)=>a<b?-1:a>b?1:0).map(String).join(","),sym=(a,b)=>{let r=new Set(a);for(let x of b)tog(r,x);return r};
 function mul(a,b){let S=new Set();for(let x of a)for(let y of b){if(++ops>cap)throw Error("cap");tog(S,x|y)}return S}
 function unique(R){let m=new Map();for(let r of R)if(r.size)m.set(key(r),r);return [...m.values()]}
 for(let c of F){if(c.length>4) return {status:"UNKNOWN",reason:"width>4",initial:V.length,remaining:V.length};let p=new Set([0n]);for(let l of c){let x=bits[vindex.get(Math.abs(l))];p=mul(p,new Set(l>0?[0n,x]:[x]))}rows.push(p)}
 const enc=r=>[...r].sort((a,b)=>a<b?-1:a>b?1:0).map(String);
 let status="UNKNOWN",reason="affine plateau",initialRows=rows.length;
 try{for(let round=0;round<=V.length;round++){
  if(rows.some(r=>r.size===1&&r.has(0n))){status="UNSAT";reason="explicit constant";break}
  let mons=[0n],M=new Map([[0n,0]]);function comb(i,l,a,cb){if(!l){cb(a);return}for(let j=i;j<=active.length-l;j++)comb(j+1,l-1,a|active[j],cb)}
  for(let d=1;d<=D;d++)comb(0,d,0n,x=>{M.set(x,mons.length);mons.push(x)});
  let G=[],basis=new Map();
  function encode(r){let b=0n;for(let x of r){let i=M.get(x);assert(i!==undefined,"monomial");b^=1n<<BigInt(i)}return b}
  for(let [i,r] of rows.entries()){let d=Math.max(...[...r].map(deg));for(let t=0;t<=D-d;t++)comb(0,t,0n,a=>{let p=mul(r,new Set([a])),b=encode(p);if(!b)return;let j=G.length;G.push({i,a});let w=1n<<BigInt(j);while(b){if(++ops>cap)throw Error("cap");let k=b.toString(2).length-1;if(!basis.has(k)){basis.set(k,[b,w]);break}let [c,v]=basis.get(k);b^=c;w^=v}})}
  peak=Math.max(peak,basis.size);let candidates=[];
  for(let [k,[b,w]] of basis)if(k<=active.length)candidates.push({k,b,w,weight:deg(b)});
  if(!candidates.length)break;
  candidates.sort((a,b)=>a.k===0?-1:b.k===0?1:a.weight-b.weight||a.k-b.k);let q=candidates[0],row=new Set(mons.filter((_,i)=>(q.b>>BigInt(i))&1n)),parents=[],replay=new Set();
  for(let j=0;j<G.length;j++)if((q.w>>BigInt(j))&1n){let {i,a}=G[j];parents.push([i,String(a)]);for(let x of rows[i]){checks++;tog(replay,x|a)}}
  assert(key(replay)===key(row),"combination replay");if(q.k===0){assert(row.has(0n)&&row.size===1,"constant");steps.push({row:enc(row),parents,contradiction:true});status="UNSAT";reason="constant in span";break}
  let pivot=mons[q.k],rhs=new Set(row);rhs.delete(pivot);assert(deg(pivot)===1&&[...rhs].every(x=>deg(x)<=1),"affine");
  let out=[];for(let r of rows){let t=new Set();for(let a of r){if(!(a&pivot)){tog(t,a);continue}for(let b of rhs){if(++ops>cap)throw Error("cap");tog(t,(a^pivot)|b)}}assert([...t].every(a=>!(a&pivot)&&deg(a)<=4),"substitute");out.push(t)}
  // Independent replay of substitution as R(x)+x*Q -> R+rhs*Q by separate decomposition.
  for(let i=0;i<rows.length;i++){let low=new Set(),high=new Set();for(let x of rows[i]){checks++;if(x&pivot)high.add(x^pivot);else low.add(x)}let alt=new Set(low);for(let x of high)for(let y of rhs){checks++;tog(alt,x|y)}assert(key(alt)===key(out[i]),"substitution replay")}
  steps.push({row:enc(row),parents,pivot:V[bits.indexOf(pivot)],rhs:enc(rhs),before:rows.length,after:unique(out).length});rows=unique(out);active=active.filter(x=>x!==pivot)
 }}catch(e){if(!String(e).includes("cap"))throw e;reason="cap"}
 return {status,reason,initial:V.length,remaining:active.length,initialRows,remainingRows:rows.length,steps,ops,checks,peak,vars:V}
 }
 let out=[];for(let [k,id] of [["joint","JOINT-24"],["random","RANDOM-3CNF-40"]]){let p=JSON.parse(s[k]),e=R.instances.find(x=>x.alias==="EB-"+id),x=B.instances.find(x=>x.id===id),G=C(x),raw=JSON.stringify(G.network)+"\n";assert(H.sha(raw)===e.sha256&&raw.length*8===e.N_bits&&H.sha(x.dimacs)===e.source_cnf.sha256,"identity");let S=H.norm(G.network),K=H.compact(S,2e6),F=H.reduce(K.F,2e6).F;assert(p.chart===JSON.stringify({gauge:S.gauge,F})+"\n","chart");let results=[];for(let t of p.proof){let u=f.up(F,t.g);if(u.bad){results.push({g:t.g,status:"UNSAT",reason:"UP"});continue}let E=f.restrict(F,u.p);results.push({g:t.g,...lane(E)})}out.push({id,instance:e.instance_id,N:e.N_bits,results})}
 return out
}
if(typeof require==='function'){let fs=require('fs'),k=['compiler','corpus','registry','hybrid','joint','random','run'];let s=Object.fromEntries(k.map((x,i)=>[x,fs.readFileSync(process.argv[i+2],'utf8')]));console.log(JSON.stringify(substitute(s),null,2));}
