#!/usr/bin/env node
// Independent no-import finite verifier for CLOCK-SUBCORE-B2-FIREWALL339
const fs=require('fs'),crypto=require('crypto');
const r=JSON.parse(fs.readFileSync(process.argv[2]||'results/raw/arc/2026-11-02_1530_LSPV1_CLOCK_SUBCORE_B2_FIREWALL339.json','utf8'));
let nchecks=0;
function check(x,y,msg){nchecks++;if(JSON.stringify(x)!==JSON.stringify(y))throw Error(msg+': '+JSON.stringify(x)+' vs '+JSON.stringify(y));}
function horn(k){let a=[[1]];for(let i=1;i<k;i++)a.push([-i,i+1]);a.push([-k]);return a;}
function models(f){let n=f.flat().reduce((z,x)=>Math.max(z,Math.abs(x)),0),count=0;for(let a=0;a<2**n;a++)if(f.every(c=>c.some(x=>Boolean((a>>(Math.abs(x)-1))&1)===(x>0))))count++;return count;}
function un(n){return '1'.repeat(n)+'0';}
function enc(f){let n=f.flat().reduce((z,x)=>Math.max(z,Math.abs(x)),0),b=Math.max(1,Math.ceil(Math.log2(n+1))),s=un(n)+un(f.length);for(let c of f){s+=un(c.length);for(let x of c)s+=(x>0?'1':'0')+Math.abs(x).toString(2).padStart(b,'0');}return s;}
function dec(s){if(!s||!/^[01]+$/.test(s))throw Error('alphabet');let i=0;function u(){let j=0;while(i<s.length&&s[i]==='1'){j++;i++;}if(i>=s.length)throw Error('frame');i++;return j;}
let n=u(),m=u(),b=Math.max(1,Math.ceil(Math.log2(n+1))),f=[];for(let p=0;p<m;p++){let k=u(),c=[];for(let t=0;t<k;t++){if(i+b+1>s.length)throw Error('truncated');let sign=s[i++]==='1',x=parseInt(s.slice(i,i+b),2);i+=b;if(x<1||x>n)throw Error('index');c.push(sign?x:-x);}f.push(c);}if(i!==s.length)throw Error('extra');return f;}
for(let row of r.rows){let f=horn(row.k);check(models(f),0,'unsat');check(dec(enc(f)),f,'roundtrip');check(enc(f).length,row.N,'input bits');check(row.W_resolution,row.k,'resolution count');check(row.W_clock_exact,'2^'+row.N+'+'+(row.k+1),'clock formula');check(models(f.slice(0,-1).concat([[row.k]])),1,'sat neighbor');for(let j=0;j<f.length;j++){if(!models(f.filter((_,i)=>i!==j)))throw Error('bad core deletion');nchecks++;}for(let mask=1;mask<(1<<f.length)-1;mask++){if(!models(f.filter((_,i)=>mask>>i&1)))throw Error('bad subset');nchecks++;}}
let pad=horn(1).concat([[2,-2]]);check([enc(horn(1)).length,enc(pad).length],[13,26],'padding');check(dec(enc(pad)),pad,'pad parse');for(let mask=1;mask<8;mask++)check(models(pad.filter((_,j)=>mask>>j&1))===0,Boolean((mask&1)&&(mask&2)),'core selection');
let width=enc(horn(1)).length;check([width,2**width],[r.clock_H1.bits,r.clock_H1.states],'clock');let h=crypto.createHash('sha256');for(let i=0;i<(1<<width);i++){let b=Buffer.alloc(Math.ceil(width/8));let v=i;for(let j=b.length-1;j>=0;j--){b[j]=v&255;v=Math.floor(v/256);}h.update(b);}check(h.digest('hex'),r.clock_H1.SHA256,'hash');
function move(i,j,ctx){return ctx&&i>=0&&i<(1<<width)-1&&j===i+1;}check([move(0,2,true),move(3,1,true),move((1<<width)-1,(1<<width),true),move(0,1,false)],[false,false,false,false],'corrupt moves');
const E=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];function parity(q){let f=[];for(let v=0;v<4;v++){let inc=E.map((e,i)=>e.includes(v)?i+1:0).filter(Boolean);for(let a=0;a<8;a++){let s=((a&1)+((a>>1)&1)+((a>>2)&1))%2;if(s===q[v])continue;f.push(inc.map((x,j)=>(a>>j)&1?-x:x));}}return f;}
let odd=parity([1,0,0,0]),even=parity([0,0,0,0]);check([models(odd),models(even)],[0,8],'parity');let del=0,flip=0;for(let i=0;i<odd.length;i++){if(!models(odd.filter((_,j)=>i!==j)))throw Error('deletion');del++;for(let p=0;p<3;p++){let f=odd.map((c,j)=>j===i?c.map((x,t)=>t===p?-x:x):c);if(!models(f))throw Error('flip');flip++;}}check([del,flip],[16,48],'parity source controls');
function guard(f,z){let s=0;for(let x=0;x<2;x++)if(f.every(c=>c.some(l=>Boolean(Math.abs(l)==1?x:z)===(l>0))))s++;return s;}
check([guard([[-2,1],[-2,-1]],0),guard([[-2,1],[-2,-1]],1)],r.guarded_boundary.UNSAT,'guard UNSAT');
check([guard([[-2,1],[-2,1]],0),guard([[-2,1],[-2,1]],1)],r.guarded_boundary.SAT,'guard SAT');
let bad=['','111','101','1001','100100','1000000','101101011100','10110101110010','not-binary'],rejected=0;for(let x of bad){try{dec(x);}catch(e){rejected++;}}check(rejected,r.malformed_rejected,'malformed');
console.log(JSON.stringify({result:'PASS',checks:nchecks,parity_deletions:del,parity_flips:flip,clock_states:1<<width},null,2));
