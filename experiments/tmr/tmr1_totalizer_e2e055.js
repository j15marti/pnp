// TMR-1/055: all-input exact-count promise totalizer, binary circuit and formal #SAT interface.
// Node >=18, revision totalizer055.v2, deterministic seed 20261115; no Lean/TM2 execution.
'use strict';
let seed=20261115,checks=0,cnfs=0,circuits=0,assignments=0,full=0;
const rnd=()=>{seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return seed>>>0;};
const ok=(b,s)=>{checks++;if(!b)throw Error(s);};
const lit=(i,b)=>[i,!!b], str=x=>JSON.stringify(x), vals=(n,z)=>Array.from({length:n},(_,j)=>(z>>j)&1);
const sat=(cs,a)=>cs.every(c=>c.some(([i,b])=>a[i]===Number(b)));
function norm(h){
 const n=h.n,d=Math.max(1,4-n),cls=[],seen=new Set(),used=new Set();
 for(const c of h.cs){ok(c.length<=3,'width');for(const [i,b] of c){ok(i>=0&&i<n&&typeof b==='boolean','lit');used.add(i);}if(!seen.has(str(c))){seen.add(str(c));cls.push(c);}}
 for(let i=0;i<n;i++)if(!used.has(i))cls.push([lit(i,1),lit(i,0)]);
 for(let j=0;j<d;j++)cls.push([lit(n+j,0)]);
 cls.push([lit(n,1),lit(n,0)]);
 const ans={n:n+d,cs:cls,d};
 ok(ans.n>=4&&cls.length>=2,'minima');ok(new Set(cls.map(str)).size===cls.length,'nodup');
 ok(new Set(cls.flatMap(c=>c.map(l=>l[0]))).size===ans.n,'alloccur');
 ok(cls.length<=h.cs.length+n+d+1,'count tax');return ans;
}
function enc(h){const w=Math.floor(Math.log2(2*h.n))+1,b=[1,1,1,0,...Array(h.n).fill(1),0];
 for(const c of h.cs)for(let j=0;j<3;j++){const v=j<c.length?2*c[j][0]+1+Number(c[j][1]):0;for(let t=0;t<w;t++)b.push(Math.floor(v/2**t)%2);}
 ok(b.length===h.n+5+3*h.cs.length*w,'Lean bits');return b;
}
function dec(b){let p=0,k=0,n=0;while(b[p]===1){k++;p++;}if(b[p++]!==0)throw Error('k');while(b[p]===1){n++;p++;}if(b[p++]!==0||k!==3||n<4)throw Error('n');
 const w=Math.floor(Math.log2(2*n))+1;if((b.length-p)%(3*w))throw Error('length');const cs=[];
 while(p<b.length){const c=[];let padded=false;for(let j=0;j<3;j++){let v=0;for(let t=0;t<w;t++){if(b[p]!==0&&b[p]!==1)throw Error('bit');v+=b[p++]*2**t;}
 if(v===0){padded=true;continue;}if(v>2*n||padded)throw Error('slot');c.push(lit(Math.floor((v-1)/2),v%2===0));}cs.push(c);}
 return {n,cs};}
function checkCNF(h){const g=norm(h),b=enc(g),f=dec(b);ok(f.n===g.n&&str(f.cs)===str(g.cs),'roundtrip');
 let a=0,z=0;for(let x=0;x<2**h.n;x++){const v=vals(h.n,x),r=sat(h.cs,v);a+=Number(r);let e=0;
 for(let y=0;y<2**g.d;y++){e+=Number(sat(g.cs,v.concat(vals(g.d,y))));full++;}ok(e===Number(r),'unique extension');assignments++;z+=e;}
 ok(a===z,'count');cnfs++;return {n:h.n,m:h.cs.length,n2:g.n,m2:g.cs.length,bits:b.length,count:z};}
const fv=(f,a,b)=>(f>>((a<<1)|b))&1;
function sc(c){const b=[...Array(c.q).fill(1),0,...Array(c.gs.length).fill(1),0],w=Math.floor(Math.log2(Math.max(2,c.q+c.gs.length)))+1;
 const put=(v,n)=>{for(let j=0;j<n;j++)b.push(Math.floor(v/2**j)%2);};for(const g of c.gs){put(g.a,w);put(g.b,w);put(g.f,4);}put(c.out,w);return b;}
