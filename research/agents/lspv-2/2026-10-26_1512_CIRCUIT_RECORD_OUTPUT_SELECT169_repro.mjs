"use strict";
/* CIRCUIT-RECORD-OUTPUT-SELECT169. No external dependencies.
   node 2026-10-26_1512_CIRCUIT_RECORD_OUTPUT_SELECT169_repro.mjs
   Prediction does NOT build occurrence tables. Audit-only maps check its output.
*/
const ck=(ok,msg)=>{if(!ok)throw Error(msg)};
class Net{
 constructor(w,K){this.w=w;this.K=K;this.D=w+3;this.H=7*(w+2);
  this.F=13*w+32;this.M=K*this.D+2;this.c0=this.M-1;this.c1=this.M;
  this.g=[];this.layers=[]}
 gate(op,a,b){ck(a&&b&&Math.abs(a)<=this.M+this.g.length&&Math.abs(b)<=this.M+this.g.length,"acyclic");
  this.g.push({op,a,b});return this.M+this.g.length}
 A(a,b){return this.gate("and",a,b)}
 O(a,b){return this.gate("or",a,b)}
 eq(a,b){return -this.O(this.A(a,-b),this.A(-a,b))}
 mux(s,a,b){return this.O(this.A(-s,a),this.A(s,b))}
 comp(U,V,up){let w=this.w;
  let av=U.slice(w,w+2).concat(U.slice(0,w)),bv=V.slice(w,w+2).concat(V.slice(0,w));
  let x=up?bv:av,y=up?av:bv,less=this.c0,eq=this.c1;
  for(let j=w+1;j>=0;j--){less=this.O(less,this.A(eq,this.A(-x[j],y[j])));eq=this.A(eq,this.eq(x[j],y[j]))}
  return less}
 build(){let K=this.K,D=this.D;
  let R=Array.from({length:K},(_,p)=>Array.from({length:D},(_,c)=>1+p*D+c));
  const h=Math.log2(K);
  for(let a=1;a<=h;a++)for(let b=a-1;b>=0;b--){
   let s=2**b,size=2**a,newR=R.slice(),pairs=[];
   for(let i=0;i<K;i++){let j=i^s;if(i>=j)continue;
    let start=this.g.length,up=(i&size)===0,sw=this.comp(R[i],R[j],up);
    ck(this.g.length-start===this.H,"H");
    newR[i]=R[i].map((v,c)=>this.mux(sw,v,R[j][c]));
    newR[j]=R[j].map((v,c)=>this.mux(sw,v,R[i][c]));
    ck(this.g.length-start===this.F,"F");
    pairs.push({i,j,start,up,sw})}
   ck(pairs.length===K/2,"pair count");this.layers.push({s,size,pairs});R=newR}
  ck(this.g.length===(K*h*(h+1)/4)*this.F,"global G");return this}
 signed(t){return Math.sign(t)*(Math.abs(t)<=this.M?Math.abs(t):this.M+3+9*(Math.abs(t)-this.M-1))}
 clause(g,r){let {op,a,b}=this.g[g],ba=this.M+1+9*g,u=ba,v=ba+1,y=ba+2;
  a=this.signed(a);b=this.signed(b);
  if(r<4){let p=r<2?[-u,a]:[u,-a],aux=r<2?ba+3:ba+4;return [p[0],p[1],aux*(r%2? -1:1)]}
  if(r<8){let t=r-4,p=t<2?[-v,b]:[v,-b],aux=t<2?ba+5:ba+6;return [p[0],p[1],aux*(t%2?-1:1)]}
  if(op==="and"){if(r===8)return [-u,-v,y];if(r<11)return [u,-y,(ba+7)*(r===9?1:-1)];return [v,-y,(ba+8)*(r===11?1:-1)]}
  if(r===8)return [u,v,-y];if(r<11)return [-u,y,(ba+7)*(r===9?1:-1)];return [-v,y,(ba+8)*(r===11?1:-1)]}
 eval(bits){ck(bits.length===this.K*this.D,"bits");
  let val=new Uint8Array(this.M+this.g.length+1);
  bits.forEach((x,i)=>val[i+1]=x);val[this.c1]=1;
  for(let i=0;i<this.g.length;i++){let {op,a,b}=this.g[i];
   let x=val[Math.abs(a)]^(a<0?1:0),y=val[Math.abs(b)]^(b<0?1:0);
   val[this.M+i+1]=op==="and"?(x&y):(x|y)}return val}
 src(bits){let val=this.eval(bits),a=new Uint8Array(this.M+9*this.g.length+1);
  for(let j=1;j<=this.M;j++)a[j]=val[j];
  this.g.forEach(({a:x,b:y},g)=>{let ba=this.M+1+9*g;
   a[ba]=val[Math.abs(x)]^(x<0?1:0);
   a[ba+1]=val[Math.abs(y)]^(y<0?1:0);
   a[ba+2]=val[this.M+g+1]});return a}
}
function predicted(C,L,r,u){
 const K=C.K,D=C.D,w=C.w,H=C.H,F=C.F;
 const l=C.layers[L],s=l.s,pairLow=2*s*Math.floor(r/s)+(r%s);
 const side=Math.floor(u/D),c=u%D,p=pairLow+side*s;
 const nxt=C.layers[L+1],ns=nxt.s,low=p&~ns;
 const nr=Math.floor(low/(2*ns))*ns+(low%ns);
 const start=(L+1)*(K/2)*F+nr*F;
 ck(nxt.pairs[nr].i===low&&nxt.pairs[nr].start===start,"indexed comparator locator");
 const asc=(low&nxt.size)===0,nextSide=(p&ns)?1:0,out=[];
 if(c<w+2){
  let t=c<w?w-1-c:2*w+1-c;
  if(nextSide===(asc?1:0))out.push([start+7*t,0,-1],[start+7*t+3,0,1],[start+7*t+4,0,-1]);
  else out.push([start+7*t,1,1],[start+7*t+3,1,-1],[start+7*t+4,1,1])}
 if(nextSide===0)out.push([start+H+3*c,1,1],[start+H+3*(D+c)+1,1,1]);
 else out.push([start+H+3*c+1,1,1],[start+H+3*(D+c),1,1]);
 return out.sort((a,b)=>a[0]-b[0]||a[1]-b[1])
}
function selectOcc(g,uses,i){
 ck(i>=0&&i<5+4*uses.length,"occ range");
 if(i===0)return [13*g+8,2,0];
 if(i<=4)return [13*g+8+i,1,1];
 let j=Math.floor((i-5)/4),r=(i-5)%4,[cg,slot,sign]=uses[j];
 return [13*cg+4*slot+r,1,r<2?+(sign===1):+(sign!==1)]
}
function rankOcc(g,uses,c,k){
 for(let i=0;i<5+4*uses.length;i++){let z=selectOcc(g,uses,i);if(z[0]===c&&z[1]===k)return i}
 return -1}
