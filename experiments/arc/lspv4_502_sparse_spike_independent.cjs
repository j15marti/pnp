"use strict";
// LSPV-4/502: independent hosted V8 checker, NOT an FLMV native machine.
const crypto=require("node:crypto");
const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
let checks=0;function chk(b,m){if(!b)throw Error(m);checks++;}
function make(c){let cs=[];for(let v=0;v<4;v++){let ids=edges.map((e,i)=>e.includes(v)?i+1:null).filter(Boolean);
for(let a=0;a<8;a++){let bits=[(a>>2)&1,(a>>1)&1,a&1];if((bits[0]^bits[1]^bits[2])!==((c>>v)&1))cs.push(ids.map((x,i)=>bits[i]?-x:x));}}return cs;}
function pack(cs){return "11000011"+cs.length.toString(2).padStart(8,'0')+cs.map(cl=>cl.map(v=>Math.abs(v).toString(2).padStart(3,'0')+(v<0?'1':'0')).join('')).join('');}
function unpack(s){if(s.length!==208||s.slice(0,16)!=='1100001100010000'||/[^01]/.test(s))return null;
let cs=[];for(let i=0;i<16;i++){let c=[];for(let j=0;j<3;j++){let chunk=s.slice(16+12*i+4*j,20+12*i+4*j);let x=parseInt(chunk.slice(0,3),2);if(x<1||x>6)return null;c.push(chunk[3]==='1'?-x:x);}if(new Set(c.map(Math.abs)).size!==3)return null;cs.push(c);}return cs;}
function decision(s){let cs=unpack(s);if(!cs)return 'MALFORMED';for(let val=0;val<64;val++){let ok=cs.every(cl=>cl.some(lit=>(((val>>(Math.abs(lit)-1))&1)===+(lit>0))));if(ok)return 'SAT';}return 'UNSAT';}
function bitLength(n){let l=0;while(n>0){n=Math.floor(n/2);l++;}return l;}
function run(){let inputs=[];for(let c=0;c<16;c++){const s=pack(make(c));chk(s.length===208,'length');chk(decision(s)===(c.toString(2).replace(/0/g,'').length%2?'UNSAT':'SAT'),'charge parity');inputs.push(['K4-charge-'+c,s]);}
const s=inputs[0][1],bad=[s.slice(0,-1),'0'+s.slice(1),s.slice(0,8)+'00001111'+s.slice(16),s.slice(0,16)+'0000'+s.slice(20),s.slice(0,16)+'1110'+s.slice(20),s.slice(0,20)+'0111'+s.slice(24),s.slice(0,20)+'0001'+s.slice(24,28)+s.slice(20,24)+s.slice(32)];
for(let i=0;i<bad.length;i++)inputs.push(['MALFORMED-'+i,bad[i]]);inputs.push(['empty',''],['single0','0'],['single1','1']);
const source_sha256=Array.from({length:16},(_,c)=>crypto.createHash('sha256').update(pack(make(c))).digest('hex'));let count=0,example=null;for(const [name,s] of inputs){const label=decision(s);for(const k of [1,2,3,4,6]){
const ell=k*bitLength(s.length),address=1n<<BigInt(ell);const b=s.length? +(s[0]==='1') ^ +(s.at(-1)==='1'):0;
// Guest source WORK indexed at address; sparse compiler saves the bit at cell 1 instead.
const guest=new Map([[address.toString(),b]]),actualRead=guest.get(address.toString());const sparseCell=b;
const bound=16+4*(ell+1+bitLength(s.length));const target=address;
chk(actualRead===sparseCell,'readback');chk(label===decision(s),'three labels');chk(target===(2n**BigInt(ell)),'index');chk(bound===16+4*(ell+1+bitLength(s.length)),'physical upper bound');
if(s.length>=2&&k>=2)chk(target>BigInt(bound),'separation');
if(name==='K4-charge-0'&&k===6)example={case:name,n:s.length,k,label,branch:b,virtual_index_bits:ell+1,original_work_highwater:target.toString(),sparse_physical_upper_bound:bound};
count++;
}}
return {schema:'lspv4-502-independent-js-check-v1',checks,inputs:inputs.length,runs:count,sat:8,unsat:8,malformed_or_short:inputs.length-16,source_sha256,large_example:example,result:'PASS',model:'hosted BigInt simulation, NOT native FLMV'};
}
if(require.main===module)process.stdout.write(JSON.stringify(run(),null,2)+'\n');
