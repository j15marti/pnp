// LSPV-1/484 restricted syntactic Res(XOR) finite parity-guard audit.
function run(){
 const ck=(b,m)=>{if(!b)throw Error(m||"failure")};
 const e=(m,b)=>m+":"+b, v=t=>t.split(":").map(Number);
 const flip=t=>{let [m,b]=v(t);return e(m,b^1)};
 const add=(x,y)=>{let a=v(x),b=v(y);return e(a[0]^b[0],a[1]^b[1])};
 const canon=a=>[...new Set(a)].sort(),same=(a,b)=>JSON.stringify(canon(a))===JSON.stringify(canon(b));
 let nodes=[],checks=0;
 function put(r,c,meta={}){nodes.push({r,c:canon(c),...meta});return nodes.length-1}
 const bl=i=>put("BOOL",[e(1<<i,0),e(1<<i,1)],{i});
 const wk=(i,x)=>put("WEAK",[...nodes[i].c,...x],{i});
 function lin(i,j,a,b){ck(nodes[i].c.includes(a)&&nodes[j].c.includes(b));return put("LIN",[...nodes[i].c.filter(t=>t!==a),...nodes[j].c.filter(t=>t!==b),add(a,b)],{i,j,a,b})}
 const dr=i=>{ck(nodes[i].c.includes("0:1"));return put("DROP",nodes[i].c.filter(t=>t!=="0:1"),{i})};
 function prove(p,q,a,b){let c=[add(a,b),flip(add(a,b))],leaves=[];
  for(let u=0;u<2;u++)for(let w=0;w<2;w++){let x=u?flip(a):a,y=w?flip(b):b;
   let k=lin(wk(p,[flip(y)]),wk(q,[flip(x)]),x,y);
   leaves.push(wk(k,c.filter(z=>z!==add(x,y))));
  }
  let d0=dr(lin(leaves[0],leaves[1],flip(b),b));
  let d1=dr(lin(leaves[2],leaves[3],flip(b),b));
  let out=dr(lin(d0,d1,flip(a),a));ck(same(nodes[out].c,c));return out;
 }
 let base=Array.from({length:5},(_,i)=>bl(i));
 let cache=new Map(base.map((id,i)=>[1<<i,id]));
 for(let mask=1;mask<32;mask++){
  let ids=[0,1,2,3,4].filter(i=>mask&(1<<i)),a=1<<ids[0];
  for(let i of ids.slice(1)){let z=a^(1<<i);if(!cache.has(z))cache.set(z,prove(cache.get(a),base[i],e(a,0),e(1<<i,0)));a=z}
  ck(same(nodes[cache.get(mask)].c,[e(mask,0),e(mask,1)]));
 }
 function check(all){for(let k=0;k<all.length;k++){let t=all[k],c=t.c;
  if(t.r==="BOOL")ck(same(c,[e(1<<t.i,0),e(1<<t.i,1)]));
  else if(t.r==="WEAK")ck(t.i<k&&all[t.i].c.every(x=>c.includes(x)));
  else if(t.r==="LIN")ck(t.i<k&&t.j<k&&all[t.i].c.includes(t.a)&&all[t.j].c.includes(t.b)&&same(c,[...all[t.i].c.filter(x=>x!==t.a),...all[t.j].c.filter(x=>x!==t.b),add(t.a,t.b)]));
  else if(t.r==="DROP")ck(t.i<k&&all[t.i].c.includes("0:1")&&same(c,all[t.i].c.filter(x=>x!=="0:1")));
  else throw Error("unknown");checks++;
 } }
 check(nodes);let corrupt=JSON.parse(JSON.stringify(nodes));corrupt[corrupt.length-1].c=["0:1"];let rejected=false;try{check(corrupt)}catch{rejected=true}ck(rejected);
 return {status:"PASS",proof_records:nodes.length,verified_records:checks,affine_masks:31,corruptions_rejected:1,scope:"syntactic Res(XOR) parity-Booleanity, not historic mixed parser"};
}
if(typeof module!=='undefined')module.exports={run};
