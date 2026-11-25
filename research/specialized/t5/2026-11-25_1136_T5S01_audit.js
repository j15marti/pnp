"use strict";
const audit=function(){
const A=[0,1,2,3,4], R=(a,b)=>[1,3].includes((b-a+5)%5), C=(a,b,c)=>(R(a,b)&&R(b,c)&&R(c,a))||(R(a,c)&&R(c,b)&&R(b,a));
let checks=0;const ok=(v)=>{checks++;if(!v)throw Error("assertion "+checks)};
const tuples=[];let ordered=0,q=0,p=0;
for(const a of A)for(const b of A)for(const c of A){if(C(a,b,c))tuples.push([a,b,c]);if(new Set([a,b,c]).size===3&&R(a,b)!==R(a,c))ordered++;if(R(a,b)!==R(a,c))q++;if(R(a,b)&&R(a,c))p++;ok(C(a,b,c)===(new Set([a,b,c]).size===3&&A.some(i=>[a,b,c].every(v=>[i,(i+1)%5,(i+2)%5].includes(v)))))}
ok(tuples.length===30&&ordered===40&&q===60&&p===20);
const head=(a,b)=>A.filter(c=>C(a,b,c));
for(const a of A)for(const b of A)ok((head(a,b).length>0)===(a!==b));
let frames=0;
for(let i=0;i<3125;i++){let t=i,f=[];for(let j=0;j<5;j++){f.push(t%5);t=Math.floor(t/5)}const valid=A.every(j=>C(f[j],f[(j+1)%5],f[(j+2)%5]));const dihedral=[1,4].some(d=>A.every(j=>f[j]===(f[0]+d*j)%5));ok(valid===dihedral);if(valid)frames++}
for(const a of A){const d=[2,3,4].map(j=>head(j,a).length).reduce((x,y)=>x*y,1);ok(d===(a<2?2:0))}
for(let a=0;a<2;a++)for(let b=0;b<2;b++){ok(C(2,a,b)===(a!==b));for(let x=0;x<2;x++){let n=0;for(const y of A)for(const z of A)if(C(1,2,y)&&C(0,1,z)&&C(4,a,y)&&C(3,b,z)&&C(x,y,z))n++;ok(n===(x===(a|b)?1:0))}}
let eqRows=0;
for(const x of A)for(const y of A){let n=0;for(let i=0;i<625;i++){let t=i,v=[];for(let j=0;j<4;j++){v.push(t%5);t=Math.floor(t/5)}if(new Set(v).size===4&&v.every(a=>a!==x&&a!==y)){n++;eqRows++}}ok(n===(x===y?24:0))}
function build(gates,input){
const values=[...A],cl=[];const v=x=>{values.push(x);return values.length-1};const add=(...a)=>{ok(new Set(a).size===3);cl.push(a)};
for(let i=0;i<5;i++)add(i,(i+1)%5,(i+2)%5);
const wire=b=>{let id=v(b);for(let j=2;j<5;j++)add(j,id,v(head(j,b)[0]));return id};
const ids=input.map(wire);
for(const [op,i,j] of gates){const a=values[ids[i]],b=j===undefined?0:values[ids[j]];const x=wire(op==="N"?1-a:a|b);if(op==="N")add(2,ids[i],x);else {const y=v(a?0:3),z=v(b?2:4);add(1,2,y);add(0,1,z);add(4,ids[i],y);add(3,ids[j],z);add(x,y,z)}ids.push(x)}
add(0,2,ids.at(-1));return {cl,values,ids}}
function split(F){const cl=[],values=[],copies=F.values.map(()=>[]);const v=x=>{values.push(x);return values.length-1};const add=(...a)=>cl.push(a);for(const c of F.cl)add(...c.map(i=>{const a=v(F.values[i]);copies[i].push(a);return a}));const puncture=cl.length-1;
for(const L of copies)for(let j=1;j<L.length;j++){const x=L[j-1],y=L[j],is=A.filter(a=>a!==values[x]).map(v);const edge=(a,b)=>add(a,b,v(head(values[a],values[b])[0]));for(let i=0;i<4;i++){edge(x,is[i]);edge(y,is[i]);for(let h=0;h<i;h++)edge(is[i],is[h])}}
return {cl,values,copies,puncture}}
let scans=0;
function gac(F,skip=-1,pins=false){const d=F.values.map(a=>pins?1<<a:31);let change=true;while(change){change=false;for(let i=0;i<F.cl.length;i++){if(i===skip)continue;const c=F.cl[i],s=[0,0,0];scans++;for(const t of tuples)if(t.every((a,j)=>d[c[j]]&(1<<a)))for(let j=0;j<3;j++)s[j]|=1<<t[j];for(let j=0;j<3;j++){let x=d[c[j]]&s[j];if(x!==d[c[j]]){d[c[j]]=x;change=true}if(!x)return null}}}return d}
let seed=20261125;const rand=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};
const cases=[[["N",0],["O",0,2]],[["N",0],["O",0,2],["N",3]]];
for(let k=0;k<32;k++){let g=[];for(let j=0;j<6;j++){let n=2+j;g.push(rand(3)===0?["N",rand(n)]:["O",rand(n),rand(n)])}cases.push(g)}
let sat=0,unsat=0,lifts=0,near=0,maxN=0,maxM=0,degree=0;
const rows=[];
for(const source of cases){ // source wires 0,1; insert guard as input 2 and renumber gates
const g=source.map(([o,i,j])=>o==="N"?[o,i<2?i:i+1]:[o,i<2?i:i+1,j<2?j:j+1]);const out=2+g.length;g.push(["N",out],["N",2],["O",out+1,out+2],["N",out+3]);let yes=false;
for(let i=0;i<8;i++){const input=[i&1,(i>>1)&1,(i>>2)&1];const src=[...input.slice(0,2)];for(const [op,a,b] of source)src.push(op==="N"?1-src[a]:src[a]|src[b]);const expected=src.at(-1)&input[2];const f=build(g,input);const h=split(f);maxN=Math.max(maxN,h.values.length);maxM=Math.max(maxM,h.cl.length);const bad=h.cl.map((c,j)=>C(...c.map(x=>h.values[x]))?-1:j).filter(j=>j>=0);ok(bad.length===(expected?0:1));if(!expected)ok(bad[0]===h.puncture);else{yes=true;lifts++}
for(let j=0;j<f.values.length;j++)ok(h.copies[j].every(x=>h.values[x]===f.values[j]));
if(i===0){near++;const pairs=new Set(),deg=h.values.map(()=>0);for(const c of h.cl){for(const a of c)deg[a]++;for(let a=0;a<3;a++)for(let b=a+1;b<3;b++){const key=[c[a],c[b]].sort((x,y)=>x-y).join(",");ok(!pairs.has(key));pairs.add(key)}}degree=Math.max(degree,...deg);ok(Math.max(...deg)<=9);ok(gac(h).every(x=>x===31));ok(gac(h,h.puncture).every(x=>x===31));ok(gac(h).every(x=>x===31));ok(gac(h,h.puncture,true)!==null);ok(gac(h,-1,true)===null)}
if(expected)ok(gac(h,-1,true)!==null);
}
if(yes)sat++;else unsat++;rows.push({source,sat:yes})}
return {checks,frames,eqRows,sat,unsat,lifts,near,maxN,maxM,degree,scans,rows}
};
console.log(JSON.stringify(audit(),null,2));
