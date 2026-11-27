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
function fixture(m,targets=[4,4]){
 let b=2*m+1,v=b,F=[],C=[],occ=[],A=[],B=[],paths=[];
 function add(S,R){let rs=new Set(R);F.push({S,R});for(let w=0;w<1<<S.length;w++)if(!rs.has(w))C.push(S.map((id,i)=>bit(w,i)?-id-1:id+1))}
 for(let i=1;i<=2*m;i++){let j=occ.length,neg=Number(i>m);occ.push({id:0,g:1,flip:neg},{id:i,g:2,flip:0},{id:0,g:1,flip:neg},{id:i,g:2,flip:0});let comm=[j,j+1,j+2,j+3],cancel=[j,j+2,j+1,j+3];A.push(...(neg?cancel:comm));B.push(...(neg?comm:cancel))}
 for(let [j,order] of [A,B].entries()){let p=range(3).map(()=>v++),path=[p];add(p,[0]);for(let oi of order){let o=occ[oi],q=range(3).map(()=>v++),R=[];for(let s=0;s<8;s++)for(let x=0;x<2;x++)R.push(s+(x<<3)+(mul(s,(x^o.flip)?o.g:0)<<4));add(p.concat([o.id],q),R);p=q;path.push(p)}add(p,[targets[j]]);paths.push(path)}
 return {m,b,v,F,C,occ,A,B,targets,paths}
}
function evaluate(S,order,w){let p=0;for(let oi of order){let o=S.occ[oi],x=Number(Boolean(w&vbit(o.id)));p=mul(p,(x^o.flip)?o.g:0)}return p}
function quotient(S,cap){let ops=0;function mm(a,b){if(++ops>cap)throw Error("CAP");return mul(a,b)}
 let pos=new Map(S.B.map((o,i)=>[o,i])),H=new Set([0]);for(let i=0;i<S.A.length;i++)for(let j=i+1;j<S.A.length;j++){let u=S.A[i],v=S.A[j];if(pos.get(u)>pos.get(v)){let a=S.occ[u].g,b=S.occ[v].g;H.add(mm(inv(mm(b,a)),mm(a,b)))}}
 for(let h of H)for(let a=0;a<8;a++)H.add(mm(mm(a,h),inv(a)));for(let a of H)for(let b of H)H.add(mm(a,b));
 let rep=range(8).map(a=>Math.min(...[...H].map(h=>mm(a,h))));
 for(let a=0;a<8;a++)for(let b=0;b<8;b++)if(rep[mm(a,b)]!==rep[mm(rep[a],rep[b])])throw Error("congruence");
 let R=new Set([0]);for(let oi of S.A){let Q=new Set();for(let a of R){Q.add(a);Q.add(rep[mm(a,S.occ[oi].g)])}R=Q}
 let [a,b]=S.targets.map(t=>rep[t]);return {status:a!==b||!R.has(a)?"NO":"UNKNOWN",H:[...H],ops,targets:[a,b]}
}
function xor(a,b){let C=new Set(a);for(let x of b)if(C.has(x))C.delete(x);else C.add(x);return C}
function prod(a,b){let C=new Set();for(let x of a)for(let y of b){let z=x|y;if(C.has(z))C.delete(z);else C.add(z)}return C}
function polynomials(S,cap){let ops=0,Q=[];function one(O,w){ops+=O.length;if(ops>cap)throw Error("CAP");return evaluate(S,O,w)}
 for(let [j,O] of [S.A,S.B].entries()){let c=one(O,0n)^S.targets[j],L=range(S.b).map(i=>one(O,vbit(i))^S.targets[j]^c),p=range(3).map(k=>new Set(bit(c,k)?[0n]:[]));
 for(let i=0;i<S.b;i++)for(let k=0;k<3;k++)if(bit(L[i],k))p[k].add(vbit(i));
 for(let i=0;i<S.b;i++)for(let l=i+1;l<S.b;l++){let z=one(O,vbit(i)|vbit(l))^S.targets[j]^c^L[i]^L[l];for(let k=0;k<3;k++)if(bit(z,k))p[k].add(vbit(i)|vbit(l))}
 Q.push(...p)}return {Q,ops}}
