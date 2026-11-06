#!/usr/bin/env node
// Standalone finite control for LSPV-4/436. Not a native FLMV emulator.
let checks=0;const ok=(x,msg='check')=>{checks++;if(!x)throw Error(msg)};
const unary=n=>'1'.repeat(n)+'0';
const encode=v=>{const s=(v+1).toString(2);return '1'.repeat(s.length-1)+'0'+s};
function decode(s){let i=0,r=0;while(s[i]==='1'){i++;r++}ok(s[i]==='0');i++;const out=[];
for(let j=0;j<r;j++){let b=1;while(s[i]==='1'){i++;b++}ok(s[i]==='0');i++;const v=parseInt(s.slice(i,i+b),2)-1;i+=b;ok(v>=0);out.push(v)}
ok(i===s.length);return out}
function graph(n){const e=[];if(n===4)for(let a=0;a<4;a++)for(let b=a+1;b<4;b++)e.push([a,b]);
if(n===8)for(let a=0;a<8;a++)for(let k=0;k<3;k++){let b=a^(1<<k);if(a<b)e.push([a,b])}
if(n===10)for(let a=0;a<5;a++)e.push([a,(a+1)%5],[a,a+5],[a+5,5+(a+2)%5]);
return e.map(x=>x.slice().sort((a,b)=>a-b)).sort((x,y)=>x[0]-y[0]||x[1]-y[1])}
function clauses(n,edges,c){const inc=Array.from({length:n},()=>[]);edges.forEach(([a,b],i)=>{inc[a].push(i+1);inc[b].push(i+1)});
ok(inc.every(v=>v.length===3));let cl=[];for(let v=0;v<n;v++){const [a,b,d]=inc[v].sort((x,y)=>x-y);
for(let p=0;p<2;p++)for(let r=0;r<2;r++)cl.push([[a,p],[b,r],[d,p^r^1^c[v]]])}return cl}
function sat(cl,M){for(let m=0;m<2**M;m++)if(cl.every(c=>c.some(([v,p])=>((m>>(v-1))&1)^p)))return true;return false}
for(const n of [4,8,10])for(const parity of [0,1]){const edges=graph(n),base=Array(n).fill(0);base[0]=parity;
ok(sat(clauses(n,edges,base),edges.length)===(parity===0),'source truth label');
const streams=Array.from({length:39},(_,e)=>Array.from({length:e%5},(_,j)=>(e*7+j*3+n)%n));
const packet=streams.map(s=>unary(s.length)+s.map(encode).join(''));const bank=Array(n).fill(0);
let cursor=0,toggles=0,reads=0;
function replay(e){const v=decode(packet[e]);reads+=packet[e].length;ok(JSON.stringify(v)===JSON.stringify(streams[e]));
for(const x of v){ok(x<n);bank[x]^=1;toggles++}}
function dfs(depth){if(depth===3)return;for(let i=0;i<3;i++){const e=cursor++,old=bank.join('');
replay(e);ok(clauses(n,edges,base.map((b,v)=>b^bank[v])).length===4*n);
dfs(depth+1);replay(e);ok(bank.join('')===old,'parent rollback')}}
dfs(0);ok(cursor===39&&bank.every(v=>v===0));ok(toggles===2*streams.reduce((n,s)=>n+s.length,0));
console.log(JSON.stringify({vertices:n,parity,streams:cursor,toggles,read_bits:reads,checks}))}
const b=[0,0],next=()=>b[0]===0?0:1;b[next()]^=1;b[next()]^=1;
ok(b[0]===1&&b[1]===1,'adaptive generator counterexample');
console.log(JSON.stringify({passed:true,checks}));
