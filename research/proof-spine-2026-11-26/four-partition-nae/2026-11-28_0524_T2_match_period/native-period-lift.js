function periodChart(G,w){
 const N=4*G.types.length,p=Array.from({length:N},(_,i)=>i),s=new Uint8Array(N),size=new Int32Array(N).fill(1),count={find:0,localWords:0,periodTests:0,rankXor:0,quotientPivotTests:0};
 function root(i){count.find++;if(p[i]===i)return [i,0];let [r,t]=root(p[i]);s[i]^=t;p[i]=r;return [r,s[i]]}
 function merge(i,j,t){let [a,x]=root(i),[b,y]=root(j);if(a===b){if((x^y)!==t)throw Error("edge");return}if(size[a]<size[b])[a,b]=[b,a];p[b]=a;s[b]=x^y^t;size[a]+=size[b]}
 for(const [a,b,t] of G.edges)merge(a,b,t);for(let i=0;i<G.types.length;i++)if(G.types[i]==="E")for(let j=1;j<4;j++)merge(4*i,4*i+j,0);
 const D=[],dedup=new Map();for(let i=0;i<G.types.length;i++)if(G.types[i]==="B"){let terms=Array.from({length:4},(_,j)=>root(4*i+j)),vs=[...new Set(terms.map(x=>x[0]))].sort((a,b)=>a-b),S=[];for(let a=0;a<2**vs.length;a++){count.localWords++;if(terms.reduce((z,[v,t])=>z+(((a>>vs.indexOf(v))&1)^t),0)===2)S.push(a)}if(!S.length)throw Error("empty");let k=JSON.stringify([vs,S]);if(dedup.has(k)){D[dedup.get(k)].owners.push(i);continue}dedup.set(k,D.length);D.push({vs,S,owners:[i],columns:vs.map(()=>0n)})}
 const first=new Map();let dim=0;for(let i=0;i<D.length;i++)for(let j=0;j<D[i].vs.length;j++){let v=D[i].vs[j];if(!first.has(v)){first.set(v,[i,j]);continue}let [a,b]=first.get(v),bit=1n<<BigInt(dim++);D[i].columns[j]^=bit;D[a].columns[b]^=bit}
 function insert(B,x){while(x){let k=x.toString(2).length-1;if(!B.has(k)){B.set(k,x);return}x^=B.get(k);count.rankXor++}}
 let H=new Map(),before=[],periodOwners=0,anchor=0n;for(const d of D){let T=new Map();for(const a of d.S){let x=0n;for(let j=0;j<d.vs.length;j++)if((a>>j)&1)x^=d.columns[j];if(!T.has(x))T.set(x,a)}let base=T.keys().next().value;anchor^=base;let S=new Set([...T.keys()].map(x=>x^base));before.push([...S]);let periods=[];for(const h of S){let ok=true;for(const x of S){count.periodTests++;if(!S.has(x^h)){ok=false;break}}if(ok)periods.push(h)}if(periods.length>1)periodOwners++;for(const h of periods)insert(H,h);d.image=T;d.anchor=base;d.periods=periods}
 const piv=[...H].sort((a,b)=>b[0]-a[0]);function proj(x){for(const [k,v] of piv){count.quotientPivotTests++;if((x>>BigInt(k))&1n)x^=v}return x}
 const after=before.map(S=>[...new Set(S.map(proj))]);
 let liftAudit=null;
 if(w){
  if(w.length!==N)throw Error("input witness length");let chosen=[],discrepancy=0n,tagged=new Map(),generators=[],original=0n;
  for(let i=0;i<D.length;i++){let d=D[i],a=d.vs.reduce((a,v,j)=>a|(Number(w[v])<<j),0);if(!d.S.includes(a))throw Error("local witness");let x=d.columns.reduce((x,v,j)=>x^((a>>j)&1?v:0n),0n);original^=x;let q=proj(x^d.anchor),y=[...d.image.keys()].find(y=>proj(y^d.anchor)===q);if(y===undefined)throw Error("no quotient representative");chosen.push(y);discrepancy^=y;
   for(const h of d.periods){if(!h)continue;let z=h,tag=1n<<BigInt(generators.length);generators.push([i,h]);while(z){let k=z.toString(2).length-1;if(!tagged.has(k)){tagged.set(k,[z,tag]);break}let [v,t]=tagged.get(k);z^=v;tag^=t;count.rankXor++}}}
  if(original)throw Error("bad original witness syndrome");let z=discrepancy,tag=0n;while(z){let k=z.toString(2).length-1;if(!tagged.has(k))throw Error("no period lift");let [v,t]=tagged.get(k);z^=v;tag^=t;count.rankXor++}
  let moves=0;for(let i=0;i<generators.length;i++)if((tag>>BigInt(i))&1n){let [j,h]=generators[i];chosen[j]^=h;moves++}
  let assignment=new Map();for(let i=0;i<D.length;i++){let d=D[i],a=d.image.get(chosen[i]);if(a===undefined)throw Error("period escaped");for(let j=0;j<d.vs.length;j++){let v=d.vs[j],b=(a>>j)&1;if(assignment.has(v)&&assignment.get(v)!==b)throw Error("carrier mismatch");assignment.set(v,b)}}
  let lifted=Array.from({length:N},(_,i)=>{let [v,t]=root(i);return (assignment.get(v)||0)^t}).join("");
  liftAudit={changedPeriods:moves,taggedRank:tagged.size,discrepancyHex:discrepancy.toString(16),lifted};
 }
 function rankProfile(sets){let B=new Map(),pre=[0];for(const S of sets){for(const x of S)insert(B,x);pre.push(B.size)}let rank=B.size;B=new Map();let suf=new Array(sets.length+1).fill(0);for(let i=sets.length-1;i>=0;i--){for(const x of sets[i])insert(B,x);suf[i]=B.size}let cuts=pre.map((x,i)=>x+suf[i]-rank);return {rank,max:Math.max(...cuts),sum:cuts.reduce((a,b)=>a+b,0),cuts}}
 let a=rankProfile(before),b=rankProfile(after);let cutLoss=a.cuts.map((x,i)=>x-b.cuts[i]);if(cutLoss.some(x=>x<0))throw Error("cut increased");
 // Every quotient word has an original preimage, and each tested period preserves full dictionary support. Global lift theorem uses tagged period generators, not implemented here.
 return {liftAudit,blocks:D.length,dimension:dim,carriers:first.size,periodOwners,periodRank:H.size,optionsBefore:before.reduce((s,x)=>s+x.length,0),optionsAfter:after.reduce((s,x)=>s+x.length,0),rankBefore:a.rank,rankAfter:b.rank,maxCutBefore:a.max,maxCutAfter:b.max,sumCutBefore:a.sum,sumCutAfter:b.sum,improvedCuts:cutLoss.filter(x=>x>0).length,maxCutLoss:Math.max(...cutLoss),count,cutProfileBefore:a.cuts,cutProfileAfter:b.cuts}
}
module.exports={periodChart};