function span(Q){let rows=new Map();for(let p of Q){let r=new Set(p);while(r.size){let a=[...r].reduce((x,y)=>x>y?x:y);if(a===0n)return "NO";if(!rows.has(a)){rows.set(a,r);break}r=xor(r,rows.get(a))}}return "UNKNOWN"}
function walsh(p,n){let Q=new Set(p),rem=new Set(range(n).map(vbit)),factor=1n,pairs=0;
 while(true){let pair=[...Q].find(z=>z!==0n&&(z&(z-1n))!==0n);if(pair===undefined)break;let a=pair&-pair,b=pair^a;if(!rem.has(a)||!rem.has(b)||(b&(b-1n)))throw Error("bad quadratic");
 let L=new Set(),M=new Set(),R=new Set();for(let z of Q){if(z===pair)continue;if(z&a)L.add(z^a);else if(z&b)M.add(z^b);else R.add(z)}
 Q=xor(R,prod(L,M));rem.delete(a);rem.delete(b);factor*=2n;pairs++}
 return {S:[...Q].some(z=>z!==0n)?0n:factor*(1n<<BigInt(rem.size))*(Q.has(0n)?-1n:1n),pairs}}
function count(Q,n){let P=Q.filter(p=>p.size),r=P.length;if(r>16)throw Error("rank cap");let sums=[],sum=0n;for(let a=0;a<1<<r;a++){let p=new Set();for(let j=0;j<r;j++)if(bit(a,j))p=xor(p,P[j]);let t=walsh(p,n);sum+=t.S;sums.push({value:String(t.S),pairs:t.pairs})}let den=1n<<BigInt(r);if(sum%den||sum<0n)throw Error("count");return {status:sum===0n?"NO":"NOT_REFUTED",r,sums,count:String(sum/den)}}
function brute(S,cap){let tested=0,ops=0,hit=0;for(let w=0n;w<1n<<BigInt(S.b);w++){if(ops+S.A.length+S.B.length>cap)break;ops+=S.A.length+S.B.length;tested++;if(evaluate(S,S.A,w)===S.targets[0]&&evaluate(S,S.B,w)===S.targets[1])hit++}let complete=BigInt(tested)===(1n<<BigInt(S.b));return {tested,ops,hit,complete,status:hit?"NOT_REFUTED":complete?"NO":"UNKNOWN"}}
function independent(S){let checks=0;for(let i=0;i<S.occ.length;i+=4){let ids=range(4).map(j=>i+j),a=S.occ[i],b=S.occ[i+1],orders=[S.A,S.B].map(O=>O.slice(i,i+4));if(orders.some(O=>O.some(j=>!ids.includes(j)))||a.id!==0||b.id===0||S.occ[i+2].id!==a.id||S.occ[i+3].id!==b.id)throw Error("alias");
 for(let x=0;x<2;x++)for(let y=0;y<2;y++){let w=(x?1n:0n)|(y?vbit(b.id):0n),v=orders.map(O=>evaluate(S,O,w));checks+=2;let expect=i<4*S.m?[4*x*y,0]:[0,4*(1-x)*y];if(v.join()!==expect.join())throw Error("identity")}}return {status:S.targets.join()==="4,4"?"NO":"UNKNOWN",checks}}
function audit(){let result=[],cap=2000000;for(let m of [1,2,4,8,16,32]){let S=fixture(m),N=native(S),initial=close(S),A=quotient(S,cap),B=polynomials(S,cap),L=span(B.Q),C=brute(S,cap),D=independent(S),H=count(B.Q,S.b),R=close(S,true);if(initial.status!=="UNKNOWN"||A.status!=="UNKNOWN"||L!=="UNKNOWN"||H.status!=="NO"||C.hit||D.status!=="NO"||R.status!=="NO")throw Error(JSON.stringify({m,initial,A,L,C,D,H,R}));result.push({m,primary:S.b,occurrences:S.occ.length,...N,initial,selective:A,linearization:L,coefficientOps:B.ops,monomials:B.Q.map(p=>p.size),brute:C,independent:D,hybrid:H,reclosure:R})}
 let S=fixture(2,[4,0]),B=polynomials(S,cap),C=brute(S,cap),H=count(B.Q,S.b);if(!C.complete||String(C.hit)!==H.count||H.status==="NO")throw Error("SAT control");
 let seed=8271,rand=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed>>>24},checks=0;for(let i=0;i<180;i++){let n=1+i%8,r=1+i%4,Q=range(r).map(()=>{let p=new Set();if(rand()%2)p.add(0n);for(let a=0;a<n;a++){if(rand()%2)p.add(vbit(a));for(let b=a+1;b<n;b++)if(rand()%2)p.add(vbit(a)|vbit(b))}return p}),H=count(Q,n),num=0;for(let w=0n;w<1n<<BigInt(n);w++){if(Q.every(p=>[...p].reduce((s,z)=>s^Number((z&w)===z),0)===0))num++;checks++}if(String(num)!==H.count)throw Error("random count")}
 return {cap,result,soundness:{source:native(S),reference:C,hybrid:H},random:{cases:180,assignments:checks}}}
console.log(JSON.stringify(audit(),null,2));
