function runM09(){
  const seed=9102026;let state=seed;
  const rng=n=>{state=(Math.imul(1664525,state)+1013904223)>>>0;return Math.floor(state/4294967296*n)};
  let flowCalls=0,bruteTuples=0;
  function check(v,E,b,x){if(x.length!==E.length)return false;let a=Array(v).fill(0);for(let i=0;i<E.length;i++){let e=E[i];if(!Number.isInteger(x[i])||x[i]<(e.l??0)||x[i]>e.u)return false;a[e.s]-=x[i];a[e.t]+=x[i]}return a.every((z,i)=>z===b[i])}
  function flow(v,E,b,margin=0,override=null){
    flowCalls++;let d=b.slice(),G=Array.from({length:v+2},()=>[]),src=v,sink=v+1, refs=[];
    function add(s,t,c){let a={t,c,rev:G[t].length},r={t:s,c:0,rev:G[s].length};G[s].push(a);G[t].push(r);return a}
    for(let i=0;i<E.length;i++){let e=E[i],l=Math.max(e.l??0,margin),u=e.u-margin;if(override&&override.i===i){l=Math.max(l,override.l??l);u=Math.min(u,override.u??u)}if(l>u)return null;d[e.s]+=l;d[e.t]-=l;refs.push([add(e.s,e.t,u-l),u-l,l])}
    if(d.reduce((a,b)=>a+b,0)!==0)return null;let need=0;
    for(let i=0;i<v;i++){if(d[i]<0){add(src,i,-d[i]);need-=d[i]}if(d[i]>0)add(i,sink,d[i])}
    while(need){let p=Array(v+2).fill(null),Q=[src];p[src]=[-1,-1];for(let j=0;j<Q.length&&p[sink]===null;j++){let s=Q[j];for(let k=0;k<G[s].length;k++){let a=G[s][k];if(a.c>0&&p[a.t]===null){p[a.t]=[s,k];Q.push(a.t)}}}if(!p[sink])return null;let delta=need;for(let t=sink;t!==src;){let [s,k]=p[t];delta=Math.min(delta,G[s][k].c);t=s}for(let t=sink;t!==src;){let [s,k]=p[t],a=G[s][k];a.c-=delta;G[t][a.rev].c+=delta;t=s}need-=delta}
    let x=refs.map(([a,c,l])=>l+c-a.c);if(!check(v,E,b,x))throw Error("bad flow");return x
  }
  function enumerate(E,visit){let x=Array(E.length).fill(0);function rec(i){if(i===E.length){bruteTuples++;visit(x.slice());return}for(x[i]=E[i].l??0;x[i]<=E[i].u;x[i]++)rec(i+1)}rec(0)}
  function demand(b,E,x){let d=b.slice();E.forEach((e,i)=>{d[e.s]+=x[i];d[e.t]-=x[i]});return d}
  function tag(E,x){return E.reduce((a,e,i)=>a^((x[i]%2)?e.g:0n),0n)}
  function eq(a,b){return a.length===b.length&&a.every((z,i)=>z===b[i])}
  function closure(v,E,b){
    let f=flow(v,E,b);if(!f)return null;
    let fixed=[];for(let i=0;i<E.length;i++)if(!flow(v,E,b,0,{i,u:f[i]-1})&&!flow(v,E,b,0,{i,l:f[i]+1}))fixed.push(i);
    // Fixed values are retained as equal bounds; rerun budget feasibility after the batch.
    let F=E.map((e,i)=>fixed.includes(i)?{...e,l:f[i],u:f[i]}:e);
    if(!flow(v,F,b))throw Error("closure invalid");
    return {F,f,fixed};
  }
  function cycleBasis(v,H){
    let par=Array.from({length:v},(_,i)=>i),root=i=>{while(par[i]!==i)i=par[i];return i},tree=Array.from({length:v},()=>[]),ch=[];
    H.forEach((e,i)=>{let a=root(e.s),b=root(e.t);if(a===b)ch.push(i);else{par[a]=b;tree[e.s].push([e.t,i]);tree[e.t].push([e.s,i])}});
    let rows=new Map(),rank=0;
    function insert(g,mask){while(g){let k=g.toString(2).length-1;if(!rows.has(k)){rows.set(k,[g,mask]);rank++;return}let [v,m]=rows.get(k);g^=v;mask^=m}}
    ch.forEach(i=>{let e=H[i],mask=1n<<BigInt(i),P=Array(v).fill(null),Q=[e.s];P[e.s]=[-1,-1];for(let j=0;j<Q.length;j++)for(let [t,k] of tree[Q[j]])if(P[t]===null){P[t]=[Q[j],k];Q.push(t)}for(let t=e.t;t!==e.s;){let [s,k]=P[t];mask^=1n<<BigInt(k);t=s}let g=0n;H.forEach((e,k)=>{if((mask>>BigInt(k))&1n)g^=e.g});insert(g,mask)});
    function solve(g){let mask=0n;while(g){let k=g.toString(2).length-1;if(!rows.has(k))return null;let [v,m]=rows.get(k);g^=v;mask^=m}return mask}
    return {rank,solve};
  }
  function orient(v,H,mask){
    let adj=Array.from({length:v},()=>[]),used=Array(H.length).fill(false),d=Array(H.length).fill(0);
    H.forEach((e,i)=>{if((mask>>BigInt(i))&1n){adj[e.s].push([e.t,i,1]);adj[e.t].push([e.s,i,-1])}});
    for(let start=0;start<v;start++){let s=start;while(true){let a=adj[s].pop();while(a&&used[a[1]])a=adj[s].pop();if(!a){if(s!==start)throw Error("non-Euler");break}let [t,i,sign]=a;used[i]=true;d[i]=sign;s=t}}
    return d
  }
  function lift(v,H,b,f,B,target){let mask=B.solve(target^tag(H,f));if(mask===null)return null;let d=orient(v,H,mask),x=f.map((z,i)=>z+d[i]);if(!check(v,H,b,x)||tag(H,x)!==target)throw Error("bad lift");return x}
  let R={seed,random:0,infeasible:0,fixedSkipped:0,fixedArcs:0,rankOneCases:0,accepted:0,declined:0,endpointDisagreements:0,fibers:0,targetChecks:0,sat:0,unsat:0,lifts:0,disagreements:0,scaling:[],hostile:null};
  for(let j=0;j<180;j++){
    R.random++;let v=4,H=[{s:0,t:1},{s:1,t:2}];for(let a=0;a<2;a++){let s=rng(3),t=(s+1+rng(2))%3;H.push({s,t})}
    H=H.map(e=>({...e,u:2+rng(3),g:BigInt(rng(16))}));
    let K=[{s:0,t:2},{s:0,t:3},{s:2,t:3}].map(e=>({...e,u:1+rng(2),g:BigInt(rng(16))}));
    let E=H.concat(K),b=demand([0,0,0,0],E,E.map(e=>rng(e.u+1))).map(x=>-x);
    if(j%9===0){b[0]-=4;b[3]+=4}
    let C=closure(v,E,b);if(!C){R.infeasible++;continue}R.fixedArcs+=C.fixed.length;
    if(C.fixed.some(i=>i<H.length)){R.fixedSkipped++;continue}
    K=C.F.slice(H.length); // keep quotient pins established by closure
    let Y=[];enumerate(K,y=>{let d=demand(b,K,y);if(d[3]===0&&d[0]+d[1]+d[2]===0)Y.push({y,d})});if(!Y.length)throw Error("empty quotient");
    let lo=Y.reduce((a,b)=>a.d[0]<b.d[0]?a:b),hi=Y.reduce((a,b)=>a.d[0]>b.d[0]?a:b);
    if(!Y.every(z=>z.d[1]===lo.d[1]))throw Error("rank not <=1");
    R.rankOneCases++;
    let accepted=!!flow(v,H,lo.d,1)&&!!flow(v,H,hi.d,1);
    let all=Y.every(z=>!!flow(v,H,z.d,1));
    if(accepted!==all){R.endpointDisagreements++;throw Error("endpoint failure")}
    if(!accepted){R.declined++;continue}R.accepted++;
    let B=cycleBasis(v,H); // high bit is a protected additional parity probe
    for(let z of Y){
      R.fibers++;let f=flow(v,H,z.d,1),S=new Set();enumerate(H,x=>{if(check(v,H,z.d,x))S.add((tag(H,x)^tag(K,z.y)).toString())});
      for(let t=0;t<16;t++){R.targetChecks++;let target=BigInt(t),x=lift(v,H,z.d,f,B,target^tag(K,z.y)),truth=S.has(String(t));if(!!x!==truth){R.disagreements++;throw Error("fiber error")}if(x){R.sat++;R.lifts++;if(!check(v,E,b,x.concat(z.y))||tag(E,x.concat(z.y))!==target)throw Error("source check")}else R.unsat++}
    }
  }
  // Midpoint at one boundary is insufficient, S08 hostile case. Pinning an absorbed arc is also unsafe.
  let H0=[{s:0,t:1,u:2,g:1n},{s:0,t:1,u:2,g:2n}],d0=[-2,2],d1=[0,0],B0=cycleBasis(2,H0);
  let initial=flow(2,H0,d0,1),end=flow(2,H0,d1,1);
  if(!initial||end||!lift(2,H0,d0,initial,B0,0n)||flow(2,H0,d0,0,{i:0,l:1,u:1})===null)throw Error("hostile setup");
  let pinned=new Set();enumerate(H0.map((e,i)=>i===0?{...e,l:1,u:1}:e),x=>{if(check(2,H0,d0,x))pinned.add(tag(H0,x).toString())});
  if(pinned.has("0")||!pinned.has("3"))throw Error("pin counterexample");
  R.hostile={oneFiberInterior:true,endpointInterior:false,pinnedSupport:[...pinned]};
  for(let h of [4,8,16,32,64,128]){
    let H=Array.from({length:h},(_,i)=>({s:0,t:1,u:4,g:i?1n<<BigInt(i-1):0n})),r=h-1;
    let K=[{s:0,t:1,u:h-1,g:0n},{s:0,t:2,u:1,g:0n},{s:0,t:2,u:1,g:1n<<BigInt(r)},{s:1,t:2,u:1,g:1n<<BigInt(r+1)}],b=[-2*h-1,2*h,1],E=H.concat(K);
    let C=closure(3,E,b);if(!C||C.fixed.length)throw Error("scale fixed");
    let dlo=demand(b,K,[h-1,1,0,0]),dhi=demand(b,K,[0,0,0,1]);
    if(!flow(3,H,dlo,1)||!flow(3,H,dhi,1))throw Error("scale endpoints");
    let B=cycleBasis(3,H),sat=0,unsat=0,checks=0;
    // Every category tested at both loop extrema; cycle targets all-zero, all-one, alternating.
    for(let y0 of [0,h-1])for(let cat=0;cat<3;cat++){let y=[y0,0,0,0];y[cat+1]=1;let d=demand(b,K,y),f=flow(3,H,d,1);
      for(let mask of [0n,(1n<<BigInt(r))-1n,((1n<<BigInt(r))-1n)/3n]){
        let target=mask^tag(K,y),x=lift(3,H,d,f,B,mask);checks++;if(!x||!check(3,E,b,x.concat(y))||tag(E,x.concat(y))!==target)throw Error("scale SAT");sat++;
        let wrong=mask^(3n<<BigInt(r));checks++;if(lift(3,H,d,f,B,wrong^tag(K,y))!==null)throw Error("scale UNSAT");unsat++;
      }
    }
    R.scaling.push({h,arcs:E.length,originalBeta:E.length-2,quotientBeta:3,rank:B.rank,treeCorrectionWidth:h,treeAvailableWidth:2,sat,unsat,checks});
  }
  R.flowCalls=flowCalls;R.bruteTuples=bruteTuples;return R
}
console.log(JSON.stringify(runM09(),null,2));
