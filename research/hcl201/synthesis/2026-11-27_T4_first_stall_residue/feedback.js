function tableCNF(F){let seen=new Set(),C=[],owners=[];for(const f of F)for(let w=0;w<2**f.vs.length;w++){if(f.ok.includes(w))continue;let c=f.vs.map((v,j)=>w>>j&1?-v:v),key=c.join(",");if(!seen.has(key)){seen.add(key);C.push(c);owners.push(f.id)}}return{C,owners}}

function canon(c){return [...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b)}

function mod(x){return (x%3+3)%3}

function hill(C,pins,residue,seed=0){
 let vars=[...new Set(C.flat().map(Math.abs))].sort((a,b)=>a-b),A=new Map(pins),free=vars.filter(v=>!A.has(v)),rng=seed>>>0,work=0,modOps=0,flips=0,changed=0,moves=[];
 for(let v of free){if(seed){rng^=rng<<13;rng^=rng>>>17;rng^=rng<<5}A.set(v,seed?rng&1:0)}
 let occ=new Map(free.map(v=>[v,[]]));for(let i=0;i<C.length;i++)for(let v of new Set(C[i].map(Math.abs)))if(occ.has(v))occ.get(v).push(i);
 function fields(c,flip=0){let k=0,sum=0;for(let l of c){work++;let s=((A.get(Math.abs(l))^(Math.abs(l)===flip?1:0))===Number(l>0))?Math.sign(l):0;k+=s*s;sum+=s}modOps+=2;return [k,mod(k),mod(sum)]}
 let endpoints=C.map(c=>[0,1].map(b=>{let k=0;for(let l of c){work++;let v=Math.abs(l),p=pins.find(x=>x[0]===v);k+=Number((p?p[1]:b)===Number(l>0))}return k}));
 let rows=C.map(c=>fields(c)),bad=rows.filter(r=>!r[0]).length,initialBad=bad;
 while(bad){let best=0,first=0,id=0,delta=Infinity;for(let v of free){let gain=0,d=0;for(let i of occ.get(v)){let r=fields(C[i],v),old=rows[i];gain+=Number(old[0]===0)-Number(r[0]===0);if(residue){modOps++;d+=Number(r[0]>0&&r[2]===0)-Number(old[0]>0&&old[2]===0)}}if(gain>best){best=gain;id=first=v;delta=d}else if(gain===best&&gain>0&&residue&&d<delta){id=v;delta=d}}
 if(!id)break;if(id!==first)changed++;A.set(id,1-A.get(id));for(let i of occ.get(id))rows[i]=fields(C[i]);let actual=rows.filter(r=>!r[0]).length;if(actual!==bad-best||actual>=bad)throw Error("flip invariant");moves.push({id,first,before:bad,after:actual});bad=actual;flips++}
 return {assignment:[...A],bad,initialBad,flips,changed,moves,work,modOps,fields:rows,endpoints};
}

function derive(C,width,limit=10000,maxLearn=128,order=null){
 let D=C.map(c=>canon(c)),keys=new Set(D.map(c=>c.join(","))),trace=[],pairs=0,litWork=0;
 let ids=order??C.map((_,i)=>i);outer:for(let a=0;a<ids.length;a++)for(let b=a+1;b<ids.length;b++){if(pairs>=limit||trace.length>=maxLearn)break outer;let i=ids[a],j=ids[b];pairs++;for(let p of C[i]){litWork+=C[j].length;if(!C[j].includes(-p))continue;let q=canon([...C[i].filter(x=>x!==p),...C[j].filter(x=>x!==-p)]);litWork+=C[i].length+C[j].length+q.length*q.length;if(q.length>width||q.some(x=>q.includes(-x))||keys.has(q.join(",")))continue;keys.add(q.join(","));D.push(q);trace.push({i,j,p,c:q});if(trace.length>=maxLearn)break outer}}return{D,trace,pairs,litWork}}

function replay(C,trace){let D=C.map(c=>canon(c)),work=0;for(let {i,j,p,c} of trace){if(!D[i]?.includes(p)||!D[j]?.includes(-p))throw Error("parents");let q=canon(D[i].filter(x=>x!==p).concat(D[j].filter(x=>x!==-p)));work+=D[i].length+D[j].length+c.length;if(JSON.stringify(q)!==JSON.stringify(c)||q.some(l=>q.includes(-l)))throw Error("resolution");D.push(q)}return{D,work}}

function arms(C,guard,P,cap=2000000){
 C=C.map(c=>canon(c));let results=[];
 for(let [name,width,kind] of [["baseline",0,0],["flips",0,1],["ded2",2,0],["table2",2,1],["residue2",2,2],["ded4",4,0],["table4",4,1],["residue4",4,2],["guided4",4,2]]){
 let t=Date.now(),initial=null,order=null;if(name==="guided4"){initial=hill(C,guard,true);order=C.map((_,i)=>i).sort((i,j)=>initial.fields[i][0]-initial.fields[j][0]||i-j)}
 let d=width?derive(C,width,10000,128,order):{D:C,trace:[],pairs:0,litWork:0},r=replay(C,d.trace),a=kind?hill(r.D,guard,kind===2):null;
 let overhead=d.pairs+d.litWork+r.work+(a?.work??0)+(a?.modOps??0)+(initial?.work??0)+(initial?.modOps??0);
 let s=overhead>=cap?{status:"UNKNOWN",work:0,nodes:0,tree:["?"]}:P.solve(r.D,guard,a?.assignment??[],cap-overhead),q=s.status==="UNSAT"?P.checkTree(r.D,guard,s.tree):{ok:false,work:0};if(s.status==="UNSAT"&&!q.ok)throw Error("bad tree");
 if(s.status==="SAT"){let z=new Map(s.tree[1]);if(!C.every(c=>c.some(l=>z.get(Math.abs(l))===Number(l>0))))throw Error("bad SAT")}
 let total=overhead+s.work+q.work,status=total>cap?"UNKNOWN_CAP":s.status;
 results.push({name,width,kind,status,verified:status==="UNSAT"&&q.ok||status==="SAT",nodes:s.nodes,search:s.work,check:q.work+r.work,overhead,total,ms:Date.now()-t,rows:r.D.length,literals:r.D.reduce((s,c)=>s+c.length,0),learned:d.trace.length,pairs:d.pairs,deriveWork:d.litWork,flips:a?.flips??0,tieChanges:a?.changed??0,bad:a?.bad??null,scoreWork:(a?.work??0)+(initial?.work??0),modOps:(a?.modOps??0)+(initial?.modOps??0),moves:a?.moves??[],initial:initial?{bad:initial.bad,flips:initial.flips}:null,trace:d.trace,tree:s.tree,table:a?{assignment:a.assignment,fields:a.fields,endpoints:a.endpoints}:null});
 }return results
}

function rup(C,cl,P){let m={n:0},a=new Map(cl.map(l=>[Math.abs(l),Number(l<0)]));return{ok:!P.up(C,a,m),work:m.n}}
module.exports={tableCNF,canon,mod,hill,derive,replay,arms,rup};
