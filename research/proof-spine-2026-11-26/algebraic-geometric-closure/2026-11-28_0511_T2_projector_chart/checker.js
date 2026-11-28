// T2 checked native chart / rank lift and rank-two projector checker. Usage: node checker.js compile.js benchmarks.json
const fs=require('node:fs');const src=fs.readFileSync(process.argv[2],'utf8');const compile=new Function('return '+src.slice(src.indexOf('function compile'),src.indexOf('function auditLocal')))();
function sha(s){const H=[],K=[];for(let p=2;K.length<64;p++){if(Array.from({length:Math.floor(Math.sqrt(p))-1},(_,i)=>i+2).some(d=>p%d===0))continue;if(H.length<8)H.push((Math.sqrt(p)%1*4294967296)|0);K.push((Math.cbrt(p)%1*4294967296)|0)}const a=new Uint8Array(Math.ceil((s.length+9)/64)*64);for(let i=0;i<s.length;i++)a[i]=s.charCodeAt(i);a[s.length]=128;let n=s.length*8;for(let i=0;i<8;i++){a[a.length-1-i]=n%256;n=Math.floor(n/256)}const R=(x,b)=>(x>>>b)|(x<<(32-b));for(let j=0;j<a.length;j+=64){const w=new Int32Array(64);for(let i=0;i<16;i++)w[i]=(a[j+4*i]<<24)|(a[j+4*i+1]<<16)|(a[j+4*i+2]<<8)|a[j+4*i+3];for(let i=16;i<64;i++){let x=w[i-15],y=w[i-2];w[i]=(w[i-16]+(R(x,7)^R(x,18)^(x>>>3))+w[i-7]+(R(y,17)^R(y,19)^(y>>>10)))|0}let [b,c,d,e,f,g,h,k]=H;for(let i=0;i<64;i++){let t=(k+(R(f,6)^R(f,11)^R(f,25))+((f&g)^(~f&h))+K[i]+w[i])|0,u=((R(b,2)^R(b,13)^R(b,22))+((b&c)^(b&d)^(c&d)))|0;[b,c,d,e,f,g,h,k]=[(t+u)|0,b,c,d,(e+t)|0,f,g,h]}[b,c,d,e,f,g,h,k].forEach((x,i)=>H[i]=(H[i]+x)|0)}return H.map(x=>(x>>>0).toString(16).padStart(8,"0")).join("")}
function native(G){
const p=Array.from({length:G.types.length*4},(_,i)=>i),sg=new Uint8Array(p.length);let bad=false;
function find(i){if(p[i]===i)return [i,0];let [r,b]=find(p[i]);sg[i]^=b;p[i]=r;return [r,sg[i]]}
function union(i,j,b){let [a,x]=find(i),[c,y]=find(j);if(a===c){if((x^y)!==b)bad=true;return}if(a>c){[a,c]=[c,a];[x,y]=[y,x]}p[c]=a;sg[c]=x^y^b}
for(let [a,b,s] of G.edges)union(a,b,s);G.types.forEach((t,v)=>{if(t==="E")for(let j=1;j<4;j++)union(4*v,4*v+j,0)});
let roots=[...new Set(p.map((_,i)=>find(i)[0]))],idx=new Map(roots.map((r,i)=>[r,i])),n=roots.length,map=p.map((_,i)=>{let[r,s]=find(i);return [idx.get(r),s]}),rows=[],unique=new Map();
G.types.forEach((t,v)=>{if(t!=="B")return;let lits=map.slice(v*4,v*4+4),ids=[...new Set(lits.map(x=>x[0]))].sort((a,b)=>a-b),words=[];for(let w=0;w<2**ids.length;w++)if(lits.reduce((z,[i,s])=>z+(((w>>ids.indexOf(i))&1)^s),0)===2)words.push(w);let k=JSON.stringify([ids,words]);if(!unique.has(k))unique.set(k,{v,ids,words,lits});rows.push({v,lits})});
if(bad||G.edges.some(([a,b,s])=>map[a][0]!==map[b][0]||(map[a][1]^map[b][1])!==s)||G.types.some((t,v)=>t==="E"&&map.slice(4*v,4*v+4).some(q=>q[0]!==map[4*v][0]||q[1]!==map[4*v][1])))throw Error("transport");
return {G,n,roots,map,rows,tables:[...unique.values()]}
}
function solve(C,pins,cap=1500000){
let work=0,checks=0,nodes=0,trace=[],peak=0;const freq=Array(C.n).fill(0);for(let r of C.tables)for(let i of r.ids)freq[i]++;
function prop(x){let changed=true;while(changed){changed=false;for(let {v,ids,words} of C.tables){if(++work>cap)return -2;let W=words.filter(w=>ids.every((i,j)=>{checks++;return x[i]===-1||x[i]===((w>>j)&1)}));if(!W.length)return v;for(let j=0;j<ids.length;j++)if(x[ids[j]]===-1&&W.every(w=>((w>>j)&1)===((W[0]>>j)&1))){x[ids[j]]=(W[0]>>j)&1;changed=true}}}return -1}
function go(x,depth){nodes++;peak=Math.max(peak,depth);let r=prop(x);if(r===-2)return {kind:"UNKNOWN"};if(r>=0){trace.push(["L",r]);return {kind:"NO"}}let i=-1;for(let j=0;j<C.n;j++)if(x[j]===-1&&(i<0||freq[j]>freq[i]))i=j;if(i<0)return {kind:"YES",x:[...x]};trace.push(["B",i]);for(let b=0;b<2;b++){let y=x.slice();y[i]=b;let t=go(y,depth+1);if(t.kind!=="NO")return t}return {kind:"NO"}}
let x=new Int8Array(C.n).fill(-1);for(let [i,b]of pins){if(x[i]>=0&&x[i]!==b)return {kind:"NO",immediate:true};x[i]=b}
let ans=go(x,1);return {...ans,work,checks,nodes,peak,trace}
}
function verify(C,pins,R){
if(R.kind==="YES"){let x=R.x,y=C.map.map(([i,s])=>x[i]^s);return {ok:C.G.edges.every(([a,b,s])=>(y[a]^y[b])===s)&&C.G.types.every((t,v)=>{let q=y.slice(4*v,4*v+4);return t==="E"?q.every(x=>x===q[0]):q.reduce((a,b)=>a+b,0)===2})&&pins.every(([i,b])=>x[i]===b),checks:C.G.edges.length+C.G.types.length}}
if(R.kind!=="NO")return {ok:false,checks:0};if(R.immediate)return {ok:pins.some(([i,b],j)=>pins.slice(0,j).some(([h,c])=>h===i&&b!==c)),checks:pins.length};
let pos=0,count=0;function replay(x){let change=true,conflict=false;while(change&&!conflict){change=false;for(let r of C.tables){let possible=[];for(let w of r.words){count++;let ok=true;for(let j=0;j<r.ids.length;j++)if(x[r.ids[j]]!==-1&&x[r.ids[j]]!==((w>>j)&1)){ok=false;break}if(ok)possible.push(w)}if(!possible.length){conflict=true;break}for(let j=0;j<r.ids.length;j++){let id=r.ids[j];if(x[id]!==-1)continue;let a=0,b=0;for(let w of possible){if((w>>j)&1)b++;else a++}if(!a||!b){x[id]=a?0:1;change=true}}}}
let e=R.trace[pos++];if(!e)return false;if(e[0]==="L")return conflict;if(conflict||e[0]!=="B"||x[e[1]]!==-1)return false;for(let b=0;b<2;b++){let y=x.slice();y[e[1]]=b;if(!replay(y))return false}return true}
let x=new Int8Array(C.n).fill(-1);for(let [i,b]of pins)x[i]=b;return {ok:replay(x)&&pos===R.trace.length,checks:count}
}
function chart(C,seeds){
let P=new Map(),bit=i=>1n<<BigInt(i),checks=0,eqs=C.rows.map(({lits})=>lits.reduce(([x,b],[i,s])=>[x^bit(i),b^s],[0n,0]));
for(let [a,b,h] of seeds){let[i,s]=C.map[a],[j,t]=C.map[b];eqs.push([bit(i)^bit(j),h^s^t])}
function red(x,b){for(let [k,v]of P){checks++;if(x&k){x^=v[0];b^=v[1]}}return [x,b]}
for(let[x,b]of eqs){[x,b]=red(x,b);if(!x){if(b)throw Error("affine contradiction");continue}let k=x&-x;for(let v of P.values())if(v[0]&k){v[0]^=x;v[1]^=b}P.set(k,[x,b])}
let forms=Array.from({length:C.n},(_,i)=>red(bit(i),0));for(let [x,b] of eqs){let a=0n,c=b;for(let i=0;i<C.n;i++)if(x&bit(i)){a^=forms[i][0];c^=forms[i][1]}if(a||c)throw Error("chart lift")}
let free=Array.from({length:C.n},(_,i)=>i).filter(i=>!P.has(bit(i)));if(free.some(i=>forms[i][0]!==bit(i)||forms[i][1]))throw Error("section");
let R=C.rows.map(({lits})=>lits.map(([i])=>forms[i][0]));function add(p,x){while(x){checks++;let k=x&-x;if(p.has(k))x^=p.get(k);else{p.set(k,x);break}}}
let a=[],b=[],L=new Map(),Q=new Map();for(let i=0;i<R.length;i++){for(let x of R[i])add(L,x);a[i]=L.size}for(let i=R.length-1;i>=0;i--){for(let x of R[i])add(Q,x);b[i]=Q.size}
let widths=a.slice(0,-1).map((x,i)=>x+b[i+1]-L.size);
let map={carrier_root_ports:C.roots,forms:forms.map(([x,b])=>[x.toString(16),b]),free,port_map:C.map},residual={rows:C.rows,forms:map.forms,free};let mapSha=sha(JSON.stringify(map)+"\n"),resSha=sha(JSON.stringify(residual)+"\n");return {rank:P.size,free:free.length,max:Math.max(0,...widths),sum:widths.reduce((a,b)=>a+b,0),widths,checks,mapSha,resSha}
}
function spectral2(a,b,c){
const dot=(x,y)=>x.reduce((s,t,i)=>s+t*y[i],0),aa=dot(a,a),bb=dot(b,b),ab=dot(a,b),D=aa*bb-ab*ab;if(!D)return null;let u=dot(a,c),v=dot(b,c),alpha=bb*u-ab*v,beta=aa*v-ab*u;
let r=c.map((x,i)=>D*x-alpha*a[i]-beta*b[i]);if([D,alpha,beta,...r].some(x=>!Number.isSafeInteger(x))||D<0||dot(a,r)||dot(b,r))throw Error("projection");
let q=dot(r,r);return {D,alpha,beta,r,l1:r.reduce((a,b)=>a+Math.abs(b),0),l2num:a.length*q,l2den:D*D}
}
function run(inst,expected,seed=[]){
let compiled=compile(inst),G=compiled.network,bytes=JSON.stringify(G)+"\n",digest=sha(bytes),N=8*bytes.length;if(expected&&digest!==expected)throw Error("sha");
let C=native(G),gauge=[[C.map[0][0],C.map[0][1]]],baseline=solve(C,gauge),bv=verify(C,gauge,baseline);if(!bv.ok)throw Error("baseline");
let parents=[];for(let [a,b,h]of seed){let [i,s]=C.map[a],[j,t]=C.map[b],rhs=h^s^t,pins=[[i,s],[j,s^rhs^1]],R=solve(C,pins,500000),V=verify(C,pins,R);if(R.kind!=="NO"||!V.ok)throw Error("seed");parents.push({ports:[a,b,h],pins,R,V})}
let base=chart(C,[]),hybrid=chart(C,seed),ablation=seed.map((_,i)=>chart(C,seed.filter((_,j)=>i!==j)));const id="STRICT-EB4-v1:sha256:"+digest;
for(let z of [base,hybrid,...ablation]){z.residual_id="RESIDUAL-v1:sha256:"+sha(JSON.stringify(["PNP-RESIDUAL-v1",id,"EMPTY","EB-AFFINE-CARRIER-CHART-v1",z.resSha,z.mapSha])+"\n");delete z.widths}
return {problem_id:"STRICT-EB4-v1",instance:(inst.id.startsWith("SAT")||inst.id.startsWith("NO")?inst.id:"EB-"+inst.id)+"@"+digest.slice(0,12),instance_id:id,original_N_bits:N,source_pin:"0c14cdc57925788cf7a451dcd5aa171dce860f2c / e315349cd6c1fe3fa696504859f28312f6aab69a / 21b9d53fb8166c819b24e708656c742cd3c24f10",guard_id:"EMPTY",residual_id:"ROOT",original_ids:{vertices:[0,G.types.length-1],ports:[0,4*G.types.length-1],edges:[0,G.edges.length-1]},cnfSha:sha(inst.dimacs),cnfN:inst.dimacs.length*8,mapSha:sha(JSON.stringify(compiled.source_map)+"\n"),n:C.n,baseline,bv,parents,base,hybrid,ablation}
}
const data=JSON.parse(fs.readFileSync(process.argv[3],'utf8'));const instances=[data.instances.find(x=>x.id==='JOINT-24'),data.instances.find(x=>x.id==='RANDOM-3CNF-40'),{"id":"SAT-1","nvars":3,"dimacs":"p cnf 3 2\n1 2 3 0\n-1 2 -3 0\n"},{"id":"SAT-2","nvars":2,"dimacs":"p cnf 2 2\n1 0\n-1 2 0\n"},{"id":"NO-1","nvars":1,"dimacs":"p cnf 1 2\n1 0\n-1 0\n"}];const expected=["e84a0ab6dc6f74deb8daeea2ccd41cca90e3d1294411877a813471760897c209","8a18e86479df916ea5c7fdd760ccd561e4fea3737a94517ab8dc2d28cc7e6bdb"];const seeds=[[0,433,0],[0,561,0],[0,960,1],[0,969,0]];console.log(JSON.stringify(instances.map((x,i)=>run(x,expected[i],i===0?seeds:[])),null,2));
