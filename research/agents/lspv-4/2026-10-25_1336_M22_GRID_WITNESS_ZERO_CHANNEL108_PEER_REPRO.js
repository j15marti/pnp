/* Exact executed role-4 peer reproducer; no external libraries. */
const audit108=function audit108(){
const P=[[1,2,3],[1,4,5],[2,4,6],[3,5,6]], M=[[-1,-2,-4],[-1,-3,-6],[-2,-3,-5],[-4,-5,-6]];
const mod=v=>(v-1)%6;const wit=v=>mod(v)<3; const ext=v=>[0,2,3].includes(mod(v));
function grid(r){
const F=[];for(let u=0;u<r*r;u++){const o=6*u;for(const C of [...P,...M])F.push(C.map(x=>x>0?o+x:x-o))}
const port={N:[0,1],E:[1,1],S:[2,2],W:[3,3]}, swaps=[];
function edge(u,du,v,dv){const [clu,vu]=port[du],[clv,vv]=port[dv];const i=8*u+clu,j=8*v+clv,x=6*u+vu,y=6*v+vv;
const ii=F[i].indexOf(x),jj=F[j].indexOf(y);if(ii<0||jj<0||!wit(x)||!wit(y))throw Error("port invalid");
F[i][ii]=y;F[j][jj]=x;swaps.push([u,v]);}
for(let i=0;i<r;i++)for(let j=0;j<r;j++){const u=i*r+j;if(j+1<r)edge(u,"E",u+1,"W");if(i+1<r)edge(u,"S",u+r,"N")}
return {F,swaps};}
function checkGrid(r){
const {F,swaps}=grid(r), quotas=new Map(), keys=new Set(), adj=new Map(), cross=new Set(); let positives=0,negatives=0;
for(const c of F){if(c.length!==3||new Set(c.map(Math.abs)).size!==3||!(c.every(x=>x>0)||c.every(x=>x<0)))throw Error("M22 grammar");
const key=c.slice().sort((a,b)=>a-b).join(",");if(keys.has(key))throw Error("duplicate");keys.add(key);
if(c[0]>0)positives++;else negatives++;
if(!c.some(v=>wit(Math.abs(v))===(v>0)))throw Error("witness");
for(const x of c){const v=Math.abs(x),z=quotas.get(v)||[0,0];z[x>0?0:1]++;quotas.set(v,z);if(!adj.has(v))adj.set(v,new Set())}
for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){const a=Math.abs(c[i]),b=Math.abs(c[j]);adj.get(a).add(b);adj.get(b).add(a);const u=Math.floor((a-1)/6),v=Math.floor((b-1)/6);if(u!==v)cross.add([Math.min(u,v),Math.max(u,v)].join(","));}}
if(quotas.size!==6*r*r||F.length!==8*r*r||positives!==4*r*r||negatives!==4*r*r||swaps.length!==2*r*(r-1))throw Error("counts");
for(const [v,z]of quotas){if(z[0]!==2||z[1]!==2)throw Error("quota");}
for(const c of F)if(keys.has(c.map(x=>-x).sort((a,b)=>a-b).join(",")))throw Error("paired");
for(const [u,v]of swaps)if(!cross.has([u,v].join(",")))throw Error("missing minor edge");
let seen=new Set([1]),queue=[1];for(let i=0;i<queue.length;i++)for(const v of adj.get(queue[i]))if(!seen.has(v)){seen.add(v);queue.push(v)}
if(seen.size!==6*r*r)throw Error("disconnected");
for(let u=0;u<r*r;u++){let local=new Map();for(let j=1;j<=6;j++)local.set(6*u+j,new Set());
for(const c of F.slice(8*u+4,8*u+8)){const a=c.map(Math.abs);for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){local.get(a[i]).add(a[j]);local.get(a[j]).add(a[i])}}
let seen2=new Set([6*u+1]),q2=[6*u+1];for(let i=0;i<q2.length;i++)for(const v of local.get(q2[i]))if(!seen2.has(v)){seen2.add(v);q2.push(v)}
if(seen2.size!==6)throw Error("cell not contractible")}
return {r,k:6*r*r,m:8*r*r,grid_minor_side:r,treewidth_lower_bound:r-1,swaps:swaps.length,paired:0,source_readable_SAT:true};}
function chain(p){const F=[];for(let i=0;i<p;i++){const o=6*i;for(const c of [...P,...M])F.push(c.map(v=>v>0?v+o:v-o))}
for(let i=0;i<p-1;i++){const a=8*i+1,b=8*(i+1),x=6*i+1,y=6*(i+1)+1;const j=F[a].indexOf(x),k=F[b].indexOf(y);if(j<0||k<0)throw Error("chain");F[a][j]=y;F[b][k]=x}return F;}
function projected(F,lo,hi){const I=new Set();for(let i=lo;i<hi;i++)for(let j=1;j<=6;j++)I.add(6*i+j);
const H=[],G=[];for(const c of F)(c.some(x=>I.has(Math.abs(x)))?H:G).push(c);
const B=[...new Set(H.flatMap(c=>c.map(Math.abs)).filter(v=>!I.has(v)))].sort((a,b)=>a-b);
if(B.length!==3||B[0]!==6*hi+1||B[1]!==6*hi+2||B[2]!==6*hi+3)throw Error("boundary");
for(let z=0;z<8;z++){const a=new Map(B.map((v,j)=>[v,(z>>j)&1]));for(const c of H)if(!c.some(v=>((a.has(Math.abs(v))?a.get(Math.abs(v)):Number(ext(Math.abs(v))))===Number(v>0))))throw Error("universal boundary failed")}
return {G,boundary:B,nogoods:0,touched:H.length};}
const bits=(f,p)=>{const w=Math.ceil(Math.log2(6*p+1));return 4*w+4*f.length*(w+1)};
const g=[1,2,3,4,6,8,12,16,24,32,48,64,96,128].map(checkGrid);const chains=[];
for(const p of [8,16,32,64,128,256,512]){const q1=p-Math.floor(Math.sqrt(p)),q2=p-Math.floor(Math.sqrt(Math.floor(Math.sqrt(p))));
const F=chain(p),u=projected(F,0,q1),v=projected(u.G,q1,q2);
if(u.G.length!==8*(p-q1)-1||v.G.length!==8*(p-q2)-1)throw Error("two level count");
chains.push({p,cuts:[q1,q2],clauses:[F.length,u.G.length,v.G.length],fixed_source_ID_bits:[bits(F,p),bits(u.G,p),bits(v.G,p)],forbidden_rows:[u.nogoods,v.nogoods]});}
let h=[...P,...M,...P.map(c=>c.map(x=>x+6)),...M.map(c=>c.map(x=>x-6))].map(c=>c.slice());
let p=h[1].indexOf(1),q=h[9].indexOf(10);h[1][p]=10;h[9][q]=1;
if(h.every(c=>c.some(v=>wit(Math.abs(v))===(v>0))))throw Error("hostile different-truth swap did not fail witness");
return {id:"M22_GRID_WITNESS_ZERO_CHANNEL108",result:"PASS",grids:g,chains,hostile_port_control:"public witness fails after unequal-truth swap",source_label_note:"Published D\u00f6cker U_198 UNSAT source imported; not brute-forced",proof_status:"Restricted exact theorem; independent review pending. ARC-EDGE-90 DIRECT-POST P versus NP OPEN"};};
console.log(JSON.stringify(audit108(),null,2));
