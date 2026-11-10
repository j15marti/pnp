// LSPV-2/534 independent JS implementation. Node 18+: node experiments/arc/lspv2_534_pyramid_xor_independent.mjs
import {createHash} from 'node:crypto';
function pyramid(h){let V=[],D=new Map();for(let r=0;r<=h;r++)for(let i=0;i<=h-r;i++){D.set(r+','+i,V.length);V.push([r,i])}
return {V,P:V.map(([r,i])=>r?[D.get((r-1)+','+i),D.get((r-1)+','+(i+1))]:[]),sink:D.get(h+',0')};}
function reach(h,b){const {P,sink}=pyramid(h);let Q=[0],seen=new Set(Q),p=0;
while(p<Q.length){let s=Q[p++];if(s&(1<<sink))return [true,p];
for(let i=0;i<P.length;i++){let bit=1<<i,t;if(s&bit)t=s^bit;else if(P[i].every(j=>s&(1<<j)))t=s|bit;else continue;
let pc=0;for(let u=t;u;u&=u-1)pc++;if(pc<=b&&!seen.has(t)){seen.add(t);Q.push(t);}}}return [false,p];}
function direct(bits){let a=[...bits];while(a.length>1){let b=[];for(let i=0;i<a.length-1;i++)b.push(a[i]^a[i+1]);a=b;}return a[0];}
function lucas(bits){let h=bits.length-1,y=0;for(let i=0;i<=h;i++)if((i&h)===i)y^=bits[i];return y;}
function source(charges){const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],b=[83,51,67,6,16];
for(let v=0;v<4;v++){let ids=edges.flatMap((e,i)=>e.includes(v)?[i+1]:[]);
for(let a=0;a<8;a++){let parity=0;for(let k=0;k<3;k++)parity^=(a>>k)&1;
if(parity!==charges[v])for(let k=0;k<3;k++)b.push(((a&(1<<k)?-ids[k]:ids[k])+256)%256);}}
return Buffer.from(b);}
function parse(buf){if(buf.length<5||buf.toString('ascii',0,3)!=='S3C')throw Error('header');
const n=buf[3],m=buf[4];if(buf.length!==5+3*m)throw Error('length');let clauses=[];
for(let i=0;i<m;i++){let row=[];for(let k=0;k<3;k++){let z=buf[5+i*3+k];z=z<128?z:z-256;if(!z||Math.abs(z)>n)throw Error('range');row.push(z)}
if(new Set(row.map(Math.abs)).size!==3)throw Error('duplicate');clauses.push(row);}return {n,clauses};}
function countModels(buf){let {n,clauses}=parse(buf),cnt=0;for(let bits=0;bits<(1<<n);bits++)
if(clauses.every(C=>C.some(l=>((bits>>(Math.abs(l)-1))&1)===+(l>0))))cnt++;return cnt;}
let out={id:'LSPV2-534',pebble:[],xor:[],controls:{},checks:0,malformed_rejected:0};
for(let h=1;h<5;h++){let [low,n]=reach(h,h+1),[high,m]=reach(h,h+2);if(low||!high)throw Error('pebbling');
out.checks+=2;out.pebble.push({height:h,vertices:pyramid(h).V.length,min_pebbles:h+2,no_goal_states:n,yes_goal_states:m});}
for(let h=0;h<16;h++){let coefficientCount=0;for(let j=0;j<=h;j++)coefficientCount+=((j&h)===j);
if(coefficientCount!==2**h.toString(2).replace(/0/g,'').length)throw Error('Lucas support');out.checks++;
const rows=h<=9?2**(h+1):80;for(let a=0;a<rows;a++){let x=[];
for(let j=0;j<=h;j++)x.push(h<=9?(a>>j)&1:Math.floor((a*37+j*j+17*j+a*j)/3)&1);
if(direct(x)!==lucas(x))throw Error('XOR discrepancy');out.checks++;}
out.xor.push({height:h,inputs:rows,nonzero_coeffs:coefficientCount});}
for(let h of [2,4,8]){if(out.xor[h].nonzero_coeffs!==2)throw Error('endpoint');out.checks++;}
if(direct([1,1,1])!==0)throw Error('AND control');out.checks++;
const odd=source([1,0,0,0]);for(const [name,charges] of [['k4_odd',[1,0,0,0]],['k4_even',[0,0,0,0]]]){
let buf=source(charges),cnt=countModels(buf);if((cnt===0)!==(name==='k4_odd'))throw Error('K4');
out.controls[name]={binary_bits:8*buf.length,clauses:16,models:cnt,sha256:createHash('sha256').update(buf).digest('hex'),vars:6};out.checks++;}
const variants=[Buffer.concat([Buffer.from('X'),odd.subarray(1)]),odd.subarray(0,-1),
Buffer.concat([odd.subarray(0,3),Buffer.from([6,15]),odd.subarray(5)]),
Buffer.concat([odd.subarray(0,5),Buffer.from([0]),odd.subarray(6)]),
Buffer.concat([odd.subarray(0,6),odd.subarray(5,6),odd.subarray(7)]),
Buffer.concat([odd.subarray(0,5),Buffer.from([7]),odd.subarray(6)])];
for(let mutant of variants){let rejected=false;try{parse(mutant)}catch{rejected=true;}
if(!rejected)throw Error('malformed accepted');out.checks++;out.malformed_rejected++;}
out.status='COMPUTATIONAL, plus known Cook/Nordstrom theorem';
out.warning='No native FLMV interpreter or SAT-decider lower bound';
console.log(JSON.stringify(out,null,2));
