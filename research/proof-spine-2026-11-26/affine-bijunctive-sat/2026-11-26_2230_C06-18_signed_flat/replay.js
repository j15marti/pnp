// Independent coordinate-pin replay of C06-18. Same generated charts and guard; no native compiler in this replay.
function replay(){
  const cases=[];
  for(const k of [2,3,4,6,8,12,16,32,64]){
    const n=2*k, chains=[]; let d=n, checks=0;
    for(const rev of [false,true])for(const off of [0,k]){
      const xs=Array.from({length:k},(_,j)=>off+j);if(rev)xs.reverse();
      let p=xs[0]; const gs=[];
      for(const x of xs.slice(1)){
        const z=d++;gs.push([p,x,z]);p=z;
        for(let a=0;a<2;a++)for(let b=0;b<2;b++)for(let c=0;c<2;c++){
          const raw=!(c===1&&a===0)&&!(a===1&&(b^c)===1);
          const compact=Number(c===0)+Number(a===1&&b===1&&c===1)-Number(a===1&&b===1&&c===0);
          if(Number(raw)!==compact||compact!==Number(c===a*b))throw Error("gate");
          checks++;
        }
      }
      chains.push({xs,p,gs});
    }
    const terms=chains.map(({xs,p})=>[
      {c:1n,pins:[[p,0]]},
      {c:1n,pins:[[p,1],...xs.map(i=>[i,1])]},
      {c:-1n,pins:[[p,0],...xs.map(i=>[i,1])]}
    ]);
    const endpoints=chains.map(c=>c.p);
    const live=n+4;
    let count=0n, control=0n, combinations=0,consistent=0;
    for(const a of terms[0])for(const b of terms[1])for(const c of terms[2])for(const e of terms[3]){
      combinations++;const map=new Map();let ok=true;
      for(const [i,v] of [...a.pins,...b.pins,...c.pins,...e.pins]){
        if(map.has(i)&&map.get(i)!==v){ok=false;break} map.set(i,v);
      }
      if(!ok)continue;consistent++;
      const free=live-map.size;
      let parity=0,freeEnd=0;
      for(const p of endpoints){if(map.has(p))parity^=map.get(p);else freeEnd++;}
      const weight=a.c*b.c*c.c*e.c;
      if(freeEnd){const mass=weight*(1n<<BigInt(free-1));count+=mass;control+=mass;}
      else{const mass=weight*(1n<<BigInt(free));if(parity)count+=mass;else control+=mass;}
    }
    if(count!==0n||control!==(1n<<BigInt(n)))throw Error("count");
    cases.push({k,d_before_guard:d,native_variables:6*(d+8*(k-1)),gate_truth_checks:checks,combinations,consistent,odd_guard_count:String(count),even_guard_count:String(control)});
  }
  return cases;
}
console.log(JSON.stringify(replay(),null,2));
