// LSPV-4/439, independent compact exhaustive-bit referee. Node.js 20+.
// Tests only the stated canonical Tseitin source language, not generic SAT.
import assert from 'node:assert/strict';
function graph(H){let E=[];let edge=(a,b)=>E.push([Math.min(a,b),Math.max(a,b)]);
 if(H===4){for(let a=0;a<4;a++)for(let b=a+1;b<4;b++)edge(a,b)}
 else if(H===8){for(let a=0;a<8;a++)for(let i=0;i<3;i++){let b=a^(1<<i);if(a<b)edge(a,b)}}
 else if(H===10){for(let i=0;i<5;i++){edge(i,(i+1)%5);edge(i,i+5);edge(i+5,5+(i+2)%5)}}
 else {let r=H/2;for(let i=0;i<r;i++){edge(i,(i+1)%r);edge(r+i,r+(i+1)%r);edge(i,r+i)}}
 E.sort((a,b)=>a[0]-b[0]||a[1]-b[1]);let V=Array.from({length:H},()=>[]);
 E.forEach(([a,b],j)=>{V[a].push(j+1);V[b].push(j+1)});V.forEach(v=>v.sort((a,b)=>a-b));assert(V.every(v=>v.length===3));return V;}
function packet(V,c){let H=V.length,w=(3*H/2).toString(2).length;
 let prefix='11010011'+'1'.repeat(H)+'0'+'1'.repeat(w)+'0'+V.flat().map(e=>e.toString(2).padStart(w,'0')).join('');let body='';
 for(let v=0;v<H;v++)for(let a=0;a<2;a++)for(let b=0;b<2;b++){
 let s=[a,b,a^b^1^c[v]];for(let j=0;j<3;j++)body+=s[j]+V[v][j].toString(2).padStart(w,'0')}
 return {text:prefix+body,base:prefix.length,w};}
function checked(edits,H){assert(edits.every(v=>Number.isInteger(v)&&v>=0&&v<H))}
function port(src,p,edits,H){let {text,base,w}=src;assert(p>=0&&p<text.length);let b=text[p];if(p<base)return b;
 let rel=p-base,slot=Math.floor(rel/(w+1));if(rel%(w+1)!==0||slot%3!==2)return b;
 let v=Math.floor(slot/12),parity=0;for(let u of edits)parity^=+(u===v);return String(Number(b)^parity)}
let checks=0;for(let H of [4,8,10,20,64]){let V=graph(H),c=Array.from({length:H},(_,j)=>j%3===0?1:0),src=packet(V,c);
 for(let t=0;t<8;t++){let edits=Array.from({length:t*2+1},(_,j)=>(j*7+t*3)%H);if(t===5)edits.push(edits[0],edits[0]);checked(edits,H);
 let dst=c.slice();edits.forEach(v=>dst[v]^=1);let full=packet(V,dst);assert.equal(full.text.length,src.text.length);
 for(let p=0;p<src.text.length;p++){assert.equal(port(src,p,edits,H),full.text[p]);checks++}
 assert.equal(dst.reduce((a,b)=>a^b,0),c.reduce((a,b)=>a^b,0)^(edits.length%2));checks++;
 }}let failed=false;try{checked([0,20],20)}catch(e){failed=true}assert(failed);checks++;
console.log(JSON.stringify({status:'PASS',checkedBitsAndControls:checks,graphs:5,descriptorGate:true}));