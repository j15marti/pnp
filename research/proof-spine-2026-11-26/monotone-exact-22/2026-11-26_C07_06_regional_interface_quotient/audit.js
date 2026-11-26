const audit = function audit(){
 const ok=(x,m)=>{if(!x)throw Error(m||"assert")}, bit=i=>1n<<BigInt(i), piv=x=>x.toString(2).length-1, parity=x=>{let r=0;while(x){x&=x-1n;r^=1}return r};
 function add(M,v,b=0){while(v){let p=piv(v),q=M.get(p);if(!q){M.set(p,[v,b]);return 1}v^=q[0];b^=q[1]}return b?-1:0}
 function reduce(M,v,b=0){for(const p of [...M.keys()].sort((a,b)=>b-a)){if(v&bit(p)){v^=M.get(p)[0];b^=M.get(p)[1]}}return [v,b]}
 function bas(V){let M=new Map();for(let v of V)add(M,v);return [...M.values()].map(x=>x[0])}
 function inter(U,V){let M=new Map(),out=[];function insert(v,t){while(v){let p=piv(v),q=M.get(p);if(!q){M.set(p,[v,t]);return}v^=q[0];t^=q[1]}if(t)out.push(t)}for(let v of bas(U))insert(v,0n);for(let v of bas(V))insert(v,v);return bas(out)}
 function boundaries(P){let S=[[]];for(let i=0;i<P.length;i++)S.push(bas([...S[i],...P[i]]));let R=Array(P.length+1);R[P.length]=[];for(let i=P.length-1;i>=0;i--)R[i]=bas([...R[i+1],...P[i]]);return S.map((s,i)=>inter(s,R[i]))}
 function width(P){return Math.max(0,...boundaries(P).map(b=>b.length))}
 function quotient(P,v){let M=new Map();add(M,v);return P.map(Q=>Q.map(x=>reduce(M,x)[0]))}
 function chart(T,E){let M=new Map();for(let [v,b] of E)if(add(M,v,b)<0)return null;
 let changed=true;while(changed){changed=false;for(let [a,b,c] of T){let u=bit(a)^bit(b),v=bit(a)^bit(c);let allowed=[];for(let s=1;s<4;s++){let C=new Map(M);if(add(C,u,s&1)>=0&&add(C,v,s>>1)>=0)allowed.push(s)}if(!allowed.length)return null;for(let t of [1,2,3]){let z=parity(BigInt(t&allowed[0]));if(allowed.every(s=>parity(BigInt(t&s))===z)){let q=add(M,(t&1?u:0n)^(t&2?v:0n),z);if(q<0)return null;changed||=q===1}}}}
 let P=[],states=[];for(let [a,b,c] of T){let [u,s]=reduce(M,bit(a)^bit(b)),[v,t]=reduce(M,bit(a)^bit(c));let list=[];for(let i=0;i<4;i++){if(!((i&1)^s)&&!((i>>1)^t))continue;let C=new Map();if(add(C,u,i&1)>=0&&add(C,v,i>>1)>=0)list.push([[u,i&1],[v,i>>1]])}if(list.length===2**bas([u,v]).length)continue;P.push([u,v]);states.push(list)}
 return {M,P,states}}
 function solve(T,E,cap){let C=chart(T,E);if(!C)return {status:"NO",width:0,pairs:0};let {M,P,states}=C,B=boundaries(P),w=Math.max(0,...B.map(x=>x.length));if(w>cap)return {status:"UNKNOWN",width:w,pairs:0};let D=new Map([[0,[]]]),pairs=0;
 for(let i=0;i<P.length;i++){let next=new Map();for(let [mask,hist] of D)for(let loc of states[i]){pairs++;let R=new Map(),bad=false;for(let j=0;j<B[i].length;j++)if(add(R,B[i][j],(mask>>j)&1)<0)bad=true;for(let [v,b] of loc)if(add(R,v,b)<0)bad=true;if(bad)continue;let z=0;for(let j=0;j<B[i+1].length;j++){let [r,b]=reduce(R,B[i+1][j]);ok(!r,"boundary not determined");z|=b<<j}if(!next.has(z))next.set(z,[...hist,...loc])}D=next;if(!D.size)return {status:"NO",width:w,pairs}}
 let H=new Map(M);for(let [v,b] of D.values().next().value)ok(add(H,v,b)>=0);let x=0n;for(let p of [...H.keys()].sort((a,b)=>a-b)){let [v,b]=H.get(p);if(parity(v&x)!==b)x^=bit(p)}ok(T.every(([a,b,c])=>{let k=[a,b,c].reduce((s,i)=>s+Number(!!(x&bit(i))),0);return k===1||k===2}),"bad witness");return {status:"YES",width:w,pairs,x}}
 const lines=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
 function instance(q,no){let T=[],id=3;for(let i=0;i<q;i++){let V=[0,1,2,id++,id++,id++,id++];for(let L of lines.slice(1))T.push(L.map(j=>V[j]))}let z=id++,t=id++;T.push(no?[0,1,2]:[0,1,z],[2,z,t]);let F=T.map((C,i)=>[...C,id+i]);return {T,F,n:id+F.length}}
 function local(F){let V=[...new Set(F.flat())].sort((a,b)=>a-b),idx=new Map(V.map((v,i)=>[v,i])),S=new Map();for(let m=0;m<2**V.length;m++){if(F.every(C=>C.reduce((s,v)=>s+((m>>idx.get(v))&1),0)===2)){let k=[0,1,2].reduce((s,v)=>s+(((m>>idx.get(v))&1)<<v),0);if(!S.has(k))S.set(k,[V,m])}}return {S,enumerated:2**V.length}}
 // Independent adversarial reconstruction from original 7 NAE IDs, not native enumeration.
 let S=new Set(),full=0;for(let m=0;m<128;m++){const val=L=>L.reduce((s,i)=>s+((m>>i)&1),0);if(lines.slice(1).every(L=>[1,2].includes(val(L)))){S.add(m&7);if([1,2].includes(val(lines[0])))full++}}ok(full===0&&[...S].sort().join()==="0,7");
 let seed=20261126;const rnd=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed};let comparisons=0,strict=0,random=0,rawNo=0,rawYes=0;
 // Track C: exact rank identity and all compatible cuts, independent of local table algorithm.
 for(let t=0;t<120;t++){let P=Array.from({length:8},()=>[BigInt(rnd()%256),BigInt(rnd()%256)]),B=boundaries(P);for(let i=1;i<8;i++)for(let v of B[i]){let W=boundaries(quotient(P,v));for(let j=0;j<B.length;j++){ok(W[j].length<=B[j].length);comparisons++;if(j===i){ok(W[j].length===B[j].length-1);strict++}}}}
 ok(width([[1n],[2n]])===0&&width(quotient([[1n],[2n]],3n))===1,"nonlocal pin control");
 // Independent exact DP reference on small private-completed native systems.
 for(let t=0;t<120;t++){let n=5+rnd()%3,T=[];for(let i=0;i<3+rnd()%8;i++){let v=[];while(v.length<3){let j=rnd()%n;if(!v.includes(j))v.push(j)}T.push(v)}let brute=false;for(let m=0;m<1<<n;m++){if(T.every(C=>[1,2].includes(C.reduce((s,v)=>s+((m>>v)&1),0)))){brute=true;break}}let R=solve(T,[],8);ok(R.status===(brute?"YES":"NO"),"DP reference");random++;if(brute)rawYes++;else rawNo++}
 let rows=[];for(let q of [1,2,4,8,16])for(let no of [false,true]){let {T,F,n}=instance(q,no); // same immutable native source and empty guard in all lanes
 let raw=solve(T,[],2),A=[],tested=0;
 // Fixed source-order disjoint windows of six; verify full physical interface before accepting.
 for(let i=0;i+6<=F.length;i+=6){let R=F.slice(i,i+6),outside=F.slice(0,i).concat(F.slice(i+6)),V=new Set(R.flat()),boundary=[...new Set(outside.flat().filter(x=>V.has(x)))].sort((a,b)=>a-b);ok(boundary.join()==="0,1,2");let a=local(R);ok([...a.S.keys()].sort().join()==="0,7");tested+=a.enumerated;A.push(a.S)}
 // Exact native support replaces all disjoint windows by equality on original anchors.
 let rem=T.slice(A.length*6),E=[[bit(0)^bit(1),0],[bit(0)^bit(2),0]],int=solve(rem,E,2);ok(int.status===(no?"NO":"YES"));
 if(int.status==="YES"){let x=int.x,k=[0,1,2].reduce((s,i)=>s+(Number(!!(x&bit(i)))<<i),0),vals=new Map();for(let i=0;i<n;i++)vals.set(i,Number(!!(x&bit(i))));for(let tab of A){let [V,m]=tab.get(k);V.forEach((v,i)=>vals.set(v,(m>>i)&1))}for(let i=A.length*6;i<T.length;i++)vals.set(F[i][3],2-T[i].reduce((s,v)=>s+vals.get(v),0));ok(F.every(C=>C.reduce((s,v)=>s+vals.get(v),0)===2),"native lift")}
 let hash=2166136261;for(let ch of JSON.stringify({F,guard:[]})){hash=Math.imul(hash^ch.charCodeAt(0),16777619)>>>0}rows.push({q,no,n,clauses:F.length,fingerprint:hash.toString(16),A_native_assignments:tested,A_regions:A.length,B_raw:raw.status,B_width:raw.width,B_pairs:raw.pairs,integrated:int.status,integrated_width:int.width,integrated_pairs:int.pairs})}
 return {seed:20261126,random_reference:{total:random,yes:rawYes,no:rawNo},width_checks:comparisons,strict_edge_drops:strict,nonlocal_guard_control:[0,1],fano_adversarial_support:[...S].sort(),full_fano_solutions:full,rows};
};
console.log(JSON.stringify(audit(),null,2));
