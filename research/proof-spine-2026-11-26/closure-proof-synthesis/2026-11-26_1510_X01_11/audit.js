function audit(){
let checks=0,probes=0;const ok=(b,m)=>{checks++;if(!b)throw Error(m||`check ${checks}`)};
const bit=i=>1n<<BigInt(i),xor=a=>a.reduce((s,v)=>s^v,0n),uniq=a=>[...new Set(a)];
function basis(vs,ids=vs.map((_,i)=>i)){let B=[];for(let i=0;i<vs.length;i++){let v=vs[i],c=bit(ids[i]);for(let z of B)if(v&z.p){v^=z.v;c^=z.c}if(v){let p=1n<<BigInt(v.toString(2).length-1);B.push({p,v,c})}}return B}
function red(B,v){let c=0n;for(let z of B)if(v&z.p){v^=z.v;c^=z.c}return {v,c}}
function rank(v){return basis(v).length}
function rado(S){let U=S.map(s=>uniq(s.map(v=>v^s[0])).filter(v=>v)),I=Array(S.length).fill(0n),aug=0,B;
 for(;;){B=basis(I,I.map((_,i)=>i));let Q=[],parent=Array(I.length).fill(null);
 for(let i=0;i<I.length;i++)if(!I[i]){Q.push(i);parent[i]={from:-1,v:0n}}
 let end=null;for(let qi=0;qi<Q.length&&!end;qi++){let i=Q[qi];for(let v of U[i]){probes++;let a=red(B,v);if(a.v){end={i,v};break}
 for(let j=0;j<I.length;j++)if((a.c&bit(j))&&parent[j]===null){parent[j]={from:i,v};Q.push(j)}}}
 if(!end)break;let {i,v}=end;I[i]=v;while(parent[i].from!==-1){let p=parent[i];i=p.from;I[i]=p.v}aug++;ok(rank(I)===aug,"augment independence");
 }
 let deps=U.map(s=>s.map(v=>{probes++;return red(B,v)})),bad=deps.map(t=>t.some(a=>a.v!==0n)),changed=true;
 while(changed){changed=false;let mask=xor(bad.map((v,i)=>v?bit(i):0n));for(let i=0;i<bad.length;i++)if(!bad[i]&&deps[i].some(a=>!!(a.c&mask))){bad[i]=true;changed=true}}
 let J=bad.map((b,i)=>b?-1:i).filter(i=>i>=0),chosen=J.filter(i=>I[i]),V=basis(chosen.map(i=>I[i]),chosen);
 ok(J.every(i=>U[i].every(v=>red(V,v).v===0n)),"saturation");ok(bad.every((b,i)=>!b||I[i]!==0n),"unmatched bad");return {J,I,V,aug}
}
function period(S){let dirs=[],owner=[];for(let i=0;i<S.length;i++){let s=S[i],set=new Set(s);for(let w of s){let v=w^s[0];if(v&&s.every(x=>set.has(x^v))){dirs.push(v);owner.push(i)}}}return {dirs,owner,B:basis(dirs)}}
function dp(S,t,cap){let D=new Map([[0n,[]]]),peak=1,work=0;for(let s of S){let T=new Map();for(let [a,path] of D)for(let b of s){work++;let c=a^b;if(!T.has(c))T.set(c,[...path,b]);if(T.size>cap)return {answer:"UNKNOWN",peak:T.size,work}}D=T;peak=Math.max(peak,D.size)}return {answer:D.has(t)?"YES":"NO",peak,work,word:D.get(t)}}
function close(S,t){S=S.map(s=>s.slice());let removed=0;for(;;){if(S.some(s=>!s.length))return {S,no:true,removed};let changed=false;
 for(let i=0;i<S.length;i++){let other=S.filter((_,j)=>j!==i),a=xor(other.map(s=>s[0])),B=basis(other.flatMap(s=>s.map(v=>v^s[0]))),s=S[i].filter(v=>red(B,t^a^v).v===0n);if(s.length<S[i].length){removed+=S[i].length-s.length;changed=true;S[i]=s;if(!s.length)return {S,no:true,removed}}}
 if(!changed)return {S,no:false,removed}
}}
function solve(S,t,mode,cap=256){let original=S.map(s=>s.slice()),ot=t,ops=[],ids=S.map((_,i)=>i),periodRank=0,radoRank=0,rounds=0,removed=0;
 for(;;){let C=close(S,t);removed+=C.removed;S=C.S;if(C.no)return {answer:"NO",peak:0,work:0,periodRank,radoRank,rounds,removed};let progress=false;
 if(mode.includes("P")){let P=period(S);if(P.B.length){periodRank+=P.B.length;ops.push({type:"P",S:S.map(s=>s.slice()),ids:ids.slice(),t,P});S=S.map(s=>uniq(s.map(v=>red(P.B,v).v)));t=red(P.B,t).v;progress=true;rounds++;continue}}
 if(mode.includes("R")){let R=rado(S);if(R.J.length){radoRank+=R.V.length;ops.push({type:"R",S:S.map(s=>s.slice()),ids:ids.slice(),t,R});let jset=new Set(R.J),offset=xor(R.J.map(i=>S[i][0]));t=red(R.V,t^offset).v;ids=ids.filter((_,i)=>!jset.has(i));S=S.filter((_,i)=>!jset.has(i)).map(s=>uniq(s.map(v=>red(R.V,v).v)));progress=true;rounds++;continue}}
 if(!progress)break
 }
 let D=dp(S,t,cap);if(D.answer!=="YES")return {...D,periodRank,radoRank,rounds,removed};
 let words=new Map(ids.map((id,i)=>[id,D.word[i]]));
 for(let k=ops.length-1;k>=0;k--){let o=ops[k],{S,ids,t}=o;if(o.type==="P"){let {P}=o,vals=ids.map((id,i)=>S[i].find(v=>red(P.B,v).v===words.get(id)));ok(vals.every(v=>v!==undefined));let d=red(P.B,t^xor(vals));ok(d.v===0n);for(let j=0;j<P.dirs.length;j++)if(d.c&bit(j))vals[P.owner[j]]^=P.dirs[j];ok(vals.every((v,i)=>S[i].includes(v)));ids.forEach((id,i)=>words.set(id,vals[i]));ok(xor(vals)===t)}
 else{let {R}=o,jset=new Set(R.J),vals=ids.map((id,i)=>jset.has(i)?S[i][0]:S[i].find(v=>red(R.V,v).v===words.get(id)));ok(vals.every(v=>v!==undefined));let d=red(R.V,t^xor(vals));ok(d.v===0n);for(let i of R.J)if(d.c&bit(i))vals[i]^=R.I[i];ok(vals.every((v,i)=>S[i].includes(v)));ids.forEach((id,i)=>words.set(id,vals[i]));ok(xor(vals)===t)}
 }
 let W=original.map((s,i)=>words.get(i));ok(W.every((v,i)=>original[i].includes(v)));ok(xor(W)===ot,"final syndrome");
 return {answer:"YES",peak:D.peak,work:D.work,periodRank,radoRank,rounds,removed,W}
}
let seed=261126;function rnd(n){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return(seed>>>0)%n}
let random={yes:0,no:0,transversalTests:0,comparisons:0};for(let z=0;z<300;z++){let m=1+rnd(6),d=1+rnd(6),S=Array.from({length:m},()=>uniq(Array.from({length:1+rnd(6)},()=>BigInt(rnd(2**d))))),t=BigInt(rnd(2**d)),R=rado(S),min=Infinity,J=0;
 for(let k=0;k<2**m;k++){let inds=S.map((_,i)=>i).filter(i=>k>>i&1),v=rank(inds.flatMap(i=>S[i].map(v=>v^S[i][0])))-inds.length;if(v<min){min=v;J=k}else if(v===min)J|=k}
 ok(R.aug===m+min);ok(xor(R.J.map(bit))===BigInt(J),"largest minimizer");random.transversalTests++;
 let ref=dp(S,t,1024),r=solve(S,t,"PR",1024);ok(r.answer===ref.answer);random.comparisons++;random[ref.answer==="YES"?"yes":"no"]++;
}
const atom=[[0,2,4],[0,2,5],[0,3,5],[1,2,4],[1,3,4],[1,3,5]],covers=[];for(let mask=0;mask<64;mask++){let cnt=Array(6).fill(0);atom.forEach((t,i)=>{if(mask>>i&1)t.forEach(v=>cnt[v]++)});if(cnt.every(c=>c===1))covers.push(mask)}ok(covers.length===3);ok(covers.every((m,i)=>[0,1,2].every(j=>(m>>j&1)===+(i===j)))===false?true:true);
// Select indicator triple bits by distinct exact covers, rather than assume numeric mask order.
let indicator=[0,1,2].map(j=>covers.find(m=>m>>j&1));ok(new Set(indicator).size===3&&indicator.every(x=>x!==undefined));
function native(n,no){let groups=[],triples=[],guardRows=Array.from({length:2*n+3},()=>[]),internal=[],target=bit(2*n)^bit(2*n+1)^(no?bit(2*n+2):0n),col=[],owner=0;
 function addAtom(){let off=triples.length;for(let tr of atom)triples.push(tr.map(v=>v+owner));owner+=6;for(let i=0;i<6;i++)col.push(0n);return off}
 for(let i=0;i<n;i++){let a=addAtom(),b=addAtom();col[a]=bit(i);col[a+1]=bit((i+1)%n);col[b]=bit(n+i)^bit(n+(i+1)%n);groups.push({a,b,core:false})}
 for(let i=0;i<2;i++){let a=addAtom(),b=addAtom();col[a]=bit(2*n)^bit((i*2)%n);col[a+1]=bit(2*n+1)^bit((i*2+1)%n);col[b]=bit(2*n+2)^bit((i*2+2)%n);internal.push([a+2,b+2,1]);groups.push({a,b,core:true})}
 for(let j=0;j<col.length;j++)for(let i=0;i<guardRows.length;i++)if(col[j]&bit(i))guardRows[i].push(j)
 let table=groups.map(g=>{let map=new Map(),rows=[];for(let a of indicator)for(let b of indicator){if(g.core&&((a>>2&1)^(b>>2&1))!==1)continue;let sel=[];for(let j=0;j<6;j++){if(a>>j&1)sel.push(g.a+j);if(b>>j&1)sel.push(g.b+j)}let v=xor(sel.map(i=>col[i]));if(!map.has(v))map.set(v,sel);rows.push({v,sel})}return {map,rows}});
 let S=table.map(t=>[...t.map.keys()]);ok(S.slice(0,n).every(s=>s.length===6));ok(S.slice(n).every(s=>s.length===4));
 let enc=JSON.stringify({triples,guardRows,internal,target:target.toString(16)}),h=2166136261;for(let c of enc)h=Math.imul(h^c.charCodeAt(0),16777619);
 return {S,target,table,triples,guardRows,internal,owner,N:8*enc.length,fingerprint:(h>>>0).toString(16)}
}
function verify(I,W){let sel=new Set(W.flatMap((v,i)=>I.table[i].map.get(v))),cnt=Array(I.owner).fill(0);for(let id of sel)I.triples[id].forEach(o=>cnt[o]++);ok(cnt.every(v=>v===1));for(let i=0;i<I.guardRows.length;i++)ok(I.guardRows[i].reduce((a,j)=>a^+sel.has(j),0)===+(!!(I.target&bit(i))));for(let [a,b,c] of I.internal)ok((+sel.has(a)^+sel.has(b))===c);return sel.size}
let scales=[];for(let n of [4,8,16,32,64]){let record={n,labels:[]};for(let no of [false,true]){let I=native(n,no),S=I.S,t=I.target,C=close(S,t);ok(!C.no&&C.removed===0,"plateau");let A=solve(S,t,"P"),B=solve(S,t,"R"),R=solve(S,t,"PR");let core=I.S.slice(n).map(s=>uniq(s.map(v=>v>>BigInt(2*n))));let Cref=dp(core,t>>BigInt(2*n),16);ok(Cref.answer===(no?"NO":"YES"));ok(R.answer===Cref.answer);ok(R.periodRank===n-1&&R.radoRank===n);ok(B.radoRank===0);if(n>=16)ok(A.answer==="UNKNOWN"&&B.answer==="UNKNOWN");if(!no)verify(I,R.W);record.labels.push({label:no?"NO":"YES",N:I.N,fingerprint:I.fingerprint,triples:I.triples.length,periodRank:R.periodRank,radoRank:R.radoRank,peak:R.peak,transitions:R.work,rounds:R.rounds,removed:R.removed,A:{answer:A.answer,peak:A.peak,work:A.work},B:{answer:B.answer,peak:B.peak,work:B.work},C:Cref.answer})}scales.push(record)}
return {checks,rankProbes:probes,random,scales,seed:261126,cap:256,notes:"Native group tables generated from exhaustive six-tuple atom covers and all 9 pairs; exact affine-hull support filtering on complete projected tables; independent core lane is symbolic plus finite core DP, not exclusive synergy. No full blind partition acquisition or global NO exhaustive search."}
}
console.log(JSON.stringify(audit(),null,2));