function run(){
 const cases=[],total={comparators:0,gates:0,compiler_rows:0,
  targets:0,gate_uses:0,cnf_occurrences:0,rank_roundtrips:0,correct_sat_rows:0};
 for(const [w,K] of [[2,4],[2,8],[2,16],[3,8],[3,16],[5,8],[5,16],[8,8]]){
  let C=new Net(w,K).build(),direct=new Map(),targets=new Map(),actual=new Map();
  C.g.forEach(({a,b},g)=>{[a,b].forEach((z,slot)=>{
   let producer=Math.abs(z)-C.M-1;
   if(producer>=0){if(!direct.has(producer))direct.set(producer,[]);
    direct.get(producer).push([g,slot,z>0?1:-1])}})});
  for(let L=0;L<C.layers.length-1;L++)for(let r=0;r<K/2;r++)for(let u=0;u<2*C.D;u++){
   let g=L*(K/2)*C.F+r*C.F+C.H+3*u+2,uses=predicted(C,L,r,u);
   ck(C.g[g].op==="or","record output OR");
   ck(JSON.stringify(uses)===JSON.stringify(direct.get(g)||[]),"all direct uses");
   ck(uses.length===(u%C.D<C.w+2?5:2),"fanout");
   targets.set(C.M+3+9*g,{g,uses});total.targets++;total.gate_uses+=uses.length}
  let bits=Array.from({length:K*C.D},(_,j)=>(17*j+Math.floor(j/3)+w+K)%2),src=C.src(bits);
  for(let g=0;g<C.g.length;g++)for(let row=0;row<13;row++){
   let cl=C.clause(g,row);
   ck(new Set(cl.map(Math.abs)).size===3,"three distinct literals");
   ck(cl.some(x=>src[Math.abs(x)]===+(x>0)),"satisfying extension");
   total.compiler_rows++;total.correct_sat_rows++;
   cl.forEach((x,k)=>{let v=Math.abs(x);if(targets.has(v)){
    if(!actual.has(v))actual.set(v,[]);actual.get(v).push([13*g+row,k,+(x>0)])}})}
  let counts={key:0,payload:0,occ:0};
  for(const [v,{g,uses}] of targets){
   const ex=Array.from({length:5+4*uses.length},(_,i)=>selectOcc(g,uses,i));
   ck(JSON.stringify(ex)===JSON.stringify(actual.get(v)||[]),"every signed source occurrence");
   ck(ex.length===(uses.length===5?25:13),"closed-form degree");
   let pos=ex.filter(q=>q[2]===1).length;
   ck(pos===4+2*uses.length&&ex.length-pos===1+2*uses.length,"signed frequency");
   ex.forEach(([cl,k],i)=>{ck(rankOcc(g,uses,cl,k)===i,"Rank/Select");total.rank_roundtrips++});
   ck(rankOcc(g,uses,13*C.g.length+1,2)===-1,"absent rank");
   counts.occ+=ex.length;total.cnf_occurrences+=ex.length;
   if(uses.length===5)counts.key++;else counts.payload++}
  total.gates+=C.g.length;total.comparators+=C.g.length/C.F;
  cases.push({w,K,layers:C.layers.length,gates:C.g.length,
     nonfinal_key_record_outputs:counts.key,nonfinal_payload_record_outputs:counts.payload,
     exact_signed_compiler_occurrences:counts.occ})}
 return {run_id:"CIRCUIT-RECORD-OUTPUT-SELECT169",seed:"deterministic",
  proof_status:"PROVED/EXACT restricted arithmetic nonfinal forward record-output inverse",
  tests:cases,assertion_categories:total,failed_assertions:0,
  limitations:["last sorting layer to scan","reverse payload network","high-fanout constants and input aliases",
   "full compiler source Rank/Select","arbitrary ordinary-SAT parser",
   "all-input SAT decision circuit compression and ARC-EDGE-90"]}}
const result=run();
if(typeof process!=="undefined"&&process.stdout&&process.argv[1]&&
 process.argv[1].includes("CIRCUIT_RECORD_OUTPUT_SELECT169"))
 process.stdout.write(JSON.stringify(result,null,2)+"\n");
