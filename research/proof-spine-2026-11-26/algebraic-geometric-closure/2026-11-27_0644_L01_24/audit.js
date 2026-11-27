function audit(){
const mod=x=>((x%3)+3)%3,par=x=>{let a=0;while(x){a^=1;x&=x-1n}return a}, bit=i=>1n<<BigInt(i);
const F=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
const A=[];for(let x=0;x<128;x++)if(F.every((_,e)=>F.reduce((s,t,j)=>s+(t.includes(e)?(x>>j&1):0),0)%2===1))A.push(x);
const lookup=new Map(A.map(x=>[(x&1)|((x>>3&1)<<1)|((x>>1&1)<<2),x]));
if(lookup.size!==8)throw Error("chart");
const pop=x=>{let n=0;while(x){n++;x&=x-1}return n};
function put(f,k,c){c=mod((f.get(k)||0)+c);if(c)f.set(k,c);else f.delete(k)}
function mul(f,g){let h=new Map;for(const [a,c] of f)for(const [b,d] of g)put(h,a^b,c*d);return h}
function reduce(k,R){let s=0;for(const [p,[u,c]] of R)if(k&bit(p)){k^=u;s^=c}return[k,s]}
function insert(R,k,c){[k,c]=(()=>{let [v,s]=reduce(k,R);return[v,s^c]})();if(!k)return c?-1:0;let p=k.toString(2).length-1;R.push([p,[k,c]]);R.sort((a,b)=>b[0]-a[0]);return 1}
function restrict(f,R){let g=new Map;for(const [k,c] of f){let [v,s]=reduce(k,R);put(g,v,s?-c:c)}return g}
function hull(f){if(!f.size)return null;let [a]=f.keys(),out=[];for(const b of f.keys()){let u=a^b;for(let c=0;c<2;c++){let ok=true;for(const [k,v] of f)if((f.get(k^u)||0)!==mod(c?-v:v)){ok=false;break}if(ok)out.push([u,c])}}return out}
function evalf(f,z){let a=0;for(const [k,c] of f)a+=par(k&z)?-c:c;return mod(a)}
function instance(b){
let T=[];for(let i=0;i<b;i++)for(let j=0;j<7;j++)T.push(F[j].map(e=>7*((j===0&&e===0)?(i+1)%b:(j===3&&e===1)?(i+b-1)%b:i)+e));
let rows=Array.from({length:7*b},()=>[]);T.forEach((t,j)=>t.forEach(e=>rows[e].push(j)));
let coords=[];for(let i=0;i<b;i++)for(let j=0;j<7;j++){let c=lookup.get(0)>>j&1,k=0n;for(let l=0;l<3;l++)if(((lookup.get(1<<l)>>j&1)^c))k^=bit(l<2?l:i+2);
for(let a=0;a<8;a++){let z=BigInt(a&3)|((a&4)?bit(i+2):0n);if((c^par(k&z))!==(lookup.get(a)>>j&1))throw Error("not affine")}
coords.push([k,c])}
for(const row of rows){let k=0n,c=0;for(let j of row){k^=coords[j][0];c^=coords[j][1]}if(k||c!==1)throw Error("not odd")}
let factors=rows.map(r=>{let f=new Map([[0n,1]]);for(let j of r){let [k,c]=coords[j];let x=new Map;put(x,0n,2);put(x,k,c?2:1);f=mul(f,x)}let g=new Map([[0n,1]]);for(let [k,c] of f)put(g,k,-c);return g});
let groups=rows.map((_,j)=>[j]);for(let i=0;i<b;i++)for(let x=0;x<7;x++)for(let y=x+1;y<7;y++)for(let z=y+1;z<7;z++)groups.push([7*i+x,7*i+y,7*i+z]);
function lane(feedback,cap=100000){let R=[],calls=0,trace=[],max=0;while(true){let changed=false;for(let J of groups){if(++calls>cap)return{status:"UNKNOWN_CAP",calls,trace,max};let f=new Map([[0n,1]]);for(let j of J)f=mul(f,restrict(factors[j],R));max=Math.max(max,f.size);if(!f.size)return{status:"UNSAT",calls,trace,rank:R.length,max,zero:J};if(feedback){let old=R.length;for(let [u,c] of hull(f)){if(insert(R,u,c)<0)throw Error("impossible equation")}if(R.length>old){trace.push({J,old,rank:R.length});changed=true;break}}}if(!changed)return{status:"UNKNOWN",calls,trace,rank:R.length,max}}}
let staticLane=lane(false),hybrid=lane(true);
let direct=0,brute=0;if(b<=6){for(let z=0;z<2**(b+2);z++){let a=coords.map(([k,c])=>c^par(k&BigInt(z)));let good=rows.every(r=>r.reduce((s,j)=>s+a[j],0)===1);let g=factors.every(f=>evalf(f,BigInt(z))===1);if(g!==good)throw Error("predicate mismatch");direct+=good;brute++}if(direct)throw Error("not NO")}
return {b,n:168*b,dimension:b+2,rows:rows.length,groups:groups.length,staticLane,hybrid,brute,direct}
}
let controls=0;for(let mask=1;mask<256;mask++){let f=new Map;for(let k=0;k<8;k++){let c=0;for(let z=0;z<8;z++)if(mask>>z&1)c+=par(BigInt(k&z))?-1:1;put(f,BigInt(k),2*c)}let E=hull(f);for(let u=0;u<8;u++)for(let c=0;c<2;c++){let want=Array.from({length:8},(_,z)=>z).every(z=>!(mask>>z&1)||par(BigInt(u&z))===c);if(want!==E.some(([v,s])=>v===BigInt(u)&&s===c))throw Error("hull");controls++}}
return {F,A,controls,scales:[3,6,12,24,48].map(instance)}
}
console.log(JSON.stringify(audit(),null,2));
