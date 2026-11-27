function phaseHorn(C,root,H,P,Q){let a=new Map(H.assignment),ids=H.fields.map((r,i)=>r[0]<=1?i:-1).filter(i=>i>=0),D=ids.map(i=>C[i]),vars=[...new Set(C.flat().map(Math.abs))].sort((a,b)=>a-b),free=vars.filter(v=>!root.some(p=>p[0]===v)),work={n:0},proof=[],full=C.slice(),rp=new Map(root);
 if(D.some(c=>c.filter(l=>a.get(Math.abs(l))===Number(l>0)).length>1))throw Error("not phase dual Horn");
 if(!P.up(D,new Map(root),work)){return{status:"UNSAT_PHASE",ids,work:work.n,proof};}
 for(let v of free)for(let b of [0,1]){if(rp.has(v))break;let q=new Map([...root,[v,b]]);if(P.up(D,q,work))continue;let cl=[b?-v:v],z=Q.rup(full,cl,P);if(!z.ok)throw Error("unsupported phase force");proof.push({cl,verify:z.work});full.push(cl);if(!P.up(full,rp,work))return{status:"UNSAT_RECL",ids,work:work.n,proof,pins:[...rp]};}
 return{status:"UNKNOWN",ids,work:work.n,proof,pins:[...rp],complementSatisfies:D.every(c=>c.some(l=>1-a.get(Math.abs(l))===Number(l>0)))};
}
module.exports={phaseHorn};
