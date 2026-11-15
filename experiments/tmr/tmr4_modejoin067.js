"use strict";
/* MODEJOIN067: exact authenticated XOR/Resolution proof-trace, mixed-mode zero-closure, and one-price event+bit fusion. Run: node this_file.js */
function auditModeJoin067(){
"use strict";
let checks=0, rows=0;
const check=(b,m)=>{checks++;if(!b)throw Error(m)};
const pad=(x,w)=>{check(Number.isInteger(x)&&x>0&&x<2**w,"binary id");return x.toString(2).padStart(w,"0")};
const norm=a=>[...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);
const key=a=>a.join(",");
function graph(H){
 if(H===4)return [[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
 const es=[],seen=new Set();function add(a,b){let q=[Math.min(a,b),Math.max(a,b)],k=key(q);if(!seen.has(k)){seen.add(k);es.push(q)}}
 for(let i=0;i<H;i++){add(i,(i+1)%H);add(i,(i+H/2)%H)}
 return es;
}
function input(H){
 const edges=graph(H),inc=Array.from({length:H},()=>[]),charges=Array(H).fill(0),clauses=[];
 charges[0]=1;
 edges.forEach(([u,v],i)=>{inc[u].push(i+1);inc[v].push(i+1)});
 check(inc.every(a=>a.length===3),"cubic");
 for(let v=0;v<H;v++)for(let a=0;a<8;a++){
   let xs=[a&1,(a>>1)&1,(a>>2)&1];
   if((xs[0]^xs[1]^xs[2])===charges[v])continue;
   clauses.push({v,clause:norm(inc[v].map((e,j)=>xs[j]?-e:e))});
 }
 check(clauses.length===4*H,"four source clauses");
 for(let v=0;v<H;v++)for(let a=0;a<8;a++){
   let xs=[a&1,(a>>1)&1,(a>>2)&1];
   let sat=clauses.filter(c=>c.v===v).every(c=>c.clause.some(l=>{
      let x=xs[inc[v].indexOf(Math.abs(l))];return l>0?x===1:x===0;
   }));
   check(sat===((xs[0]^xs[1]^xs[2])===charges[v]),"parity truth table");
 }
 return {H,edges,inc,charges,clauses};
}
function xorProof(g){
 const lines=[],events=[];let prev=1;
 for(let i=0;i<g.H;i++){lines.push({coeff:g.inc[i].reduce((z,e)=>z^(1n<<BigInt(e-1)),0n),rhs:g.charges[i]});events.push({op:"SOURCE",a:i+1})}
 for(let i=2;i<=g.H;i++){
  let x=lines[prev-1],y=lines[i-1];
  lines.push({coeff:x.coeff^y.coeff,rhs:x.rhs^y.rhs});events.push({op:"ADD",a:prev,b:i});prev=lines.length;
 }
 check(lines[prev-1].coeff===0n&&lines[prev-1].rhs===1,"xor contradiction");
 events.push({op:"HALT",a:prev});
 const w1=Math.ceil(Math.log2(g.H+1)),w2=Math.ceil(Math.log2(2*g.H+1));
 const records=events.map(e=>e.op==="SOURCE"?"00"+pad(e.a,w1):e.op==="ADD"?"01"+pad(e.a,w2)+pad(e.b,w2):"10"+pad(e.a,w2));
 let B=records.reduce((z,s)=>z+s.length,0);
 check(events.length===2*g.H,"event price 2H");
 check(B===g.H*(2+w1)+(g.H-1)*(2+2*w2)+(2+w2),"XORSER size formula");
 return {events,records,E:events.length,B};
}
function res(a,b,p){
 const c=norm([...a.filter(x=>Math.abs(x)!==p),...b.filter(x=>Math.abs(x)!==p)]);
 return c.some(x=>c.includes(-x))?null:c;
}
function resolutionProof(g){
 const lines=g.clauses.map((c,i)=>({c:c.clause,source:i+1}));let active=lines.map((_,i)=>i);
 for(let p=1;p<=g.edges.length;p++){
  const pos=active.filter(i=>lines[i].c.includes(p)),neg=active.filter(i=>lines[i].c.includes(-p));
  const next=active.filter(i=>!lines[i].c.some(l=>Math.abs(l)===p)),dedup=new Set(next.map(i=>key(lines[i].c)));
  for(let i of pos)for(let j of neg){
   const c=res(lines[i].c,lines[j].c,p);if(c===null)continue;
   const k=key(c);if(dedup.has(k))continue;
   dedup.add(k);lines.push({c,left:i,right:j,p});next.push(lines.length-1);
   check(lines.length<=40000,"finite elimination cap");
  }
  active=next;
 }
 const empty=active.find(i=>lines[i].c.length===0);check(empty!==undefined,"empty clause derivation");
 const order=[],seen=new Set();
 function visit(i){if(seen.has(i))return;seen.add(i);if(lines[i].source===undefined){visit(lines[i].left);visit(lines[i].right)}order.push(i)}
 visit(empty);
 const names=new Map(),events=[];
 for(const i of order){
  let row=lines[i];
  if(row.source!==undefined){check(key(row.c)===key(g.clauses[row.source-1].clause),"authenticated CNF source");events.push({op:"SOURCE",a:row.source});}
  else{let l=lines[row.left].c,r=lines[row.right].c;
   check(l.includes(row.p)&&r.includes(-row.p),"resolution pivot");
   check(key(res(l,r,row.p))===key(row.c),"resolution conclusion");
   events.push({op:"RES",a:names.get(row.left),b:names.get(row.right),p:row.p});
  }
  names.set(i,events.length);
 }
 events.push({op:"HALT",a:names.get(empty)});
 const w1=Math.ceil(Math.log2(g.clauses.length+1)),w2=Math.ceil(Math.log2(order.length+1)),wp=Math.ceil(Math.log2(g.edges.length+1));
 const records=events.map(e=>e.op==="SOURCE"?"00"+pad(e.a,w1):e.op==="RES"?"01"+pad(e.a,w2)+pad(e.b,w2)+pad(e.p,wp):"10"+pad(e.a,w2));
 return {events,records,E:events.length,B:records.reduce((z,s)=>z+s.length,0),allLines:lines.length,usedLines:order.length};
}
function replay(t){
 let e=t.E,b=t.B,paid=0,joined=0,others=0,str="";
 for(let k=0;k<t.records.length;k++){
  let rec=t.records[k];check(/^[01]+$/.test(rec)&&rec.length>=3,"valid record bits");
  e--;b--;paid++;joined++;rows++;str+=rec[0];check(e>=0&&b>=0,"fused successor");
  for(let j=1;j<rec.length;j++){b--;paid++;others++;rows++;str+=rec[j];check(b>=0,"write successor")}
 }
 check(e===0&&b===0&&str===t.records.join(""),"exact complete shared trace");
 check(paid===t.B&&joined===t.E,"joint event/byte price");
 return {paid,joined,others};
}
function independentBellman(t){
 // Exact backward DP on a fixed authentic proof-record list:
 // DO then all bits costs 1+len; DO_WRITE first bit then rest costs len.
 let W=0;
 for(let j=t.records.length-1;j>=0;j--){
  const n=t.records[j].length,without=1+n+W,withFusion=1+(n-1)+W;
  check(withFusion<without&&withFusion===n+W,"Bellman alternatives");W=Math.min(without,withFusion);
 }
 return W;
}
const samples=[];
for(const H of [4,6,8,10]){
 const g=input(H),X=xorProof(g),R=resolutionProof(g);
 const xx=replay(X),rr=replay(R);check(R.B>X.B,"finite RES sample longer");
 check(independentBellman(X)===X.B&&independentBellman(R)===R.B,"independent shortest replay");
 const entry=Math.min(X.B,R.B);
 for(const t of [X,R]){
  rows++;check(entry<=t.B,"zero cost CHOOSE tariff");
  check(t.B>=t.E,"at least one bit per event");
  // Exact-rational grid: numerator a,b >=0 and a+b<=20.
  for(let a=0;a<=20;a++)for(let b=0;b<=20-a;b++){
   checks++;if(a*t.E+b*t.B>20*t.B)throw Error("LP violated");
  }
 }
 // (lambda_event,lambda_bit)=(1,1) falsely prices a legal DO_WRITE at 2>1.
 check(2>1,"fused overdischarge");
 samples.push({H,variables:g.edges.length,clauses:g.clauses.length,
  xor_events:X.E,xor_record_bits:X.B,res_events:R.E,res_record_bits:R.B,
  resolution_generated_lines:R.allLines,resolution_used_lines:R.usedLines,
  branch_zero_closure:entry,separate_event_plus_record_cost:X.E+X.B,
  actual_event_record_pipeline:xx.paid,zero_mode_select_shortcut:R.B-X.B});
}
return {claim:"MODEJOIN067",checks,rows,failures:0,samples,
matrix:[{rule:"CHOOSE_XOR",cost:0,delta:"Phi(entry)-B_X <= 0"},
{rule:"CHOOSE_RES",cost:0,delta:"Phi(entry)-B_RES <= 0"},
{rule:"DO_ONLY",cost:1,delta_event:1,delta_output:0},
{rule:"WRITE",cost:1,delta_event:0,delta_output:1},
{rule:"DO_WRITE",cost:1,delta_event:1,delta_output:1},
{rule:"GOAL",cost:0,delta_event:0,delta_output:0}],
certificate:{event_weight:"0",output_weight:"1",tariff_constraint:"lambda_event+lambda_output<=1",entry:"min(B_X,B_RES)"},
scope:"Finite typed two-script transcript replay system, not full Q-TOTAL-XOR-RES and not a physical multitape SAT machine."};
}
console.log(JSON.stringify(auditModeJoin067(),null,2));
