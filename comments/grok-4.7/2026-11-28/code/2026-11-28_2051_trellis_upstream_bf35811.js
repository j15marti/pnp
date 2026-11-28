function trellis(H,edges,m,cap=12){
 const p=Array.from({length:m},(_,i)=>i),root=i=>{while(p[i]!==i)i=p[i];return i};
 for(const [a,b] of edges)p[root(a)]=root(b);
 const group=new Map();for(let i=0;i<m;i++){let r=root(i);if(!group.has(r))group.set(r,[]);group.get(r).push(i)}
 const blocks=[...group.values()],cols=Array(m).fill(0n);let b=0n;
 for(let j=0;j<H.length;j++){let q=1n<<BigInt(j);if(H[j]&1n)b|=q;for(let i=0;i<m;i++)if(H[j]&(1n<<BigInt(i+1)))cols[i]|=q}
 let operations=0;const add=(B,v)=>{while(v){operations++;let k=v&-v;if(!B.has(k)){B.set(k,v);break}v^=B.get(k)}};
 const inSpan=(B,v)=>{while(v){operations++;let k=v&-v;if(!B.has(k))return false;v^=B.get(k)}return true};
 const suf=Array(blocks.length+1);suf[blocks.length]=new Map();for(let i=blocks.length-1;i>=0;i--){const B=new Map(suf[i+1]);for(const j of blocks[i])add(B,cols[j]);suf[i]=B}
 const pref=new Map(),widths=[0];for(let i=0;i<blocks.length;i++){for(const j of blocks[i])add(pref,cols[j]);widths.push(pref.size+suf[i+1].size-suf[0].size)}
 const maxWidth=Math.max(...widths),maxBlock=Math.max(0,...blocks.map(a=>a.length));
 const stats={blocks:blocks.length,maxBlock,maxWidth,totalRank:suf[0].size,operations,decision:"UNKNOWN"};
 if(maxBlock>cap||maxWidth>cap)return stats;
 let states=new Map([[0n,0n]]);let peak=1,transitions=0;for(let i=0;i<blocks.length;i++){let V=blocks[i],ind=new Map(V.map((v,j)=>[v,j])),local=edges.filter(e=>ind.has(e[0]));let options=new Map();for(let s=0;s<2**V.length;s++){if(local.some(([a,b])=>(s>>ind.get(a)&1)&&(s>>ind.get(b)&1)))continue;let t=0n,z=0n;for(let j=0;j<V.length;j++)if(s>>j&1){t^=cols[V[j]];z|=1n<<BigInt(V[j]+1)}if(!options.has(t))options.set(t,z)}
 const next=new Map();for(const [u,z] of states)for(const [v,w] of options){transitions++;let t=u^v;if(inSpan(suf[i+1],b^t)&&!next.has(t))next.set(t,z|w)}states=next;peak=Math.max(peak,states.size);if(!states.size)break}
 return {...stats,operations,peak,transitions,decision:states.has(b)?"YES":"NO",witness:states.has(b)?states.get(b).toString(16):null}
}
module.exports={trellis};
