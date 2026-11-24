function experiment(){
const bit=i=>1n<<BigInt(i),hi=x=>x.toString(2).length-1;
function red(x,B){while(x&&B.has(hi(x)))x^=B.get(hi(x));return x}
function add(x,B){x=red(x,B);if(x)B.set(hi(x),x)}
function bas(xs){let b=new Map;for(let x of xs)add(x,b);return b}
function par(x){let p=0;while(x){x&=x-1n;p^=1}return p}
function solve(rows,vals){let B=new Map;for(let i=0;i<rows.length;i++){let r=rows[i],v=vals[i];while(r&&B.has(hi(r))){let [s,w]=B.get(hi(r));r^=s;v^=w}if(r)B.set(hi(r),[r,v]);else if(v)throw Error("lift")}let z=0n;for(let i of [...B.keys()].sort((a,b)=>a-b)){let [r,v]=B.get(i);if(par(r&z)^v)z|=bit(i)}return z}
const C=c=>[0n,0n,c],val=(f,z)=>f[2]^par(f[0]&z)^(par(f[1]&z)<<1);
function mask(b,z){let m=15;for(let f of b)m&=~(1<<val(f,z));return m}
function xm(a,b){let r=0;for(let i=0;i<4;i++)for(let j=0;j<4;j++)if((a>>i&1)&&(b>>j&1))r|=1<<(i^j);return r}
function valid(bs,z,brute=false){for(let b of bs){let D=b.bundles.map(x=>mask(x,z));if(D.some(x=>!x))return false;if(b.cycle){if(brute){let ok=false;function go(i,s){if(ok)return;if(i===D.length){ok=s===0;return}for(let j=0;j<4;j++)if(D[i]>>j&1)go(i+1,s^j)}go(0,0);if(!ok)return false}else if(!(D.reduce(xm,1)&1))return false}}return true}
function lift(bs,z){for(let b of bs){let D=b.bundles.map(x=>mask(x,z)),h=[1],s=0,ds=[];if(b.cycle){for(let m of D)h.push(xm(h.at(-1),m));for(let i=D.length-1;i>=0;i--){let j=[0,1,2,3].find(j=>(D[i]>>j&1)&&(h[i]>>(s^j)&1));if(j===undefined)throw Error("lift2");ds.unshift(j);s^=j}}else ds=[Math.log2(D[0]&-D[0])];s=0;for(let i=0;i<ds.length;i++){let t=s^ds[i];for(let f of b.bundles[i])if((s^t)===val(f,z))throw Error("exclusion");s=t}if(b.cycle&&s)throw Error("cycle")}}
function close(src){let bs=src.map(b=>({cycle:b.cycle,bundles:b.bundles.map(x=>x.map(f=>f.slice()))})),pins=[],probes=0;
while(true){let next=null;for(let b of bs){for(let bundle of b.bundles){let rows=[...bas(bundle.flatMap(f=>f.slice(0,2))).values()];if(rows.length>4)continue;let good=[];for(let w=0;w<1<<rows.length;w++){probes++;let z=solve(rows,rows.map((_,i)=>w>>i&1));if(mask(bundle,z))good.push(w)}if(!good.length)return {bad:true,pins,probes};for(let u=1;u<1<<rows.length;u++){let a=par(BigInt(u&good[0]));if(good.every(w=>par(BigInt(w&u))===a)){let r=0n;rows.forEach((x,i)=>{if(u>>i&1)r^=x});next=[r,a];break}}if(next)break}if(next)break;if(b.bundles.every(x=>x.every(f=>!f[0]&&!f[1]))&&!valid([b],0n))return {bad:true,pins,probes}}if(!next)return {bs,pins,probes};let [r,a]=next,p=bit(hi(r));pins.push(next);for(let b of bs)for(let bundle of b.bundles)for(let f of bundle)for(let i=0;i<2;i++)if(f[i]&p){f[i]^=r;f[2]^=a<<i}}
}
function run(src,d){let cl=close(src),{pins,probes}=cl,stats={pins:pins.length,probes,width:0,peak:0,attempts:0,merges:0};if(cl.bad)return {count:0n,...stats};let steps=[];for(let b of cl.bs)b.bundles.forEach((x,j)=>x.forEach((f,i)=>steps.push({f,end:i===x.length-1,last:j===b.bundles.length-1,cycle:b.cycle})));
let rows=steps.flatMap(s=>s.f.slice(0,2)),B=new Map,deps=[];
rows.forEach((r,i)=>{let c=bit(i);while(r&&B.has(hi(r))){let [s,t]=B.get(hi(r));r^=s;c^=t}if(r)B.set(hi(r),[r,c]);else deps.push(c)});
let cols=rows.map((_,i)=>{let c=0n;deps.forEach((r,j)=>{if(r&bit(i))c|=bit(j)});return c}),suf=[ ];suf[steps.length]=new Map;
for(let i=steps.length-1;i>=0;i--){suf[i]=new Map(suf[i+1]);add(cols[2*i],suf[i]);add(cols[2*i+1],suf[i])}
let pre=new Map,states=new Map([["0/0/1",{p:0n,F:0,R:1,c:1n,z:0n,H:new Map}]]);stats.peak=1;
for(let i=0;i<steps.length;i++){let s=steps[i],out=new Map;add(cols[2*i],pre);add(cols[2*i+1],pre);stats.width=Math.max(stats.width,pre.size+suf[i+1].size-deps.length);
for(let st of states.values())for(let y=0;y<4;y++){stats.attempts++;let p=st.p^(y&1?cols[2*i]:0n)^(y&2?cols[2*i+1]:0n);if(red(p,suf[i+1]))continue;let F=st.F|1<<(y^s.f[2]),R=st.R;if(s.end){let D=15^F;if(!D)continue;if(s.cycle){R=xm(R,D);if(s.last&&!(R&1))continue}F=0;if(s.last)R=1}let key=p+"/"+F+"/"+R,z=st.z|(BigInt(y)<<BigInt(2*i)),old=out.get(key);if(!old)out.set(key,{p,F,R,c:st.c,z,H:new Map(st.H)});else{stats.merges++;old.c+=st.c;add(old.z^z,old.H);for(let v of st.H.values())add(v,old.H)}}states=out;stats.peak=Math.max(stats.peak,states.size)}
let st=states.get("0/0/1");if(!st)return {count:0n,...stats};let free=d-pins.length-B.size,z=solve([...pins.map(x=>x[0]),...rows],[...pins.map(x=>x[1]),...rows.map((_,i)=>Number(st.z>>BigInt(i)&1n))]);lift(src,z);return {count:st.c*(1n<<BigInt(free)),rank:st.H.size+free,z,...stats}}
let seed=20261124;function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>8)%n}let totals={tests:0,sat:0,unsat:0,pins:0,probes:0,attempts:0,merges:0,hullChecks:0,verifiedLifts:0,maxWidth:0,peak:0},scales=[];
function check(bs,d,want=null,r=null){let a=run(bs,d);if(want===null){let zs=[];for(let z=0;z<1<<d;z++)if(valid(bs,BigInt(z),true))zs.push(BigInt(z));want=BigInt(zs.length);r=zs.length?bas(zs.map(z=>z^zs[0])).size:null}if(a.count!==want)throw Error("count "+a.count+" != "+want);if(want){if(!valid(bs,a.z))throw Error("bad lift");totals.verifiedLifts++;if(r!==null){if(a.rank!==r)throw Error("rank "+a.rank+" "+r);totals.hullChecks++}}totals.tests++;totals[want?"sat":"unsat"]++;for(let k of ["pins","probes","attempts","merges"])totals[k]+=a[k];totals.maxWidth=Math.max(totals.maxWidth,a.width);totals.peak=Math.max(totals.peak,a.peak);return a}
for(let t=0;t<120;t++){let d=2+rnd(5),bs=[];for(let j=0;j<1+rnd(3);j++){let cycle=!!rnd(2),bundles=[];for(let k=0;k<(cycle?3+rnd(2):1);k++){let f=[];for(let i=0;i<1+rnd(5);i++)f.push([BigInt(rnd(1<<d)),BigInt(rnd(1<<d)),rnd(4)]);bundles.push(f)}bs.push({cycle,bundles})}check(bs,d)}
check([{cycle:false,bundles:[[C(0),C(1),C(2),[bit(0),bit(0),3]]]}],2,2n,1);
function family(n,bad){let bundles=[];for(let i=0;i<n;i++){let a=bad?0n:bit(2*i),b=bit(2*i+1);bundles.push([C(2),C(3),[a,a,bad?1:2],[b,b,2]])}bundles.push([C(0),C(2),C(3)]);return [{cycle:true,bundles}]}
for(let n of [2,3,4])for(let bad of [false,true])check(family(n,bad),2*n);
for(let n of [8,16,32,64])for(let bad of [false,true]){let a=check(family(n,bad),2*n,bad?0n:4n**BigInt(n)-3n**BigInt(n),bad?null:2*n);scales.push({n,bad,count:String(a.count),width:a.width,peak:a.peak,attempts:a.attempts})}
return {seed:20261124,totals,scales}}
console.log(JSON.stringify(experiment(),null,2));
