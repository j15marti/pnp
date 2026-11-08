#!/usr/bin/env node
'use strict';
// Independent compact public verifier for restricted checkpoint accounting.
// Full original-source, both-label, and malformed tests are in local archive.
const A=require('node:assert/strict');
const E=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
function k4(ch){const out=[];for(let v=0;v<4;v++){
 const ids=E.map((e,i)=>e.includes(v)?i:-1).filter(i=>i>=0);
 for(let z=0;z<8;z++){
 const b=[z>>2&1,z>>1&1,z&1];
 if((b[0]^b[1]^b[2])!==ch[v])out.push(ids.map((id,j)=>[b[j],id]));
 }}return out;}
function enc(cls){return '10110101'+'010000'+cls.length.toString(2).padStart(12,'0')+
 cls.map(c=>c.map(([s,v])=>String(s)+v.toString(2).padStart(4,'0')).join('')).join('');}
const c0=k4([1,0,0,0]),c1=k4([0,1,0,0]);
function truth(c,mask){return c.every(row=>row.some(([s,v])=>((mask>>v)&1)!==s));}
for(const c of [c0,c1]){A.equal(c.length,16);
 A.equal(Array.from({length:64},(_,x)=>x).some(x=>truth(c,x)),false);
 for(let i=0;i<16;i++)A.equal(Array.from({length:64},(_,x)=>x)
 .some(x=>truth(c.filter((_,j)=>j!==i),x)),true);}
const v=[];for(let a=6;a<16;a++)for(let b=a+1;b<16;b++)for(let c=b+1;c<16;c++)
 for(let m=0;m<7;m++)v.push([[m>>2&1,a],[m>>1&1,b],[m&1,c]]);
const fixed=v.slice(0,23),children=Array.from({length:128},(_,i)=>enc([
 ...(i%2?c1:c0),...fixed,v[23+i]]));
A.equal(new Set(children).size,128);A(children.every(s=>s.length===626));
const P=266,L=626;
function run(k){const anchors=[];let compared=0,probed=0,copied=0,hits=0,fresh=0;
 for(const input of children){let match=false;
 for(const a of anchors){match=true;for(let p=0;p<P;p++){
 compared++;if(input[p]!==a[p]){match=false;break;}}
 if(match)break;}
 if(match){hits++;probed+=L-P;copied+=64;}
 else {fresh++;probed+=P+120*30+L-P;if(k){anchors.unshift(input.slice(0,P));
 if(anchors.length>k)anchors.pop();}}
 }
 return {fresh_prefixes:fresh,prefix_reuses:hits,guest_probes:probed,
 compares:compared,snapshot_bits:copied,peak_checkpoint_bits:anchors.length*(P+64+16),
 charged:probed+compared+copied};}
const none=run(0),single=run(1),both=run(2);
A.equal(none.guest_probes,540928);A.equal(single.prefix_reuses,0);
A.equal(single.compares,4699);A.equal(both.fresh_prefixes,2);
A.equal(both.prefix_reuses,126);A.equal(both.guest_probes,53812);
A.equal(both.compares,35884);A.equal(both.snapshot_bits,8064);
A.equal(both.charged,97760);A.equal(both.peak_checkpoint_bits,692);
console.log(JSON.stringify({role:'LSPV-2/501',status:'RESTRICTED',children:children.length,
 input_bits:L,checkpoint_prefix_bits:P,baseline:none,one_checkpoint:single,
 two_checkpoints:both,all_128_guests_still_finish:true},null,2));
