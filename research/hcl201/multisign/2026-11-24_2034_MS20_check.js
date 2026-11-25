function run(){
  const stats={assertions:0,coarseJoins:0,outsideJoins:0,residueJoins:0,cosets:0,closureRows:0,maxLive:0};
  const check=(v)=>{stats.assertions++;if(!v)throw Error("assert "+stats.assertions)};
  const abs=x=>x<0n?-x:x,mod=(x,m)=>(x%m+m)%m;
  function gcd(a,b){a=abs(a);b=abs(b);while(b){[a,b]=[b,a%b]}return a}
  function eg(a,b){let x=1n,y=0n;while(b){let q=a/b;[a,b]=[b,a%b];[x,y]=[y,x-q*y]}return [a,x]}
  function basis(xs){let b=[];for(let x of xs){for(let y of b)if((x^y)<x)x^=y;if(x){b.push(x);b.sort((a,b)=>a>b?-1:a<b?1:0)}}return b}
  function inside(x,b){for(let y of b)if((x^y)<x)x^=y;return x===0n}
  function atom(c,x){return {a:c,g:0n,l:c,u:c,x,b:[],n:1n}}
  function add(a,b){return {a:a.a+b.a,g:gcd(a.g,b.g),l:a.l+b.l,u:a.u+b.u,x:a.x^b.x,b:basis([...a.b,...b.b]),n:a.n*b.n}}
  function union(a,b){if(!a)return b;return {a:a.a,g:gcd(gcd(a.g,b.g),a.a-b.a),l:a.l<b.l?a.l:b.l,u:a.u>b.u?a.u:b.u,x:a.x,b:basis([...a.b,...b.b,a.x^b.x]),n:a.n+b.n}}
  function put(m,k,v){m.set(k,union(m.get(k),v))}
  function coset(a,b,Q,M){let p=gcd(a.g,M),q=gcd(b.g,M),r=mod(a.a,p),s=mod(Q-b.a,q),d=gcd(p,q);if((s-r)%d!==0n)return null;let z=q/d,inv=z===1n?0n:mod(eg(p/d,z)[1],z),l=p*z;return {r:mod(r+p*mod((s-r)/d*inv,z),l),l,K:M/l}}
  function solve(blocks,target,Q,M,cap=100000n){
    let nodes=[],offset=0;
    function tree(l,r){let v={id:nodes.length,l,r,ins:new Map(),out:new Map(),allowed:new Map(),dp:new Map()};nodes.push(v);if(r-l===1){v.options=blocks[l].map(o=>({...o,x:1n<<BigInt(offset++)}));for(let o of v.options)put(v.ins,o.tag,atom(o.c,o.x))}else{let mid=(l+r)>>1;v.L=tree(l,mid);v.R=tree(mid,r);for(let [k,a] of v.L.ins)for(let [j,b] of v.R.ins){stats.coarseJoins++;put(v.ins,k^j,add(a,b))}}return v}
    let root=tree(0,blocks.length),base=root.ins.get(target);
    if(!base)return {kind:"UNSAT",coarse:false,maxK:0n};
    stats.closureRows+=offset-base.b.length; // exact coarse annihilator rank, retained as implied metadata
    if(Q<base.l||Q>base.u)return {kind:"UNSAT",coarse:true,maxK:0n};
    root.out.set(target,atom(0n,0n));
    for(let v of nodes){if(!v.L)continue;for(let [k,a] of v.L.ins)for(let [j,b] of v.R.ins){stats.outsideJoins++;let o=v.out.get(k^j);if(o){put(v.L.out,k,add(o,b));put(v.R.out,j,add(o,a))}}}
    let maxK=0n;
    for(let v of nodes){let K=0n;for(let [k,a] of v.ins){let b=v.out.get(k);if(!b)continue;stats.cosets++;let c=coset(a,b,Q,M);if(c){v.allowed.set(k,c);K+=c.K}}if(K>maxK)maxK=K}
    if(maxK>cap)return {kind:"UNKNOWN",capped:true,maxK};
    const good=(v,k,r)=>{let c=v.allowed.get(k);return c&&mod(r-c.r,c.l)===0n};
    for(let v of [...nodes].reverse()){
      if(v.options){for(let o of v.options){let r=mod(o.c,M);if(good(v,o.tag,r))put(v.dp,o.tag+":"+r,atom(o.c,o.x))}}
      else for(let [k,a] of v.L.dp)for(let [j,b] of v.R.dp){stats.residueJoins++;let [ka,ra]=k.split(":"),[kb,rb]=j.split(":"),t=Number(ka)^Number(kb),r=mod(BigInt(ra)+BigInt(rb),M);if(good(v,t,r))put(v.dp,t+":"+r,add(a,b))}
      stats.maxLive=Math.max(stats.maxLive,v.dp.size);
      let bound=[...v.allowed.values()].reduce((s,c)=>s+c.K,0n);check(BigInt(v.dp.size)<=bound)
    }
    let p=root.dp.get(target+":"+mod(Q,M));
    if(!p)return {kind:"UNSAT",coarse:true,maxK,modEmpty:true};
    stats.closureRows+=base.b.length-p.b.length; // exact modular closure, guard Q retained
    // All new affine identities are implied by retained residue support: no chart change or extra branch.
    let kind=p.l===Q&&p.u===Q?"SAT":Q<p.l||Q>p.u?"UNSAT":"UNKNOWN";
    return {kind,p,base,maxK};
  }
  function reference(bs,target){let arr=[{c:0n,tag:0,x:0n}],off=0;for(let b of bs){let opts=b.map(o=>({...o,x:1n<<BigInt(off++)}));arr=arr.flatMap(a=>opts.map(o=>({c:a.c+o.c,tag:a.tag^o.tag,x:a.x^o.x})))}return arr.filter(a=>a.tag===target)}
  let seed=20261124;function rand(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>8)%n}
  const random={cases:0,sat:0,unsat:0,unknown:0,referenceSAT:0,referenceUNSAT:0,modComparisons:0,witnesses:0};
  function audit(bs,t,Q,M){let all=reference(bs,t),exact=all.filter(a=>a.c===Q),r=solve(bs,t,Q,M),actual=all.filter(a=>mod(a.c-Q,M)===0n);random.cases++;random[exact.length?"referenceSAT":"referenceUNSAT"]++;random[r.kind.toLowerCase()]++;check(r.kind!=="SAT"||exact.length>0);check(r.kind!=="UNSAT"||!exact.length);
    if(r.p){random.modComparisons++;let h=actual.reduce((a,o)=>union(a,atom(o.c,o.x)),undefined);check(!!h&&h.n===r.p.n&&h.l===r.p.l&&h.u===r.p.u);check(h.b.length===r.p.b.length&&h.b.every(x=>inside(x,r.p.b))&&inside(h.x^r.p.x,r.p.b));check(actual.some(a=>a.x===r.p.x&&a.c===r.p.a));if(r.kind==="SAT"){check(exact.some(a=>a.x===r.p.x));random.witnesses++}}
    else if(r.modEmpty){check(actual.length===0);random.modComparisons++}
  }
  for(let i=0;i<120;i++){let n=2+rand(6),bs=Array.from({length:n},()=>Array.from({length:2+rand(2)},()=>({tag:rand(4),c:BigInt(rand(25)-12)})));let t=rand(4),all=reference(bs,t),Q=all.length&&i%3===0?all[rand(all.length)].c:BigInt(rand(65)-32);audit(bs,t,Q,BigInt(2+rand(11)));let d=all.reduce((s,o)=>abs(o.c-Q)>s?abs(o.c-Q):s,0n);audit(bs,t,Q,d+1n)}
  const choices=ws=>ws.map(c=>[{c:0n,tag:0},{c,tag:0}]);
  const prime=x=>{for(let i=2;i*i<=x;i++)if(x%i===0)return false;return x>1};
  const crt=[];for(let n of [4,8,16,32,64]){let ps=[];for(let p=2*n+1;ps.length<n;p++)if(prime(p))ps.push(BigInt(p));let M=ps.reduce((a,b)=>a*b,1n),ws=ps.map(p=>M/p),Q=ws.reduce((a,w,i)=>a+(i%2===0?w:0n),0n),U=ws.reduce((a,w)=>a+w,0n),bad=Q+2n*ws[n-1];check(U<M&&bad<=U&&bad>Q);let a=solve(choices(ws),0,Q,M),b=solve(choices(ws),0,bad,M);check(a.kind==="SAT"&&a.p.n===1n&&a.maxK===1n);check(b.kind==="UNSAT"&&b.maxK===1n);let witness=ws.reduce((s,w,i)=>s+(i%2===0?w:0n),0n);check(witness===a.p.a);for(let i=0;i<n;i++)check(((a.p.x>>BigInt(2*i+(i%2===0?1:0)))&1n)===1n);crt.push({n,modulusBits:M.toString(2).length,budgetBits:(Q<U-Q?Q:U-Q).toString(2).length,maxK:a.maxK.toString(),satCount:a.p.n.toString(),sat:a.kind,neighbor:b.kind})}
  const holes=[];for(let n of [4,8,16,32,64]){let W=14n*(1n<<BigInt(4*n)),bs=choices([3n,5n,7n,9n,...Array(n).fill(W)]),Q=W*BigInt(n/2)+11n,a=solve(bs,0,Q,7n),b=solve(bs,0,Q+1n,7n);check(a.kind==="UNSAT"&&a.modEmpty);check(b.kind!=="UNSAT"&&!!b.p);holes.push({n,weightBits:W.toString(2).length,modulus:7,maxK:a.maxK.toString(),hole:a.kind,neighbor:b.kind,neighborModCount:b.p.n.toString()})}
  let weak=solve(choices([2n,6n]),0,4n,2n);check(weak.kind==="UNKNOWN");
  let capped=solve(choices([1n,1n,1n,1n]),0,2n,1000000007n,10n);check(capped.kind==="UNKNOWN"&&capped.capped);
  return {seed:20261124,random,crt,holes,controls:{weakModulus:weak.kind,capped:capped.kind},stats};
}
console.log(JSON.stringify(run(),null,2));
