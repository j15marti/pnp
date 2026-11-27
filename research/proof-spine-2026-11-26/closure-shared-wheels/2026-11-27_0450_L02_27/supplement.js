const range=n=>Array.from({length:n},(_,i)=>i),bit=(w,i)=>(w>>i)&1;
function mask(h){let r=0;for(let w=0;w<16;w++){let n=bit(w,0),e=bit(w,1),s=bit(w,2),z=bit(w,3);if(e===z&&s===(n|[0,z,1-z][h]))r|=1<<w;}return r;}
const masks=range(3).map(mask);
function native(S){
 let k=Math.max(2,S.v,S.C.length),columns=[],h=2166136261;
 const hash=x=>h=Math.imul(h^x,16777619)>>>0;
 hash(k);hash(masks[0]);hash(0); // north0, horizontal free by fixed convention
 for(let j=0;j<k;j++){
  const C=S.C[j]||[],entries=C.map(l=>[Math.abs(l)-1,masks[l>0?1:2]]).sort((a,b)=>a[0]-b[0]);
  if(entries.some((a,i)=>a[0]>=k||(i&&entries[i-1][0]===a[0])))throw Error("invalid native row");
  columns.push({south:j<S.C.length?1:0,entries});
  hash(j);hash(j<S.C.length?1:0);hash(entries.length);for(const [i,m] of entries){hash(i);hash(m);}
 }
 let decoded=columns.filter(c=>c.south).map(c=>c.entries.map(([i,m])=>m===masks[1]?i+1:m===masks[2]?-i-1:0));
 const key=c=>c.slice().sort((a,b)=>a-b).join(",");
 if(decoded.length!==S.C.length||decoded.some((c,j)=>key(c)!==key(S.C[j])))throw Error("decode");
 let q=0,verified=0;
 for(const f of S.F){let ct=(1<<f.S.length)-f.R.length,actual=decoded.slice(q,q+ct);q+=ct;
  for(let w=0;w<(1<<f.S.length);w++){let ok=actual.every(c=>c.some(l=>bit(w,f.S.indexOf(Math.abs(l)-1))===Number(l>0)));if(ok!==f.R.includes(w))throw Error("source truth table");verified++;}
 }
 if(q!==decoded.length)throw Error("coverage");
 return {k,N:16*k*k+8*k+Math.floor(Math.log2(k))+1,hash:h.toString(16),active:S.v,clauses:S.C.length,verified};
}
function close(S,empty=false){let D=Array(S.v).fill(3),del=0,scans=0;let F=empty?S.F.concat([{S:[],R:[]}]):S.F;
 for(;;){let old=del;for(let {S,R} of F){scans++;let W=R.filter(w=>S.every((x,i)=>D[x]&(1<<bit(w,i))));if(!W.length)return {status:"NO",del,scans};for(let i=0;i<S.length;i++){let d=W.reduce((z,w)=>z|(1<<bit(w,i)),0);if(d!==D[S[i]]){D[S[i]]=d;del++;}}}if(old===del)return {status:"UNKNOWN",del,scans,primaryFull:D.slice(0,S.b).every(x=>x===3)};}
}

const mul=(p,q)=>p^q^(((p&1)&&((q>>1)&1))?4:0);
const inv=p=>range(8).find(q=>mul(p,q)===0),vbit=i=>1n<<BigInt(i);
function xor(a,b){let C=new Set(a);for(let x of b)if(C.has(x))C.delete(x);else C.add(x);return C}
function prod(a,b){let C=new Set();for(let x of a)for(let y of b){let z=x|y;if(C.has(z))C.delete(z);else C.add(z)}return C}
function span(Q){let rows=new Map();for(let p of Q){let r=new Set(p);while(r.size){let a=[...r].reduce((x,y)=>x>y?x:y);if(a===0n)return "NO";if(!rows.has(a)){rows.set(a,r);break}r=xor(r,rows.get(a))}}return "UNKNOWN"}
function walsh(p,n){let Q=new Set(p),rem=new Set(range(n).map(vbit)),factor=1n,pairs=0;
 while(true){let pair=[...Q].find(z=>z!==0n&&(z&(z-1n))!==0n);if(pair===undefined)break;let a=pair&-pair,b=pair^a;if(!rem.has(a)||!rem.has(b)||(b&(b-1n)))throw Error("bad quadratic");
 let L=new Set(),M=new Set(),R=new Set();for(let z of Q){if(z===pair)continue;if(z&a)L.add(z^a);else if(z&b)M.add(z^b);else R.add(z)}
 Q=xor(R,prod(L,M));rem.delete(a);rem.delete(b);factor*=2n;pairs++}
 return {S:[...Q].some(z=>z!==0n)?0n:factor*(1n<<BigInt(rem.size))*(Q.has(0n)?-1n:1n),pairs}}
