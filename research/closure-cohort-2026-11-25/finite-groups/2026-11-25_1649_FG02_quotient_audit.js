function quotientAudit(){
 let seed=1649;const rng=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296};let checks=0;
 function ck(x){checks++;if(!x)throw Error("quotient mismatch")}
 const ids=n=>Array.from({length:n},(_,i)=>i),par=x=>{let a=0;while(x){x&=x-1;a^=1}return a};
 function tabs(k,q){return ids(k).map(()=>[0,1].map(()=>[0,1].map(()=>ids(1<<q).filter(()=>rng()<.55))))}
 function brute(A,T,q,h){const k=A.length,S=new Set();for(let m=0;m<(1<<k);m++){let X=new Set([0]);for(let i=0;i<k;i++){let t=h;for(let j=0;j<k;j++)if(A[i][j]&&(m&(1<<j)))t^=1;let Y=new Set();for(const a of X)for(const g of T[i][t][(m>>i)&1])Y.add(a^g);X=Y}for(const g of X)S.add((par(m)<<q)|g)}return S}
 // states are (last/next parity, cumulative parity, cumulative guard), with remembered first bit
 function cyc(T,q,h){let k=T.length,S=new Set(),G=1<<q;for(let f=0;f<2;f++){let D=new Map([[f*2*G,[]]]);for(let i=0;i<k;i++){let E=new Map();for(const [key,path] of D){let a=Math.floor(key/(2*G)),r=key%(2*G),p=r>>q,g=r%G;for(let b=0;b<2;b++){if(i===k-1&&b!==f)continue;for(const v of T[i][h^b][a])E.set(b*2*G+((p^a)<<q)+(g^v),[...path,[a,v]])}}D=E}for(const [key,path]of D)S.add(key%(2*G))}return S}
 // A = diag(d)+ L R, row L and columns R represented by r-bit numbers
 function low(T,q,h,L,R,d,r){const k=T.length,G=1<<q,S=new Set();for(let z=0;z<(1<<r);z++){let D=new Set([0]);for(let i=0;i<k;i++){let E=new Set();for(const key of D){let u=key>>(q+1),p=(key>>q)&1,g=key%G;for(let a=0;a<2;a++)for(const v of T[i][h^par(L[i]&z)^(d[i]&a)][a])E.add(((u^(a?R[i]:0))<<(q+1))|((p^a)<<q)|(g^v))}D=E}for(const key of D)if((key>>(q+1))===z)S.add(key%(2*G))}return S}
 let cycleRoots=0,lowRoots=0,signatureChecks=0;
 for(let x=0;x<240;x++){const n=3+Math.floor(rng()*7),q=1+Math.floor(rng()*3),r=1+Math.floor(rng()*3),T=tabs(n,q),A=ids(n).map(i=>ids(n).map(j=>+((i+1)%n===j))),L=ids(n).map(()=>Math.floor(rng()*(1<<r))),R=ids(n).map(()=>Math.floor(rng()*(1<<r))),d=L.map((l,i)=>par(l&R[i])),B=ids(n).map(i=>ids(n).map(j=>par(L[i]&R[j])^(i===j?d[i]:0)));for(let h=0;h<2;h++){let a=brute(A,T,q,h),b=cyc(T,q,h),c=brute(B,T,q,h),e=low(T,q,h,L,R,d,r);for(let s=0;s<(2<<q);s++){ck(a.has(s)===b.has(s));ck(c.has(s)===e.has(s));signatureChecks+=2}}cycleRoots++;lowRoots++}
 return {seedInitial:1649,cycleRoots,lowRoots,signatureChecks,checks,scope:"arbitrary child signature tables, no supplied child graph or rank acquisition, signature decision only; main audit verifies actual graph reconstruction"}
}
console.log(JSON.stringify(quotientAudit(),null,2));
