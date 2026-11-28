function quotientExperiment(H,edges,m,opts={}){
 const cap=opts.cap??3000000,dictCap=opts.dictCap??64,tc=opts.trellisCap??12;
 let count={ops:0,localWords:0,periodTests:0,quotients:0,filterTests:0,pairTests:0,pairProducts:0,rankOps:0,transitions:0,peakStates:0,peakOptions:0,rounds:0},trace=[],rank0=H.length;
 const tick=(n=1)=>{count.ops+=n;if(count.ops>cap)throw Error("cap")};
 let b=0n,cols=Array(m).fill(0n);for(let j=0;j<H.length;j++){let q=1n<<BigInt(j);if(H[j]&1n)b|=q;for(let i=0;i<m;i++)if(H[j]&(1n<<BigInt(i+1)))cols[i]|=q}
 const pop=x=>{let s=0;while(x){s++;x&=x-1n}return s};
 const add=(B,x)=>{while(x){tick();count.rankOps++;let p=x&-x;if(!B.has(p)){B.set(p,x);return}x^=B.get(p)}};
 const rem=(B,x)=>{while(x){tick();count.rankOps++;let p=x&-x;if(!B.has(p))return false;x^=B.get(p)}return true};
 const group=Array.from({length:m},(_,i)=>i),root=i=>{while(group[i]!==i)i=group[i];return i};
 for(let [a,c] of edges)group[root(a)]=root(c);let g=new Map();for(let i=0;i<m;i++){let r=root(i);if(!g.has(r))g.set(r,[]);g.get(r).push(i)}
 let blocks=[],seq=0,original=[];for(let V of g.values()){if(V.length>tc)return{decision:"UNKNOWN block cap",block:V.length};let I=new Map(V.map((v,i)=>[v,i])),E=edges.filter(e=>I.has(e[0])),S=new Map();for(let w=0;w<2**V.length;w++){tick();count.localWords++;if(E.some(([a,c])=>(w>>I.get(a)&1)&&(w>>I.get(c)&1)))continue;let s=0n,z=0n;for(let j=0;j<V.length;j++)if(w>>j&1){s^=cols[V[j]];z|=1n<<BigInt(V[j]+1)}if(!S.has(s))S.set(s,z)}let Q={id:seq++,S};blocks.push(Q);original.push({id:Q.id,V,S:[...S].map(([s,z])=>[s.toString(16),z.toString(16)])})}
 let initialBlocks=blocks.length,initialOptions=blocks.reduce((a,c)=>a+c.S.size,0),initialCut=null,finalCut=null,baseResult=null;
 const state=()=>{count.peakOptions=Math.max(count.peakOptions,blocks.reduce((n,B)=>n+B.S.size,0))};
 const basisOf=B=>{let G=new Map(),first=B.S.keys().next().value;for(let x of B.S.keys())add(G,x^first);return{G,first}};
 function suffix(){let A=Array(blocks.length+1),off=Array(blocks.length+1).fill(0n);A[blocks.length]=new Map();for(let i=blocks.length-1;i>=0;i--){let B=new Map(A[i+1]),{G,first}=basisOf(blocks[i]);for(let x of G.values())add(B,x);A[i]=B;off[i]=off[i+1]^first}return{A,off}}
 function cut(){let {A,off}=suffix(),P=new Map(),w=0;for(let i=0;i<blocks.length;i++){for(let x of basisOf(blocks[i]).G.values())add(P,x);w=Math.max(w,P.size+A[i+1].size-A[0].size)}return{w,rank:A[0].size,A,off}}
 function period(S){if(S.size%2||S.size<2)return 0n;let first=S.keys().next().value;for(let x of S.keys()){let p=x^first;if(!p)continue;let ok=true;for(let y of S.keys()){tick();count.periodTests++;if(!S.has(y^p)){ok=false;break}}if(ok)return p}return 0n}
 // keep lift frames; all dictionaries store original independent-set bitmask for their own disjoint owners
 function project(p,owner){let old=blocks.map(B=>({id:B.id,S:B.S})),oldb=b,k=p&-p,pi=x=>x&k?x^p:x;b=pi(b);blocks=blocks.map(B=>{let S=new Map();for(let [x,z] of B.S){tick();let y=pi(x);if(!S.has(y))S.set(y,z)}return{id:B.id,S}});trace.push({kind:"period",owner,p:p.toString(16),oldb:oldb.toString(16),beforeSizes:old.map(B=>[B.id,B.S.size])});frames.push({kind:"period",old,oldb,p,owner});count.quotients++}
 const frames=[];
 function fuse(i,j,S){let A=blocks[i],B=blocks[j],id=seq++;frames.push({kind:"fuse",A,B,id});trace.push({kind:"fuse",a:A.id,b:B.id,id,size:S.size});blocks=blocks.filter((_,k)=>k!==i&&k!==j);blocks.splice(i,0,{id,S})}
 function restrict(){let {A,off}=suffix();if(!rem(A[0],b^off[0]))return{no:true};let P=new Map(),po=0n,changed=false;for(let i=0;i<blocks.length;i++){let C=blocks[i],B=new Map(A[i+1]);for(let x of P.values())add(B,x);let S=new Map();for(let [x,z] of C.S){tick();count.filterTests++;if(rem(B,b^po^off[i+1]^x))S.set(x,z)}if(!S.size)return{no:true};if(S.size<C.S.size){changed=true;trace.push({kind:"filter",id:C.id,from:C.S.size,to:S.size});blocks[i]={id:C.id,S}}let {G,first}=basisOf(blocks[i]);for(let x of G.values())add(P,x);po^=first}return{changed}}
 function trellis(allowActual=false){let C=cut();if(!rem(C.A[0],b^C.off[0]))return{decision:"NO affine",w:C.w,rank:C.rank};if(C.w>tc&&!allowActual)return{decision:"UNKNOWN width",w:C.w,rank:C.rank};let T=new Map([[0n,new Map()]]);for(let i=0;i<blocks.length;i++){let B=blocks[i],U=new Map();for(let [u,z] of T)for(let [v,w] of B.S){tick();count.transitions++;let t=u^v;if(rem(C.A[i+1],b^t^C.off[i+1])&&!U.has(t)){let q=new Map(z);q.set(B.id,v);U.set(t,q)}if(U.size>2**tc)return{decision:"UNKNOWN state cap",w:C.w,rank:C.rank}}T=U;count.peakStates=Math.max(count.peakStates,T.size);if(!T.size)return{decision:"NO",w:C.w,rank:C.rank}}return T.has(b)?{decision:"YES",w:C.w,rank:C.rank,choices:T.get(b)}:{decision:"NO",w:C.w,rank:C.rank}}
 function lift(choices){for(let i=frames.length-1;i>=0;i--){let f=frames[i];if(f.kind==="fuse"){let t=choices.get(f.id);choices.delete(f.id);let ok=false;for(let x of f.A.S.keys()){tick();if(f.B.S.has(t^x)){choices.set(f.A.id,x);choices.set(f.B.id,t^x);ok=true;break}}if(!ok)throw Error("fuse lift")}else{let k=f.p&-f.p,pi=x=>x&k?x^f.p:x,actual=0n;for(let B of f.old){let t=choices.get(B.id),x=[...B.S.keys()].find(y=>pi(y)===t);if(x===undefined)throw Error("period lift");choices.set(B.id,x);actual^=x}let delta=actual^f.oldb;if(delta){if(delta!==f.p)throw Error("lift discrepancy");let x=choices.get(f.owner)^f.p,B=f.old.find(B=>B.id===f.owner);if(!B.S.has(x))throw Error("period owner");choices.set(f.owner,x)}}}
 let z=0n;for(let B of original){let t=choices.get(B.id),q=B.S.find(([s])=>BigInt("0x"+s)===t);if(!q)throw Error("original lift");z|=BigInt("0x"+q[1])}return z}
 let result;try{state();let c=cut();initialCut={w:c.w,rank:c.rank};if(opts.baseline){result=trellis(true)}else{
 for(;;){count.rounds++;state();let did=false;
 // absorb first nonzero period, then re-evaluate all exact dictionaries
 for(let B of blocks){let p=period(B.S);if(p){project(p,B.id);did=true;break}}if(did)continue;
 if(opts.filter!==false){let z=restrict();if(z.no){result={decision:"NO affine/private filter"};break}if(z.changed)continue}
 if(opts.fuse!==false){
 let seen=new Map(),pairs=new Set(),best=null,candidates=[];for(let i=0;i<blocks.length;i++){let S=[...blocks[i].S.keys()];for(let a=0;a<S.length;a++)for(let c=a+1;c<S.length;c++){tick();let d=S[a]^S[c];if(!seen.has(d))seen.set(d,new Set());let I=seen.get(d);for(let j of I){if(j===i)continue;let k=j+":"+i;if(pairs.has(k))continue;pairs.add(k);tick();count.pairTests++;let A=blocks[j].S,B=blocks[i].S;if(A.size*B.size>dictCap*dictCap)continue;let T=new Map();outer:for(let [x,z] of A)for(let [y,w] of B){tick();count.pairProducts++;if(!T.has(x^y))T.set(x^y,z|w);if(T.size>dictCap)break outer}if(T.size>dictCap)continue;let p=period(T);if(p||(opts.fuseAny&&T.size<A.size*B.size)){candidates.push({a:blocks[j].id,b:blocks[i].id,S:T});}}I.add(i)}}if(candidates.length){let used=new Set();candidates.sort((a,b)=>a.S.size-b.S.size||a.a-b.a||a.b-b.b);for(let c of candidates){if(used.has(c.a)||used.has(c.b))continue;let i=blocks.findIndex(B=>B.id===c.a),j=blocks.findIndex(B=>B.id===c.b);if(i<0||j<0)throw Error('batch index');fuse(Math.min(i,j),Math.max(i,j),c.S);used.add(c.a);used.add(c.b)}continue}}
 result=trellis(true);break}
 }
 if(result.decision==="YES"){let z=lift(result.choices);delete result.choices;let s=0n;for(let i=0;i<m;i++)if(z&(1n<<BigInt(i+1)))s^=cols[i];let target=H.reduce((v,h,i)=>v|((h&1n)<<BigInt(i)),0n);if(s!==target||edges.some(([a,c])=>(z>>BigInt(a+1)&1n)&&(z>>BigInt(c+1)&1n)))throw Error("lift validation");result.witness=z.toString(16)}
 }catch(e){if(e.message!=="cap")throw e;result={decision:"UNKNOWN work cap"}}
 return{...result,initialBlocks,initialOptions,initialCut,finalBlocks:blocks.length,finalOptions:blocks.reduce((a,B)=>a+B.S.size,0),count,trace,original};
}


module.exports={quotientExperiment};
