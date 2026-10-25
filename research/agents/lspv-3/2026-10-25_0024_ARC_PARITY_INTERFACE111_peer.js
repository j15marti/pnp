// ARC-PARITY-INTERFACE111. Standard Node.js. Finite evidence only; ARC OPEN.
'use strict';
const assert=require('node:assert/strict');
let checks=0;function ok(x){assert(x);checks++;}
function xor(a,b,c){let rows=[];for(let x=0;x<2;x++)for(let y=0;y<2;y++)for(let z=0;z<2;z++)if(z!==(x^y))rows.push([x?-a:a,y?-b:b,z?-c:c]);return rows}
function pin(v,d,p,q){let a=[];for(let x=0;x<2;x++)for(let y=0;y<2;y++)a.push([d?v:-v,x?-p:p,y?-q:q]);return a}
function mod(b,side,d){let first=side?2*b+2:b+1,gs=[],yy=i=>first+i;
for(let i=0;i<b-1;i++)gs.push(xor(i?yy(i-1):1,i+2,yy(i)));
gs.push(pin(yy(b-2),d,yy(b-1),yy(b)));return gs}
function litSat(l,a){return l>0?!!a[Math.abs(l)]:!a[Math.abs(l)]}
function sat(cs,a){return cs.every(c=>c.some(l=>litSat(l,a)))}
function witness(b,d,x){let a={};for(let i=0;i<b;i++)a[i+1]=x[i];for(let side=0;side<2;side++){
let f=side?2*b+2:b+1,par=0;for(let i=0;i<b-1;i++){par^=x[i+1];if(i===0)par^=x[0];a[f+i]=par}
a[f+b-1]=0;a[f+b]=0}return a}
function encode(cs){let names=[...new Set(cs.flat().map(Math.abs))].sort((a,b)=>a-b),map=new Map(names.map((x,i)=>[x,i+1]));let m=cs.length,n=names.length,h=Math.ceil(Math.log2(Math.max(n,m)+1));let bits='1'.repeat(h)+'0'+n.toString(2).padStart(h,'0')+m.toString(2).padStart(h,'0');for(let c of cs)for(let l of c)bits+=(l<0?'1':'0')+map.get(Math.abs(l)).toString(2).padStart(h,'0');return {bits,names,h,m}}
function decode(p){let {bits,names,h,m}=p,at=3*h+1,cs=[];for(let j=0;j<m;j++){let c=[];for(let t=0;t<3;t++){let sign=bits[at++],id=parseInt(bits.slice(at,at+h),2);at+=h;c.push((sign==='1'?-1:1)*names[id-1])}cs.push(c)}ok(at===bits.length);return cs}
function flatten(groups){return groups.flat()}
let data=[];for(let b of [3,4,5,6,8,10,16,32,64,128])for(let d of [0,1]){
let A=mod(b,0,0),B=mod(b,1,d),parent=flatten([...A,...B]);ok(parent.length===8*b);ok(new Set(parent.map(JSON.stringify)).size===8*b);ok(new Set(parent.flat().map(Math.abs)).size===3*b+2);ok(parent.every(c=>new Set(c.map(Math.abs)).size===3));
let rec=encode(parent);ok(JSON.stringify(decode(rec))===JSON.stringify(parent));let children=[A,B].map(flatten),childBits=[];for(let ch of children){let v=encode(ch);ok(JSON.stringify(decode(v))===JSON.stringify(ch));childBits.push(v.bits.length)}
let grand=[];for(let groups of [A,B]){let cut=Math.floor((b-1)/2);for(let g of [flatten(groups.slice(0,cut)),flatten(groups.slice(cut))]){let v=encode(g);ok(JSON.stringify(decode(v))===JSON.stringify(g));grand.push(v.bits.length)}}
if(b<=10){let yes=0;for(let x=0;x<(1<<b);x++){let xx=Array.from({length:b},(_,i)=>(x>>i)&1),as=witness(b,d,xx),par=xx.reduce((p,v)=>p^v,0),v=sat(parent,as);ok(v===(d===0&&par===0));ok(sat(children[0],as)===(par===0));ok(sat(children[1],as)===(par===d));yes+=v}ok(yes===(d===0?1<<(b-1):0))}
data.push({b,delta:d,parent_bits:rec.bits.length,level1_bits:childBits,level2_bits:grand})}
console.log(JSON.stringify({run:'ARC-PARITY-INTERFACE111',checks,rows:data,claim:'finite independent roundtrip/source-name/orientation test; no universal ARC successor'},null,2));