function dc(b){let p=0,q=0,g=0;while(b[p]===1){q++;p++;}if(b[p++]!==0||q<1)throw Error('q');while(b[p]===1){g++;p++;}if(b[p++]!==0)throw Error('g');
 const w=Math.floor(Math.log2(Math.max(2,q+g)))+1;if(b.length!==p+g*(2*w+4)+w)throw Error('source size');const get=n=>{let v=0;for(let j=0;j<n;j++){if(b[p]!==0&&b[p]!==1)throw Error('source bit');v+=b[p++]*2**j;}return v;};
 const gs=[];for(let j=0;j<g;j++){const a=get(w),bb=get(w),f=get(4);if(a>=q+j||bb>=q+j)throw Error('predecessor');gs.push({a,b:bb,f});}
 const out=get(w);if(out>=q+g)throw Error('output');return {q,gs,out};}
function toCNF(c){const cs=[],used=new Set();for(let j=0;j<c.gs.length;j++){const {a,b,f}=c.gs[j],z=c.q+j;used.add(a);used.add(b);
 for(let u=0;u<2;u++)for(let v=0;v<2;v++)cs.push([lit(a,u===0),lit(b,v===0),lit(z,fv(f,u,v)===1)]);}
 cs.push([lit(c.out,1)]);if(c.out<c.q)used.add(c.out);
 for(let j=0;j<c.q;j++)if(!used.has(j))cs.push([lit(j,1),lit(j,0),lit(j,1)]);
 const out=[],seen=new Set();for(const v of cs)if(!seen.has(str(v))){seen.add(str(v));out.push(v);}
 return {n:c.q+c.gs.length,cs:out};}
function chkCircuit(c){const b=sc(c),z=dc(b);ok(str(z)===str(c),'source roundtrip');const h=toCNF(z),g=norm(h),e=enc(g);
 ok(h.cs.length<=4*h.n,'density old');ok(g.cs.length<=4*g.n,'density new');ok(str(dec(e).cs)===str(g.cs),'target roundtrip');
 let cnt=0;for(let x=0;x<2**c.q;x++){const a=vals(c.q,x),w=a.slice();for(const t of c.gs)w.push(fv(t.f,w[t.a],w[t.b]));let ext=0;
 for(let j=0;j<2**c.gs.length;j++)for(let k=0;k<2**g.d;k++){ext+=Number(sat(g.cs,a.concat(vals(c.gs.length,j),vals(g.d,k))));full++;}
 ok(ext===w[c.out],'circuit full extension');cnt+=ext;assignments++;}
 circuits++;return {q:c.q,G:c.gs.length,n2:g.n,m2:g.cs.length,sourceBits:b.length,formalBits:e.length,count:cnt};}
const examples=[];const controls=[{n:0,cs:[]},{n:0,cs:[[]]},{n:1,cs:[]},{n:1,cs:[[lit(0,1)]]},{n:1,cs:[[lit(0,1)],[lit(0,0)]]},{n:2,cs:[[lit(0,1)],[lit(0,1)]]},{n:3,cs:[[lit(0,1),lit(1,1),lit(2,1)]]},{n:4,cs:[]}];
for(const h of controls){const v=checkCNF(h);if(examples.length<4)examples.push(v);}
for(let j=0;j<500;j++){const n=rnd()%5,m=rnd()%9,cs=[];for(let t=0;t<m;t++){if(cs.length&&rnd()%5===0){cs.push(cs[rnd()%cs.length]);continue;}const c=[];for(let k=rnd()%4;k>0;k--)if(n)c.push(lit(rnd()%n,rnd()%2));cs.push(c);}checkCNF({n,cs});}
const basic=[{q:1,gs:[],out:0},{q:1,gs:[{a:0,b:0,f:6}],out:1},{q:2,gs:[],out:0},{q:2,gs:[{a:0,b:1,f:8}],out:2},{q:4,gs:[],out:0}];
for(const c of basic){const v=chkCircuit(c);if(examples.length<8)examples.push(v);}
for(let t=0;t<210;t++){const q=1+rnd()%4,G=rnd()%5,gs=[];for(let j=0;j<G;j++)gs.push({a:rnd()%(q+j),b:rnd()%(q+j),f:rnd()%16});chkCircuit({q,gs,out:rnd()%(q+G)});}
let rejects=0;for(const [fn,s] of [[dc,[1,0,0]],[dc,[1,1,0]],[dec,[1,1,1]],[dec,[1,1,1,0,1,0]]]){try{fn(s);throw Error('accepted invalid');}catch(e){ok(e.message!=='accepted invalid','malformed rejected');rejects++;}}
console.log(JSON.stringify({revision:'totalizer055.v2',seed:20261115,cnfs,circuits,assignments,full,assertions:checks,rejects,failures:0,examples,status:'COMPUTATIONAL',source:'experiments/tmr/tmr1_totalizer_e2e055.js'},null,2));
