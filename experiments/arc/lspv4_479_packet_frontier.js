'use strict';
// LSPV-4/479 exact finite packet-block separator optimization.
// No external dependencies; Node >=18. This establishes ONLY a syntactic
// graph-preserving separator minimum, never SAT computational hardness.
function assert(b,msg){if(!b)throw Error(msg||'assertion');}
function graph(label,n,edges){
 const seen=new Set(),a=Array(n).fill(0);
 for(const [u,v] of edges){assert(Number.isInteger(u)&&Number.isInteger(v)&&u!==v&&u>=0&&v>=0&&u<n&&v<n,'invalid edge');
 const key=[Math.min(u,v),Math.max(u,v)].join(':');assert(!seen.has(key),'duplicate');seen.add(key);a[u] |= 2**v;a[v] |= 2**u;
 }for(let i=0;i<n;i++)assert(edges.filter(e=>e.includes(i)).length===3,'not cubic');return {label,n,edges,adj:a};
}
function K4(){let es=[];for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)es.push([i,j]);return graph('K4',4,es);}
function K33(){let es=[];for(let i=0;i<3;i++)for(let j=3;j<6;j++)es.push([i,j]);return graph('K3,3',6,es);}
function cube(){let es=[];for(let i=0;i<8;i++)for(let j=i+1;j<8;j++)if(((i^j).toString(2).match(/1/g)||[]).length===1)es.push([i,j]);return graph('cube Q3',8,es);}
function petersen(){let es=[];for(let i=0;i<5;i++){es.push([i,(i+1)%5],[i,i+5],[i+5,5+(i+2)%5]);}return graph('Petersen',10,es);}
function prism(m){let es=[];for(let i=0;i<m;i++){es.push([i,(i+1)%m],[i+m,m+(i+1)%m],[i,i+m]);}return graph('prism C'+m+' x K2',2*m,es);}
function pop(x){let c=0;while(x){x&=x-1;c++;}return c;}
function cuts(G){let {n,edges}=G,out=new Uint8Array(1<<n);for(let mask=0;mask<(1<<n);mask++){let c=0;for(let [u,v] of edges)if(((mask>>>u)^(mask>>>v))&1)c++;out[mask]=c;}return out;}
function exact(G,K,cut){let n=G.n,lim=(1<<n),dp=new Uint8Array(lim); dp.fill(255);dp[0]=0;let pred=new Int32Array(lim);pred.fill(-1);
 for(let mask=1;mask<lim;mask++){
  for(let block=mask;block;block=(block-1)&mask){if(pop(block)>K)continue;let parent=mask^block;let x=Math.max(dp[parent],cut[mask]);if(x<dp[mask]){dp[mask]=x;pred[mask]=parent;}}
 }
 let parts=[],cur=lim-1;while(cur){let prev=pred[cur];assert(prev>=0,'bad witness');parts.push(Array.from({length:n},(_,i)=>i).filter(i=>((cur^prev)>>>i)&1));cur=prev;}
 parts.reverse();let max=0,mask=0;for(let p of parts){assert(p.length>0&&p.length<=K,'block bound');for(let v of p)mask|=1<<v;max=Math.max(max,cut[mask]);}assert(mask===lim-1&&max===dp[lim-1],'invalid witness');return {K,optimum:dp[lim-1],blocks:parts};
}
function exactTree(G,K,cut){
 // Optimal max connector size over full rooted binary trees whose leaves
 // contain at most K vertex packets; all source variables remain original.
 const n=G.n,lim=1<<n,dp=new Uint8Array(lim),split=new Int32Array(lim);dp.fill(255);
 dp[0]=0;for(let mask=1;mask<lim;mask++){
  if(pop(mask)<=K){dp[mask]=cut[mask];continue;}
  let low=mask&-mask;for(let a=(mask-1)&mask;a;a=(a-1)&mask){
   if(!(a&low))continue;let b=mask^a;if(!b)continue;
   let val=Math.max(cut[mask],dp[a],dp[b]);if(val<dp[mask]){dp[mask]=val;split[mask]=a;}
  }
 }
 function validate(mask){if(pop(mask)<=K)return cut[mask];let a=split[mask],b=mask^a;assert(a>0&&b>0,'bad tree');return Math.max(cut[mask],validate(a),validate(b));}
 assert(validate(lim-1)===dp[lim-1],'tree witness');
 return {K,optimum:dp[lim-1]};
}
function bruteOrders(G,cut){let n=G.n,used=0,best=255,count=0;
 function visit(mask,peak){if(mask===(1<<n)-1){best=Math.min(best,peak);count++;return;}
 for(let i=0;i<n;i++){let b=1<<i;if(!(mask&b))visit(mask|b,Math.max(peak,cut[mask|b]));}}
 visit(0,0);return {best,count};
}
function modelCounts(G){let n=G.n,m=G.edges.length,eq=Array.from({length:n},()=>[]);G.edges.forEach(([u,v],i)=>{eq[u].push(i);eq[v].push(i);});assert(eq.every(x=>x.length===3),'bad packets');
 let even=0,odd=0;
 if(m<=12)for(let a=0;a<2**m;a++){let bits=eq.map(row=>row.reduce((p,i)=>p^((a>>>i)&1),0));if(bits.every(b=>b===0))even++;if(bits[0]===1&&bits.slice(1).every(b=>b===0))odd++;}
 return {expectedEven:2**(m-n+1),expectedOdd:0,checkedExhaustive:m<=12,even:m<=12?even:null,odd:m<=12?odd:null};
}
function run(){let tested=0,rows=[];for(let G of [K4(),K33(),cube(),petersen(),prism(6)]){
 let cut=cuts(G),h_num=Infinity,h_den=1,halfMin=Infinity;for(let mask=1;mask<(1<<G.n)-1;mask++){let p=pop(mask);if(p>G.n/2)continue;if(cut[mask]*h_den<h_num*p){h_num=cut[mask];h_den=p;}if(p===G.n/2)halfMin=Math.min(halfMin,cut[mask]);tested++;}
 let opts=[];for(let K of [1,2,3].filter(k=>k<G.n/2)){let v=exact(G,K,cut);assert(v.optimum>=halfMin-(3*K),'crude check');opts.push({...v,tree:exactTree(G,K,cut)});assert(opts.at(-1).tree.optimum<=v.optimum,'tree worse than path');tested+=1<<G.n;}
 if(G.n<=8){let brute=bruteOrders(G,cut);assert(brute.best===opts[0].optimum,'brute disagrees');tested+=brute.count;}
 let mc=modelCounts(G);if(mc.checkedExhaustive){assert(mc.even===mc.expectedEven&&mc.odd===0,'model count mismatch');tested+=2**G.edges.length;}
 rows.push({name:G.label,vertices:G.n,edges:G.edges.length,h:[h_num,h_den],halfCut:halfMin,blocks:opts,modelCount:mc});
 }
 return {kind:'LSPV4_479_packet_frontier',status:'COMPUTATIONAL finite block-optima, PROVED/RESTRICTED structural lemma in separate report',checks:tested,rows};}
let out=run();process.stdout.write(JSON.stringify(out,null,2)+'\n');
