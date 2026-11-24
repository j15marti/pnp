function experiment(){
  const mod=(x,m)=>((x%m)+m)%m;
  const gcd=(a,b)=>{a=Math.abs(a);b=Math.abs(b);while(b){[a,b]=[b,a%b]}return a};
  function eg(a,b){if(b===0)return [Math.abs(a),a<0?-1:1,0];const [g,s,t]=eg(b,a%b);return [g,t,s-Math.trunc(a/b)*t]}
  const dot=(a,b)=>a.reduce((s,v,i)=>s+v*b[i],0);
  const add=(a,b)=>a.map((v,i)=>v+b[i]);
  const bal=(n,E,x)=>{let b=Array(n).fill(0);E.forEach(([s,t],i)=>{b[s]-=x[i];b[t]+=x[i]});return b};
  const equal=(a,b)=>a.every((v,i)=>v===b[i]);
  let stats={flowCalls:0,augmentations:0,bases:0,thresholdTests:0,layers:0,lifts:0,referenceTuples:0};
  function feasible(n,E,b,lo,hi){
    stats.flowCalls++;if(lo.some((v,i)=>v>hi[i]))return null;
    let need=b.map((v,i)=>v-bal(n,E,lo)[i]),A=Array.from({length:n+2},()=>[]),S=n,T=n+1;
    function edge(s,t,c){let a={v:t,c,rev:A[t].length},r={v:s,c:0,rev:A[s].length};if(s===t)a.rev++;A[s].push(a);A[t].push(r);return a}
    let es=E.map(([s,t],i)=>edge(s,t,hi[i]-lo[i]));let total=0;
    need.forEach((v,i)=>{if(v<0){edge(S,i,-v);total-=v}else if(v>0)edge(i,T,v)});
    while(total>0){let p=Array(n+2).fill(null),q=[S];p[S]=[-1,-1];for(let k=0;k<q.length&&p[T]===null;k++){let v=q[k];A[v].forEach((e,j)=>{if(e.c>0&&p[e.v]===null){p[e.v]=[v,j];q.push(e.v)}})}if(p[T]===null)return null;let d=total;for(let v=T;v!==S;){let [u,j]=p[v];d=Math.min(d,A[u][j].c);v=u}for(let v=T;v!==S;){let [u,j]=p[v],e=A[u][j];e.c-=d;A[v][e.rev].c+=d;v=u}total-=d;stats.augmentations++}
    return es.map((e,i)=>hi[i]-e.c);
  }
  function basis(n,E,ids){
    stats.bases++;let P=Array.from({length:n},(_,i)=>i),adj=Array.from({length:n},()=>[]),C=[];
    function root(i){while(P[i]!==i)i=P[i];return i}
    for(let i of ids){let [s,t]=E[i];if(root(s)!==root(t)){P[root(s)]=root(t);adj[s].push([t,i,1]);adj[t].push([s,i,-1]);continue}
      let c=Array(E.length).fill(0);c[i]=1;let p=Array(n).fill(null),q=[t];p[t]=[-1,-1,0];for(let k=0;k<q.length&&p[s]===null;k++){let v=q[k];for(let [w,j,sgn] of adj[v])if(p[w]===null){p[w]=[v,j,sgn];q.push(w)}}
      for(let v=s;v!==t;){let [u,j,sgn]=p[v];c[j]=sgn;v=u}C.push(c)
    }return C;
  }
  function certify(n,E,u,f,g,M){
    const b=bal(n,E,f),zero=u.map(()=>0);
    const variable=u.map((_,i)=>{let hi=u.slice(),lo=zero.slice();hi[i]=f[i]-1;lo[i]=f[i]+1;return feasible(n,E,b,zero,hi)!==null||feasible(n,E,b,lo,u)!==null});
    let ids=variable.flatMap((v,i)=>v?[i]:[]),full=basis(n,E,ids),H=full.reduce((d,c)=>gcd(d,dot(c,g)),M);
    let r=u.map((v,i)=>variable[i]?Math.min(f[i],v-f[i]):0),W=M,Ls=[];
    while(W!==H){let accepted=false;let thresholds=[...new Set(r.filter(v=>v>0))].sort((a,b)=>b-a);
      for(let t of thresholds){stats.thresholdTests++;let C=basis(n,E,ids.filter(i=>r[i]>=t)),h=C.map(c=>mod(dot(c,g),W)),D=h.reduce(gcd,W),L=W/D;if(L===1||L-1>t)continue;
        let used=new Set();C.forEach(c=>c.forEach((v,i)=>{if(v)used.add(i)}));used.forEach(i=>r[i]-=L-1);
        Ls.push({C,h,old:W,new:D,L,used:[...used]});W=D;stats.layers++;accepted=true;break;
      }if(!accepted)break;
    }
    function lift(target){
      let diff=mod(target-dot(f,g),M);if(diff%W!==0)return null;let x=f.slice();
      for(let j=Ls.length-1;j>=0;j--){let {C,h,old,L}=Ls[j],a=[],d=old;
        for(let v of h){let [dd,s,t]=eg(d,v);a=a.map(c=>c*s);a.push(t);d=dd}
        if(diff%d!==0)throw Error("preimage");let k=mod(diff/d,old/d);let z=Array(E.length).fill(0);C.forEach((c,i)=>c.forEach((v,e)=>z[e]+=mod(a[i]*k,L)*v));
        let lo=z.map(v=>Math.floor(v/L)),hi=z.map(v=>Math.ceil(v/L)),q=feasible(n,E,Array(n).fill(0),lo,hi);if(q===null)throw Error("rounding");
        let delta=z.map((v,i)=>v-L*q[i]);if(delta.some(v=>Math.abs(v)>L-1))throw Error("margin");
        x=add(x,delta);diff=mod(diff-dot(delta,g),M);if(diff%old!==0)throw Error("quotient");stats.lifts++;
      }
      if(diff!==0||!equal(bal(n,E,x),b)||x.some((v,i)=>v<0||v>u[i])||mod(dot(x,g),M)!==mod(target,M))throw Error("bad lift");return x
    }
    return {H,W,Ls,variable,lift,baseline:mod(dot(f,g),M)};
  }
  function reference(n,E,u,f,g,M){let b=bal(n,E,f),support=new Set(),x=u.map(()=>0);function rec(i){if(i===u.length){stats.referenceTuples++;if(equal(bal(n,E,x),b))support.add(mod(dot(x,g),M));return}for(let v=0;v<=u[i];v++){x[i]=v;rec(i+1)}}rec(0);return support}
  let seed=20261124;function rnd(n){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return (seed>>>0)%n}
  let out={seed:20261124,random:0,targets:0,sat:0,unsat:0,unknown:0,exactNetworks:0,nontrivialLayers:0,multipleLayers:0,referenceSat:0,referenceUnsat:0,wrong:0,structured:[]};
  for(let t=0;t<200;t++){let n=2+rnd(3),m=2+rnd(5),M=[4,6,8,12,15][rnd(5)],E=Array.from({length:m},()=>[rnd(n),rnd(n)]),u=E.map(()=>rnd(6)),f=u.map(v=>rnd(v+1)),g=E.map(()=>rnd(M));let c=certify(n,E,u,f,g,M),R=reference(n,E,u,f,g,M);out.random++;if(c.W===c.H)out.exactNetworks++;if(c.Ls.length)out.nontrivialLayers++;if(c.Ls.length>1)out.multipleLayers++;
    for(let x=0;x<M;x++){out.targets++;let actual=R.has(x),delta=mod(x-c.baseline,M);if(actual)out.referenceSat++;else out.referenceUnsat++;if(delta%c.W===0){if(!actual||!c.lift(x))throw Error("false SAT");out.sat++}else if(delta%c.H!==0){if(actual)throw Error("false UNSAT");out.unsat++}else out.unknown++}
  }
  for(let h of [1,2,4,8,16,32,64]){
    // All arcs parallel; common reserve edge, h order-3 edges and h order-2 edges,
    // and a thin variable arc with an even tag. Mod 12: attainable subgroup 2Z.
    let E=Array.from({length:2*h+2},()=>[0,1]),f=[3,...Array(h).fill(2),...Array(h).fill(1),0],u=[6,...Array(h).fill(4),...Array(h).fill(2),1],g=[0,...Array(h).fill(4),...Array(h).fill(6),2];
    let c=certify(2,E,u,f,g,12);if(c.H!==2||c.W!==2||c.Ls.length!==2||!c.variable.at(-1))throw Error("structured");
    let sat=0,unsat=0;for(let x=0;x<12;x++){if(x%2===0){if(!c.lift(x))throw Error("missing");sat++}else{if(mod(x-c.baseline,12)%c.H===0)throw Error("bad bound");unsat++}}
    out.structured.push({h,arcs:E.length,cycleRank:E.length-1,layerExponents:c.Ls.map(z=>z.L),sat,unsat,fullUniformMargin:5,commonEdgeMargin:3,chosenFundamentalCenteredMargin:2*h+3,thinArcVariable:true});
  }
  // False converse: capacity-one owner choice, group 5, support {0,1,2}, lattice full.
  {let E=[[0,1],[0,1],[0,1]],u=[1,1,1],f=[1,0,0],g=[0,1,2],c=certify(2,E,u,f,g,5),R=reference(2,E,u,f,g,5);if(c.W!==5||c.H!==1||R.has(3)||!R.has(2))throw Error("thin");out.thin={W:c.W,H:c.H,actual:[...R].sort(),unknownTargets:[1,2,3,4]}}
  return {...out,...stats};
}
console.log(JSON.stringify(experiment(), null, 2));
