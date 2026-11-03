// LSPV-2 354 compact reproducible gate/slot restriction check; no dependencies.
'use strict';
const assert = require('node:assert/strict');
const norm = a => [...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||y-x);
let tested=0,slots=0,paid=0;
for(const x of [null,0,1])for(const y of [null,0,1])for(const sx of [-1,1])for(const sy of [-1,1]){
 const rho={};if(x!==null)rho[1]=x;if(y!==null)rho[2]=y;
 const old=[{q:5,a:sx,b:2*sy},{q:6,a:5,b:-2},{q:7,a:-6,b:1}],map={},gates=[],res=[];
 let next=4;
 const gate=(a,b)=>{assert.notEqual(Math.abs(a),Math.abs(b));assert(Math.max(Math.abs(a),Math.abs(b))<=next);let q=++next;gates.push({q,a,b});return q};
 const lit=(p)=>Object.hasOwn(rho,Math.abs(p))?Boolean(rho[Math.abs(p)])===(p>0):Math.sign(p)*(map[Math.abs(p)]||Math.abs(p));
 const spec=(a)=>{let v=a.map(lit);return v.some(t=>t===true)?null:norm(v.filter(t=>t!==false))};
 const d=gate(3,4),f=gate(d,-3),e=gate(f,4),T=gate(-f,-e);
 const slotsFor=g=>[norm([-g.q,g.a]),norm([-g.q,g.b]),norm([g.q,-g.a,-g.b])];
 const derive=(a,b,p)=>{assert(a.includes(p)&&b.includes(-p));let c=norm(a.filter(x=>x!==p).concat(b.filter(y=>y!==-p)));assert(!c.some(v=>c.includes(-v)));res.push(c);return c};
 const [ds,fs,es,Ts]=gates.map(slotsFor);
 const rf=derive(derive(fs[0],ds[0],d),fs[1],3);
 const re=derive(es[0],rf,f);
 const rt=derive(derive(Ts[2],rf,f),re,e);
 assert.deepEqual(rf,[-f]);assert.deepEqual(re,[-e]);assert.deepEqual(rt,[T]);
 for(const oldGate of old){let a=lit(oldGate.a),b=lit(oldGate.b),q;
  let extra=[];
  if(a===false||b===false){let other=a===false?b:a;q=gate(f,typeof other==='number'?other:3);extra=[derive(slotsFor(gates.at(-1))[0],rf,f)];}
  else if(a===true&&b===true){q=gate(T,-f);const h=slotsFor(gates.at(-1));extra=[derive(derive(h[2],rt,-T),rf,f)];}
  else if(a===true||b===true){q=gate(T,a===true?b:a);extra=[derive(slotsFor(gates.at(-1))[2],rt,-T)];}
  else q=gate(a,b);
  map[oldGate.q]=q;
  const candidates=slotsFor(gates.at(-1)).concat(extra);
  const originals=[[-oldGate.q,oldGate.a],[-oldGate.q,oldGate.b],[oldGate.q,-oldGate.a,-oldGate.b]];
  for(const src of originals){const wanted=spec(src);if(wanted===null)continue;assert(candidates.some(c=>JSON.stringify(c)===JSON.stringify(wanted)));slots++;}
 }
 assert(gates.length===7);assert(res.length<=11);paid+=gates.length+res.length;tested++;
}
console.log(JSON.stringify({status:'PASS',cases:tested,exact_nontautological_slots:slots,paid_nodes_all_tests:paid,model:'source-independent two-input signed-AND VARDEF+strict RES; four shared rail gates'}));
