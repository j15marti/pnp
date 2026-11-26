// P4RC13 independent finite certificate. Node.js 18+.
function audit(){
 const ck=(x,m)=>{if(!x)throw Error(m)},words=d=>Array.from({length:2**d},(_,i)=>Array.from({length:d},(_,j)=>i>>(d-1-j)&1)),key=w=>w.join(""),eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b),sum=w=>w.reduce((a,b)=>a+b,0);
 const cache=new Map();
 function orientations(W,d){
  const id=d+":"+W.map(key).sort().join(",");if(cache.has(id))return cache.get(id);
  const meet=[],lattice=[];
  for(const s of words(d)){
   const q=s.map(x=>2*x-1);
   if(new Set(W.map(w=>sum(w.map((x,i)=>x*q[i])))).size!==1)continue;
   const O=W.map(w=>q.map((_,j)=>sum(w.slice(0,j).map((x,i)=>x*q[i])))),Oset=new Set(O.map(w=>w.join(",")));
   const closed=f=>O.every(a=>O.every(b=>Array.from({length:4*d+1},(_,i)=>i-2*d).every(t=>{const z=a.map((x,i)=>f(x,b[i]+t));return Oset.has(z.map(x=>x-z[0]).join(","))})));
   if(closed(Math.min)){meet.push(s);if(closed(Math.max))lattice.push(s);}
  }
  const r={meet,lattice};cache.set(id,r);return r;
 }
 function binaryClosure(W,d){
  if(!W.length)return [];
  return words(d).filter(x=>x.every((a,i)=>W.some(w=>w[i]===a))&&x.every((a,i)=>x.every((b,j)=>W.some(w=>w[i]===a&&w[j]===b))));
 }
 const bij=(W,d)=>eq(binaryClosure(W,d).map(key).sort(),W.map(key).sort()),anti=W=>W.filter(w=>W.some(v=>v.every((x,i)=>x===1-w[i]))).length/2;
 const finite={},sizePairs={},remaining={},native={};
 for(let d=1;d<=4;d++){
  let c={tables:0,meet_admitted:0,lattice_admitted:0,meet_only:0,sign_words_checked:0,meet_only_matching_fail:0,both_decline_matching_fail:0};
  for(let p=0;p<2;p++){
   const A=words(d).filter(w=>sum(w)%2===p);
   for(let m=1;m<1<<A.length;m++){
    const W=A.filter((_,i)=>m>>i&1),{meet:h,lattice:l}=orientations(W,d);
    ck(bij(h,d),"orientation relation not bijunctive");c.tables++;c.sign_words_checked+=2**d;c.meet_admitted+=+!!h.length;c.lattice_admitted+=+!!l.length;
    if(h.length&&!l.length){c.meet_only++;ck(h.length===1,"unique one-sided sign");if(anti(W)===1)c.meet_only_matching_fail++;}
    if(d===4){let k=h.length+","+l.length;sizePairs[k]=(sizePairs[k]||0)+1;if(!h.length&&anti(W)===1){c.both_decline_matching_fail++;k=W.length+","+bij(W,d);remaining[k]=(remaining[k]||0)+1;}}
   }
  }
  finite[d]=c;
 }
 for(const s of words(4).filter(x=>sum(x)===2)){
  const A=words(4).filter(w=>sum(w.map((x,i)=>x*(2*s[i]-1)))===0);
  ck(A.length===6,"balanced native support");
  for(let m=1;m<64;m++){
   const W=A.filter((_,i)=>m>>i&1),h=orientations(W,4).meet;
   const k=[!!h.length,anti(W)!==1,bij(W,4)].join(",");native[k]=(native[k]||0)+1;
   ck(h.length||anti(W)!==1||bij(W,4),"native trichotomy");
  }
 }
 const T=[[1,0,0,1],[0,0,1,1],[3,0,1,0],[0,1,0,1],[9,1,0,0],[0,1,1,0],[2,5,4,2],[4,2,3,4],[9,5,2,3],[5,4,3,4],[2,3,4,5],[4,4,2,4],[2,3,5,2],[3,3,5,5],[5,4,2,3],[4,7,4,5],[3,5,5,2],[5,2,3,3],[6,6,6,7],[7,6,7,7],[1,7,7,7],[7,7,7,6],[6,2,6,6],[7,6,6,6],[9,8,8,9],[8,8,9,9],[1,8,9,8],[8,9,8,9],[6,9,8,8],[8,9,9,8]];
 const rows=Array.from({length:40},()=>[]);T.forEach((t,j)=>t.forEach((v,c)=>rows[10*c+v].push(j)));ck(rows.every(r=>r.length===3),"native degree");
 // Actual open shores. Ports in first-shore cyclic order; other side uses reverse order.
 // Port IDs: internal elements6,1 hit external tuples28,26; internal tuples4,8 hit exterior element9.
 const ids=[28,26,4,8];let all=[];
 function rec(P,R,J){
  let p=P.slice();for(;;){let ch=false;for(const row of R){let on=row.filter(j=>p[j]===1),fr=row.filter(j=>p[j]===-1);if(on.length>1||!on.length&&!fr.length)return null;if(on.length){for(const j of fr){p[j]=0;ch=true;}}else if(fr.length===1){p[fr[0]]=1;ch=true;}}if(!ch)break;}
  const j=J.find(j=>p[j]===-1);if(j===undefined)return p;
  for(const x of [0,1]){let q=p.slice();q[j]=x;const v=rec(q,R,J);if(v!==null)return v;}return null;
 }
 function cap(inside){
  const J=Array.from({length:inside?24:6},(_,j)=>inside?j:j+24);
  const R=rows.filter((_,i)=>inside?i%10<8:i%10>=8).map(r=>r.map(j=>J.includes(j)?j:30+ids.indexOf(j)));
  ck(R.every(r=>r.every(j=>j>=0&&j<34)),"open stub identity");
  const W=[];
  for(const w of words(4)){let p=Array(34).fill(-1);ids.forEach((j,i)=>p[J.includes(j)?j:30+i]=w[i]);if(rec(p,R,J)!==null)W.push(w);}
  return W;
 }
 const A=cap(true),B=cap(false).map(w=>w.slice().reverse());
 const sa=orientations(A,4),sb=orientations(B,4);ck(sa.meet.length===1&&!sa.lattice.length,"native comparator is meet-only");
 const compatible=sa.meet.some(a=>sb.meet.some(b=>a.every((x,i)=>x===1-b[3-i])));ck(compatible,"two-shore coherent signs");
 return {finite,orientation_cardinality_pairs:sizePairs,remaining_abstract:remaining,native_balanced_occurrences:native,native_cap:{inside:A,outside_reverse:B,inside_meet:sa.meet,outside_meet:sb.meet,compatible},note:"Native rotation and full source planarity independently certified by RC12; this checker replays open masks and coherent signs, not full global height solver."};
}
console.log(JSON.stringify(audit(),null,2));
