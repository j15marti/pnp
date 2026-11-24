function run(){
const L={checks:0,closureScans:0,deletions:0,periodTests:0,quotients:0,removedRank:0,conflicts:0,zeroCharacters:0,edges:0,peak:0,referenceTuples:0,profiles:0,lifts:0};
const eq=(a,b)=>{L.checks++;if(a!==b)throw Error(`${a} != ${b}`)};
function parity(x){let p=0;while(x){x&=x-1n;p^=1}return p}
function top(x){return x.toString(2).length-1}
function reduce(x,B){let p=0;for(const [k,[v,s]] of [...B].sort((a,b)=>b[0]-a[0]))if((x>>BigInt(k))&1n){x^=v;p^=s}return [x,p]}
function add(B,x,p=0){let [v,s]=reduce(x,B);p^=s;if(!v)return !p;B.set(top(v),[v,p]);return true}
function accum(M,k,v){let n=(M.get(k)||0n)+v;if(n)M.set(k,n);else M.delete(k)}
function affine(fs){let a=0n,B=new Map();for(const f of fs){a^=f[0];for(const t of f)add(B,t^f[0])}return [a,B]}
function close(fs,b,q,h=null){fs=fs.map(f=>f.slice());const tag=r=>h===null?r[0]:(r[0]<<BigInt(q))|BigInt(r[1]);const target=h===null?b:(b<<BigInt(q))|BigInt(h);while(true){L.closureScans++;if(fs.some(f=>!f.length))return null;let change=false;for(let i=0;i<fs.length&&!change;i++){let [a,B]=affine(fs.filter((_,j)=>j!==i).map(f=>f.map(tag)));let keep=fs[i].filter(r=>reduce(target^a^tag(r),B)[0]===0n);if(keep.length!==fs[i].length){L.deletions+=fs[i].length-keep.length;fs[i]=keep;change=true}}if(!change)return fs}}
function channel(fs,b,chi){let F=fs.map(f=>{let M=new Map();for(const [t,g,w] of f)accum(M,t,parity(BigInt(g&chi))?-w:w);return M});if(F.some(m=>!m.size)){L.zeroCharacters++;return 0n}let B=new Map();
for(const M of F){let [a,wa]=M.entries().next().value;for(const [x,wx] of M){if(wx!==wa&&wx!==-wa)continue;let h=x^a,s=wx===wa?0:1;L.periodTests++;if([...M].every(([y,wy])=>M.get(y^h)===(s?-wy:wy))){if(!add(B,h,s)){L.conflicts++;return 0n}}}}
if(B.size){L.quotients++;L.removedRank+=B.size}
const [target,phase]=reduce(b,B);
F=F.map(M=>{let Q=new Map();for(const [t,w] of M){let [r,s]=reduce(t,B);accum(Q,r,s?-w:w)}return Q});
if(F.some(m=>!m.size))return 0n;
const suffix=[];for(let i=0;i<=F.length;i++)suffix.push(affine(F.slice(i).map(m=>[...m.keys()])));
let D=new Map([[0n,1n]]);
for(let i=0;i<F.length;i++){let E=new Map();let [a,S]=suffix[i+1];for(const [x,u] of D)for(const [t,v] of F[i]){L.edges++;let y=x^t;if(reduce(target^a^y,S)[0]===0n)accum(E,y,u*v)}D=E;L.peak=Math.max(L.peak,D.size)}
let z=D.get(target)||0n,den=1n<<BigInt(B.size);eq(z%den,0n);return (phase?-z:z)/den}
function profile(fs,b,q){L.profiles++;let c=close(fs,b,q);if(!c)return Array(1<<q).fill(0n);let a=Array.from({length:1<<q},(_,j)=>channel(c,b,j));return a.map((_,h)=>{let z=a.reduce((s,v,j)=>s+(parity(BigInt(j&h))?-v:v),0n);eq(z%BigInt(a.length),0n);return z/BigInt(a.length)})}
function ref(fs,b,q){let out=Array(1<<q).fill(0n);function go(i,t,g,w){if(i===fs.length){L.referenceTuples++;if(t===b)out[g]+=w;return}for(const [a,h,v]of fs[i])go(i+1,t^a,g^h,w*v)}go(0,0n,0,1n);return out}
function lift(fs,b,q,h){let c=close(fs,b,q,h);if(!c)return null;let selected=[];for(let i=0;i<c.length;i++){let found=false;for(const r of c[i]){let trial=c.map((f,j)=>j===i?[r]:f);let d=close(trial,b,q,h);if(d&&profile(d,b,q)[h]>0n){c=d;selected.push(r);found=true;break}}if(!found)throw Error("lift failed")}eq(selected.reduce((s,r)=>s^r[0],0n),b);eq(selected.reduce((s,r)=>s^r[1],0),h);L.lifts++;return selected}
let seed=120241120;function rand(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}
let sat=0,unsat=0;for(let k=0;k<160;k++){let q=1+rand(3),d=1+rand(5),fs=Array.from({length:2+rand(4)},()=>Array.from({length:1+rand(5)},()=>[BigInt(rand(1<<d)),rand(1<<q),BigInt(1+rand(3))]));let b=BigInt(rand(1<<d)),p=profile(fs,b,q),r=ref(fs,b,q);for(let h=0;h<p.length;h++){eq(p[h],r[h]);if(p[h]>0){sat++;if(k<40)lift(fs,b,q,h)}else unsat++}}
// Arbitrary signed rows: zero intermediate is algebraic, not semantic closure.
for(let k=0;k<100;k++){let fs=Array.from({length:3},()=>Array.from({length:4},()=>[BigInt(rand(8)),rand(4),BigInt(rand(5)-2)]));let b=BigInt(rand(8));let p=profile(fs,b,2),r=ref(fs,b,2);p.forEach((v,h)=>eq(v,r[h]))}
function occurrence(scopes,domains,bits){let by=new Map(),tags=scopes.map(s=>s.map(()=>Array(bits).fill(0n))),guards=scopes.map(s=>s.map(()=>0));scopes.forEach((s,i)=>s.forEach((v,j)=>{if(!by.has(v))by.set(v,[]);by.get(v).push([i,j])}));let pos=0;for(const [v,occ]of by){let [i,j]=occ[0];guards[i][j]=1;for(const [k,l]of occ.slice(1))for(let z=0;z<bits;z++){let e=1n<<BigInt(pos++);tags[i][j][z]^=e;tags[k][l][z]^=e}}return scopes.map((s,i)=>domains[i].map(word=>{let t=0n,g=0;word.forEach((v,j)=>{for(let z=0;z<bits;z++)if(v&(1<<z))t^=tags[i][j][z];if(guards[i][j])g^=(v&1)});return [t,g,1n]}))}
let triples=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];let nae=Array.from({length:8},(_,i)=>[i&1,(i>>1)&1,(i>>2)&1]);let fano=[];for(let r=-1;r<14;r++){let fs=occurrence(triples,triples.map((_,i)=>nae.filter((w,j)=>j!==0&&j!==7||r>=0&&i===Math.floor(r/2)&&j===(r%2?7:0))),1);let p=profile(fs,0n,1);eq(p[0]+p[1],r<0?0n:5n);fano.push(p.map(String));if(r>=0)lift(fs,0n,1,p[0]>0?0:1)}
let edges=[];for(let i=0;i<5;i++)for(let j=i+1;j<5;j++)edges.push([i,j]);let legal=[];for(let a=0;a<4;a++)for(let b=0;b<4;b++)if(a!==b)legal.push([a,b]);let k5=[];for(let j=-1;j<10;j++){let es=edges.filter((_,i)=>i!==j);let fs=occurrence(es,es.map(()=>legal),2);let p=profile(fs,0n,1);eq(p[0]+p[1],j<0?0n:24n);k5.push(p.map(String));}
// Every per-key period is trivial because g's low bit identifies t.
// z in {0,2,4} is a nonaffine two-bit feature. Two factors per coordinate.
let scales=[];for(const k of [4,8,16,32,64]){let fs=[];for(let copy=0;copy<2;copy++)for(let i=0;i<k;i++){let e=1n<<BigInt(i),f=[];for(let t=0;t<2;t++)for(let z of [0,2,4])f.push([t?e:0n,t|z,1n]);fs.push(f)}let before={...L};let p=profile(fs,0n,3);let mass=2n**BigInt(k)*3n**BigInt(2*k);eq(p.reduce((s,v)=>s+v,0n),mass);for(let h=1;h<8;h+=2)eq(p[h],0n);for(let h=0;h<8;h+=2)eq(p[h],2n**BigInt(k)*(3n**BigInt(2*k)+(h===0?3n:-1n))/4n);scales.push({k,profile:p.map(String),edges:L.edges-before.edges,rank:L.removedRank-before.removedRank,periodTests:L.periodTests-before.periodTests})}
// incompatible eigenperiod: convolution of [1,1] and [1,-1] cancels.
let pp=profile([[[0n,0,1n],[1n,0,1n]],[[0n,0,1n],[1n,1,1n]]],0n,1);eq(pp[0],1n);eq(pp[1],1n);
return {L,sat,unsat,fano,k5,scales};
}
console.log(JSON.stringify(run(),null,2));
