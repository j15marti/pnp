// Self-contained original-source, exact SAT-subset check. No external dependencies.
const graphs={
 K4:[4,Array.from({length:4},(_,a)=>Array.from({length:4-a-1},(_,b)=>[a,a+b+1])).flat()],
 Cube:[8,Array.from({length:8},(_,u)=>[0,1,2].map(j=>[u,u^(1<<j)]).filter(([a,b])=>a<b)).flat()],
 Petersen:[10,[[0,1],[1,2],[2,3],[3,4],[0,4],[0,5],[1,6],[2,7],[3,8],[4,9],[5,7],[6,8],[7,9],[5,8],[6,9]]],
 Bridge:[10,[[0,2],[0,3],[1,2],[1,3],[2,3],[0,4],[1,4],[5,7],[5,8],[6,7],[6,8],[7,8],[5,9],[6,9],[4,9]]]
};
let tests=0;const ok=(b,m)=>{tests++;if(!b)throw Error(m)};
function analyze(n,edges,chi){
 const inc=Array.from({length:n},()=>[]);edges.forEach(([u,v],i)=>{inc[u].push(i);inc[v].push(i)});
 ok(inc.every(x=>x.length===3),'not cubic');const clauses=[];
 for(let v=0;v<n;v++)for(let i=0;i<8;i++){
   let a=[i&1,(i>>1)&1,(i>>2)&1];if((a[0]^a[1]^a[2])===chi[v])continue;
   clauses.push(inc[v].map((e,j)=>a[j]?-(e+1):e+1));
 }
 const failure=[];const singleton=new Set();let models=0;
 for(let mask=0;mask<(1<<edges.length);mask++){
  let miss=0n;clauses.forEach((C,j)=>{
   const satisfied=C.some(l=>l>0?Boolean(mask&(1<<(l-1))):!(mask&(1<<(-l-1))));
   if(!satisfied)miss|=1n<<BigInt(j);
  });
  failure.push(miss);if(miss===0n)models++;
  if(miss && (miss&(miss-1n))===0n)singleton.add(miss.toString(2).length-1);
 }
 const odd=chi.reduce((x,y)=>x^y,0);ok(Boolean(models)===!odd,'SAT vs parity');
 if(odd){
   const e=[...singleton];const core=e.reduce((m,j)=>m|(1n<<BigInt(j)),0n);
   ok(e.length>=n,'core lower bound');ok(failure.every(m=>(m&core)!==0n),'core UNSAT');
   for(let j=0;j<clauses.length;j++){
    const subset=((1n<<BigInt(clauses.length))-1n)^(1n<<BigInt(j));
    const sat=failure.some(f=>(f&subset)===0n);
    ok(sat===singleton.has(j),'essential deletion');
   }
   if(n===4){for(let q=0;q<65536;q++){
    const sat=failure.some(f=>(f&BigInt(q))===0n);
    ok(sat===((BigInt(q)&core)!==core),'all K4 subsets');
   }}
   return e.length;
 }
 return 0;
}
const output={};for(const [name,[n,es]] of Object.entries(graphs)){
 output[name]=analyze(n,es,[1,...Array(n-1).fill(0)]);
 analyze(n,es,Array(n).fill(0));
}
ok(output.K4===16 && output.Cube===32 && output.Petersen===40 && output.Bridge===36,'core sizes');
console.log(JSON.stringify({status:'PASS',assertions:tests,essential_counts:output,model:'small exact original-edge enumeration; not FLMV'},null,2));
