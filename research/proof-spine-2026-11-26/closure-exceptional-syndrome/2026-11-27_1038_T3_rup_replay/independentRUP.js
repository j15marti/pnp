function verifyRUP(fs,gauge,base,proof){
 let stats={localWords:0,clausesChecked:0,propScans:0,derived:0,checkPartial:0};
 // Verify every base clause has a specific local factor that entails it, or is the justified gauge.
 for(const c of base){if(c.length===1&&c[0]===-gauge)continue;
  let f=fs.find(f=>c.every(l=>f.vs.includes(Math.abs(l)))&&f.ok.every(w=>{stats.localWords++;return c.some(l=>((w>>f.vs.indexOf(Math.abs(l)))&1)===Number(l>0))}));
  if(!f)throw Error("base clause not implied");stats.clausesChecked++}
 // Negative proof only requires sound implications, not CNF equivalence; independently test all local partial assignment implications for support propagation.
 const keys=new Set(base.map(c=>c.join(",")));
 for(const f of fs){let w=f.vs.length;for(let i=0;i<3**w;i++){let n=i,p=new Map();for(let k=0;k<w;k++){let t=n%3;n=Math.floor(n/3);if(t)p.set(f.vs[k],t-1)}stats.checkPartial++;let support=f.ok.some(a=>[...p].every(([v,b])=>((a>>f.vs.indexOf(v))&1)===b));if(support)continue;let covered=false;for(const c of base){if(c.every(l=>p.has(Math.abs(l))&&p.get(Math.abs(l))!==Number(l>0))){covered=true;break}}if(!covered)throw Error("missing forbidden partial")}}
 function conflict(C,assumptions){let a=new Set(assumptions);if([...a].some(l=>a.has(-l)))return true;
 for(;;){let newLit=0;for(const c of C){stats.propScans++;if(c.some(l=>a.has(l)))continue;const u=c.filter(l=>!a.has(-l));if(!u.length)return true;if(u.length===1){newLit=u[0];break}}
 if(!newLit)return false;a.add(newLit)}}
 const db=base.slice();
 for(const c of proof){if(!conflict(db,c.map(l=>-l)))throw Error("RUP");db.push(c);stats.derived++}
 if(proof.at(-1).length)throw Error("empty clause missing");
 return{...stats,corruptRejected:!conflict(base,[])};
}
