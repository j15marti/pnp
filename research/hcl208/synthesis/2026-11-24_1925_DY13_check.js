function main(){
 const out={seed:20261124,random:{sat:0,unsat:0},fano:[],cycles:[],chain:[],clique:[],ledger:{closureScans:0,pins:0,gaussXors:0,sccCalls:0,generatorClosures:0,candidates:0,referenceWords:0,checks:0}};
 const L=out.ledger, bit=i=>1n<<BigInt(i), has=(x,i)=>Number((x>>BigInt(i))&1n);
 function parity(x){let p=0;while(x){x&=x-1n;p^=1}return p}
 function ok(b,c){return c.some(l=>has(b,Math.abs(l)-1)===(l>0?1:0))}
 function check(q,msg){L.checks++;if(!q)throw Error(msg)}
 function valid(b,C,R){return C.every(c=>ok(b,c))&&R.every(([a,r])=>parity(a&b)===r)}
 function gauss(n,R){let a=R.map(([v,r])=>[v,r]),p=0;for(let i=0;i<n;i++){let j=a.findIndex(([v],k)=>k>=p&&has(v,i));if(j<0)continue;[a[p],a[j]]=[a[j],a[p]];for(let k=0;k<a.length;k++)if(k!==p&&has(a[k][0],i)){a[k][0]^=a[p][0];a[k][1]^=a[p][1];L.gaussXors++}p++}return a.some(([v,r])=>v===0n&&r)?null:a.slice(0,p)}
 function closure(n,C,R){let P=0n,B=0n;function pin(i,v){if(has(P,i))return has(B,i)===v;P|=bit(i);if(v)B|=bit(i);L.pins++;return true}
  while(true){L.closureScans++;let change=false;
   for(const c of C){if(c.some(l=>has(P,Math.abs(l)-1)&&ok(B,[l])))continue;let a=c.filter(l=>!has(P,Math.abs(l)-1));if(!a.length)return null;if(a.length===1){if(!pin(Math.abs(a[0])-1,Number(a[0]>0)))return null;change=true;break}}
   if(change)continue;
   let r=gauss(n,R.map(([a,b])=>[a&~P,b^parity(a&B)]));if(r===null)return null;
   let single=r.find(([a])=>(a&(a-1n))===0n);if(single){let i=0;while(!has(single[0],i))i++;if(!pin(i,single[1]))return null;continue}
   return {P,B,R:r};
  }
 }
 function base(n,C){L.sccCalls++;const g=Array.from({length:2*n},()=>[]),h=g.map(()=>[]);const ix=l=>2*(Math.abs(l)-1)+(l<0?1:0);for(const c of C){if(!c.length)return null;let a=ix(c[0]),b=ix(c[c.length-1]);g[a^1].push(b);h[b].push(a^1);g[b^1].push(a);h[a].push(b^1)}let seen=new Set(),ord=[],s=Array(2*n).fill(-1);
  function dfs(v){if(seen.has(v))return;seen.add(v);for(const u of g[v])dfs(u);ord.push(v)}
  function rev(v,k){if(s[v]>=0)return;s[v]=k;for(const u of h[v])rev(u,k)}
  for(let v=0;v<2*n;v++)dfs(v);let k=0;for(const v of ord.reverse())if(s[v]<0)rev(v,k++);
  let b=0n;for(let i=0;i<n;i++){if(s[2*i]===s[2*i+1])return null;if(s[2*i]>s[2*i+1])b|=bit(i)}check(C.every(c=>ok(b,c)),"SCC witness");return b;
 }
 function solve(n,C,R){C=C.map(c=>[...new Set(c)]).filter(c=>!c.some(l=>c.includes(-l)));let z=closure(n,C,R);if(!z)return {w:null,k:0,g:0};let D=C.slice();for(let i=0;i<n;i++)if(has(z.P,i))D.push([has(z.B,i)?i+1:-(i+1)]);
  let b=base(n,D);if(b===null)return {w:null,k:z.R.length,g:0};
  // A fresh fixed-point check at stagnation, no inferred constraint from the anchor.
  let again=closure(n,C,R);check(again&&again.P===z.P&&again.B===z.B,"closure replay");
  let G=Array.from({length:n},()=>[]);
  for(let c of D){let q=c.map(l=>has(b,Math.abs(l)-1)?-l:l);check(q.some(l=>l<0),"zero model");
   if(q.length===2&&((q[0]>0)!==(q[1]>0))){let p=q.find(l=>l>0),m=q.find(l=>l<0);G[-m-1].push(p-1)}
  }
  let cl=[],keys=new Set();
  for(let i=0;i<n;i++){let S=bit(i),stack=[i];while(stack.length){for(let j of G[stack.pop()])if(!has(S,j)){S|=bit(j);stack.push(j)}}L.generatorClosures++;
   if(!keys.has(S.toString())){keys.add(S.toString());cl.push(S)}}
  let k=z.R.length,w=null;
  function visit(start,left,S){L.candidates++;let x=b^S;if(valid(x,D,z.R)){check(valid(x,C,R),"original witness");w=x;return true}if(!left)return false;
   for(let j=start;j<cl.length;j++)if(visit(j+1,left-1,S|cl[j]))return true;return false}
  visit(0,k,0n);return {w,k,g:cl.length};
 }
 function ref(n,C,R){let a=0;for(let b=0n;b<(1n<<BigInt(n));b++){L.referenceWords++;if(valid(b,C,R))a++}return a}
 let seed=out.seed>>>0;function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>8)%n}
 for(let t=0;t<160;t++){let n=3+rnd(7),C=[],R=[];for(let j=0;j<rnd(3*n)+2;j++){let a=1+rnd(n),b=1+rnd(n);C.push([rnd(2)?a:-a,rnd(2)?b:-b])}for(let j=0;j<rnd(5);j++){let a=0n;for(let i=0;i<n;i++)if(rnd(2))a|=bit(i);R.push([a,rnd(2)])}let r=ref(n,C,R),s=solve(n,C,R);check((s.w!==null)===(r>0),"random");out.random[r?"sat":"unsat"]++}
 // NAE source: two physical pair observations per owner, spanning-forest fundamental cycles.
 function compile(n,triples,flip=-1){let edges=[],C=[],R=[],forest=Array.from({length:n},()=>[]);
  function path(a,b){let seen=new Set([a]),q=[[a,0n]];for(let j=0;j<q.length;j++){let [v,m]=q[j];if(v===b)return m;for(let [u,e] of forest[v])if(!seen.has(u)){seen.add(u);q.push([u,m^bit(e)])}}return null}
  for(let i=0;i<triples.length;i++){let t=triples[i],c=[];for(let j=1;j<=2;j++){let e=edges.length,a=t[0],b=t[j],p=path(a,b);edges.push([a,b]);if(p===null){forest[a].push([b,e]);forest[b].push([a,e])}else R.push([p^bit(e),0]);let sign=Number(flip===3*i)^Number(flip===3*i+j);c.push(sign?-(e+1):e+1)}C.push(c)}
  function lift(y){let x=0n,seen=new Set();for(let i=0;i<n;i++)if(!seen.has(i)){seen.add(i);let q=[i];for(let j=0;j<q.length;j++){let v=q[j];for(let [u,e] of forest[v])if(!seen.has(u)){seen.add(u);q.push(u);if(has(x,v)^has(y,e))x|=bit(u)}}}
   check(edges.every(([a,b],e)=>(has(x,a)^has(x,b))===has(y,e)),"NAE observation lift");return x}
  return {C,R,n:edges.length,lift};
 }
 function nae(x,T,f){return T.every((t,i)=>{let v=t.map((a,j)=>has(x,a)^Number(f===3*i+j));return v.some(b=>b!==v[0])})}
 let F=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
 for(let f=-1;f<21;f++){let a=compile(7,F,f),s=solve(a.n,a.C,a.R),r=0;for(let x=0n;x<128n;x++){L.referenceWords++;if(nae(x,F,f))r++}check((s.w!==null)===(r>0),"Fano");if(s.w!==null)check(nae(a.lift(s.w),F,f),"Fano lift");out.fano.push({flip:f,models:r,rank:s.k,sat:s.w!==null})}
 for(let m of [3,9,33,129]){let T=Array.from({length:m},(_,i)=>[i,(i+1)%m,i+m]);for(let f of [-1,0]){let a=compile(2*m,T,f),s=solve(a.n,a.C,a.R);check(s.w!==null&&nae(a.lift(s.w),T,f)&&s.k===1,"loose cycle");out.cycles.push({owners:m,flip:f,rank:s.k,sat:true})}}
 for(let n of [8,32,128]){let C=[];for(let i=1;i<n;i++)C.push([-i,i+1],[i,-(i+1)]);for(let b of [0,1]){let R=[[(1n<<BigInt(n))-1n,b]],s=solve(n,C,R);check((s.w!==null)===(b===0),"equality chain");out.chain.push({n,target:b,rank:s.k,sat:s.w!==null})}}
 // Multicolored-clique construction: 3 classes of 3. All pairs across classes
 // compatible except for UNSAT control, where class 0 has no edges to class 1.
 for(let k of [2,3,4])for(let bad of [false,true]){let n=3*k,C=[],R=[];for(let a=0;a<k;a++){let mask=0n;for(let i=0;i<3;i++){mask|=bit(3*a+i);for(let j=i+1;j<3;j++)C.push([-(3*a+i+1),-(3*a+j+1)])}R.push([mask,1])}
 if(bad)for(let i=1;i<=3;i++)for(let j=4;j<=6;j++)C.push([-i,-j]);let s=solve(n,C,R),r=ref(n,C,R);check((s.w!==null)===(r>0)&&Boolean(r)===!bad,"clique");out.clique.push({k,bad,rank:s.k,models:r,sat:s.w!==null})}
 return out;
}
console.log(JSON.stringify(main(),null,2));
