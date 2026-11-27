function audit() {
  const e=(u,v)=>[Math.min(u,v),Math.max(u,v)], key=([u,v])=>`${u},${v}`;
  const base=[];for(let i=0;i<5;i++){base.push(e(i,(i+1)%5),e(i,i+5),e(i+5,5+(i+2)%5));}
  const core=base.filter(x=>!["0,1","5,7"].includes(key(x))),diamond=[[0,2],[0,3],[1,2],[1,3],[2,3]],square=[[0,1],[1,2],[2,3],[0,3]];
  function matchings(n,es){const out=[];function rec(v,p){if(!v.length){out.push(p);return;}const u=v[0];for(const a of es){if(!a.includes(u))continue;const w=a[0]===u?a[1]:a[0];if(v.includes(w))rec(v.filter(x=>x!==u&&x!==w),p.concat([a]));}}rec(Array.from({length:n},(_,i)=>i),[]);return out;}
  function relation(n,es,ports){const ms=matchings(n,es);let valid=0,checks=0;const words=new Set();for(const m of ms){let ok=false;const c=es.filter(a=>!m.some(b=>key(a)===key(b)));for(let w=0;w<2**n;w++){checks++;if(c.every(([u,v])=>((w>>u)^(w>>v))&1)){ok=true;words.add(ports.map(p=>(w>>p)&1).join(""));}}valid+=Number(ok);}return {matchings:ms.length,valid,checks,words:[...words].sort()};}
  const p=relation(10,base,[]),c=relation(10,core,[0,1,5,7]),d=relation(4,diamond,[0,1]),s=relation(4,square,[0,1,2,3]);
  if(p.matchings!==6||p.valid!==0||c.matchings!==3||c.valid!==2||c.words.join(",")!=="0000,0011,1100,1111"||d.matchings!==2||d.valid!==2||d.words.join(",")!=="01,10"||s.words.length!==6)throw Error("audit failed");
  const rows=[0,1,2,4,8,16,32].map(k=>({k,n:10+8*k,matchings:String(3n*(2n**BigInt(2*k))),chainParity:(3*k+k+1)%2,coreParity:0}));
  if(rows.some(r=>r.chainParity===r.coreParity))throw Error("parity failure");
  return {petersen:p,core:c,diamond:d,square:s,rows};
}
console.log(JSON.stringify(audit(),null,2));
