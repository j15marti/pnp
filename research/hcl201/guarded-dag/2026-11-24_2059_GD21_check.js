// GD21: supplied block specialization, no dependencies. node this_file.js
function run(){
 const out={assertions:0, cases:0, sat:0, unsat:0, words:0, controls:[], closureScans:0};
 const check=(b)=>{out.assertions++;if(!b)throw Error("assertion "+out.assertions)};
 const product=(a)=>a.reduce((p,b)=>p.flatMap(x=>b.map(y=>[...x,y])),[[]]);
 const key=x=>x.join(",");
 const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]].map(t=>({rows:[(1<<t[0])^(1<<t[1]),(1<<t[0])^(1<<t[2])],rhs:[0,0]}));
 const par=x=>{let p=0;while(x){p^=1;x&=x-1}return p};
 const hit=(p,x)=>p.rows.every((r,i)=>par(r&x)===p.rhs[i]);
 function test(name,blocks,holes,n){
  const ids=blocks.map(b=>b.map((_,i)=>i)), universe=product(ids), H=new Set(holes.map(key)), L=universe.filter(t=>!H.has(key(t)));
  // Rank-two local avoidance has full affine hull; rank>=2 also for every product packet.
  // Certified singleton affine closure scans at root and every emitted child: no strict row.
  const scan=ps=>{out.closureScans++;check(ps.every(p=>p.rows.length===2&&p.rows[0]!==p.rows[1]&&p.rows.every(r=>r!==0)))};
  blocks.forEach(scan);check(L.length===universe.length-H.size);
  for(let j=0;j<blocks.length;j++)check(new Set(L.map(t=>t[j])).size===ids[j].length);
  const boxes=[], seen=new Set;
  for(let bits=1;bits<(1<<holes.length);bits++){
   const sub=holes.filter((_,i)=>bits&(1<<i)), box=ids.map((_,j)=>[...new Set(sub.map(t=>t[j]))].sort((a,b)=>a-b));
   const k=JSON.stringify(box);
   if(!seen.has(k)&&product(box).every(t=>H.has(key(t)))){seen.add(k);boxes.push(box)}
  }
  let credit=0;const children=new Map;
  function child(j,del){const k=j+":"+key(del);if(!children.has(k)){const ps=blocks[j].filter((_,i)=>!del.includes(i));scan(ps);children.set(k,ps);credit+=1+2*ps.length;}return k}
  const base=ids.map((_,j)=>child(j,[])), terms=boxes.map(b=>b.map((d,j)=>child(j,d)));
  const satChild=new Map([...children].map(([k,ps])=>[k,Array.from({length:1<<n},(_,x)=>x).find(x=>ps.every(p=>!hit(p,x)))]));
  const pred=base.some(k=>satChild.get(k)!==undefined)||terms.some(t=>t.every(k=>satChild.get(k)!==undefined));
  let count=0;
  for(const x of product(blocks.map(()=>Array.from({length:1<<n},(_,i)=>i)))){
   const v=blocks.map((b,j)=>b.map((p,i)=>hit(p,x[j])?i:-1).filter(i=>i>=0));
   const actual=!L.some(t=>t.every((i,j)=>v[j].includes(i)));
   const formula=v.some(a=>!a.length)||boxes.some(b=>v.every((a,j)=>a.every(i=>b[j].includes(i))));
   check(actual===formula);out.words++;if(actual)count++;
  }
  check(pred===(count>0));
  if(pred){let x=blocks.map(()=>0);const i=base.findIndex(k=>satChild.get(k)!==undefined);if(i>=0)x[i]=satChild.get(base[i]);else x=terms.find(t=>t.every(k=>satChild.get(k)!==undefined)).map(k=>satChild.get(k));check(!L.some(t=>t.every((i,j)=>hit(blocks[j][i],x[j]))))}
  const mass=2*blocks.length*L.length;
  out.cases++;out[count?"sat":"unsat"]++;
  out.controls.push({name,holes:H.size,models:count,boxes:boxes.length,distinctChildren:children.size,credit,mass,contracts:credit<=mass});
 }
 test("Fano full",[fano,fano],[],7);
 for(let i=0;i<7;i++)for(let j=0;j<7;j++)test("Fano single "+i+","+j,[fano,fano],[[i,j]],7);
 test("Fano two adjacent holes",[fano,fano],[[0,0],[0,1]],7);
 test("Fano two diagonal holes",[fano,fano],[[0,0],[1,1]],7);
 test("Fano all-copy SAT",[fano.slice(1),fano.slice(1)],[],7);
 // 2-bit singleton packets: exact cover and overlapping rank-two planes in 3 bits.
 const p=[0,1,2,3].map(i=>({rows:[1,2],rhs:[i&1,i>>1]}));
 test("three block cover",[p,p,p],[],2);
 test("three block holes",[p,p,p],[[0,0,0],[0,0,1],[1,0,0],[1,0,1]],2);
 // Minimal rank-two cover of F2^2 plus one more family is unnecessary; use two
 // disjoint singleton lists to show an exact rule can fail the credit gate.
 test("small two by two",[p.slice(0,2),p.slice(0,2)],[[0,0]],2);
 return out;
}
const result=run();if(typeof console!=="undefined")console.log(JSON.stringify(result,null,2));