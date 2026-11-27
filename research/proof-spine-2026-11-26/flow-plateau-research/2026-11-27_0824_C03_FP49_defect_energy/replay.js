// FP49 independent replay: rebuild native IDs, complement components and flow lift.
const crypto = require('crypto');
function replay(r,fr=false,base=true){
  const z=r, clauses=[];
  const clause=(vs,bs)=>clauses.push(vs.map((v,j)=>[v,1-bs[j]]));
  if(base) for(let w=0;w<8;w++) clause([0,1,z],[w>>2,w>>1&1,w&1]);
  for(let i=0;i<r;i++) for(let w=0;w<8;w++){
    const a=w>>2,b=w>>1&1,c=w&1,s=+(fr&&i===r-1);
    if((a^b)!==s) clause([i,(i+1)%r,z],[a,b,c]);
  }
  for(let w=0;w<4;w++) clause([0,1,z],[0,w>>1,w&1]);
  const occ=Array.from({length:r+1},()=>[]),port=[],E=[],opts=[],fixed=[],seams=[];
  clauses.forEach((c,j)=>{port[j]=[];c.forEach(([v,p],k)=>occ[v].push([j,k,p]));});
  let n=0;
  function edge(u,v,s){E.push([Math.min(u,v),Math.max(u,v),s]);return E.length-1;}
  occ.forEach((os,v)=>{
    const len=os.length*6,cyc=[]; for(let j=0;j<len;j++)cyc.push(edge(n+j,n+(j+1)%len,1));
    opts[v]=[cyc.filter((_,i)=>i%2),cyc.filter((_,i)=>!(i%2))];
    os.forEach(([j,k,p],i)=>{const a=n+6*i;edge(a,a+5,0);port[j][k]=(p?[1,4,2,3]:[1,2,4,3]).map(t=>a+t);});n+=len;
  });
  clauses.forEach((_,j)=>{
    const a=n++,b=n++;fixed.push(edge(a,b,1));seams[j]=fixed.at(-1);
    for(let k=0;k<3;k++)for(let h=0;h<2;h++){
      const u=port[j][k][2*h+1],v=port[j][(k+1)%3][2*h];
      if(k===0){const w=h?b:a;edge(u,w,0);edge(w,v,0);}else edge(u,v,0);
    }
  });
  const sorted=E.slice().sort((a,b)=>a[0]-b[0]||a[1]-b[1]);
  if(new Set(sorted.map(e=>e.slice(0,2).join(','))).size!==E.length)throw Error('duplicate');
  const deg=Array(n).fill(0); E.forEach(([u,v])=>{if(u===v)throw Error('loop');deg[u]++;deg[v]++;});if(deg.some(d=>d!==3))throw Error('degree');
  const sha=crypto.createHash('sha256').update(JSON.stringify(sorted)).digest('hex');
  let words=[];
  if(r<=6){for(let j=0;j<2**(r+1);j++)words.push(Array.from({length:r+1},(_,i)=>j>>i&1));}
  else {words.push(Array(r+1).fill(0),[...Array(r).fill(1),0], [...Array(r).fill(0),1]);for(let i=0;i<r;i++)words.push(Array.from({length:r+1},(_,j)=>+(j===i)));for(const k of [2,r/2,r-1])words.push(Array.from({length:r+1},(_,j)=>+(j<k)));}
  words=[...new Map(words.map(w=>[w.join(''),w])).values()];
  let hist={};
  for(const w of words){
    const M=new Set(fixed);opts.forEach((op,i)=>op[w[i]].forEach(e=>M.add(e)));
    const bad=[];clauses.forEach((c,i)=>{if(!c.some(([v,p])=>w[v]===p))bad.push(i);});
    const energy=+base+ +(w[0]===0)+Array.from({length:r},(_,i)=>+((w[i]^w[(i+1)%r])!==+(fr&&i===r-1))).reduce((a,b)=>a+b,0);
    const H=Array.from({length:n},()=>[]),P=Array(n).fill(0),omit=new Set(bad.map(i=>seams[i])),B=new Set();
    E.forEach(([u,v],i)=>{if(!M.has(i)){H[u].push([v,i]);H[v].push([u,i]);}else if(!omit.has(i)){B.add(i);P[u]^=1;P[v]^=1;}});
    let odd=0; const seen=new Set();
    for(let s=0;s<n;s++)if(!seen.has(s)){
      let u=s,prev=-1,carry=0,len=0;
      do{if(H[u].length!==2||seen.has(u))throw Error('cycle');seen.add(u);len++;const [v,e]=H[u].find(([v])=>v!==prev);carry^=P[u];if(v!==s&&carry)B.add(e);prev=u;u=v;}while(u!==s);
      if(carry)throw Error('lift parity');odd+=len%2;
    }
    const d=Array(n).fill(0);for(const i of B){const [u,v]=E[i];d[u]^=1;d[v]^=1;}
    if(d.some(Boolean)||odd!==2*bad.length||bad.length!==energy||[...M].filter(e=>!B.has(e)).length!==energy)throw Error('energy');
    hist[energy]=(hist[energy]||0)+1;
  }
  return {r,fr,base,n,sha,words:words.length,hist};
}
for(const r of [3,4,6,8,16,32,64])console.log(JSON.stringify(replay(r)));
console.log(JSON.stringify(replay(4,true)));console.log(JSON.stringify(replay(3,false,false)));
