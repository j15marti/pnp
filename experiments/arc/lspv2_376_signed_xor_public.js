'use strict';
// LSPV-2/376 compact public verifier, distinct original wires only.
// Full Python producer, independent JavaScript checker and all certificates are in the local archive.
function main() {
  let checks=0;
  function check(ok,msg){checks++;if(!ok)throw Error(msg)}
  function norm(a) {const s=[...new Set(a)];
    check(s.length===a.length,'duplicate literal');check(s.every(x=>Number.isInteger(x)&&x!==0&&!s.includes(-x)),'tautology');
    return s.sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
  }
  function eq(a,b){return JSON.stringify(norm(a))===JSON.stringify(norm(b))}
  function res(a,b,p){let A=new Set(a),B=new Set(b);
    if(!A.has(p)){let z=A;A=B;B=z}
    check(A.has(p)&&B.has(-p),'unsigned pivot');
    return norm([...new Set([...A].filter(x=>x!==p).concat([...B].filter(x=>x!==-p)))]);
  }
  const all=[12,3,10,5,0,15];let count=0;
  for(const a of all)for(const b of all){const u=a&b;
    check(u!==6&&(u^15)!==6,'one-gate XOR');
    for(const c of all.concat([u,u^15]))for(const d of all.concat([u,u^15])){
      const v=c&d;count++;
      check(v!==6&&(v^15)!==6,'two-gate XOR');
    }
  }
  let derived=0;
  for(const s of [1,-1])for(const t of [1,-1]){
    const A=s, B=2*t;
    const def=[
      [[-3,A],[-3,-B],[3,-A,B]],
      [[-4,-A],[-4,B],[4,A,-B]],
      [[-5,-3],[-5,-4],[5,3,4]]
    ].map(a=>a.map(norm));
    const [u,v,w]=def;
    const c1=res(w[2],u[0],3);
    const c2=res(c1,v[1],4);
    const c3=res(w[1],v[2],4);
    const c4=res(w[0],u[2],3);
    const c5=res(w[2],u[1],3);
    const c6=res(c5,v[0],4);
    derived+=6;
    let target=[];
    for(let a=0;a<2;a++)for(let b=0;b<2;b++){
      const aVal=s===1?Boolean(a):!a;
      const bVal=t===1?Boolean(b):!b;
      const wVal=aVal===bVal;
      target.push(norm([a?-1:1,b?-2:2,wVal?5:-5]));
    }
    const actual=[c2,c3,c4,c6];
    check(JSON.stringify(target.map(JSON.stringify).sort())===JSON.stringify(actual.map(JSON.stringify).sort()),'XOR interface mismatch');
  }
  return {status:'PASS',signed_input_combinations:4,paid_gates_per_interface:3,
          native_resolutions_per_interface:6,two_gate_superset_cases:count,
          total_strict_resolution_replays:derived,assertions:checks,
          scope:'source-independent signed AND2 DEF plus strict RES; not full Rmix341'};
}
if(typeof module!=='undefined'&&require.main===module)console.log(JSON.stringify(main(),null,2));
