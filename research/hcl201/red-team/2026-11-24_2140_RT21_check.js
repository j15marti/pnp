"use strict";
function check(){
  const D=[1,2,4,7], points=[0,4,3,2], lines=D.map((d,i)=>[points[i],points[i]^d]);
  const ctr={assertions:0,localWords:0,referenceWords:0,hallSubsets:0,closureScans:0,forcedRows:0,deletedPackets:0,basisLifts:0,visibilityDirections:0,polarChecks:0,peerChecks:0};
  const ok=(x,msg)=>{ctr.assertions++;if(!x)throw Error(msg)};
  const bit=i=>1n<<BigInt(i);
  function parity(x){let p=0;while(x){x&=x-1n;p^=1}return p;}
  function basis(rows){let B=[];for(let x of rows){for(let y of B)if((x^y)<x)x^=y;if(x){B.push(x);B.sort((a,b)=>a>b?-1:a<b?1:0)}}return B;}
  const rank=rows=>basis(rows).length;
  const dot=(a,x)=>parity(a&x);
  const obs=(P,x)=>dot(P.a,x)+2*dot(P.b,x);
  const bad=(P,x)=>obs(P,x)===P.s;
  const normals=D.map(d=>[1,2,3,4,5,6,7].filter(u=>parity(BigInt(u&d))===0).slice(0,2));
  function gadget(P,n){return D.map((d,j)=>{let [a,b]=normals[j].map(v=>BigInt(v)<<BigInt(n));let s=parity(BigInt(normals[j][0]&points[j]))+2*parity(BigInt(normals[j][1]&points[j]));return {a:j===0?a^P.a:a,b:j===0?b^P.b:b,s:j===0?s^P.s:s};});}
  function expand(F,n,indices){let out=[],start=n;let groups=[];for(let i=0;i<F.length;i++){if(indices.has(i)){groups.push({pos:out.length,off:n,source:i});out.push(...gadget(F[i],n));n+=3;}else out.push(F[i]);}return {F:out,n,groups,start};}
  const baseLines=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
  const e=i=>i===0?0n:bit(i-1);
  const root=baseLines.map(([a,b,c])=>({a:e(a)^e(b),b:e(a)^e(c),s:0}));
  const satRoot=root.map((p,i)=>({...p,s:i===0?1:0}));
  function words(F,n){let out=[],near=[];for(let x=0n;x<bit(n);x++){ctr.referenceWords++;let violations=F.map((p,i)=>bad(p,x)?i:-1).filter(i=>i>=0);if(!violations.length)out.push(x);if(violations.length===1)near.push([x,violations[0]]);}return {out,near};}
  function hall(F,n){for(let m=1;m<(1<<F.length);m++){ctr.hallSubsets++;let P=F.filter((p,i)=>m>>i&1),r=rank(P.flatMap(p=>[p.a,p.b]));ok(r>=P.length-(P.length===F.length?1:0),"Hall");if(P.length===F.length)ok(r===n&&r===P.length-1,"full deficiency");}}
  function visibility(F,n){for(let x=1n;x<bit(n);x++){ctr.visibilityDirections++;ok(F.filter(p=>obs(p,x)!==0).length>=3,"visibility");}}
  function polar(P,n){let q=0n,k=0;for(let i=0;i<n;i++)for(let j=i+1;j<n;j++,k++)if((dot(P.a,bit(i))*dot(P.b,bit(j)))^(dot(P.a,bit(j))*dot(P.b,bit(i))))q|=bit(k);return q;}
  function basisCandidate(F,n,x,skip){const rows=F.filter((p,i)=>i!==skip).map(p=>[p.a,p.b,p.a^p.b].filter((a,j)=>dot(a,x)!==([p.s&1,p.s>>1,(p.s&1)^(p.s>>1)][j])));function dfs(i,B){if(i===rows.length)return B.length===n;for(let a of rows[i]){let b=basis([...B,a]);if(b.length>B.length&&dfs(i+1,b))return true;}return false;}ctr.basisLifts++;return dfs(0,[]);}
  // Coordinate-free local feasible support using actual independent observations.
  function local(P){ctr.closureScans++;const B=basis(P.flatMap(p=>p.rows.map(r=>r.a)));let dict=new Map();for(let x=0;x<(1<<B.length);x++){let a=0n;for(let i=0;i<B.length;i++)if(x>>i&1)a^=B[i];dict.set(a,x);}
    const forms=P.map(p=>p.rows.map(r=>[dict.get(r.a),r.b]));let legal=[];for(let x=0;x<(1<<B.length);x++){ctr.localWords++;if(forms.every(f=>!f.every(([a,b])=>parity(BigInt(a&x))===b)))legal.push(x);}
    if(!legal.length)return {contradiction:true,rank:B.length};
    const anchor=legal[0],H=basis(legal.map(x=>BigInt(x^anchor)));
    if(H.length===B.length)return {rank:B.length,dim:H.length,legal:legal.length};
    for(let q=1;q<(1<<B.length);q++)if(H.every(h=>dot(h,BigInt(q))===0)){let a=0n;for(let i=0;i<B.length;i++)if(q>>i&1)a^=B[i];return {rank:B.length,dim:H.length,legal:legal.length,force:{a,b:parity(BigInt(q&anchor))}};}
    throw Error("hull");
  }
  function packet(P){return {rows:[{a:P.a,b:P.s&1},{a:P.b,b:P.s>>1}]};}
  function normalize(P){let M=new Map();for(let r of P.rows){let {a,b}=r;while(a){let j=a.toString(2).length-1;if(!M.has(j)){M.set(j,{a,b});break;}let z=M.get(j);a^=z.a;b^=z.b;}if(a===0n&&b)return null;}return {rows:[...M.values()]};}
  function closure(F,n,cap){let live=F.map(packet),guards=[];const apply=r=>{ctr.forcedRows++;guards.push(r);let pivot=bit(r.a.toString(2).length-1);live=live.map(P=>normalize({rows:P.rows.map(z=>z.a&pivot?{a:z.a^r.a,b:z.b^r.b}:z)})).filter(P=>{if(!P)ctr.deletedPackets++;return P;});};
    while(true){let r=null;for(let P of live){if(P.rows.length===0)return {unsat:true,guards,live};if(P.rows.length===1){r={a:P.rows[0].a,b:P.rows[0].b^1};break;}}
      if(!r&&cap>=2){outer:for(let i=0;i<live.length;i++)for(let j=i+1;j<live.length;j++){let z=local([live[i],live[j]]);if(z.contradiction)return {unsat:true,guards,live};if(z.force){r=z.force;break outer;}}}
      if(!r&&cap>=3){outer:for(let i=0;i<live.length;i++)for(let j=i+1;j<live.length;j++)for(let k=j+1;k<live.length;k++){let z=local([live[i],live[j],live[k]]);if(z.contradiction)return {unsat:true,guards,live};if(z.force){r=z.force;break outer;}}}
      if(!r)return {unsat:false,guards,live};apply(r);
    }
  }
  function finish(C,n){if(C.unsat)return {sat:false,rank:0};let B=basis(C.live.flatMap(p=>p.rows.map(r=>r.a)));ok(B.length<=6,"contracted rank");let z=local(C.live);if(z.contradiction)return {sat:false,rank:B.length};
    // independent row observation enumeration plus exact back-substitution, no full private enumeration.
    let coeff=new Map();for(let x=0;x<(1<<B.length);x++){let a=0n;for(let i=0;i<B.length;i++)if(x>>i&1)a^=B[i];coeff.set(a,x);}
    for(let x=0;x<(1<<B.length);x++){if(C.live.some(P=>P.rows.every(r=>parity(BigInt(coeff.get(r.a)&x))===r.b)))continue;let rows=[...C.guards,...B.map((a,i)=>({a,b:x>>i&1}))];let M=new Map();for(let {a,b} of rows){while(a){let j=a.toString(2).length-1;if(!M.has(j)){M.set(j,{a,b});break;}let z=M.get(j);a^=z.a;b^=z.b;}ok(a!==0n||b===0,"lift consistency");}let w=0n;for(let j of [...M.keys()].sort((a,b)=>a-b)){let {a,b}=M.get(j);if(dot(a,w)!==b)w^=bit(j);}ok(rows.every(r=>dot(r.a,w)===r.b),"lift");return {sat:true,rank:B.length,w};}return {sat:false,rank:B.length};}
  // Local gadget and exact private lift checks.
  ok(new Set(lines.flat()).size===8,"partition");
  for(let s=0;s<4;s++){let P={a:1n,b:2n,s},G=gadget(P,2);for(let x=0n;x<4n;x++){let S=[];for(let p=0;p<8;p++){let w=x|(BigInt(p)<<2n);ctr.localWords++;if(G.every(Q=>!bad(Q,w)))S.push(p);}ok(JSON.stringify(S)===JSON.stringify(bad(P,x)?[]:lines[0]),"gadget fiber");}}
  // I21 peer: B4 integer balance + even parity exactly NAE with unique private bit.
  for(let x=0;x<8;x++){let a=x&1,b=x>>1&1,c=x>>2&1;let d=a^b^c;ctr.peerChecks++;ok((a+b+c+d===2)===(x!==0&&x!==7),"I21 B4");ok([0,1].filter(z=>a+b+c+z===2).length===(x!==0&&x!==7?1:0),"I21 unique lift");}
  // I21 clause split against original four-argument NAE, all 16 boundary words.
  for(let x=0;x<16;x++){let a=x&1,b=x>>1&1,c=x>>2&1,r=x>>3&1,nae=(a,b,c)=>!(a===b&&b===c);ctr.peerChecks++;ok([0,1].some(y=>nae(a,b,y)&&nae(y^1,c,r))===(x!==0&&x!==15),"I21 split");}
  const R=words(root,6),S=words(satRoot,6);ok(R.out.length===0&&S.out.length>0,"Fano labels");hall(root,6);visibility(root,6);
  const small=[];
  for(let i=0;i<7;i++)for(let [label,F] of [["UNSAT",root],["SAT",satRoot]]){let E=expand(F,6,new Set([i])),W=words(E.F,E.n),ref=label==="SAT"?S:R;ok(W.out.length===2*ref.out.length,"count");hall(E.F,E.n);visibility(E.F,E.n);let rootC=closure(E.F,E.n,2);ok(!rootC.unsat&&!rootC.guards.length,"pair closure");ctr.polarChecks++;ok(rank(E.F.map(p=>polar(p,E.n)))===E.F.length,"polar independent");let C=closure(E.F,E.n,3),Z=finish(C,E.n);ok(Z.sat===(label==="SAT"),"triple decision");if(Z.sat)ok(E.F.every(p=>!bad(p,Z.w)),"source witness");if(label==="UNSAT"){for(let [x,skip] of W.near.slice(0,12))ok(basisCandidate(E.F,E.n,x,skip),"maximum signed basis candidate");}small.push({owner:i,label,models:W.out.length,near:W.near.length,forced:C.guards.length,remainingRank:Z.rank});}
  let scaling=[];
  for(let [label,F0] of [["UNSAT",root],["SAT",satRoot]]){let F=F0,n=6,G=0;let anchor=label==="SAT"?S.out[0]:R.near[0][0],badidx=label==="SAT"?-1:R.near[0][1];for(let depth=1;depth<=3;depth++){let E=expand(F,n,new Set(F.map((p,i)=>i)));G+=F.length;n=E.n;F=E.F;badidx=badidx<0?-1:badidx*4;for(let seed=0;seed<8;seed++){let w=anchor;for(let [j,g] of E.groups.entries())if((j+seed)%2)w|=bit(g.off);let bads=F.map((p,i)=>bad(p,w)?i:-1).filter(i=>i>=0);ok(bads.length===(badidx<0?0:1)&&(badidx<0||bads[0]===badidx),"neighbor lift");}anchor|=0n;let row={label,depth,owners:F.length,rank:rank(F.flatMap(p=>[p.a,p.b])),candidateLiftExponent:G};ok(row.rank===F.length-1,"scaling rank");if(depth===1){let C0=closure(F,n,2);ok(!C0.unsat&&!C0.guards.length,"scaled pair closure");let C=closure(F,n,3),Z=finish(C,n);ok(Z.sat===(label==="SAT"),"scaled contraction");if(Z.sat)ok(F.every(p=>!bad(p,Z.w)),"scaled witness");row.tripleRows=C.guards.length;row.remainingRank=Z.rank;}scaling.push(row);}}
  return {partition:lines,normals,rootModels:R.out.length,signedNeighborModels:S.out.length,counts:ctr,small,scaling,limitations:"Small cases exhaustive, depth 1 generic triple closure; depths 2-3 rank and eight deterministic lifts per level, not full closure/Hall enumeration. No native compiler, full matching/portfolio, kernel or measured CM."};
}
console.log(JSON.stringify(check(), null, 2));
