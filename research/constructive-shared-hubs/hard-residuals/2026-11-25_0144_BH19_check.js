const fs=require('fs');
const specs=[
  [
    "1fc8b6c",
    "research/constructive-shared-hubs/multisign-dag/2026-11-25_0021_BD18_pairs_0.json"
  ],
  [
    "1e765e0",
    "research/constructive-shared-hubs/multisign-dag/2026-11-25_0021_BD18_pairs_1.json"
  ],
  [
    "80b4721",
    "research/constructive-shared-hubs/multisign-dag/2026-11-25_0021_BD18_pairs_2.json"
  ],
  [
    "37578c1",
    "research/constructive-shared-hubs/multisign-dag/2026-11-25_0021_BD18_pairs_3.json"
  ],
  [
    "33f9839",
    "research/constructive-shared-hubs/multisign-dag/2026-11-25_0021_BD18_pairs_4.json"
  ],
  [
    "ecbbf26",
    "research/hcl201/multisign/2026-11-25_0028_MS24_results.json"
  ],
  [
    "ab85c85",
    "research/constructive-shared-hubs/hard-residuals/2026-11-25_0042_BH18_feedback_results.json"
  ],
  [
    "bdda062d",
    "research/hcl201/interfaces/2026-11-25_0120_I25_orbit_results.json"
  ],
  [
    "ee97e4fb",
    "research/hcl201/multisign/2026-11-25_0136_MS26_results.json"
  ]
];
function run(inputs){
const bit=i=>1n<<BigInt(i),assert=(x,m)=>{if(!x)throw Error(m)},same=(x,y)=>JSON.stringify(x)===JSON.stringify(y);
const ms=inputs[5],bh=inputs[6],ii=inputs[7],ms26=inputs[8];
const nine=[[6,229],[8,200],[8,229],[145,218],[145,249],[248,295],[248,308],[249,295],[250,312]];
function prep(o,imports=[],orbit=null,extra=[]){let R=o.rowMap.length,own=o.rowMap.map(x=>x[0]),groups=o.ownerIDs.map((_,i)=>own.flatMap((x,j)=>x===i?[j]:[])),bits=own.map((_,i)=>bit(i));let s={R,own,groups,bits,live:o.live.slice(),p:o.pairHex.map(x=>BigInt("0x"+x)),ng:[],id:o.id,guard:o.guard};let flip=[];
if(orbit)for(let d of groups){let m=new Map(d.filter(a=>s.live[a]).map(a=>[o.rowMap[a][1],a]));for(let a of d)if(s.live[a]){flip[a]=m.get(o.rowMap[a][1].replace(/[01]/g,x=>x==="0"?"1":"0"));assert(flip[a]!==undefined,"flip")}}
function cut(a,b){s.p[a]&=~bits[b];s.p[b]&=~bits[a]}
for(let u of imports){assert(same(u.guard,o.guard),"guard");for(let a of u.removedRows||[]){s.live[a]=false;if(orbit)s.live[flip[a]]=false}for(let[a,h]of u.delta||[]){let v=BigInt("0x"+h);for(let b=0;b<R;b++)if(v&bits[b]){cut(a,b);if(orbit&&flip[a]!==undefined&&flip[b]!==undefined)cut(flip[a],flip[b]);}}for(let q of u.nogoods||[]){let t=q.rows;s.ng.push(t);if(orbit&&t.every(a=>flip[a]!==undefined))s.ng.push(t.map(a=>flip[a]));}}
if(orbit)for(let a of orbit.anchorRows)s.live[a]=false;
for(let [a,b]of extra)cut(a,b);
return s}
function stats(){return {scans:0,checks:0,nogoods:0,removed:0,cuts:0,nodes:0,branches:0}}
function domains(s){return s.groups.map(g=>g.filter(a=>s.live[a]))}
function close(s,t,use){for(;;){t.scans++;let d=domains(s);if(d.some(g=>!g.length))return false;let masks=d.map(g=>g.reduce((v,a)=>v|s.bits[a],0n)),change=false;for(let a=0;a<s.R;a++)if(s.live[a])for(let j=0;j<d.length;j++)if(j!==s.own[a]){t.checks++;if(!(s.p[a]&masks[j])){s.live[a]=false;t.removed++;change=true;break}}if(change)continue;if(use)for(let z of s.ng){t.nogoods++;if(z.some(a=>!s.live[a]))continue;let u=z.filter(a=>d[s.own[a]].length!==1);if(!u.length)return false;if(u.length===1){s.live[u[0]]=false;t.removed++;change=true}else if(u.length===2){let[a,b]=u;if(s.p[a]&s.bits[b]){s.p[a]&=~s.bits[b];s.p[b]&=~s.bits[a];t.cuts++;change=true}}}if(!change)return true}}
function clone(s){return {...s,live:s.live.slice(),p:s.p.slice()}}
function solve(root,use,cap){let t=stats(),start=root.live.filter(Boolean).length;let rootState=clone(root),initialOK=close(rootState,t,use),after=rootState.live.filter(Boolean).length;function f(s,already=false){if(t.nodes>=cap)return {status:"DECLINE"};t.nodes++;if(!already&&!close(s,t,use))return {status:"UNSAT"};let d=domains(s);if(d.every(g=>g.length===1))return {status:"SAT",rows:d.flat()};let g=d.filter(g=>g.length>1).sort((a,b)=>a.length-b.length||a[0]-b[0])[0];let masks=d.map(x=>x.reduce((v,a)=>v|s.bits[a],0n));function score(a){let z=0;for(let j=0;j<d.length;j++)if(j!==s.own[a]){let w=s.p[a]&masks[j];for(;w;w&=w-1n)z++}return z}let order=g.map(a=>[a,score(a)]).sort((a,b)=>b[1]-a[1]||a[0]-b[0]);for(let[a]of order){t.branches++;let h=clone(s);for(let b of g)if(a!==b)h.live[b]=false;let z=f(h);if(z.status!=="UNSAT")return z}return {status:"UNSAT"}}let z=initialOK?f(rootState,true):{status:"UNSAT"};if(z.rows){assert(z.rows.every(a=>root.live[a]),"row");assert(z.rows.every(a=>z.rows.every(b=>a===b||!!(root.p[a]&root.bits[b]))),"pair");assert(!root.ng.some(q=>q.every(a=>z.rows.includes(a))),"triple verify")}return {...z,start,after,t}}
const jobs=[];for(let i=0;i<5;i++){let o=inputs[i],im=[ms.jobs[i].combined,bh.jobs.find(x=>x.mode===true&&same(x.guard,o.guard)&&x.id===o.id)];for(let mode of ["base","pair-import","joint"]) {let s=prep(o,mode==="base"?[]:im);let z=solve(s,mode==="joint",128);jobs.push({i,id:o.id,guard:o.guard,mode,...z})}
if(i<3){let or=ii.tests[i],s=prep(o,im,or),t=stats();assert(close(s,t,false),"anchor close");assert(same(s.live.flatMap((v,a)=>v?[a]:[]),or.liveRows),"anchor IDs");let extra=i===1?[...nine,...ms26.results.shared[2].deletedPairs]:[];let a=prep(o,im,or,extra);jobs.push({i,id:o.id,guard:o.guard,mode:"joint-anchor",anchorRows:or.anchorRows,extraCuts:extra.length,...solve(a,true,128)})}}
function make(lines,relaxed=false){let rowMap=lines.flatMap((_,i)=>[1,2,3,4,5,6,...(i===0&&relaxed?[0]:[])].map(a=>[i,String(a)])),p=rowMap.map(([i,a])=>rowMap.reduce((v,[j,b],r)=>i!==j&&lines[i].every((x,k)=>!lines[j].includes(x)||((+a>>k&1)===(+b>>lines[j].indexOf(x)&1)))?v|bit(r):v,0n).toString(16));return {rowMap,pairHex:p,live:rowMap.map(()=>true),ownerIDs:lines.map((_,i)=>i),id:"NAE",guard:[]}}
let lines=[];for(let a=1;a<8;a++)for(let b=a+1;b<8;b++){let c=a^b;if(c>b)lines.push([a,b,c])}
let controls=[];for(let relax of [false,true]){let q=make(lines,relax),models=0;for(let w=0;w<128;w++)if(lines.every((e,i)=>{let a=e.reduce((v,x,k)=>v|((w>>(x-1)&1)<<k),0);return a!==0&&a!==7||relax&&i===0&&a===0}))models++;let z=solve(prep(q),true,10000);assert(z.status===(models?"SAT":"UNSAT"),"Fano");controls.push({relax,models,...z})}
return {jobs,controls};
}
const inputs=process.argv.slice(2).map(p=>JSON.parse(fs.readFileSync(p,'utf8')));if(inputs.length!==specs.length)throw Error('provide nine JSON inputs in listed order');console.log(JSON.stringify(run(inputs),null,2));
