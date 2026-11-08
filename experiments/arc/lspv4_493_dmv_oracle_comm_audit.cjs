/* LSPV-4/493: independent JS finite controls (not a proof of the Dell asymptotic theorem). */
function run493(){
  let assertions=0;
  function ok(b,label){assertions++;if(!b)throw Error("failed: "+label)}
  function sat(cs,n){for(let bits=0;bits<(1<<n);bits++){let good=cs.every(c=>c.some(l=>(((bits>>(Math.abs(l)-1))&1)===Number(l>0))));if(good)return true}return false}
  function combos(n){let a=[];for(let i=1;i<=n;i++)for(let j=i+1;j<=n;j++)for(let k=j+1;k<=n;k++)a.push([i,j,k]);return a}
  function dense(n){let cs=[];for(const t of combos(n))for(let mask=0;mask<8;mask++)cs.push(t.map((v,i)=>mask&(1<<i)?-v:v));return cs}
  function encode(n,cs){let m=cs.length,b=Math.ceil(Math.log2(128*(n+m+3)));let z="1".repeat(b)+"0"+n.toString(2).padStart(b,"0")+m.toString(2).padStart(b,"0");for(const c of cs){ok(c.length===3&&new Set(c.map(Math.abs)).size===3&&c.every(l=>l!==0&&Math.abs(l)<=n),"strict clause");for(const l of c)z+="1"+(l<0?"1":"0")+Math.abs(l).toString(2).padStart(b,"0")}ok(z.length===3*b+1+3*m*(b+2),"encoder length");return z}
  let matrix=[];
  for(const n of [3,4,5,6,8]){
    let clauses=dense(n),pos=combos(n);
    ok(clauses.length===8*pos.length,"dense count");
    ok(sat(pos,n),"all-positive satisfiable");
    ok(!sat(clauses,n),"all-signed dense unsatisfiable");
    const e=encode(n,clauses);
    matrix.push({variables:n,clauses:clauses.length,encoded_bits:e.length});
  }
  let cs=dense(3),satNum=0,unsatNum=0;
  for(let mask=0;mask<256;mask++){const f=cs.filter((c,i)=>(mask>>i)&1);let ans=sat(f,3);ok(ans===(mask!==255),"three-variable exhaustive");ans?satNum++:unsatNum++}
  ok(satNum===255&&unsatNum===1,"three-variable distribution");
  const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
  function oddK4(pivot){let charges=Array(4).fill(0);if(pivot>=0)charges[pivot]=1;let cls=[];for(let v=0;v<4;v++){let inc=edges.map((e,i)=>e.includes(v)?i+1:0).filter(Boolean);ok(inc.length===3,"K4 degree");for(let mask=0;mask<8;mask++){let parity=((mask&1)?1:0)+((mask&2)?1:0)+((mask&4)?1:0);if((parity%2)!==charges[v])cls.push(inc.map((id,j)=>mask&(1<<j)?-id:id))}}return cls}
  for(const p of [-1,0,1,2,3]){let f=oddK4(p);ok(f.length===16,"four parity clauses per vertex");ok(sat(f,6)===(p<0),"K4 parity");encode(6,f)}
  let fractions=[[1,3],[1,2],[3,4],[9,10],[99,100]].map(([p,q])=>{let aa=p/q,ee=(3-3*aa)/2;ok(aa<1&&ee>0&&3*aa<3-ee,"exponent gap");return {a:`${p}/${q}`,epsilon:ee,outbound_source_power:3*aa}});
  return {scope:"COMPUTATIONAL finite controls; asymptotic theorem from Dell-van Melkebeek (2014)",assertions,dense:matrix,all_three_var:{SAT:satNum,UNSAT:unsatNum},tseitin_K4_charge_sources:5,rational_cases:fractions,failures:0};
}
if (typeof require!=="undefined" && require.main===module) console.log(JSON.stringify(run493(),null,2));
if (typeof module!=="undefined") module.exports={run493};