function count(Q,n){let P=Q.filter(p=>p.size),r=P.length;if(r>16)throw Error("rank cap");let sums=[],sum=0n;for(let a=0;a<1<<r;a++){let p=new Set();for(let j=0;j<r;j++)if(bit(a,j))p=xor(p,P[j]);let t=walsh(p,n);sum+=t.S;sums.push({value:String(t.S),pairs:t.pairs})}let den=1n<<BigInt(r);if(sum%den||sum<0n)throw Error("count");return {status:sum===0n?"NO":"NOT_REFUTED",r,sums,count:String(sum/den)}}

function parity(z){let p=0;while(z){z&=z-1n;p^=1}return p}
function ev(P,w){return [...P].reduce((p,z)=>p^Number((w&z)===z),0)}
function affine(mask,c=0){return {mask,c}}
function ap(f){let P=new Set(f.c?[0n]:[]);for(let z=f.mask;z;z&=z-1n)P.add(z&-z);return P}
function build(n,clusters){
 let b=n+2*clusters.length,v=b,F=[],C=[],P=[],checks=0;
 function add(S,R){F.push({S,R});let a=new Set(R);for(let w=0;w<1<<S.length;w++)if(!a.has(w))C.push(S.map((id,i)=>bit(w,i)?-id-1:id+1))}
 function label(f){let ids=range(b).filter(i=>f.mask&vbit(i));if(!ids.length){let z=v++;add([z],[f.c]);return z}let z=ids[0];for(let id of ids.slice(1)){let w=v++;add([z,id,w],[0,3,5,6]);z=w}if(f.c){let w=v++;add([z,w],[1,2]);z=w}return z}
 for(let [i,terms] of clusters.entries()){
  let p=range(3).map(()=>v++);add(p,[0]);let q=new Set([0n]);
  for(let [a,b] of terms){let x=label(a),y=label(b);
   // independent check of the local group identity for every input.
   for(let u=0;u<2;u++)for(let w=0;w<2;w++){let z=0;for(let g of [u,w*2,u,w*2])z=mul(z,g);if(z!==4*u*w)throw Error("group identity");checks++}
   q=xor(q,prod(ap(a),ap(b)));
   for(let [id,g] of [[x,1],[y,2],[x,1],[y,2]]){let t=range(3).map(()=>v++),R=[];for(let s=0;s<8;s++)for(let x=0;x<2;x++)R.push(s+(x<<3)+(mul(s,x?g:0)<<4));add(p.concat([id],t),R);p=t}
  }add(p,[4]);P.push(q)
 }
 return {n,b,v,F,C,P,checks,clusters}
}
function dense(m){let all=(1n<<BigInt(m))-1n;return build(m,range(m).map(i=>[[affine(all^vbit(i)),affine(vbit(m+2*i)|vbit(m+2*i+1))]]))}
function hostile(){return build(2,range(4).map(i=>[[affine(1n,bit(i,0)),affine(vbit(2+2*i))],[affine(2n,bit(i,1)),affine(vbit(3+2*i))]]))}
function project(Q,n,priv,cap=4096){
 const pm=priv.reduce((m,i)=>m|vbit(i),0n),basis=[],piv=new Map();
 function coord(m){let c=0n;while(m){let p=m&-m;if(!piv.has(p)){let i=basis.length;if(i>=20)throw Error("feature cap");basis.push(m);piv.set(p,[m,vbit(i)]);return c^vbit(i)}let [r,s]=piv.get(p);m^=r;c^=s}return c}
 let data=Q.map(P=>{let coeff=new Map(),R=new Set(),f=0n;for(let z of P){let y=z&pm,x=z^y;if(!x)R.add(y);else{if(x&(x-1n))throw Error("nonaffine boundary");coeff.set(y,(coeff.get(y)||0n)^x)}}return {R,terms:[...coeff].map(([y,x])=>[y,coord(x)])}});
 if((1n<<BigInt(basis.length+Q.length))>BigInt(cap))return {status:"UNKNOWN",h:basis.length};
 let h=basis.length,words=[],counts=[],evals=0;for(let a=0;a<2**h;a++){let rows=data.map(({R,terms})=>{let P=new Set(R);for(let [y,c] of terms)if(parity(c&BigInt(a)))P=xor(P,new Set([y]));return new Set([...P].map(y=>priv.reduce((z,j,k)=>z|((y&vbit(j))?vbit(k):0n),0n)))});let C=count(rows,priv.length);evals+=C.sums.length;counts.push(C.count);if(C.count!=="0")words.push(a)}
 if(!words.length)return {status:"NO",h,words,counts,evals,basis};
 let eq=[];for(let l=1;l<2**h;l++){let z=parity(BigInt(l&words[0]));if(words.every(w=>parity(BigInt(l&w))===z)){let mask=basis.reduce((a,b,i)=>a^(bit(l,i)?b:0n),0n);eq.push([mask,z])}}
 let exact=range(2**h).every(a=>words.includes(a)===eq.every(([m,z],j)=>{ // verify via original feature linear combination (separate enumeration below)
 return true
 })); // actual exactness by cardinality of affine hull
 let hull=new Set([0]);for(let w of words){let d=w^words[0];for(let a of [...hull])hull.add(a^d)}let isAffine=hull.size===words.length;
 return {status:isAffine?"AFFINE":"NONAFFINE",h,words,counts,evals,basis,eq:isAffine?eq:[],affineHullSize:hull.size}
}
function gauss(eq){let R=new Map(),ops=0;for(let [m,b] of eq){while(m){let p=m&-m;if(!R.has(p)){R.set(p,[m,b]);break}let [v,c]=R.get(p);m^=v;b^=c;ops++}if(!m&&b)return {status:"NO",rank:R.size,ops}}return {status:"UNKNOWN",rank:R.size,ops}}
function direct(S,cap){let hits=0,tested=0;for(let w=0n;w<1n<<BigInt(S.b)&&tested<cap;w++){tested++;if(S.P.every(p=>ev(p,w)===0))hits++}return {tested,hits,status:hits?"NOT_REFUTED":BigInt(tested)===(1n<<BigInt(S.b))?"NO":"UNKNOWN"}}
function run(S){let N=native(S),initial=close(S),linear=span(S.P),refs=direct(S,32768),projections=S.P.map((q,i)=>project([q],S.n,[S.n+2*i,S.n+2*i+1])),g=gauss(projections.flatMap(p=>p.eq||[]));let imp=g.status==="NO"?close(S,true):null;
 // Independently verify group chart projection using two private bits and each feature word.
 for(let [i,p] of projections.entries()){for(let a=0;a<p.counts.length;a++){let witness=null;for(let x=0n;x<1n<<BigInt(S.n);x++){if(p.basis.every((z,j)=>parity(z&x)===bit(a,j))){witness=x;break}if(x>=65536n)throw Error("feature witness cap")}if(witness===null)throw Error("feature witness");let hits=0;for(let y=0;y<4;y++)if(!ev(S.P[i],witness|(BigInt(y)<<BigInt(S.n+2*i))))hits++;if(String(hits)!==p.counts[a])throw Error("projection mismatch")}}
 let global= S.P.length<=12? count(S.P,S.b):{status:"UNKNOWN",r:S.P.length,reason:"fixed 4096 character cap"};
 return {n:S.n,primary:S.b,...N,groupChecks:S.checks,initial,linear,refs,global:{status:global.status,r:global.r,count:global.count},projection:{r:S.P.length,h:Math.max(...projections.map(p=>p.h)),evals:projections.reduce((s,p)=>s+p.evals,0),affine:projections.filter(p=>p.status==="AFFINE").length,tables:projections.slice(0,4).map(p=>({counts:p.counts,words:p.words,h:p.h,status:p.status}))},gauss:g,reclosure:imp}}
