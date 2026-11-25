function run(raw,bs,bs20,rt){
let checks=0;function ck(q,msg){checks++;if(!q)throw Error(msg)}
const B=i=>1n<<BigInt(i),bit=(x,i)=>Number((x>>BigInt(i))&1n);
function ins(M,v){while(v){let p=v&-v;if(M.has(p))v^=M.get(p);else{M.set(p,v);return true}}return false}
function has(M,v){while(v){let p=v&-v;if(!M.has(p))return false;v^=M.get(p)}return true}
function parity(x){let s=0;while(x){x&=x-1n;s^=1}return s}
const eq=(i,b)=>[B(i),b], match=(p,x)=>p.every(([a,b])=>parity(a&x)===b);
function nae(C){return C.map(c=>[0,1].map(b=>c.map(l=>eq(Math.abs(l)-1,b^+(l<0)))))}
function reg(O){return O.map(o=>o.bad.map(b=>o.t.map((v,j)=>eq(v,(b>>j)&1))))}
function liftPackets(g){return g.packets.map(p=>[p.map(([mask,b])=>{let a=0n;for(let j=0;j<g.exterior.length-1;j++)if(mask&(1<<j))a^=B(g.exterior[j+1]-1)^B(g.exterior[0]-1);return [a,b]})])}
function normalize(p){let M=new Map();for(let [a,b] of p){while(a){let l=a&-a;if(!M.has(l)){M.set(l,[a,b]);break}let q=M.get(l);a^=q[0];b^=q[1]}if(!a&&b)return null}let keys=[...M.keys()].sort((a,b)=>a>b?-1:a<b?1:0);for(let l of keys){let q=M.get(l);for(let k of keys)if(k<l&&(M.get(k)[0]&l)){let t=M.get(k);M.set(k,[t[0]^q[0],t[1]^q[1]])}}return keys.reverse().map(k=>M.get(k))}
function closeUnits(F,guard){let g=new Map(guard),scans=0,changed=true;while(changed){changed=false;for(let f of F)for(let p of f){scans++;let q=[];for(let [a,b] of p){for(let [i,c] of g)if(a&B(i)){a^=B(i);b^=c}q.push([a,b])}q=normalize(q);if(q===null)continue;if(q.length===0)return {g,unsat:true,scans};if(q.length===1){let [a,b]=q[0];if((a&(a-1n))===0n){let i=a.toString(2).length-1;g.set(i,b^1);changed=true}}}}return {g,scans,unsat:false}}
// F is a list of zero equations, each an XOR of affine indicators. Unit closure only for
// registries of disjoint forbidden packets, not for arbitrary XOR functions.
function span(n,F,guard=[],mult=0,cap=8192,unit=true,verify=false){
 let cl=unit?closeUnits(F,guard):{g:new Map(guard),unsat:false,scans:0};
 if(cl.unsat)return {status:"UNSAT-unit",scans:cl.scans};
 let pins=[...cl.g].map(([i,b])=>eq(i,b)), free=Array.from({length:n},(_,i)=>i).filter(i=>!cl.g.has(i));
 let funcs=F.map(f=>f.slice());
 if(mult)for(let f of F)for(let i of free)funcs.push(f.map(p=>[...p,eq(i,1)]));
 const m=funcs.length, constIdx=m; funcs.push([[]]);for(let i of free)funcs.push([[eq(i,1)]]);
 let P=[],D=new Map();let maps=funcs.map(f=>{let ids=new Set();for(let p of f){let q=normalize([...p,...pins]);if(q===null)continue;let k=q.map(([a,b])=>a.toString(16)+":"+b).join(",");if(!D.has(k)){D.set(k,P.length);P.push(q)}let j=D.get(k);if(ids.has(j))ids.delete(j);else ids.add(j)}return [...ids]});
 let col=P.map(p=>Array.from({length:n},(_,i)=>p.reduce((s,[a],j)=>s|(bit(a,i)?B(j):0n),0n)));
 let rhs=P.map(p=>p.reduce((s,[,b],j)=>s|(b?B(j):0n),0n));
 let suf=col.map(C=>{let S=Array(n+1);S[n]=new Map();for(let i=n-1;i>=0;i--){S[i]=new Map(S[i+1]);ins(S[i],C[i])}return S});
 let basis=[{s:rhs.map((a,j)=>has(suf[j][0],a)?a:null),w:0n}],peak=1,peakStates=0,trans=0,visits=0;
 for(let i=0;i<n;i++){
  let next=[],M=new Map(),index=new Map();
  for(let q of basis)for(let b of cl.g.has(i)?[cl.g.get(i)]:[0,1]){
   trans++;let s=q.s.map((a,j)=>{visits++;if(a===null)return null;let z=a^(b?col[j][i]:0n);return has(suf[j][i+1],z)?z:null});
   let v=0n;for(let j=0;j<s.length;j++)if(s[j]!==null){let k=j+":"+s[j];if(!index.has(k))index.set(k,index.size);v|=B(index.get(k))}
   if(index.size>cap)return {status:"OPEN-cap",i,peak,peakStates:index.size,trans,visits,scans:cl.scans};
   if(ins(M,v))next.push({s,w:q.w|(b?B(i):0n)});
  }basis=next;peak=Math.max(peak,basis.length);peakStates=Math.max(peakStates,index.size)
 }
 let V=new Map(),full=new Map();
 function evaluate(w){return funcs.reduce((a,f,i)=>a|(f.reduce((t,p)=>t^+match(p,w),0)?B(i):0n),0n)}
 for(let q of basis){let v=maps.reduce((a,f,i)=>a|(f.reduce((t,j)=>t^+(q.s[j]!==null),0)?B(i):0n),0n);ck(v===evaluate(q.w),"streamed values");ins(V,v);ins(full,v)}
 const pivot=V.get(B(constIdx)),dirs=[...V.entries()].filter(([p])=>p>B(constIdx)).map(([,v])=>v>>BigInt(m+1));
 let dim=dirs.length,status=pivot===undefined?"UNSAT-span":"OPEN",affineCuts=pivot===undefined?null:free.length-dim;
 let witness=basis.find(q=> (evaluate(q.w)&(B(m)-1n))===0n);
 if(witness)status="SAT-witness";
 if(verify){for(let w=0n;w<B(n);w++){if([...cl.g].some(([i,b])=>bit(w,i)!==b))continue;let v=evaluate(w);ck(has(full,v),"full exact evaluation span");if((v&(B(m)-1n))===0n)ck(pivot!==undefined,"no false rejection")}}
 return {status,packets:P.length,equations:m,rank:V.size,affineCuts,dimension:dim,peak,peakStates,trans,visits,scans:cl.scans,witness:witness?.w.toString()??null};
}
ck(JSON.stringify(raw.O)===JSON.stringify(bs.source.O),"same raw registry");
const K=bs.common.find(x=>x.K===16).residual;const base=reg(raw.O),wide=nae(K.C);
function lift(word){let A={};for(let i of [...new Set(K.C.flat().map(Math.abs))])A[i]=bit(BigInt(word),i-1);for(let {v:x,bucket} of K.log.slice().reverse()){let needs=new Set();for(let c of bucket){let z=c.map(l=>A[Math.abs(l)]^+(l<0));if(z.every(b=>b===z[0]))needs.add(z[0]^1)}ck(needs.size<=1,"reverse lift");A[x]=needs.size?[...needs][0]:0}let w=Object.entries(A).reduce((s,[i,b])=>s|(b?B(+i-1):0n),0n);ck(base.every(f=>!f.some(p=>match(p,w))),"raw witness");return w.toString()}
const out={};
for(let [name,F,g] of [["raw",base,bs20.raw.gauge],["wide",wide,bs20.wide.gauge]]){
 let L=liftPackets(g);let standalone=span(24,F),combined=span(24,[...F,...L]);out[name]={standalone,combined,learned:L.length};
 for(let s of [standalone,combined])if(s.witness!==null){ck(F.every(f=>!f.some(p=>match(p,BigInt(s.witness)))),"actual witness");if(name==="wide")s.sourceLift=lift(s.witness)}
}
const fano=[[1,2,3],[1,4,5],[1,6,7],[2,4,6],[2,5,7],[3,4,7],[3,5,6]];
out.fano=[];for(let i=-1;i<21;i++){let C=fano.map(c=>c.slice());if(i>=0)C[i/3|0][i%3]*=-1;let F=nae(C),a=span(7,F,[],0,8192,true,true),b=span(7,F,[],1,8192,true,true);let models=0;for(let w=0n;w<128n;w++)if(F.every(f=>!f.some(p=>match(p,w))))models++;ck(models===(i<0?0:10),"Fano models");out.fano.push({i,models,a,b})}
out.rt=[];for(let c of rt.controls){let F=reg(c.registry);let a=span(c.n,F),b=span(c.n,F,[],1);let models=0;for(let w=0n;w<B(c.n);w++)if(F.every(f=>!f.some(p=>match(p,w))))models++;ck(models===0,"RT root");let o=c.registry[0],G=F.slice();G[0]=o.bad.map(b=>o.t.map((v,j)=>eq(v,((b^1)>>j)&1)));let z=span(c.n,G,[],1);let count=0;for(let w=0n;w<B(c.n);w++)if(G.every(f=>!f.some(p=>match(p,w))))count++;ck(count>0,"RT sign neighbor");ck(!z.status.startsWith("UNSAT"),"RT no false rejection");out.rt.push({n:c.n,a,b,neighbor:z,models:count})}
out.chains=[];for(let d of [2,3,8,16,32,64]){let k=3,n=d*k,Q=Array.from({length:k},(_,i)=>Array.from({length:d},(_,j)=>eq(i*d+j,1)));let a=span(n,[Q,[...Q,[]]],[],0,8192,false,d===2),b=span(n,[Q,Q],[],0,8192,false,d===2);ck(a.status==="UNSAT-span"&&b.status==="SAT-witness","opposite/same parity chains");out.chains.push({d,n,a,b})}
// Counterexample: two independent syndrome equations with target outside image but inside affine hull.
let h=[[eq(0,1),eq(1,1)]], j=[[eq(0,0),eq(1,0)]];
out.hole=span(2,[[...h,[]],[...j,[]]],[],0,8192,false,true);ck(out.hole.status==="OPEN","joint nonlinear missing word");
return {checks,...out}
}
if(typeof require!=='undefined'&&require.main===module){const fs=require('fs');console.log(JSON.stringify(run(...process.argv.slice(2).map(p=>JSON.parse(fs.readFileSync(p)))),null,2));}
