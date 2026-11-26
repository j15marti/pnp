function certificate(){
  const check=(x,m)=>{if(!x)throw Error(m)},Q=[];for(let i=0;i<16;i++){const t=[3,2,1,0].map(j=>(i>>j)&1);if(t.reduce((a,b)=>a+b,0)===2)Q.push(t)}
  const pairs=[];for(let a=0;a<4;a++)for(let b=a+1;b<4;b++)pairs.push((1<<a)|(1<<b));
  const counts=[0,0,0];let localChecks=0;
  for(let j=0;j<729;j++){
    let x=j,E=[];for(const p of pairs){const k=x%3;x=Math.floor(x/3);for(let z=0;z<k;z++)E.push(p)}
    if([1,2,4,8].some(p=>E.filter(e=>e&p).length>2))continue;
    const modes=pairs.filter(a=>a<(15^a)&&E.includes(a)&&E.includes(15^a));check(modes.length<=2,"two types");counts[modes.length]++;
    if(modes.length===2)check(E.length===4&&new Set(E).size===4,"C4");
    for(let s=0;s<(1<<E.length);s++){let v=0,bad=false,sel=[];E.forEach((e,i)=>{if(s>>i&1){if(v&e)bad=true;v|=e;sel.push(e)}});const actual=s===0||!bad&&v===15;const predicted=s===0||sel.length===2&&modes.some(a=>sel.includes(a)&&sel.includes(15^a));check(actual===predicted,"local relation");localChecks++}
  }
  const swap=(T,a,b,c)=>{const x=T[a][c];T[a][c]=T[b][c];T[b][c]=x};
  const keys=t=>t.map((x,c)=>4*x+c);
  const instance=k=>{const T=Array.from({length:k},(_,b)=>Q.map(t=>t.map(x=>x+2*b))).flat();for(let b=0;b<k-1;b++)swap(T,6*b,6*(b+1),b%2);return T};
  const packing=(T,S)=>{const E=new Set();for(const i of S)for(const e of keys(T[i])){if(E.has(e))return false;E.add(e)}return true};
  const cover=(T,S)=>S.size===T.length/3&&packing(T,S);
  const exactCovers=T=>{const n=T.length/3,rows=Array.from({length:4*n},()=>[]);T.forEach((t,j)=>keys(t).forEach(e=>rows[e].push(j)));let out=0;function rec(left,chosen){if(!left.size){check(cover(T,chosen),"exact cover");out++;return}let opts=null;for(const e of left){const a=rows[e].filter(i=>keys(T[i]).every(v=>left.has(v)));if(opts===null||a.length<opts.length)opts=a}for(const i of opts){const L=new Set(left);keys(T[i]).forEach(v=>L.delete(v));rec(L,new Set([...chosen,i]))}}rec(new Set(rows.keys()),new Set());return out};
  const scales=[];for(const k of [4,8,16,32,64]){
    const T=instance(k),n=T.length/3;const rows=Array.from({length:4*n},()=>0);T.forEach(t=>keys(t).forEach(e=>rows[e]++));check(rows.every(x=>x===3)&&new Set(T.map(t=>t.join(","))).size===T.length,"E3 distinct");
    const P=new Set();for(let b=0;b<k;b++)for(const j of b<k/2?[0,5]:[1,4])P.add(6*b+j);P.delete(6*(k/2-1));check(packing(T,P)&&P.size===n-1,"one defect");
    const C0=new Set(),C1=new Set();for(let b=0;b<k;b++){C0.add(6*b+1);C0.add(6*b+4);C1.add(6*b);C1.add(6*b+5)}check(cover(T,C0)&&cover(T,C1),"lifts");
    const min=Math.min(...[C0,C1].map(C=>[...P].filter(i=>!C.has(i)).length));check(min===k-1,"distance");const owners=new Map();for(const i of P)for(const e of keys(T[i]))owners.set(e,i);let exceptions=0;for(let i=0;i<T.length;i++)if(!P.has(i)){const M=new Map();for(const e of keys(T[i]))if(owners.has(e)){const a=owners.get(e);M.set(a,(M.get(a)||0)+1)}if(M.size!==2||[...M.values()].some(x=>x!==2))exceptions++}
    const row={k,tuples:T.length,min,exceptions};if(k<=8){row.exactCovers=exactCovers(T);check(row.exactCovers===1+2**k,"phase count")}scales.push(row)
  }
  // Independently verify width-two resolution projection against exhaustive extensions.
  let seed=225805;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};let projectionChecks=0;
  const test=(F,s)=>F.every(c=>c.some(l=>Boolean(s>>(Math.abs(l)-1)&1)===(l>0)));
  for(let q=0;q<256;q++){const F=[];for(let j=0;j<10;j++){const a=1+rnd(6),b=1+rnd(6);F.push([rnd(2)?a:-a,rnd(2)?b:-b])}let R=F.map(c=>[...new Set(c)]).filter(c=>!c.some(x=>c.includes(-x)));
    for(const v of [5,6]){const P=R.filter(c=>c.includes(v)),M=R.filter(c=>c.includes(-v));R=R.filter(c=>!c.includes(v)&&!c.includes(-v));for(const p of P)for(const m of M){const c=[...new Set([...p.filter(x=>x!==v),...m.filter(x=>x!==-v)])];if(!c.some(x=>c.includes(-x)))R.push(c)}const K=new Map();R.forEach(c=>K.set(c.sort((a,b)=>a-b).join(","),c));R=[...K.values()]}
    for(let s=0;s<16;s++){const actual=[0,16,32,48].some(t=>test(F,s|t));check(actual===test(R,s),"projection");projectionChecks++}
  }
  return {localChecks,localTypes:counts,scales,projectionChecks,planarity:"Checked by separate Python source audit, not by this script"};
}
console.log(JSON.stringify(certificate(),null,2));
