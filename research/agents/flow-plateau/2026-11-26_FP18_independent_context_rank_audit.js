'use strict';
// FP18 independent direct path and raw-flow audit. No project dependencies.
function fp18Audit() {
  const edge=(u,v)=>[u,v], key=(u,v)=>Math.min(u,v)+","+Math.max(u,v);
  function region(k){
    const W=[];for(let i=0;i<k;i++)W.push(edge(4*i+2,4*(k+i)+1));
    for(let i=0;i<k-1;i++)W.push(edge(4*(k+i)+2,4*(k+i+1)+3));
    const used=new Set(W.flat()),B=Array.from({length:8*k},(_,i)=>i).filter(i=>!used.has(i));
    if(B.length!==4*k+2)throw Error("port count");return {W,B};
  }
  function pairing(k,W,x){
    const nbr=Array.from({length:8*k},()=>[]);
    function link(u,v){nbr[u].push(v);nbr[v].push(u)}
    for(const [u,v] of W)link(u,v);
    for(let j=0;j<2*k;j++){const a=4*j,b=(x>>j)&1;link(a,a+(b?3:1));link(a+2,a+(b?1:3))}
    return nbr;
  }
  function trace(k,W,x,y){
    const nbr=pairing(k,W,x);
    for(let i=0;i<k-1;i++){const u=4*i+((y>>i)&1?3:1),v=4*(i+1);nbr[u].push(v);nbr[v].push(u)}
    let u=0,prev=-1,steps=0;
    while(true){
      if(u===4*(k-1)+1)return true;
      const v=nbr[u].find(v=>v!==prev);
      if(v===undefined)return false;
      prev=u;u=v;if(++steps>8*k)throw Error("path loop");
    }
  }
  let entries=0,allPhases=0;
  for(let k=1;k<=10;k++){const {W}=region(k),m=2**(k-1);for(let x=0;x<m;x++)for(let y=0;y<m;y++){if(trace(k,W,x,y)!==(x===y))throw Error("identity");entries++}}
  for(let k=1;k<=5;k++){const {W}=region(k);for(let x=0;x<2**(2*k);x++)for(let y=0;y<2**(k-1);y++){if(trace(k,W,x,y)!==((x&((1<<k)-1))===y))throw Error("forced test bits");allPhases++}}
  let sources=0,sourceWords=0;
  for(const k of [1,2,4,8,16,32,64]){
    const {W,B}=region(k),L=8*k,s=2*L,t=s+1,edges=[];
    for(let j=0;j<4*k;j++)for(let i=0;i<4;i++)edges.push([4*j+i,4*j+(i+1)%4,"a",j,i]);
    for(const [u,v] of W){edges.push([u,v,"w"]);edges.push([u+L,v+L,"w"])}
    const removed=B.filter(v=>v>=4*k).slice(-2);
    for(const v of B)if(!removed.includes(v))edges.push([v,v+L,"w"]);else for(const u of [v,v+L])edges.push([u,((u%2)^Number(u>=L))?s:t,"w"]);
    edges.push([s,t,"z"]);
    const deg=new Int32Array(t+1),unique=new Set(),adj=Array.from({length:t+1},()=>[]);
    const parity=u=>u===s?0:u===t?1:(u%2)^Number(u>=L);
    for(const [u,v] of edges){if(u===v||unique.has(key(u,v))||parity(u)===parity(v))throw Error("source structure");unique.add(key(u,v));deg[u]++;deg[v]++;adj[u].push(v);adj[v].push(u)}
    if(deg.some(d=>d!==3))throw Error("cubic");
    const seen=new Set([0]),stack=[0];while(stack.length){for(const v of adj[stack.pop()])if(!seen.has(v)){seen.add(v);stack.push(v)}}
    if(seen.size!==t+1)throw Error("disconnected");sources++;
    for(let w=0;w<16;w++){
      const xorA=new Int32Array(t+1),xorB=new Int32Array(t+1),bAdj=Array.from({length:t+1},()=>[]);
      let zeros=0;
      for(const [u,v,typ,j,i] of edges){const a=Number(typ==="a"),b=Number(typ==="w"||(typ==="a"&&i%2===((j*17+w*13+Math.floor(j/7))%2)));
        xorA[u]^=a;xorA[v]^=a;xorB[u]^=b;xorB[v]^=b;if(!a&&!b)zeros++;if(b){bAdj[u].push(v);bAdj[v].push(u)}}
      if(zeros!==1||xorA.some(x=>x)||xorB.some(x=>x)||bAdj.some(x=>x.length!==2))throw Error("flow");
      const seenB=new Set();for(let u=0;u<=t;u++)if(!seenB.has(u)){let p=-1,v=u,len=0;do{seenB.add(v);const q=bAdj[v].find(q=>q!==p);p=v;v=q;len++}while(v!==u);if(len%2)throw Error("odd factor")}
      sourceWords++;
    }
  }
  const E=[[0,2],[0,6],[0,9],[1,3],[1,7],[1,10],[2,10],[2,11],[3,8],[3,11],[4,5],[4,9],[4,11],[5,6],[5,10],[6,7],[7,8],[8,9]];
  function flows(n,E){const f=[];for(let x=0;x<2**E.length;x++){let odd=0;for(let i=0;i<E.length;i++)if(x>>i&1)odd^=(1<<E[i][0])^(1<<E[i][1]);if(!odd)f.push(x)}return f}
  const F=flows(12,E),full=(1<<18)-1,protect=full^(1<<5),states=[];
  for(const a of F)for(const b of F)if(((a|b)&protect)===protect)states.push([a,b]);
  const start=states.findIndex(([a,b])=>a===110469&&b===185822);if(start<0)throw Error("start");
  const reached=new Set([start]),q=[start];while(q.length){const [a,b]=states[q.pop()];const d=new Set([a,b,a^b]);for(let i=0;i<states.length;i++){const [c,e]=states[i];if(!reached.has(i)&&[c,e,c^e].some(x=>d.has(x))){reached.add(i);q.push(i)}}}
  if(F.length!==128||states.length!==30||reached.size!==18||[...reached].some(i=>(states[i][0]|states[i][1])===full))throw Error("core trap");
  if(!F.includes(96734)||!F.includes(178037)||(96734|178037)!==full)throw Error("core witness");
  const Q=[[2,3],[2,7],[3,4],[3,8],[4,9],[5,7],[5,8],[6,8],[6,9],[7,9]],ports=[4,5,2,6],Qwords=new Set();
  for(let x=0;x<3**10;x++){let y=x;const sums=new Int32Array(10);for(const [u,v] of Q){const c=y%3+1;y=Math.floor(y/3);sums[u]^=c;sums[v]^=c}if([3,7,8,9].every(v=>!sums[v])&&ports.every(v=>sums[v]))Qwords.add(ports.map(v=>sums[v]).join(""))}
  if(Qwords.size!==9||[...Qwords].some(w=>w[0]!==w[1]||w[2]!==w[3]))throw Error("four-pole");
  const P=[];for(let i=0;i<5;i++){P.push([i,(i+1)%5],[i+5,5+(i+2)%5],[i,i+5])}
  const PF=flows(10,P),pfull=(1<<15)-1;let pn=0,pp=0;for(const a of PF)for(const b of PF){const z=pfull^(a|b);if(z===0)pp++;if(z!==0&&(z&(z-1))===0)pn++}
  if(pp!==0||pn!==270)throw Error("Petersen");
  return {identityEntries:entries,allPhaseContextChecks:allPhases,sourceGraphs:sources,sourcePhaseWords:sourceWords,coreFlows:F.length,protectedStates:states.length,reached:reached.size,properReached:0,fourPoleWords:Qwords.size,petersenFlows:PF.length,petersenOneDefect:pn,petersenProper:pp};
}
console.log(JSON.stringify(fp18Audit(),null,2));
