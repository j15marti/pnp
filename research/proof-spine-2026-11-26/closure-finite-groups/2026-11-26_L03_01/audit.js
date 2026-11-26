const audit = function(){
  const assert=(x,m)=>{if(!x)throw Error(m)};
  const mk=k=>{let e=[];for(let r=0;r<k;r++)for(let c=0;c<k;c++){let v=r*k+c;if(c+1<k)e.push([v,1,v+1,3]);if(r+1<k)e.push([v,2,v+k,0])}return e};
  const encode=(k,e,bit)=>{let w=Array(k*k).fill(0);e.forEach(([a,p,b,q],i)=>{if(bit(i)){w[a]|=1<<p;w[b]|=1<<q}});return w};
  const direct=(k,e,w)=>{for(let [a,p,b,q] of e)if(((w[a]>>p)&1)!==((w[b]>>q)&1))return false;for(let r=0;r<k;r++)for(let c=0;c<k;c++){let x=w[r*k+c];if((r===0&&(x&1))||(c===k-1&&(x&2))||(r===k-1&&(x&4))||(c===0&&(x&8)))return false}return true};
  const row=(k,w)=>{let prev=Array(k).fill(0);for(let r=0;r<k;r++){let west=0;for(let c=0;c<k;c++){let x=w[r*k+c];if((x&1)!==prev[c]||((x>>3)&1)!==west)return false;prev[c]=(x>>2)&1;west=(x>>1)&1}if(west)return false}return prev.every(x=>x===0)};
  let tests=0,splices=0,labels=0,seed=26112603;const rnd=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed>>>31};
  let results=[];
  for(const k of [2,3,4,8,16,32,64,128]){
    const e=mk(k),m=e.length,n=k*k;
    const cuts=[];for(let p=Math.ceil(n/3);p<=Math.floor(2*n/3);p++){let c=0; // count exact cut from direct edge scan at small sizes, analytic endpoint formula otherwise
      if(k<=32)c=e.filter(([a,,b])=>a<p&&p<=b).length;
      else {let r=Math.floor(p/k),j=p%k;c=(r>0?k-j:0)+(r+1<k?j:0)+(j>0?1:0)}
      assert(c>=k,"cut bound");tests++;cuts.push(c)}
    let yes=0,no=0,patternChecks=0;
    if(k<=3){const maps=cuts.map(()=>new Map());for(let mask=0;mask<(1<<m);mask++){
        let w=encode(k,e,i=>(mask>>i)&1);assert(direct(k,e,w)&&row(k,w),"valid");yes++;tests++;
        let [a,p]=e[mask%m];let bad=w.slice();bad[a]^=1<<p;assert(!direct(k,e,bad)&&!row(k,bad),"invalid");no++;tests++;
        for(let j=0;j<cuts.length;j++){let pfx=Math.ceil(n/3)+j;let key=e.map(([a,,b],i)=>a<pfx&&pfx<=b?((mask>>i)&1):"").join("");maps[j].set(key,(maps[j].get(key)||0)+1)}
      }
      maps.forEach((map,j)=>{assert(map.size===2**cuts[j],"pattern count");for(let v of map.values())assert(v===2**(m-cuts[j]),"fiber");patternChecks+=map.size;tests+=map.size+1});
    } else {for(let t=0;t<16;t++){let w=encode(k,e,()=>rnd());assert(direct(k,e,w)&&row(k,w),"valid big");yes++;tests++;let [a,p]=e[(t*97)%m];let bad=w.slice();bad[a]^=1<<p;assert(!direct(k,e,bad)&&!row(k,bad),"invalid big");no++;tests++}}
    for(let t=0;t<32;t++){let pfx=Math.ceil(n/3)+(t%cuts.length);let i=e.findIndex(([a,,b])=>a<pfx&&pfx<=b);let bits=e.map(()=>rnd());let w=encode(k,e,j=>bits[j]);bits[i]^=1;let z=encode(k,e,j=>bits[j]);let hybrid=w.slice(0,pfx).concat(z.slice(pfx));assert(!direct(k,e,hybrid)&&!row(k,hybrid),"cross splice");splices++;tests++}
    labels+=yes+no;results.push({k,blocks:n,internalEdges:m,balancedBoundaries:cuts.length,minCut:Math.min(...cuts),maxCut:Math.max(...cuts),yes,no,patternChecks})
  }
  return {seed:26112603,tests,splices,labels,results}
};
console.log(JSON.stringify(audit(),null,2));
