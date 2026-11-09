'use strict';
/* LSPV-2/506: independent finite abstract FLMV indexed-WORK spike.
   This is NOT native FLMV execution, and NOT a general SAT solver. */
const crypto = require('crypto');
let assertionCount = 0;
function insist(test, description) { if (!test) throw Error(description); assertionCount++; }
const K4 = [[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
function signedSource(mask) {
  const body = [];
  for(let v=0;v<4;v++){
    const e=K4.map((p,i)=>p.indexOf(v)>=0?i+1:0).filter(Boolean);
    for(let z=0;z<8;z++){
      const b=[z&1,(z>>1)&1,(z>>2)&1];
      if((b[0]^b[1]^b[2])!==((mask>>v)&1)){
        body.push(e.map((id,j)=>b[j]?-id:id).join(' ')+' 0\n');
      }
    }
  }
  return 'p cnf 6 16\n'+body.join('');
}
const sources = new Map(Array.from({length:16},(_,k)=>[signedSource(k),k]));
function truth(source) {
 if(!sources.has(source)) return 'MALFORMED';
 const rows=source.trim().split('\n').slice(1).map(row=>row.trim().split(' ').slice(0,3).map(Number));
 for(let val=0;val<64;val++){
   if(rows.every(c=>c.some(l=>Boolean(val&(1<<(Math.abs(l)-1)))===(l>0)))) return 'SAT';
 }
 return 'UNSAT';
}
class Machine {
 constructor(){this.idx=[];this.idxHead=0;this.wHead=0n;this.inputHead=0;this.work=new Map();this.high=0n;this.indexHigh=0;this.steps=0;}
 load(address){const s=address.toString(2); this.idx=Array.from(s,Number);this.idxHead=0;this.indexHigh=Math.max(this.indexHigh,s.length);this.steps+=s.length;}
 jump(){this.wHead=BigInt('0b'+(this.idx.join('')||'0'));this.idx=[];this.idxHead=0;this.steps++;}
 read(){this.high=this.high>this.wHead?this.high:this.wHead;this.steps++;return this.work.get(this.wHead.toString())??0;}
 snapshot(){return JSON.stringify({work:[...this.work],index:this.idx,idxHead:this.idxHead,wHead:this.wHead.toString(),inputHead:this.inputHead,pc:'GUEST_ENTRY'});}
}
function execute(source, spike, k){
 const m=new Machine();
 insist(m.read()===0,'initial guest blank');
 if(spike){
  const length=Buffer.byteLength(source);
  const b=(length+2).toString(2).length;
  const far=1n<<BigInt(k*b);
  m.load(far);m.jump();insist(m.read()===0,'far blank');
  m.load(0n);m.jump();
 }
 insist(m.idx.length===0 && m.wHead===0n,'restored head/index');
 return {state:m.snapshot(),high:m.high,indexHigh:m.indexHigh,steps:m.steps,label:truth(source)};
}
let pairs=0,pass=0,peak=0n;
const labels={SAT:0,UNSAT:0,MALFORMED:0};
const valid=[...sources.keys()];
const invalid=['','p bad 6 16\n',valid[0]+'\n',valid[0].slice(0,-1),valid[0].replace('p cnf','p bad'),'p cnf 6 16\n0\n'];
for(const src of valid.concat(invalid)){
 const label=truth(src);labels[label]++;
 if(sources.has(src)){
  let parity=0,mask=sources.get(src);for(let i=0;i<4;i++)parity^=(mask>>i)&1;
  insist(label===(parity?'UNSAT':'SAT'),'charge parity');
 } else insist(label==='MALFORMED','malformed fixture');
 for(const k of [1,2,3,4]){
  const low=execute(src,false,k), high=execute(src,true,k);
  insist(low.state===high.state,'checkpoint equality');
  insist(low.label===high.label && low.label===label,'label equality');
  insist(low.high===0n,'low high-water');
  const size=Buffer.byteLength(src),expected=1n<<BigInt(k*(size+2).toString(2).length);
  insist(high.high===expected,'exact indexed high-water');
  insist(high.indexHigh===expected.toString(2).length,'index bits');
  if(high.high>peak)peak=high.high;
  if(high.high>BigInt(size*size))pass++;
  pairs++;
 }
 insist(truth(src+'x')==='MALFORMED','corrupted trailer');
}
const digest=crypto.createHash('sha256').update(signedSource(0)).digest('hex');
insist(digest==='9fa4c20d987e11a768d3a3c28960c154f451399975f491fdb36a997c2ae2e1a4','prior exact original byte hash');
console.log(JSON.stringify({run:'LSPV-2/506',checks:assertionCount,pairs,labels,max_highwater:peak.toString(),highwater_gt_n2:pass,original_source0_sha256:digest,native_flmv_emulator:false,general_sat_decider:false},null,2));
