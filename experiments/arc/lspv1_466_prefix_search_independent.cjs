// LSPV-1/466 independent finite exhaustive witness-prefix control; run: node thisfile.cjs
'use strict';
const F=[[1],[2],[-1,-2]], FS=[[1],[2]];
let checks=0;
const chk=(x,m)=>{checks++;if(!x)throw Error(m)};
const sort=a=>[...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);
function resolve(a,b,p){if(a.includes(p)&&b.includes(-p)){}else if(a.includes(-p)&&b.includes(p)){[a,b]=[b,a]}else return null;let s=new Set([...a,...b]);s.delete(p);s.delete(-p);if([...s].some(x=>s.has(-x)))return null;return sort([...s])}
function decode(z){let out=[];for(let i=0;i<2;i++){let p=1+z%2;z=Math.floor(z/2),b=z%4;z=Math.floor(z/4);let a=z%4;z=Math.floor(z/4);out.push([a,b,p])}return out}
function check(F,z){let cs=F.map(sort);for(let [a,b,p] of decode(z)){if(a>=cs.length||b>=cs.length)return false;let r=resolve(cs[a],cs[b],p);if(r===null)return false;cs.push(r)}return cs.at(-1).length===0}
let valid=[];for(let z=0;z<1024;z++){if(check(F,z))valid.push(z);chk(!check(FS,z),'SAT input accepted')}
chk(valid.length===8,'eight witnesses');let s='';for(let i=0;i<10;i++){let pref=s+'0';s+=valid.some(z=>z.toString(2).padStart(10,'0').startsWith(pref))?'0':'1';chk(valid.some(z=>z.toString(2).padStart(10,'0').startsWith(s)),'prefix')}chk(parseInt(s,2)===205,'expected certificate');chk(check(F,205),'accepted certificate');chk(resolve([1,2],[-1,-2],1)===null,'tautological resolvent');chk(resolve([1],[-1],1).length===0,'empty');chk(valid.every(z=>check(F,z)),'every valid recorded');
console.log(JSON.stringify({assertions:checks,exhaustive_records:1024,valid_records:valid.length,corrupt_rejected:1024-valid.length,recovered_proof:205,unrestricted_P_vs_NP:'OPEN'}));
