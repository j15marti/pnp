// TMR-5/016 independently authored hosted-V8/Node-compatible physical-controller audit.
// Run: node experiments/tmr/tmr5_shifted_mirror_redteam016.cjs
function audit016() {
"use strict";
const get=(x,p)=>p===0?"<":p===x.length+1?">":x[p-1];
const parity=x=>[...x].reduce((a,b)=>a^(b==="1"?1:0),0);
const expected=x=>{if(x.length%3)return "MALFORMED";let m=0;for(let i=0;i<x.length;i+=3)m|=1<<parseInt(x.slice(i,i+3),2);return m===255?"UNSAT":"SAT"};
const init=(d,abstract)=>({phase:d?"U":"S",r:d,p:0,bh:0,ch:0,B:{},C:{},bv:new Set([0]),cv:new Set([0]),mask:0,buf:"",label:"",time:0,abstract});
const bit=(t,i)=>t[i]||0;
const phi=(s,x)=>{let q=x.length+1,z=parity(x),p=s.p;switch(s.phase){case"U":return s.r+3*q+1+2*q*z;case"S":return 3*q-p+1+2*q*z;case"R":return p+q+1+2*q*z;case"D":return 3*q-p+1;case"E":return p+q+1;case"A":return q-p+1;case"H":return 0;default:throw Error("phase")}};
function next(s,x){let q=x.length+1,p=s.p,f=s.phase,read=get(x,p);if(f==="U"){if(!(p===0&&s.r>0))throw Error("bootstrap");s.ch++;s.cv.add(s.ch);if(!--s.r)s.phase="S";}
else if(f==="S"){if(!(p<q))throw Error("scan");if(read==="1"){s.C[s.ch]=bit(s.C,s.ch)^1;if(!s.abstract)s.B[s.bh]=bit(s.B,s.bh)^1;}if(++s.p===q)s.phase="R";}
else if(f==="R"){if(!(p>0))throw Error("return");if(--s.p===0)s.phase=bit(s.abstract?s.C:s.B,s.abstract?s.ch:s.bh)?"D":"A";}
else if(f==="D"){if(++s.p===q)s.phase="E";}
else if(f==="E"){if(--s.p===0)s.phase="A";}
else if(f==="A"){if(p===q){s.phase="H";s.label=s.buf?"MALFORMED":s.mask===255?"UNSAT":"SAT";}else{if(read==="0"||read==="1"){s.buf+=read;if(s.buf.length===3){s.mask|=1<<parseInt(s.buf,2);s.buf="";}}else if(read!=="<")throw Error("read");s.p++;}}
else throw Error("halted");s.time++;}
function check(c,a,x,d){const keys=["phase","p","bh","ch","mask","buf","label","time","r"];for(const k of keys)if(c[k]!==a[k])throw Error("proj "+k);if(JSON.stringify(c.C)!==JSON.stringify(a.C))throw Error("contents");
if(c.bv.size!==a.bv.size||c.cv.size!==a.cv.size)throw Error("visited");
if(c.phase==="U"){if(c.ch!==d-c.r||c.p!==0||Object.values(c.B).some(Boolean)||Object.values(c.C).some(Boolean))throw Error("bootstrap invariant");}
else {if(c.ch!==c.bh+d)throw Error("heads");
const all=new Set([...Object.keys(c.B).map(Number),...Object.keys(c.C).map(k=>+k-d),c.bh]);for(const j of all)if(bit(c.B,j)!==bit(c.C,j+d))throw Error("shift mirror");
const z=c.phase==="S"?parity(x.slice(0,Math.max(0,c.p-1))):parity(x);
if(bit(c.C,c.ch)!==z)throw Error("source binding");
}}
let res={id:"TMR5-SM16",timeZone:"America/Los_Angeles",implementation:"hosted V8 independently written, source below; original TMR4 JS inspected but not executed",status:"COMPUTATIONAL finite; new constant-offset symbolic theorem CANDIDATE/RESTRICTED; P versus NP OPEN",shifts:[0,1,2,3,4,7],cases:0,edges:0,sat:0,unsat:0,malformed:0,odd:0,offInvariantWitnesses:0,offInvariantMissingTransitions:0,maxLength:0,failures:0};
function test(x,d){let c=init(d,false),a=init(d,true),n=0;check(c,a,x,d);if(phi(a,x)!==d+3*(x.length+1)+1+2*(x.length+1)*parity(x))throw Error("potential init");
while(c.phase!=="H"){let p=phi(a,x);next(c,x);next(a,x);check(c,a,x,d);if(p!==1+phi(a,x))throw Error("Bellman");n++;if(n>d+5*(x.length+1)+2)throw Error("bound")}
if(n!==d+3*(x.length+1)+1+2*(x.length+1)*parity(x)||c.label!==expected(x)||a.label!==c.label)throw Error("classification or runtime");
if(c.bv.size+c.cv.size!==d+2||phi(a,x)!==0)throw Error("space or terminal");
res.cases++;res.edges+=n;res.maxLength=Math.max(res.maxLength,x.length);res.odd+=parity(x);res[c.label==="SAT"?"sat":c.label==="UNSAT"?"unsat":"malformed"]++;}
const samples=[""];for(let n=1;n<=9;n++)for(let i=0;i<2**n;i++)samples.push(i.toString(2).padStart(n,"0"));samples.push("000001010011100101110111","0".repeat(45),"1".repeat(51),"100".repeat(16),"101".repeat(17));
for(const d of res.shifts){for(const x of samples)test(x,d);
for(const x of ["1","001","1".repeat(9)]){let c=init(d,false),a=init(d,true);Object.assign(c,{phase:"R",r:0,p:1,ch:d,B:{0:1},C:{[d]:0}});Object.assign(a,{phase:"R",r:0,p:1,ch:d,C:{[d]:0}});
while(c.phase!=="H")next(c,x);while(a.phase!=="H")next(a,x);
let difference=c.time-a.time;if(difference!==2*(x.length+1)||c.label!==a.label)throw Error("hostile");
res.offInvariantWitnesses++;res.offInvariantMissingTransitions+=difference;}}
return res;
}
console.log(JSON.stringify(audit016(),null,2));
