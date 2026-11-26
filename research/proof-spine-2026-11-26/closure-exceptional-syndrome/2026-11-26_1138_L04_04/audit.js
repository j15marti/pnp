console.log(JSON.stringify((function audit(){
let checks=0;const check=(v)=>{checks++;if(!v)throw Error("assert "+checks)};
const f=s=>"1".repeat(s.length)+"0"+s, bin=n=>n.toString(2);
const rules=[];for(const q of [0,2,3])for(const a of [1,2])rules.push([q,a,0,a===1?2:3,a,a,1,1]);rules.push([3,0,0,4,0,0,0,0]);for(const a of [1,2])rules.push([4,a,a,4,a,a,0,0]);rules.push([4,0,0,1,0,0,2,2]);
const encode=(r,x,t)=>f(r.flat().map(a=>f(bin(a))).join(""))+f(x)+f(bin(t));
function parse(w){let p=0;function read(s,at){let j=at;while(s[j]==="1")j++;if(s[j]!=="0"||j+1+j-at>s.length)throw Error("frame");return [s.slice(j+1,j+1+j-at),j+1+j-at]}let z,x,T;[z,p]=read(w,p);[x,p]=read(w,p);[T,p]=read(w,p);if(!/^(0|1[01]*)$/.test(T)||!/^[0]*$/.test(w.slice(p)))throw Error("clock");let t=Number.parseInt(T,2);if(t>w.length**2)throw Error("cap");let a=[],i=0;while(i<z.length){let b;[b,i]=read(z,i);if(!/^(0|1[01]*)$/.test(b))throw Error("field");a.push(parseInt(b,2))}if(a.length%8)throw Error("rules");let R=[];for(let j=0;j<a.length;j+=8)R.push(a.slice(j,j+8));return{R,x,t,N:w.length}}
const init=(x,k,p)=>k===0&&p>=0&&p<x.length?Number(x[p])+1:0;
const delta=[-1,1,0], clone=x=>JSON.parse(JSON.stringify(x));
function run(src){let {R,x,t}=src,q=0,p=[0,0],mem=[new Map(),new Map()],rows=[];while(q!==1&&rows.length<t){let a=p.map((v,k)=>mem[k].get(v)??init(x,k,v));let r=R.findIndex(z=>z[0]===q&&z[1]===a[0]&&z[2]===a[1]);if(r<0)break;let z=R[r];rows.push({q,p:[...p],a,r,b:z.slice(4,6),next:z[3],d:z.slice(6,8)});for(let k=0;k<2;k++){mem[k].set(p[k],z[k+4]);p[k]+=delta[z[k+6]]}q=z[3]}return{rows,final:{q,p}}}
function perms(rows){let P=[0,1].map(k=>rows.map((_,i)=>i).sort((a,b)=>rows[a].p[k]-rows[b].p[k]||a-b)),I=P.map(p=>{let a=[];p.forEach((v,i)=>a[v]=i);return a});return{P,I}}
function local(s,tr){let {rows,final}=tr;if(!rows.length||rows.length>s.t||rows[0].q!==0||rows[0].p.some(v=>v!==0)||final.q!==1)return false;return rows.every((e,i)=>{let z=s.R[e.r],n=rows[i+1]??final;return z&&e.q!==1&&JSON.stringify(z)===JSON.stringify([e.q,...e.a,e.next,...e.b,...e.d])&&n.q===e.next&&e.p.every((p,k)=>Number.isInteger(p)&&Math.abs(p)<=i&&n.p[k]===p+delta[e.d[k]])})}
function direct(s,tr){if(!local(s,tr))return false;let mem=[new Map(),new Map()];for(const e of tr.rows)for(let k=0;k<2;k++){if((mem[k].get(e.p[k])??init(s.x,k,e.p[k]))!==e.a[k])return false;mem[k].set(e.p[k],e.b[k])}return true}
function sorted(s,tr,pr){if(!local(s,tr))return false;let {P,I}=pr,{rows}=tr,l=rows.length;for(let k=0;k<2;k++){if(P[k].length!==l||I[k].length!==l)return false;for(let j=0;j<l;j++){let i=P[k][j],r=I[k][j];if(!Number.isInteger(i)||i<0||i>=l||!Number.isInteger(r)||r<0||r>=l||I[k][i]!==j||P[k][r]!==j)return false;let e=rows[i],prior=j?rows[P[k][j-1]]:null;if(prior&&(prior.p[k]>e.p[k]||(prior.p[k]===e.p[k]&&P[k][j-1]>=i)))return false;if((prior&&prior.p[k]===e.p[k]?prior.b[k]:init(s.x,k,e.p[k]))!==e.a[k])return false}}return true}
let scales=[], tested=0;
for(let m of [4,8,16,32,64,128,256,512]){let x="01".repeat(m/2),t=2*m+2,s=parse(encode(rules,x,t)),no=parse(encode(rules,x.slice(0,-1)+"0",t)),late=parse(encode(rules,x,t-1)),tr=run(s),pr=perms(tr.rows);check(s.N===no.N&&s.N===late.N);check(tr.final.q===1&&tr.rows.length===t);check(run(no).final.q!==1&&run(late).final.q!==1);check(direct(s,tr)&&sorted(s,tr,pr));check(!direct(no,tr)&&!sorted(no,tr,pr));check(!direct(late,tr)&&!sorted(late,tr,pr));
let bad=clone(pr);bad.P[0][0]=bad.P[0][1];check(!sorted(s,tr,bad));bad=clone(pr);[bad.P[0][0],bad.P[0][1]]=[bad.P[0][1],bad.P[0][0]];bad.I[0]=[];bad.P[0].forEach((v,i)=>bad.I[0][v]=i);check(!sorted(s,tr,bad));
for(let i=0;i<tr.rows.length;i++){let e=clone(tr);e.rows[i].a[0]=(e.rows[i].a[0]+1)%3;check(!direct(s,e)&&!sorted(s,e,pr));tested++}
scales.push({m,N:s.N,steps:t,events:2*t,tableauCells:2*(t+1)*(2*t+m+1),labelNeighbors:2})}
let rogue=parse(encode([[0,0,0,2,1,0,2,2],[2,2,0,1,2,0,2,2]],"",2)),fake={rows:[{q:0,p:[0,0],a:[0,0],r:0,b:[1,0],next:2,d:[2,2]},{q:2,p:[0,0],a:[2,0],r:1,b:[2,0],next:1,d:[2,2]}],final:{q:1,p:[0,0]}};
check(local(rogue,fake));check(!direct(rogue,fake)&&!sorted(rogue,fake,perms(fake.rows)));check(run(rogue).final.q!==1);
return{checks,mutatedRecords:tested,scales,rogueLocallyLegalButGloballyInvalid:true,mode:"semantic record checks, explicit source simulation, not compiled SAT or circuit minimization"};
})(),null,2));
