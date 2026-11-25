function productionAudit(){
  const bit=(x,i)=>Number((x>>BigInt(i))&1n), par=x=>{let p=0;while(x){x&=x-1n;p^=1}return p}, ok=(w,B)=>B.every(c=>c.some(l=>bit(w,Math.abs(l)-1)===(l>0?1:0))), ax=(w,A)=>A.every(([m,b])=>par(w&m)===b);
  function insert(P,v){while(v){let k=v.toString(2).length-1;if(P.has(k))v^=P.get(k);else{P.set(k,v);return true}}return false}
  function member(P,v){while(v){let k=v.toString(2).length-1;if(!P.has(k))return false;v^=P.get(k)}return true}
  function trellis(n,B,A,pins=[],cap=1024){let blocks=B.map(c=>c.map(l=>Math.abs(l)-1)),used=new Set(blocks.flat());if(used.size!==blocks.flat().length)throw Error("not matching");for(let i=0;i<n;i++)if(!used.has(i))blocks.push([i]);let col=Array.from({length:n},(_,i)=>A.reduce((s,[m,b],j)=>s|(BigInt(bit(m,i))<<BigInt(j)),0n)),target=A.reduce((s,[m,b],j)=>s|(BigInt(b)<<BigInt(j)),0n);let suf=Array(blocks.length+1);suf[blocks.length]=new Map();for(let i=blocks.length-1;i>=0;i--){suf[i]=new Map(suf[i+1]);for(let v of blocks[i])insert(suf[i],col[v])}let D=new Map([[0n,0n]]),U=new Map(),max=1,work=0,width=0;for(let i=0;i<blocks.length;i++){let E=new Map(),bl=blocks[i];for(let v of bl)insert(U,col[v]);let union=new Map(U);for(let v of suf[i+1].values())insert(union,v);width=Math.max(width,U.size+suf[i+1].size-union.size);for(let [s,w] of D)for(let t=0;t<2**bl.length;t++){work++;let u=0n,q=0n;for(let j=0;j<bl.length;j++)if((t>>j)&1){u|=1n<<BigInt(bl[j]);q^=col[bl[j]]}if(i<B.length&&!ok(u,[B[i]]))continue;if(pins.some(([v,b])=>bl.includes(v)&&bit(u,v)!==b))continue;let r=s^q;if(member(suf[i+1],target^r)&&!E.has(r)){if(E.size===cap)return {status:"UNKNOWN",work,max,width};E.set(r,w|u)}}D=E;max=Math.max(max,D.size)}let w=D.get(target);if(w!==undefined&&(!ok(w,B)||!ax(w,A)||!pins.every(([v,b])=>bit(w,v)===b)))throw Error("bad lift");return {status:w===undefined?"UNSAT":"SAT",w:w?.toString(16),rank:suf[0].size,width,max,work}}
  const cases=[];let guarded=0;
  for(let pairs of [12,32,64,128]){let n=2*pairs,B=Array.from({length:pairs},(_,i)=>[2*i+1,2*i+2]);let A=B.map((c,i)=>[(1n<<BigInt(2*i))|(1n<<BigInt(2*i+1)),1]); // high rank width zero
    for(let bad of [false,true]){let rows=A.map(x=>x.slice());if(bad){rows.push([1n,0],[2n,0])}let r=trellis(n,B,rows);if(r.status!==(bad?"UNSAT":"SAT"))throw Error("bad result");cases.push({n,bad,kind:"independent",...r})}
    // adjacent equality of first bit across pair blocks; plus pair parity; width at most one.
    const link=Array.from({length:pairs-1},(_,i)=>[(1n<<BigInt(2*i))|(1n<<BigInt(2*i+2)),0]);let rows=[...A,...link];for(let bad of [false,true]){let ar=bad?[...rows,[1n,0],[1n<<BigInt(n-2),1]]:rows;let r=trellis(n,B,ar);if(r.status!==(bad?"UNSAT":"SAT"))throw Error("bad result");cases.push({n,bad,kind:"chain",...r})}
    // paid forced coordinate probes; x0=0 fixes all remaining pairs on chain, test every coordinate.
    let pins=[[0,0]];for(let i=0;i<n;i++)for(let b=0;b<2;b++){let r=trellis(n,B,rows,[...pins,[i,b]]);if(r.status!==((i%2===b)?"SAT":"UNSAT"))throw Error("bad force");guarded++}
  }
  return {cases,guarded};
}
console.log(JSON.stringify(productionAudit(),null,2));
