function coreAudit(){
  let state=9007;const rnd=()=>((state=(Math.imul(state,1664525)+1013904223)>>>0)/4294967296);
  let counts={graphs:0,ideals:0,fibers:0,targets:0,globalPeriods:0,guardedNotGlobal:0,neutralRequired:0};
  const parity=(mask,l)=>{let s=0;for(let u=0;u<l.length;u++)if(mask>>u&1)s^=l[u];return s};
  for(let trial=0;trial<200;trial++){
    const n=1+Math.floor(rnd()*7),l=Array.from({length:n},()=>Math.floor(rnd()*4)),R=Array.from({length:n},()=>Array(n).fill(false));
    for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)R[i][j]=rnd()<0.3;
    for(let k=0;k<n;k++)for(let i=0;i<n;i++)for(let j=0;j<n;j++)R[i][j] ||= R[i][k]&&R[k][j];
    const valid=a=>R.every((row,i)=>row.every((r,j)=>!r||!(a>>i&1)||(a>>j&1))), A=Array.from({length:1<<n},(_,i)=>i).filter(valid),support=new Set(A.map(a=>parity(a,l)));
    counts.graphs++;counts.ideals+=A.length;
    for(const p of [...new Set(l)].filter(x=>x)){
      const U=l.reduce((m,x,i)=>m|((x!==0&&x!==p?1:0)<<i),0), J=[...new Set(A.map(a=>a&U))];let universal=true,allBad=Array(4).fill(false),neutralRequired=false;
      for(const j of J){
        const fiber=A.filter(a=>(a&U)===j),vals=new Set(fiber.map(a=>parity(a,l)));
        let low=j,high=(1<<n)-1;
        for(let g=0;g<n;g++)for(let u=0;u<n;u++)if(U>>u&1){
          if((j>>u&1)&&(u===g||R[u][g]))low|=1<<g;
          if(!(j>>u&1)&&(u===g||R[g][u]))high&=~(1<<g);
        }
        if(!fiber.includes(low)||!fiber.includes(high)||fiber.some(a=>(a&low)!==low||(a&high)!==a))throw Error("interval");
        const free=l.some((x,g)=>x===p&&((low^high)>>g&1));
        const frozen=l.every((x,g)=>x!==p||l.some((_,u)=>(U>>u&1)&&(((j>>u&1)&&R[u][g])||(!(j>>u&1)&&R[g][u]))));
        if(free===frozen||vals.size!==(free?2:1))throw Error("frozen formula");
        universal&&=free;counts.fibers++;
        for(let t=0;t<4;t++){
          const red=x=>Math.min(x,x^p),bad=red(parity(low,l))===red(t)&&frozen&&parity(low,l)!==t;
          const truth=[...vals].some(v=>red(v)===red(t))&&!vals.has(t);
          if(bad!==truth)throw Error("bad fiber");
          allBad[t] ||= bad;counts.targets++;
        }
        if(free)for(const a of fiber){
          let b=a, moves=0;const g=l.findIndex((x,i)=>x===p&&((low^high)>>i&1));
          if(!(a>>g&1)){
            for(let u=n-1;u>=0;u--)if((high>>u&1)&&!(b>>u&1)){
              b|=1<<u;moves++;if(!valid(b))throw Error("up move");
              if(l[u]===p)break;
            }
          }else{
            for(let u=0;u<n;u++)if((b>>u&1)&&!(low>>u&1)){
              b&=~(1<<u);moves++;if(!valid(b))throw Error("down move");
              if(l[u]===p)break;
            }
          }
          if((b&U)!==j||(parity(a,l)^parity(b,l))!==p)throw Error("lift");
          neutralRequired ||= moves>1;
        }
      }
      if(universal){if([...support].some(v=>!support.has(v^p)))throw Error("global period");counts.globalPeriods++;}
      if(!universal&&allBad.some(x=>!x))counts.guardedNotGlobal++;
      if(neutralRequired)counts.neutralRequired++;
    }
  }
  const fixtures={neutral:"002 011 020 101 102 112 212 220",MF01:"000 001 012 020 110 120 122 200 201 210 211",U:"000 002 010 011 021 022 100 101 111 201 202 221",V:"000 002 010 011 021 022 100 101 111 201 202 221 110"};
  const source={};
  for(const [name,s] of Object.entries(fixtures)){
    const T=s.split(" ").map(x=>[...x].map(Number)),M=[];
    for(const a of T.filter(t=>t[0]===0))for(const b of T.filter(t=>t[0]===1))for(const c of T.filter(t=>t[0]===2)){
      if(new Set([a[1],b[1],c[1]]).size===3)M.push((1<<a[2])^(1<<b[2])^(1<<c[2]));
    }
    source[name]={triples:T.length,matchings:M.length,support:[...new Set(M)].sort((a,b)=>a-b),sat:M.includes(7)};
  }
  if(source.U.sat||!source.V.sat||!source.neutral.sat||!source.MF01.sat)throw Error("source");
  return {seed:9007,counts,source};
}
console.log(JSON.stringify(coreAudit(), null, 2));
