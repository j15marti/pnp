/* LSPV-2/420 independent exhaustive semantic verifier. Node.js standard library only. */
function verify(candidate){
 function model(C,env){
  let v=new Map(env);
  for(let j=0;j<C.gates.length;j++){
   let g=C.gates[j],a=v.has(g.a)?v.get(g.a):(g.a<C.n?0:undefined),
       b=v.has(g.b)?v.get(g.b):(g.b<C.n?0:undefined);
   if(a===undefined||b===undefined)throw Error('bad input');
   v.set(C.n+j,(g.f>>((b<<1)|a))&1);
  }
  return C.output<C.n?(v.get(C.output)??0):v.get(C.output)
 }
 function independent(C){
  let active=new Set(),seen=new Set(),stack=[C.output];
  while(stack.length){let x=stack.pop();if(seen.has(x))continue;seen.add(x);if(x<C.n)active.add(x);else{let g=C.gates[x-C.n];stack.push(g.a,g.b)}}
  const ids=[...active].sort((a,b)=>a-b),found=new Set();
  if(ids.length>12)throw Error('oracle cap');
  for(let a=0;a<2**ids.length;a++){
   let env=new Map(ids.map((x,i)=>[x,(a>>i)&1])),v=model(C,env);
   for(let x of ids){env.set(x,1-env.get(x));if(model(C,env)!==v)found.add(x);env.set(x,1-env.get(x))}
  }
  return [...found].sort((a,b)=>a-b)
 }
 let seed=2026420,checks=0,stats={one:0,nested:0,sparse:0,bad:0};
 function eq(a,b){checks++;if(JSON.stringify(a)!==JSON.stringify(b))throw Error('mismatch '+JSON.stringify([a,b]))}
 function test(c,k){eq(candidate(c).support,independent(c));stats[k]++}
 function rand(){seed=(Math.imul(seed,1103515245)+12345)>>>0;return seed}
 for(let n=1;n<=5;n++)for(let a=0;a<n;a++)for(let b=0;b<n;b++)for(let f=0;f<16;f++)test({n,gates:[{a,b,f}],output:n},'one');
 for(let n=2;n<=5;n++)for(let i=0;i<350;i++){
  let gates=[],k=0,count=1+rand()%5;
  for(let j=0;j<count;j++){
    let a=rand()%(n+j),b=rand()%(n+j),f=rand()%16;
    if(((f^(f>>1)^(f>>2)^(f>>3))&1)&&k>=2)f^=8;
    if((f^(f>>1)^(f>>2)^(f>>3))&1)k++;
    gates.push({a,b,f});
  }
  test({n,gates,output:n+count-1},'nested')
 }
 for(let f of [1,6,8,9,15])test({n:1000000000,gates:[{a:927341225,b:927341225,f}],output:1000000000},'sparse');
 test({n:2,gates:[{a:0,b:1,f:6},{a:2,b:1,f:6}],output:3},'nested');
 let four={n:4,gates:[{a:0,b:1,f:8},{a:4,b:2,f:8},{a:5,b:3,f:8}],output:6};
 test(four,'nested');eq(candidate(four).support,[0,1,2,3]);
 for(let c of [{n:1,gates:[{a:1,b:0,f:8}],output:1},{n:1,gates:[{a:0,b:0,f:-1}],output:1},{n:1,gates:[],output:1}]){
   let bad=false;try{candidate(c)}catch(e){bad=true}eq(bad,true);stats.bad++;
 }
 return {version:'LSPV2-420-INDEPENDENT',seed:2026420,checks,stats,method:'independent exhaustive Boolean evaluation of output cones',status:'PASS'}
}
if(typeof require!=='undefined'&&typeof module!=='undefined'&&require.main===module){
 console.log(JSON.stringify(verify(require('./lspv2_420_fpt_semantic_support.js').fpt),null,2));
}
if(typeof module!=='undefined')module.exports={verify};
