function run(){
const assert=(a,m)=>{if(!a)throw Error(m||"assert")};
const pc=x=>{let n=0;while(x){x&=x-1n;n++}return n};
const bit=i=>1n<<BigInt(i);
const cube=(ids,values)=>{let m=0n,v=0n;ids.forEach((id,j)=>{m|=bit(id);if(values[j])v|=bit(id)});return {m,v,ids}};
const join=(a,b)=>((a.v^b.v)&a.m&b.m)?null:{m:a.m|b.m,v:a.v|b.v};
const CAP=10000000;
function budget(){return {ops:0,tick(){if(++this.ops>CAP)throw Error("CAP")}}}
function spectrum(cubes,n,t,b){
  const F=new Map([[0n,1n<<BigInt(n)]]);let terms=0,intersections=0;
  function add(m,v,sign){const a=BigInt(sign)*(1n<<BigInt(n-pc(m)));let u=m;for(;;){b.tick();terms++;const z=(F.get(u)||0n)+(pc(u&v)%2?-a:a);if(z)F.set(u,z);else F.delete(u);if(!u)break;u=(u-1n)&m}}
  function walk(i,cur,d){for(let j=i;j<cubes.length;j++){b.tick();const c=join(cur,cubes[j]);if(!c)continue;intersections++;if(d===t)return false;add(c.m,c.v,d%2?1:-1);if(!walk(j+1,c,d+1))return false}return true}
  if(!walk(0,{m:0n,v:0n},0))return {status:"OVERLAP",terms,intersections};
  const mass=F.get(0n)||0n;if(!mass)return {status:"NO",terms,intersections};
  const rows=[];for(const [u,a] of F){b.tick();if(u&& (a===mass||a===-mass))rows.push([u,a===mass?0:1])}
  return {status:"OK",mass,rows,terms,intersections,sparsity:F.size};
}
function gauss(rows){const piv=new Map();for(let [m,r] of rows){while(m){const p=m&-m;if(!piv.has(p)){piv.set(p,[m,r]);break}const [v,s]=piv.get(p);m^=v;r^=s}if(!m&&r)return "NO"}return "UNKNOWN"}
function make(k,odd=true){
  const s=2**(k+1),V=2*s,E=s*k,H=2**k,n=E+H,clauses=[];
  for(let v=0;v<V;v++){const ids=Array.from({length:k},(_,j)=>v<s?v*k+j:((v-s-j+s)%s)*k+j);const q=odd&&v===0?1:0;let j=0;
    for(let w=0;w<2**k;w++){if((pc(BigInt(w))%2)===q)continue;const vals=ids.map((_,a)=>(w>>a)&1);const t=E+2*j,u=t+1;j++;
      clauses.push(cube([...ids,t],[...vals,0]),cube([...ids,u],[...vals,0]),cube([...ids,t,u],[...vals,0,0]),cube([...ids,t,u],[...vals,1,1]));
    }}
  return {k,s,V,E,H,n,clauses};
}
function group(F,mode,b){const count=Array(F.n).fill(0);for(const c of F.clauses){b.tick();for(const i of c.ids){b.tick();count[i]++}}const max=Math.max(...count),hubs=new Set(count.flatMap((c,i)=>c*2>max?[i]:[])),g=new Map();
  for(const c of F.clauses){b.tick();const ids=c.ids.filter(i=>mode==="scope"||!hubs.has(i)).sort((a,b)=>a-b);const key=ids.join(",");if(!g.has(key))g.set(key,{ids,cubes:[]});g.get(key).cubes.push(c)}return {g,hubs};
}
function direct(F,G,b){const rows=[];let words=0;
  for(const {ids,cubes} of G.g.values()){
    const mask=ids.reduce((m,i)=>m|bit(i),0n);const wrong=new Set();let possible=null;
    for(let w=0;w<2**ids.length;w++){let x=0n;ids.forEach((i,j)=>{if((w>>j)&1)x|=bit(i)});const active=cubes.filter(c=>{b.tick();return ((x^c.v)&mask)===0n});
      const aux=Array.from(new Set(active.flatMap(c=>c.ids.filter(i=>!(mask&bit(i))))));assert(aux.length<=2,"private pattern check");
      let any=false;for(let a=0;a<2**aux.length;a++){let z=x;aux.forEach((i,j)=>{if((a>>j)&1)z|=bit(i)});words++;b.tick();if(active.every(c=>((z^c.v)&c.m)!==0n))any=true}
      if(!any)wrong.add(w);else{const p=pc(BigInt(w))%2;if(possible===null)possible=p;else assert(possible===p,"not parity")}
    }
    assert(wrong.size===2**(ids.length-1)&&possible!==null,"wrong parity partition");rows.push([mask,possible]);
  }return {status:gauss(rows),words,rows};
}
function initial(F,b){let assigned=0;for(const c of F.clauses){b.tick();if(c.ids.length<=1)assigned++}assert(!assigned,"unit closure not empty");return assigned}
function digest(F){let h=14695981039346656037n;for(const c of F.clauses){for(const x of [c.m,c.v]){for(const ch of x.toString(16)){h^=BigInt(ch.charCodeAt(0));h=BigInt.asUintN(64,h*1099511628211n)}}h^=255n}return h.toString(16)}
function test(k,odd=true){const F=make(k,odd);const A=budget();initial(F,A);const S=group(F,"scope",A);let sr=0;for(const {cubes} of S.g.values()){const x=spectrum(cubes,F.n,3,A);assert(x.status==="OK");sr+=x.rows.length}assert(!sr);
  const B=budget();initial(F,B);const G=group(F,"hub",B);const D=direct(F,G,B);
  const C=budget();initial(F,C);const H=group(F,"hub",C);let rows=[],terms=0,intersections=0,sp=0,maxrank=0;
  for(const {ids,cubes} of H.g.values()){const x=spectrum(cubes,F.n,3,C);assert(x.status==="OK"&&x.rows.length===1&&x.sparsity===2);rows.push(...x.rows);terms+=x.terms;intersections+=x.intersections;sp=Math.max(sp,x.sparsity);maxrank=Math.max(maxrank,pc(cubes.reduce((m,c)=>m|c.m,0n)));initial(F,C)}
  assert(rows.length===F.V);const status=gauss(rows);assert(status===D.status);const rk= Math.max(2,F.n,F.clauses.length);return {k,odd,n:F.n,vertices:F.V,clauses:F.clauses.length,gridBits:16*rk*rk+8*rk+Math.floor(Math.log2(rk))+1,hash:digest(F),scopeRows:sr,scopeOps:A.ops,directOps:B.ops,directWords:D.words,direct:D.status,hybridOps:C.ops,regions:H.g.size,detectedHubs:H.hubs.size,maxrank,terms,intersections,sparsity:sp,status,rows:rows.map(([m,r])=>[m.toString(16),r])};
}
const jobs=[2,3,4,5].map(k=>test(k));const control=test(2,false);
const F=make(2);const G=group(F,"hub",budget());const first=G.g.values().next().value.cubes;
const miss=spectrum(first.slice(1),F.n,3,budget());assert(miss.status==="OK"&&miss.rows.length===0);
const duplicate=spectrum([first[0],first[0],first[0],first[0]],F.n,3,budget());assert(duplicate.status==="OVERLAP");
let exhaustive=0;for(const {ids,cubes} of G.g.values()){const all=Array.from(new Set(cubes.flatMap(c=>c.ids)));const mask=ids.reduce((m,i)=>m|bit(i),0n);let support=0;for(let w=0;w<2**all.length;w++){let x=0n;all.forEach((i,j)=>{if((w>>j)&1)x|=bit(i)});const sat=cubes.every(c=>((x^c.v)&c.m)!==0n);if(sat)support++;const s=spectrum;const parity=pc(x&mask)%2;const expected=ids.every(i=>i<2)?1:0; // determine independently using direct row below
const row=direct(F,{g:new Map([["r",{ids,cubes}]])},budget()).rows[0];assert(sat===(parity===row[1]));exhaustive++;}assert(support===2**(all.length-1))}
return {CAP,jobs,control,hostile:{missingClause:miss.rows.length,overlap:duplicate.status,exhaustive}};
}
console.log(JSON.stringify(run(),null,2));
