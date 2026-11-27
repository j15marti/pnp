function extract(db,C,m){let a=new Map(C.map(l=>[Math.abs(l),l<0])),steps=[];for(;;){let changed=false;for(let i=0;i<db.length;i++){m.scans++;let u=0,n=0,hit=false;for(let l of db[i]){m.literals++;let b=a.get(Math.abs(l));if(b===undefined){u=l;n++}else if(b===(l>0)){hit=true;break}}if(hit)continue;if(!n)return{steps,conflict:i};if(n===1){a.set(Math.abs(u),u>0);steps.push([u,i]);changed=true}}if(!changed)throw Error("not RUP")}}

function verifyLocal(db,C,W,m){let positions=new Map();const insert=(l,p)=>{if(positions.has(Math.abs(l)))throw Error("duplicate assignment");positions.set(Math.abs(l),{l,p})};for(const l of C)insert(-l,-1);for(let i=0;i<W.steps.length;i++)insert(W.steps[i][0],i);
function falseBefore(l,i){m.tests++;let t=positions.get(Math.abs(l));return !!t&&t.l===-l&&t.p<i}
for(let i=0;i<W.steps.length;i++){let [l,j]=W.steps[i],c=db[j];if(!c||!c.includes(l)||c.filter(x=>x===l).length!==1||c.some(x=>x!==l&&!falseBefore(x,i)))throw Error("bad unit reason");m.units++}
let end=db[W.conflict];if(!end||end.some(l=>!falseBefore(l,W.steps.length)))throw Error("bad conflict");m.conflicts++;return true}

function build(base,layers){let db=base.slice(),proof=[],m={scans:0,literals:0};for(let L of layers){let start=db.length,entries=L.map(C=>({clause:C,reason:extract(db,C,m)}));proof.push({start,entries});db.push(...L)}return{proof,m}}

function verify(base,proof){let db=base.slice(),m={tests:0,units:0,conflicts:0},empty=false;for(let L of proof){if(L.start!==db.length)throw Error("bad layer index");for(let q of L.entries){verifyLocal(db,q.clause,q.reason,m);if(!q.clause.length)empty=true}db.push(...L.entries.map(x=>x.clause))}if(!empty)throw Error("no root empty");return m}
module.exports={extract,verifyLocal,build,verify};
