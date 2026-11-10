// LSPV-2/533, independently executable source-authenticated indexed-tape controls.
// node experiments/arc/lspv2_533_sparse_index_compact.mjs
import crypto from 'node:crypto';
function ck(z,m){if(!z)throw Error(m)}
function cnf(c,n){return Buffer.from([83,51,67,n,c.length,...c.flat().map(x=>x<0?x+256:x)])}
function k4(odd){let ed=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],c=[];
 for(let v=0;v<4;v++){let e=ed.map((z,i)=>z.includes(v)?i+1:0).filter(Boolean);
 for(let m=0;m<8;m++){let b=[(m>>2)&1,(m>>1)&1,m&1];
 if(b.reduce((a,x)=>a+x,0)%2!==(odd&&v===0?1:0))c.push(e.map((x,i)=>b[i]?-x:x))}}
 return cnf(c,6)}
function decision(b){if(b.length<5||b.subarray(0,3).toString()!=='S3C')return'MALFORMED';
 let n=b[3],m=b[4];if(n<1||n>8||b.length!==5+3*m)return'MALFORMED';
 let cs=[];for(let j=0;j<m;j++){let r=[...b.subarray(5+3*j,8+3*j)].map(v=>v>127?v-256:v);
 if(r.some(v=>v===0||Math.abs(v)>n)||new Set(r.map(Math.abs)).size!==3)return'MALFORMED';cs.push(r)}
 for(let a=0;a<(1<<n);a++)if(cs.every(r=>r.some(v=>Boolean(a&(1<<(Math.abs(v)-1)))===(v>0))))return'SAT';
 return'UNSAT'}
function sparse(p){let head=0n,index='',mem=new Map(),reads=[],hi=1n,peak=0,paid=0;
 const bits=v=>v.toString(2).length;
 for(let j=0;j<p.length;j++){let op=p[j];
  if(op==='i0'||op==='i1'){index+=op[1];paid+=2}
  else if(op==='jump'){head=index?BigInt('0b'+index):0n;index='';hi=hi>head+1n?hi:head+1n;paid+=bits(head)+3}
  else if(op==='left'||op==='right'){head=op==='left'?(head>0n?head-1n:0n):head+1n;hi=hi>head+1n?hi:head+1n;paid++}
  else{paid+=(mem.size+1)*(bits(head)+1)+4;
   if(op==='read')reads.push(mem.has(head.toString())?1:0);
   else if(op==='w1')mem.set(head.toString(),1);
   else if(op==='w0')mem.delete(head.toString());else throw Error('opcode')}
  let layout=[...mem.keys()].reduce((s,x)=>s+3+BigInt(x).toString(2).length,0)+index.length+bits(head)+8*(j+2);
  peak=Math.max(peak,layout);ck(peak<=32*(j+2)**2,'layout limit');
 }
 return {head,index,mem,hi,peak,paid,reads}}
function dense(p){let tape=[0],head=0,index='',read=[],hi=1;
 for(let op of p){if(op==='i0'||op==='i1')index+=op[1];
 else if(op==='jump'){head=index?parseInt(index,2):0;index='';ck(head<=64,'dense head')}
 else if(op==='left')head=Math.max(0,head-1);else if(op==='right')head++;
 else{while(tape.length<=head)tape.push(0);
 if(op==='read')read.push(tape[head]);else if(op==='w0')tape[head]=0;else if(op==='w1')tape[head]=1;else throw Error('bad')}
 hi=Math.max(hi,head+1)}
 return {head,index,hi,read,live:tape.map((b,i)=>b?i:null).filter(v=>v!==null)}}
let cases=[['K4-odd',k4(true)],['K4-even',k4(false)],['SAT-one',cnf([[1,2,3]],3)],
 ['UNSAT-8',cnf(Array.from({length:8},(_,m)=>[1,2,3].map((x,j)=>m&(1<<(2-j))?-x:x)),3)],
 ['empty-SAT',cnf([],3)],['bad-magic',Buffer.from([66,65,68,3,0])],
 ['truncated',cnf([[1,2,3]],3).subarray(0,7)],['alias',cnf([[1,1,3]],3)],['zero',cnf([[0,2,3]],3)]];
const ops=['i0','i1','jump','read','w0','w1','left','right'];
let checks=0,programs=0;
function test(p){let a=sparse(p),b=dense(p);
 ck(Number(a.head)===b.head&&a.index===b.index,'heads');
 ck(a.hi===BigInt(b.hi)&&a.reads.join(',')===b.read.join(','),'read/highwater');
 ck([...a.mem.keys()].map(Number).sort((x,y)=>x-y).join(',')===b.live.join(','),'contents');
 ck(a.paid<=32*(p.length+1)**3,'work charge');checks+=4;programs++}
function visit(p,d){test(p);if(d>=4)return;for(let o of ops)visit([...p,o],d+1)}
visit([],0);
let controls=[];
for(let [name,b] of cases){const n=8*b.length,p=['i1',...Array(n).fill('i0'),'jump','w1','read','w0','read'],r=sparse(p);
 ck(r.hi===(1n<<BigInt(n))+1n,'remote head');ck(r.reads.join(',')==='1,0'&&r.mem.size===0,'write-clear');
 ck(r.peak<=32*(p.length+1)**2,'sparse peak');
 let h=crypto.createHash('sha256').update(b).digest('hex'),label=decision(b);
 controls.push({name,label,N:n,sha256:h,index_highwater_bits:r.hi.toString(2).length,sparse_layout_upper:r.peak,paid_proxy:r.paid,steps:p.length});
 checks+=3}
console.log(JSON.stringify({run:533,programs,checks,cases:controls},null,2));
