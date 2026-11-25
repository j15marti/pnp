const fs=require('fs');
const specs=[
  [
    "1e765e0e95ae0a6eeea5a1b43a5c8c525f82e5fd",
    "research/constructive-shared-hubs/multisign-dag/2026-11-25_0021_BD18_pairs_1.json"
  ],
  [
    "ecbbf26c6a5d9b2b53f5942b1889131c3ebe1fce",
    "research/hcl201/multisign/2026-11-25_0028_MS24_results.json"
  ],
  [
    "ab85c853f3296c2423910ba3aee8b7db8189037c",
    "research/constructive-shared-hubs/hard-residuals/2026-11-25_0042_BH18_feedback_results.json"
  ],
  [
    "bdda062d50962d29343f7413764acfdf5edbc21b",
    "research/hcl201/interfaces/2026-11-25_0120_I25_orbit_results.json"
  ]
];
function run(inputs){
 const bit=i=>1n<<BigInt(i), assert=(a,m)=>{if(!a)throw Error(m)}, eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
 const prior=[[6,229],[8,200],[8,229],[145,218],[145,249],[248,295],[248,308],[249,295],[250,312]];
 function prepare(o,imports=[],orbit=null){
  let R=o.rowMap.length,own=o.rowMap.map(x=>x[0]),groups=o.ownerIDs.map((_,i)=>own.flatMap((x,j)=>x===i?[j]:[]));
  let st={o,R,own,groups,live:o.live.slice(),p:o.pairHex.map(x=>BigInt("0x"+x)),ng:[]};
  let f=[];if(orbit)for(let d of groups){let m=new Map(d.filter(a=>st.live[a]).map(a=>[o.rowMap[a][1],a]));for(let a of d)if(st.live[a]){f[a]=m.get(o.rowMap[a][1].replace(/[01]/g,x=>x==="0"?"1":"0"));assert(f[a]!==undefined,"orbit")}}
  function cut(a,b){st.p[a]&=~bit(b);st.p[b]&=~bit(a)}
  for(let u of imports){assert(eq(u.guard,o.guard),"guard");for(let a of u.removedRows||[]){st.live[a]=false;if(orbit)st.live[f[a]]=false}
   for(let [a,h] of u.delta||[])for(let b=0;b<R;b++)if(BigInt("0x"+h)&bit(b)){cut(a,b);if(orbit&&f[a]!==undefined&&f[b]!==undefined)cut(f[a],f[b])}
   for(let q of u.nogoods||[]){let t=q.rows;st.ng.push(t);if(orbit&&t.every(a=>f[a]!==undefined))st.ng.push(t.map(a=>f[a]))}
  }
  if(orbit){for(let a of orbit.anchorRows)st.live[a]=false}
  return st;
 }
 const ds=s=>s.groups.map(a=>a.filter(i=>s.live[i])), count=s=>s.live.filter(Boolean).length;
 function close(s,stats,unitOnly=false){
  while(true){
   let d=ds(s);if(d.some(a=>!a.length))return false;
   let masks=d.map(a=>a.reduce((v,i)=>v|bit(i),0n)),change=false;
   for(let a=0;a<s.R;a++)if(s.live[a])for(let i=0;i<d.length;i++)if(i!==s.own[a]){
    stats.ac++;if(!(s.p[a]&masks[i])){s.live[a]=false;change=true;break}
   }
   if(change)continue;
   for(let t of s.ng){stats.nogood++;if(t.some(a=>!s.live[a]))continue;let u=t.filter(a=>d[s.own[a]].length!==1);
    if(!u.length)return false;if(u.length===1){s.live[u[0]]=false;change=true}
    if(!unitOnly&&u.length===2){let[a,b]=u;if(s.p[a]&bit(b)){s.p[a]&=~bit(b);s.p[b]&=~bit(a);change=true}}
   }if(!change)return true;
  }
 }
 function affine(s,stats,projection=true){
  let d=ds(s),R=s.R,C=bit(R),P=new Map(),bits=Array.from({length:R+1},(_,i)=>bit(i));
  function high(v){return v.toString(2).length-1}
  function insert(v){while(v){let h=high(v),p=P.get(h);if(!p){P.set(h,v);return}v^=p;stats.xor++}}
  function reduce(v){let out=0n;while(v){let h=high(v),p=P.get(h);if(p){v^=p;stats.xor++}else{out|=bits[h];v^=bits[h]}}return out}
  for(let a of d)insert(a.reduce((v,i)=>v|bits[i],C));
  for(let i=0;i<d.length;i++)for(let j=i+1;j<d.length;j++){
   let a=d[i],b=d[j],par=Array.from({length:a.length+b.length},(_,i)=>i),root=i=>{while(i!==par[i])i=par[i];return i};
   for(let x=0;x<a.length;x++)for(let y=0;y<b.length;y++){stats.pairScans++;if(s.p[a[x]]&bits[b[y]])par[root(x)]=root(a.length+y)}
   let cc=new Map();[...a,...b].forEach((v,i)=>{let z=root(i);cc.set(z,(cc.get(z)||0n)|bits[v])});
   for(let v of cc.values())insert(v);
  }
  stats.gauss++;
  if(reduce(C)===0n)return {ok:false,rank:P.size,bad:[]};
  if(!projection)return {ok:true,rank:P.size,bad:[]};
  let red=bits.map(v=>reduce(v)),bad=[];
  for(let a of d){let Q=new Map(),D=[];for(let i of [...a,R]){let v=red[i],w=bits[i];while(v){let h=high(v),p=Q.get(h);if(!p){Q.set(h,[v,w]);break}v^=p[0];w^=p[1];stats.xor++}if(!v)D.push(w)}
   for(let i of a)if(D.some(w=>!!(w&C)!==!!(w&bits[i])))bad.push(i)
  }
  return {ok:true,rank:P.size,bad};
 }
 function stats(){return {ac:0,nogood:0,pairScans:0,xor:0,gauss:0,probes:0}}
 function clone(s){return {...s,live:s.live.slice(),p:s.p.slice()}}
 function fixed(s,t,alg){for(;;){if(!close(s,t))return false;if(!alg)return true;let r=affine(s,t);if(!r.ok)return false;if(!r.bad.length)return true;for(let a of r.bad)s.live[a]=false}}
 function probe(root,alg,cap,priority=[]){
  let s=clone(root),t=stats(),dels=[],cuts=[],events=[],ok=fixed(s,t,alg),initial=count(s);
  let order=[...new Set([...priority,...s.groups.slice().sort((a,b)=>a.filter(i=>s.live[i]).length-b.filter(i=>s.live[i]).length).flat()])];
  for(let a of order){if(!ok||t.probes>=cap)break;if(!s.live[a])continue;
   let h=clone(s);for(let b of h.groups[h.own[a]])if(b!==a)h.live[b]=false;t.probes++;
   let acOK=close(h,t),acMask=h.live.slice(),final=acOK,rank=null;
   if(final&&alg){let z=affine(h,t);rank=z.rank;if(!z.ok)final=false;else{for(let b of z.bad)h.live[b]=false;final=fixed(h,t,true)}}
   let nr=[],np=[],affineOnly=0;
   if(!final){s.live[a]=false;dels.push(a);nr.push(a)}
   else for(let b=0;b<s.R;b++)if(s.live[b]&&s.own[a]!==s.own[b]&&(s.p[a]&bit(b))&&!h.live[b]){
    s.p[a]&=~bit(b);s.p[b]&=~bit(a);cuts.push([a,b]);np.push(b);if(acMask[b])affineOnly++
   }
   if(nr.length||np.length)events.push({pivot:a,acOK,final,rank,rows:nr,pairs:np,affineOnly});
   if(nr.length||np.length)ok=fixed(s,t,alg);
  }
  if(ok)ok=fixed(s,t,alg);
  return {status:ok?"OPEN":"UNSAT",initial,end:count(s),deletedRows:dels,deletedPairs:cuts,events,stats:t};
 }
 function reference(s){let d=ds(s),vis=0,models=0,word=[];function f(i){if(i===d.length){vis++;if(s.ng.some(t=>t.every(a=>word.includes(a))))return;models++;return}for(let a of d[i])if(word.every(b=>s.p[a]&bit(b))){word.push(a);f(i+1);word.pop()}}f(0);return {models,completeCompatibleWords:vis}}
 function chart(id,groups,allowed){let rowMap=groups.flatMap((d,i)=>d.map(x=>[i,String(x)])),ownerIDs=groups.map((_,i)=>i),p=rowMap.map(([i,a])=>rowMap.reduce((v,[j,b],k)=>i!==j&&allowed(i,a,j,b)?v|bit(k):v,0n).toString(16));return {id,guard:[],ownerIDs,rowMap,live:rowMap.map(()=>true),pairHex:p}}
 function gated(odd){
  const E=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],inc=Array.from({length:4},(_,i)=>E.map((e,j)=>e.includes(i)?j:-1).filter(x=>x>=0));
  function feature(i,a,j){let x=Number(a),k=inc[i].indexOf(j),u=x>>2&1,v=x>>1&1;return [u,v,u^v][k]^(odd&&i===3&&k===2?1:0)}
  let o=chart("gated-"+(odd?"odd":"even"),[[0,1],...Array.from({length:4},()=>Array.from({length:9},(_,i)=>i))],(i,a,j,b)=>{
   if(i===0)return a==="1"||b!=="8";if(j===0)return b==="1"||a!=="8";if(a==="8"||b==="8")return true;
   let k=E.findIndex(e=>e.includes(i-1)&&e.includes(j-1));return feature(i-1,a,k)===feature(j-1,b,k)
  });let s=prepare(o),t=stats();assert(fixed(s,t,true),"root affine");let g0=clone(s);g0.live[1]=false;let expected=reference(g0),base=probe(g0,false,1000),joint=probe(g0,true,1000),root=probe(s,true,1000);assert((joint.status==="UNSAT")===odd,"gate control");assert(expected.models===(odd?0:128),"reference gate");assert(base.status==="OPEN","AC should stall");assert(root.deletedRows.includes(0)===odd,"gate forcing");
  return {id:o.id,expected,base,joint,root};
 }
 function fano(del){
  let E=[];for(let a=1;a<8;a++)for(let b=a+1;b<8;b++){let c=a^b;if(c>b)E.push([a,b,c])}if(del)E.pop();
  let o=chart("Fano-"+del,E.map(()=>[1,2,3,4,5,6]),(i,a,j,b)=>E[i].every((v,k)=>!E[j].includes(v)||((Number(a)>>k&1)===(Number(b)>>E[j].indexOf(v)&1))));
  let s=prepare(o),expected=reference(s),p=probe(s,true,1000);assert(p.status==="OPEN"&&p.deletedRows.length===0&&p.deletedPairs.length===0,"raw NAE barrier");assert((expected.models>0)===del,"Fano control");return {id:o.id,expected,p};
 }
 const [o,ms,bh,ii]=inputs,im=[ms.jobs[1].combined,bh.jobs.find(x=>x.mode===true&&x.ref.startsWith("1e765e0"))],or=ii.tests[1];
 let baseline=prepare(o,im),anch=prepare(o,im,or),ta=stats();assert(close(anch,ta,true),"anchor close");assert(eq(anch.live.flatMap((v,i)=>v?[i]:[]),or.liveRows),"anchor identity");
 for(let[a,b]of prior){anch.p[a]&=~bit(b);anch.p[b]&=~bit(a)}
 let priority=[...new Set(prior.flat())];
 let shared=[];for(let [name,s]of [["combined",baseline],["I25+MS25-anchor",anch]])for(let alg of [false,true])shared.push({name,alg,guard:o.guard,representativeAnchor:name.includes("anchor")?or.anchorRows:null,...probe(s,alg,64,priority)});
 return {shared,controls:[gated(true),gated(false),fano(false),fano(true)]};
}
const inputs=process.argv.slice(2).map(p=>JSON.parse(fs.readFileSync(p,'utf8')));if(inputs.length!==specs.length)throw Error('four inputs in listed order');console.log(JSON.stringify(run(inputs),null,2));
