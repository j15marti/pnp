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
  ],
  [
    "ee97e4fb999b380ca981c892ce6913369b5e574a",
    "research/hcl201/multisign/2026-11-25_0136_MS26_results.json"
  ]
];
function run(inputs){
 const assert=(x,m)=>{if(!x)throw Error(m)}, bit=i=>1n<<BigInt(i),eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
 const [o,ms,bh,ii,ms26]=inputs,prior=[[6,229],[8,200],[8,229],[145,218],[145,249],[248,295],[248,308],[249,295],[250,312]];
 function init(o){let own=o.rowMap.map(x=>x[0]),groups=o.ownerIDs.map((_,i)=>own.flatMap((x,j)=>x===i?[j]:[])),R=own.length;let f=own.map((i,a)=>groups[i].find(b=>o.rowMap[b][1]===o.rowMap[a][1].replace(/[01]/g,x=>x==="0"?"1":"0")));return {R,own,groups,f,live:o.live.slice(),p:o.pairHex.map(x=>BigInt("0x"+x)),ng:[]}}
 function clone(s){return {...s,live:s.live.slice(),p:s.p.slice(),ng:s.ng.slice()}}
 function cut(s,a,b){let old=!!(s.p[a]&bit(b));s.p[a]&=~bit(b);s.p[b]&=~bit(a);return old}
 function close(s,t){for(;;){let d=s.groups.map(g=>g.filter(a=>s.live[a]));if(d.some(g=>!g.length))return false;let masks=d.map(g=>g.reduce((z,a)=>z|bit(a),0n)),ch=false;for(let a=0;a<s.R;a++)if(s.live[a])for(let j=0;j<d.length;j++)if(j!==s.own[a]){t.ac++;if(!(s.p[a]&masks[j])){s.live[a]=false;ch=true;break}}if(ch)continue;for(let g of s.ng){t.ng++;if(g.some(a=>!s.live[a]))continue;let u=g.filter(a=>d[s.own[a]].length!==1);if(!u.length)return false;if(u.length===1){s.live[u[0]]=false;ch=true}if(u.length===2&&cut(s,...u))ch=true}if(!ch)return true}}
 function stats(){return {ac:0,ng:0,orbitPair:0}}
 function sym(s){let keys=new Set(s.ng.map(g=>g.slice().sort((a,b)=>a-b).join(",")));for(let a=0;a<s.R;a++)if(s.live[a]){assert(s.f[a]!==undefined&&s.live[s.f[a]]&&s.f[s.f[a]]===a,"row symmetry");for(let b=0;b<s.R;b++)if(s.live[b]&&s.own[a]!==s.own[b])assert(!!(s.p[a]&bit(b))===!!(s.p[s.f[a]]&bit(s.f[b])),"pair symmetry")}for(let g of s.ng)assert(keys.has(g.map(a=>s.f[a]).sort((a,b)=>a-b).join(",")),"triple symmetry")}
 function anchor(s,rows,t){let h=clone(s);for(let a of rows)h.live[a]=false;return {h,ok:close(h,t)}}
 function exportCuts(s,h,t){let f=s.f,removed=[],pairs=[];const has=(a,b)=>h.live[a]&&h.live[b]&&!!(h.p[a]&bit(b));for(let a=0;a<s.R;a++)if(s.live[a]&&!h.live[a]&&!h.live[f[a]])removed.push(a);for(let a=0;a<s.R;a++)if(s.live[a])for(let b=a+1;b<s.R;b++)if(s.live[b]&&s.own[a]!==s.own[b]&&(s.p[a]&bit(b))){t.orbitPair++;if(!has(a,b)&&!has(f[a],f[b]))pairs.push([a,b])}return {removed,pairs}}
 function apply(s,c){for(let a of c.removed)s.live[a]=false;for(let [a,b] of c.pairs)cut(s,a,b)}
 function reference(s){let n=0,models=[];function go(i,w){if(i===s.groups.length){if(!s.ng.some(g=>g.every(a=>w.includes(a)))){n++;models.push(w.slice())}return}for(let a of s.groups[i])if(s.live[a]&&w.every(b=>s.p[a]&bit(b)))go(i+1,[...w,a])}go(0,[]);return models}
 function cnt(s){return s.live.filter(Boolean).length}
 let root=init(o),t=stats();assert(close(root,t),"initial root");
 let imports=[ms.jobs[1].combined,bh.jobs.find(x=>x.mode===true&&x.ref.startsWith("1e765e0"))];
 for(let u of imports){assert(eq(u.guard,o.guard),"guard");for(let a of u.removedRows||[]){root.live[a]=false;root.live[root.f[a]]=false}for(let [a,h] of u.delta||[])for(let b=0;b<root.R;b++)if(BigInt("0x"+h)&bit(b)){cut(root,a,b);cut(root,root.f[a],root.f[b])}for(let q of u.nogoods||[]){root.ng.push(q.rows,q.rows.map(a=>root.f[a]))}assert(close(root,t),"import closure")}
 sym(root);let or=ii.tests[1],z=anchor(root,or.anchorRows,t);assert(z.ok,"anchor");assert(eq(z.h.live.flatMap((x,i)=>x?[i]:[]),or.liveRows),"actual I25 rows");let s0=clone(z.h),s1=clone(z.h),s2=clone(z.h);
 for(let [a,b]of prior)cut(s1,a,b);assert(close(s1,t),"MS25");s2=clone(s1);let actual=ms26.results.shared.find(x=>x.name==="I25+MS25-anchor"&&!x.alg);assert(eq(actual.representativeAnchor,or.anchorRows),"anchor identity");for(let [a,b]of actual.deletedPairs)cut(s2,a,b);for(let a of actual.deletedRows)s2.live[a]=false;assert(close(s2,t),"MS26");
 let variants=[];for(let [name,h]of [["I25",s0],["I25+MS25",s1],["I25+MS25+MS26",s2]]){let g=clone(root),c=exportCuts(g,h,t);apply(g,c);assert(close(g,t),"root after transport");sym(g);variants.push({name,anchorRows:cnt(h),rootRows:cnt(g),...c})}
 let controls=[],seed=19;function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}
 for(let k=0;k<80;k++){let n=3+rnd(4),rowMap=Array.from({length:2*n},(_,a)=>[a>>1,String(a&1)]),rel=Array.from({length:n},()=>Array(n).fill(3));for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)rel[i][j]=rel[j][i]=1+rnd(3);let c={ownerIDs:Array.from({length:n},(_,i)=>i),rowMap,live:rowMap.map(()=>true),pairHex:rowMap.map(([i,x])=>rowMap.reduce((v,[j,y],b)=>i!==j&&(rel[i][j]&(1<<(Number(x)^Number(y))))?v|bit(b):v,0n).toString(16))};let g=init(c),u=stats(),before=reference(g),ok=close(g,u);if(!ok){assert(!before.length,"root false reject");continue}sym(g);let h=anchor(g,[1],u);if(!h.ok){assert(!before.length,"anchor false reject");controls.push({models:0,anchorRejected:true,rows:0,pairs:0});continue}let ar=reference(h.h);assert(ar.length*2===before.length,"orbit count");let cuts=exportCuts(g,h.h,u);apply(g,cuts);let after=reference(g);assert(eq(before,after),"root model sets");controls.push({models:before.length,anchorRejected:false,rows:cuts.removed.length,pairs:cuts.pairs.length})}
 return {shared:{id:o.id,guard:o.guard,anchorOwner:or.anchorOwner,removedAnchorRows:or.anchorRows,rootRows:cnt(root),variants,stats:t},controls};
}
const inputs=process.argv.slice(2).map(p=>JSON.parse(fs.readFileSync(p,'utf8')));if(inputs.length!==specs.length)throw Error('five input JSON files in specs order');console.log(JSON.stringify(run(inputs),null,2));
