// node BS17_check.js S23_inputs.json
const fs=require('fs');
function run(data){
let assertions=0;const ok=x=>{assertions++;if(!x)throw Error("assert "+assertions)};
const bit=(w,i)=>(w>>i)&1, full=(n)=>Array.from({length:2**n},(_,i)=>i);
function solve(n,O,pin,project,cap=10){
 const stat={scans:0,rows:0,forces:0,discovery:0,projectionRows:0,eliminated:0,peakCells:0,peakWidth:0,branches:0,verify:0,lookups:0};
 const pins=Array(n).fill(-1);if(pin>=0)pins[0]=pin;
 const init=O.map(o=>({v:o.t.slice(),a:full(o.t.length).filter(w=>!(o.bad||[0,7]).includes(w))}));
 const value=(v,p)=>v.reduce((s,x,i)=>s+(p[x]<<i),0);
 function updatePeak(F){stat.peakCells=Math.max(stat.peakCells,F.reduce((s,f)=>s+f.a.length+f.v.length,0));stat.peakWidth=Math.max(stat.peakWidth,...F.map(f=>f.v.length),0)}
 function close(F,p){
   let change=true;while(change){change=false;let G=[];
    for(const f of F){stat.scans++;let keep=f.v.map((v,i)=>p[v]<0?i:-1).filter(i=>i>=0);let a=[];
     for(const w of f.a){stat.rows++;if(f.v.some((v,i)=>p[v]>=0&&bit(w,i)!==p[v]))continue;a.push(keep.reduce((s,j,i)=>s+(bit(w,j)<<i),0))}
     if(!a.length)return null;
     let v=keep.map(i=>f.v[i]);a=[...new Set(a)];
     for(let i=0;i<v.length;i++){let b=bit(a[0],i);if(a.every(w=>bit(w,i)===b)){if(p[v[i]]>=0&&p[v[i]]!==b)return null;if(p[v[i]]<0){p[v[i]]=b;change=true;stat.forces++}}}
     if(a.length<2**v.length)G.push({v,a});
    }F=G;updatePeak(F);
   }return F
 }
 function dpll(F,p,limit){if(stat.branches>=limit)return {label:"UNKNOWN"};stat.branches++;F=close(F,p);if(!F)return {label:"UNSAT"};if(!F.length)return {label:"SAT",p:p.map(v=>v<0?0:v)};let count=Array(n).fill(0);for(const f of F)for(const v of f.v)count[v]++;let v=count.indexOf(Math.max(...count));for(const b of [0,1]){let t=p.slice();t[v]=b;let z=dpll(F,t,limit);if(z.label!=="UNSAT")return z;}return {label:"UNSAT"}}
 let F=close(init,pins),stack=[],ret,declineWidth=null,removed=new Set();
 while(project&&F&&F.length){
   let best=null;for(let v=0;v<n;v++){if(pins[v]>=0||removed.has(v))continue;let ids=[];let U=new Set();for(let i=0;i<F.length;i++){stat.discovery++;if(F[i].v.includes(v)){ids.push(i);for(const w of F[i].v)if(w!==v)U.add(w)}}if(!ids.length)continue;let u=[...U].sort((a,b)=>a-b);if(!best||u.length<best.u.length)best={v,ids,u};}
   if(!best)break;if(best.u.length>cap){declineWidth=best.u.length;break;}
   const {v,ids,u}=best;const chosen=ids.map(i=>F[i]);const sets=chosen.map(f=>new Set(f.a));const allowed=[],lift=new Map();let local=Array(n).fill(0);
   for(let w=0;w<2**u.length;w++){stat.projectionRows++;u.forEach((x,j)=>local[x]=bit(w,j));for(let b=0;b<2;b++){local[v]=b;let good=true;for(let i=0;i<chosen.length;i++){stat.lookups++;if(!sets[i].has(value(chosen[i].v,local))){good=false;break}}if(good){allowed.push(w);lift.set(w,b);break}}}
   if(!allowed.length){F=null;break;}stack.push({v,u,lift});removed.add(v);stat.eliminated++;let idset=new Set(ids);F=F.filter((f,i)=>!idset.has(i));if(allowed.length<2**u.length)F.push({v:u,a:allowed});updatePeak(F);F=close(F,pins);
 }
 if(!F)ret={label:"UNSAT"};else ret=dpll(F,pins.slice(),10000);
 if(ret.label==="SAT"){for(let i=stack.length-1;i>=0;i--){let s=stack[i];ret.p[s.v]=s.lift.get(value(s.u,ret.p));ok(ret.p[s.v]===0||ret.p[s.v]===1)}
  for(const o of O){stat.verify++;ok(!(o.bad||[0,7]).includes(value(o.t,ret.p)))}if(pin>=0)ok(ret.p[0]===pin)}
 return {...stat,declineWidth,label:ret.label,witness:ret.p?.join("")??null,liftRows:stack.reduce((s,x)=>s+x.lift.size,0)};
}
const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]].map(t=>({t}));
const controls=[...data,{id:"Fano",n:7,O:fano,pins:[-1,0,1]},{id:"Fano-delete",n:7,O:fano.slice(1),pins:[-1,0,1]}];
const jobs=[];for(const d of controls){for(let i=0;i<d.pins.length;i++){let p=d.pins[i];let direct=solve(d.n,d.O,p,false),combined=solve(d.n,d.O,p,true);ok(direct.label===combined.label);ok(direct.label===(d.id==="Fano"?"UNSAT":"SAT"));jobs.push({id:d.id,job:i,pin:p,direct,combined})}}
let quadratic=[];for(let k=1;k<=9;k++){let N=2**k,c=[0,0];for(let x=0;x<N;x++)for(let y=0;y<N;y++){let z=x&y,p=0;while(z){p^=1;z&=z-1;}c[p]++}ok(c[0]===2**(2*k-1)+2**(k-1));ok(c[1]===2**(2*k-1)-2**(k-1));quadratic.push({k,counts:c,minForbiddenPacketsForQ0:Math.ceil(c[1]/N),minForbiddenPacketsForQ1:Math.ceil(c[0]/N)})}
return {assertions,jobs,quadratic,cap:10,inputRef:"40881304c3fb5cff076fb8f52142a55d44b9291d"};
}
console.log(JSON.stringify(run(JSON.parse(fs.readFileSync(process.argv[2],'utf8'))),null,2));
