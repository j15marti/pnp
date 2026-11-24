// MS03 standalone Node.js exact small tests
function experiment(){
const bit=i=>1n<<BigInt(i), low=x=>x&-x, par=x=>{let p=0;while(x){x&=x-1n;p^=1}return p};
const lin=m=>m!==0n&&(m&(m-1n))===0n, quad=m=>m!==0n&&!lin(m);
function toggle(s,m){if(s.has(m))s.delete(m);else s.add(m)}
function add(a,b){let s=new Set(a);for(const m of b)toggle(s,m);return s}
function sub(p,x,L){let s=new Set();for(const m of p){if(m&x){for(const l of L)toggle(s,(m^x)|l)}else toggle(s,m)}return s}
function poly(a,b,v){let p=new Set();if(v[0])toggle(p,0n);if(v[0]^v[1])toggle(p,a);if(v[0]^v[2])toggle(p,b);if(v[0]^v[1]^v[2]^v[3])toggle(p,a|b);return p}
function row(m,c){let p=new Set(c?[0n]:[]);while(m){let x=low(m);m^=x;toggle(p,x)}return p}
function domain(a,b,ok){let allowed=[];for(let t=0;t<4;t++)if(ok[t])allowed.push(t);
if(!allowed.length)return [new Set([0n])];if(allowed.length===4)return [];
if(allowed.length===3)return [poly(a,b,ok.map(v=>v?0:1))];
let ans=[];for(let m=1;m<4;m++){let c=par(BigInt(m&allowed[0]));if(allowed.every(t=>par(BigInt(m&t))===c))ans.push(row((m&1?a:0n)^(m&2?b:0n),c))}return ans}
function reduce(eqs,phase,vars){let es=eqs.map(p=>new Set(p)), ph=new Set(phase),steps=0;
for(;;){let basis=new Map(), found=null;
for(let p0 of es){let p=new Set(p0);for(;;){let m=null;for(let z of p)if(quad(z)&&(m===null||z>m))m=z;
if(m===null){if(p.size){found=p;}break}if(basis.has(m))p=add(p,basis.get(m));else{basis.set(m,p);break}}
if(found)break}
if(!found)return {eq:[...basis.values()],phase:ph,vars,steps};
let x=[...found].find(lin);if(x===undefined)return null;
found.delete(x);es=es.map(p=>sub(p,x,found));ph=sub(ph,x,found);vars^=x;steps++;
}}
function gauss(p,vars){let f=1n;while(vars){let x=low(vars);vars^=x;let l=new Set(),rest=new Set();for(let m of p){if(m&x)toggle(l,m^x);else toggle(rest,m)}
let y=[...l].find(lin);if(y===undefined){if(l.has(0n))return 0n;p=rest;f*=2n;continue}
l.delete(y);p=sub(rest,y,l);vars^=y;f*=2n;}return p.has(0n)?-f:f}
function sumFiltered(R){let total=0n, calls=0;const eq=R.eq;
function rec(i,p){if(i===eq.length){total+=gauss(p,R.vars);calls++;return}rec(i+1,p);rec(i+1,add(p,eq[i]))}
rec(0,R.phase);let den=bit(eq.length);if(total%den)throw Error("noninteger");return [total/den,calls]}
function mass(I,c,extra=[]){const {n,d,r,F,A}=I, vars=bit(n)-1n, base=[...A,...extra];let qmax=0,calls=0,chars=0,affineSteps=0,triple=0;
for(const f of F)base.push(...domain(bit(f.a),bit(f.b),f.ok));
for(let j=r;j<d;j++){let p=new Set(c&bit(j)?[0n]:[]);for(let f of F)p=add(p,poly(bit(f.a),bit(f.b),f.off.map(v=>Number((v>>BigInt(j))&1n))));base.push(p)}
let b=reduce(base,new Set(),vars);if(!b)return {z:0n,qmax,calls,chars,affineSteps,triple};
let z=0n;for(let l=0n;l<bit(r);l++){chars++;let eq=[...base],ph=new Set(par(l&c)?[0n]:[]);
for(let f of F){let ok=f.ok.map((v,t)=>v&&f.gen[t].every(g=>!par(l&g)));if(ok.filter(Boolean).length===3)triple++;
eq.push(...domain(bit(f.a),bit(f.b),ok));ph=add(ph,poly(bit(f.a),bit(f.b),f.off.map(v=>par(l&v))))}
let R=reduce(eq,ph,vars);if(!R)continue;qmax=Math.max(qmax,R.eq.length);affineSteps+=R.steps;let [s,k]=sumFiltered(R);z+=s;calls+=k}
if(z<0n)throw Error("negative mass");return {z,qmax,calls,chars,affineSteps,triple}}
function evaluate(p,x){let z=0;for(let m of p)if((x&m)===m)z^=1;return z}
function local(I,x){if(I.A.some(p=>evaluate(p,x)))return null;let offset=0n,s=new Set([0n]);for(let f of I.F){let t=Number((x>>BigInt(f.a))&1n)+2*Number((x>>BigInt(f.b))&1n);if(!f.ok[t])return null;offset^=f.off[t];for(let g of f.gen[t])for(let v of [...s])s.add(v^g)}return {offset,s}}
function brute(I){let out=new Map();for(let x=0n;x<bit(I.n);x++){let L=local(I,x);if(!L)continue;for(let v of L.s){let c=v^L.offset;out.set(c,(out.get(c)||0n)+bit(I.r)/BigInt(L.s.size))}}return out}
function witness(I,c){let x=0n,extra=[];for(let j=0;j<I.n;j++){let z=row(bit(j),0);if(mass(I,c,[...extra,z]).z>0n)extra.push(z);else{x|=bit(j);extra.push(row(bit(j),1))}}let L=local(I,x);if(!L||!L.s.has(c^L.offset))throw Error("bad witness");return x}
let seed=0x2013030;function rnd(n){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return (seed>>>0)%n}
let stat={seed:"0x2013030",networks:0,targets:0,sat:0,unsat:0,witnesses:0,characters:0,gaussCalls:0,maxQ:0,tripleSurvivorOccurrences:0,affineSteps:0,gaussReferenceChecks:0,scaling:[]};
for(let i=0;i<350;i++){let n=2+rnd(6),p=new Set();for(let a=0;a<n;a++){if(rnd(2))p.add(bit(a));for(let b=a+1;b<n;b++)if(rnd(2))p.add(bit(a)|bit(b))}if(rnd(2))p.add(0n);let exact=0n;for(let x=0n;x<bit(n);x++)exact+=evaluate(p,x)?-1n:1n;if(exact!==gauss(p,bit(n)-1n))throw Error("gauss mismatch");stat.gaussReferenceChecks++}
for(let j=0;j<180;j++){let n=2+rnd(6),d=2+rnd(4),r=rnd(Math.min(3,d)+1),F=[],A=[];
for(let k=0;k<2+rnd(5);k++){let a=rnd(n),b=rnd(n-1);if(b>=a)b++;F.push({a,b,ok:Array.from({length:4},()=>rnd(5)!==0),off:Array.from({length:4},()=>BigInt(rnd(2**d))),gen:Array.from({length:4},()=>Array.from({length:rnd(3)},()=>BigInt(rnd(2**r))))})}
for(let k=0;k<rnd(3);k++)A.push(row(BigInt(rnd(2**n)),rnd(2)));
let I={n,d,r,F,A},B=brute(I);stat.networks++;
for(let c=0n;c<bit(d);c++){let M=mass(I,c);if(M.z!==(B.get(c)||0n))throw Error("mass mismatch "+j+" "+c);stat.targets++;stat.characters+=M.chars;stat.gaussCalls+=M.calls;stat.affineSteps+=M.affineSteps;stat.tripleSurvivorOccurrences+=M.triple;stat.maxQ=Math.max(stat.maxQ,M.qmax);if(M.z){stat.sat++;if(stat.witnesses<150){witness(I,c);stat.witnesses++}}else stat.unsat++}}
for(let h of [4,8,16,32,64,128]){let F=[],A=[];for(let i=0;i<h;i++){F.push({a:0,b:1,ok:[true,true,true,true],off:[0n,0n,0n,0n],gen:[[],[],[],[1n]]});F.push({a:i+2,b:0,ok:[true,true,true,true],off:[0n,bit(i+1),0n,bit(i+1)],gen:[[],[],[],[]]})}F.push({a:0,b:1,ok:[true,true,true,true],off:[0n,0n,0n,bit(h+1)],gen:[[],[],[],[]]});
let I={n:h+2,d:h+2,r:1,F,A},S=mass(I,bit(h+1)|1n),U=mass(I,1n);if(S.z!==1n||U.z!==0n)throw Error("scale");if(h<=32)witness(I,bit(h+1)|1n);stat.scaling.push({h,variables:I.n,ambientRank:I.d,nonaffineGuardOccurrences:U.triple,maxQ:Math.max(S.qmax,U.qmax),satMass:String(S.z),unsatMass:String(U.z),charactersSAT:S.chars,charactersUNSAT:U.chars,gaussSAT:S.calls,gaussUNSAT:U.calls})}
return stat;
}
console.log(JSON.stringify(experiment(),null,2));