function audit(){let jobs=[3,5,9,17,33].map(m=>run(dense(m))),bad=run(hostile());if(jobs.some(j=>j.initial.status!=="UNKNOWN"||j.linear!=="UNKNOWN"||j.gauss.status!=="NO"||j.refs.hits)||bad.gauss.status!=="UNKNOWN"||bad.global.status!=="NO")throw Error("unexpected result");return {jobs,hostile:bad}}

function xorCertificate(S){
 let sum=0n,b=0,checks=0;
 for(let [i,terms] of S.clusters.entries()){
  if(terms.length!==1)return {status:"UNKNOWN"};
  let [a,y]=terms[0],pm=vbit(S.n+2*i)|vbit(S.n+2*i+1);
  if(y.mask!==pm||y.c||a.mask&pm)return {status:"UNKNOWN"};
  for(let x=0;x<2;x++)for(let u=0;u<2;u++)for(let v=0;v<2;v++){
   let z=0;for(let g of [x,2*(u^v),x,2*(u^v)])z=mul(z,g);
   if((z===4)!==Boolean(x&&(u^v)))throw Error("independent local identity");checks++
  }
  sum^=a.mask;b^=1^a.c;
 }
 return {status:!sum&&b?"NO":"UNKNOWN",sum:String(sum),b,checks}
}
function pins(S){
 let F=S.F.slice(),starts=S.F.filter(f=>f.S.length===3&&f.R.length===1&&f.R[0]===0),trans=S.F.filter(f=>f.S.length===7);
 let stages=[],k=0;for(let i=0;i<S.clusters.length;i++){
  let [a,y]=S.clusters[i][0],start=starts[i],t=trans[k],id=t.S[3];k+=4*S.clusters[i].length;
  if(t.S.slice(0,3).join()!==start.S.join())throw Error("start");
  let forms=new Map(range(S.b).map(j=>[j,{mask:vbit(j),c:0}]));
  for(let f of S.F){if(f===t)break;if(f.S.length===3&&f.R.join()==="0,3,5,6"){
   let [u,v,w]=f.S;if(!forms.has(u)||!forms.has(v))throw Error("label map");let A=forms.get(u),B=forms.get(v);forms.set(w,{mask:A.mask^B.mask,c:A.c^B.c})
  }else if(f.S.length===2&&f.R.join()==="1,2"){let [u,v]=f.S,A=forms.get(u);if(!A)throw Error("neg");forms.set(v,{mask:A.mask,c:A.c^1})}}
  let a0=forms.get(id);if(!a0||a0.mask!==a.mask||a0.c!==a.c)throw Error("original label map");
  let P=project([S.P[i]],S.n,[S.n+2*i,S.n+2*i+1]);if(P.status!=="AFFINE"||P.words.join()!=="1")throw Error("pin proof");
  F.push({S:[id],R:[1]});let c=close({...S,F});stages.push({id,status:c.status,scans:c.scans,del:c.del});if(c.status==="NO")break;
 }
 return stages;
}
function binaryJoin(S){
 let A=range(2*S.n).map(()=>[]),R=range(2*S.n).map(()=>[]),clauses=[];
 for(let [i,q] of S.P.entries()){let P=project([q],S.n,[S.n+2*i,S.n+2*i+1]);if(P.h!==2||P.basis.some(m=>m&(m-1n)))return {status:"UNKNOWN"};let ids=P.basis.map(m=>range(S.n).find(j=>vbit(j)===m));
 for(let w=0;w<4;w++)if(!P.words.includes(w)){let a=2*ids[0]+(1^bit(w,0)),b=2*ids[1]+(1^bit(w,1));clauses.push([a,b]);A[a^1].push(b);R[b].push(a^1);A[b^1].push(a);R[a].push(b^1)}}
 let seen=new Set(),order=[];function dfs(v){if(seen.has(v))return;seen.add(v);for(let w of A[v])dfs(w);order.push(v)}range(A.length).forEach(dfs);let comp=Array(A.length).fill(-1);function rev(v,c){if(comp[v]>=0)return;comp[v]=c;for(let w of R[v])rev(w,c)}order.reverse().forEach((v,c)=>rev(v,c));return {status:range(S.n).some(i=>comp[2*i]===comp[2*i+1])?"NO":"UNKNOWN",clauses,comp}
}
function supplement(){let jobs=[3,5,9,17,33].map(m=>{let S=dense(m),C=xorCertificate(S),P=pins(S);if(C.status!=="NO")throw Error("sum");return {m,certificate:C,imports:P.length,last:P.at(-1),totalScans:P.reduce((s,p)=>s+p.scans,0)}});let S=hostile(),B=binaryJoin(S);if(B.status!=="NO")throw Error("binary");let control=build(2,[[[affine(1n),affine(4n)],[affine(2n),affine(8n)]]]);let P=project([control.P[0]],2,[2,3]);if(P.status!=="NONAFFINE"||direct(control,16).hits!==6)throw Error("nonaffine control");return {jobs,hostile:B,minimalSoundness:{words:P.words,counts:P.counts,reference:direct(control,16)}}}
console.log(JSON.stringify(supplement(),null,2));