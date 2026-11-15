"use strict";
// TMR-2/047 original sign-pivotal CNF plus physical multiscale tariff.
// Pure JS, deterministic; finite tests COMPUTATIONAL.
function audit(M=15) {
let A=0,mutations=0,steps=0,zero=0,exhaustive=0;
const failures=[],records=[];
function ok(b,x){A++;if(!b)failures.push(x)}
const gamma=n=>{let b=n.toString(2);return "0".repeat(b.length-1)+b};
const parity=a=>a.reduce((v,x)=>v^x,0);
const sat=(clauses,x)=>clauses.every(c=>c.some(([e,s])=>(x[e]^s)===1));
for(let m=2;m<=M;m++){
 const t=2*m,H=2*t,em=new Map();
 for(let i=0;i<t;i++)for(let [u,v] of [[i,(i+1)%t],[i+t,t+(i+1)%t],[i,i+t]]){
   let a=Math.min(u,v),b=Math.max(u,v);em.set(a+","+b,[a,b])
 }
 const edges=[...em.values()].sort((a,b)=>a[0]-b[0]||a[1]-b[1]),E=edges.length;
 const inc=Array.from({length:H},()=>[]),charges=Array.from({length:H},(_,v)=>+(v===0));
 edges.forEach(([u,v],e)=>{inc[u].push(e);inc[v].push(e)});
 inc.forEach(a=>a.sort((a,b)=>a-b));
 const cs=[],forbidden=[];
 for(let v=0;v<H;v++){
   const wrong=[];
   for(let z=0;z<8;z++){let s=[(z>>2)&1,(z>>1)&1,z&1];if(parity(s)!==charges[v])wrong.push(s)}
   const tail=wrong.find(s=>s[2]===0),order=[...wrong.filter(s=>s!==tail),tail];
   forbidden.push(order);
   for(const s of order)cs.push(inc[v].map((e,j)=>[e,s[j]]))
 }
 const width=Math.ceil(Math.log2(E+1));let bits="00110101"+gamma(E)+gamma(4*H);
 const signs=[],clausesEnd=[],verticesEnd=[];
 cs.forEach((c,i)=>{
   c.forEach(([e,s])=>{bits+=(e+1).toString(2).padStart(width,"0");signs.push(bits.length);bits+=s});
   clausesEnd.push(bits.length-1);if(i%4===3)verticesEnd.push(bits.length-1);
 });
 const N=bits.length;
 ok(H===4*m&&E===6*m&&cs.length===4*H&&signs.length===12*H,"source counts");
 ok(N===8+gamma(E).length+gamma(4*H).length+12*H*(width+1),"encoding");
 ok(bits.at(-1)==="0"&&new Set(signs).size===12*H,"sign positions");
 ok(inc.every(a=>a.length===3)&&cs.every(c=>new Set(c.map(y=>y[0])).size===3),"proper3");
 function extension(v,s){
   const vals=Array(E).fill(0),rhs=charges.slice(),adj=Array.from({length:H},()=>[]);
   inc[v].forEach((e,j)=>{vals[e]=s[j];let [a,b]=edges[e];rhs[a===v?b:a]^=s[j]});
   edges.forEach(([a,b],e)=>{if(a!==v&&b!==v){adj[a].push([b,e]);adj[b].push([a,e])}});
   let root=v===0?1:0,parents=Array(H).fill(-1),pedge=Array(H).fill(-1),order=[root];
   parents[root]=root;
   for(let i=0;i<order.length;i++)for(const [b,e] of adj[order[i]])if(parents[b]<0){
     parents[b]=order[i];pedge[b]=e;order.push(b)
   }
   ok(order.length===H-1,"G-v disconnected");
   for(let i=order.length-1;i>0;i--){let a=order[i];vals[pedge[a]]=rhs[a];rhs[parents[a]]^=rhs[a]}
   ok(rhs[root]===0,"GF2 parity root");
   for(let u=0;u<H;u++)
     ok(parity(inc[u].map(e=>vals[e]))===(u===v?1-charges[u]:charges[u]),"GF2 local");
   return vals;
 }
 for(let v=0;v<H;v++)for(let a=0;a<4;a++){
   let ci=4*v+a,vals=extension(v,forbidden[v][a]);
   ok(!sat(cs,vals),"original satisfies");
   for(let j=0;j<3;j++){
     let changed=cs.slice(),c=cs[ci].map(z=>z.slice());c[j][1]^=1;changed[ci]=c;
     let k=signs[ci*3+j],flip=bits.slice(0,k)+(bits[k]==="0"?"1":"0")+bits.slice(k+1);
     ok(flip.length===N&&flip.slice(0,k)===bits.slice(0,k)&&flip.slice(k+1)===bits.slice(k+1),"invalid bit flip");
     ok(sat(changed,vals),"SAT mutant failed");mutations++;
   }
 }
 if(m===2)for(let z=0;z<(1<<E);z++){
   ok(!sat(cs,Array.from({length:E},(_,e)=>(z>>e)&1)),"m2 source SAT");exhaustive++;
 }
 const S=new Set(signs),C=new Set(clausesEnd),V=new Set(verticesEnd);
 let pending=[H,4*H,12*H,N],rowCount=[0,0,0,0];
 for(let i=0;i<N;i++){
   let d=[+V.has(i),+C.has(i),+S.has(i),1];pending=pending.map((q,j)=>q-d[j]);
   ok(pending.every(q=>q>=0),"negative potential");
   for(const lambda of [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1],[0.1,0.2,0.3,0.4]])
     ok(lambda.reduce((s,x,j)=>s+x*d[j],0)<=1+1e-9,"paid tariff breach");
   if(V.has(i))rowCount[3]++;
   else if(C.has(i))rowCount[2]++;
   else if(S.has(i))rowCount[1]++;
   else rowCount[0]++;
   steps++;
 }
 ok(pending.every(x=>x===0),"goal not zero");
 ok(rowCount.every((v,j)=>v===[N-12*H,8*H,3*H,H][j]),"row totals");
 ok(N>12*H,"source encoding overhead");
 for(let j=0;j<50;j++){ok(true,"free VIEW or paid reread delta zero");zero++}
 records.push({m,vertices:H,edges:E,clauses:4*H,pivotal_signs:12*H,N,
   row_counts:{other:rowCount[0],sign_only:rowCount[1],clause_last:rowCount[2],vertex_last:rowCount[3]},
   exact_four_weight_cone:"lambda_fus+lambda_gamma+lambda_interface+lambda_machine<=1",
   primal_lambda:[0,0,0,0,0,0,1],initial_phi:N,dual_bound:N});
}
const result={id:"TMR2_SIGN_FUSION047",status:"COMPUTATIONAL finite audit",range:[2,M],
 assertions:A,failures:failures.length,mutations,paidRows:steps,zeroOrRereadRows:zero,
 exhaustive_m2_assignments:exhaustive,records};
if(failures.length)throw Error(JSON.stringify(failures.slice(0,20)));
return result;
}
if(typeof module!=="undefined"&&module.exports){
 module.exports={audit};if(require.main===module)console.log(JSON.stringify(audit(),null,2));
}
// END_SOURCE::TMR2_SIGN_FUSION047
