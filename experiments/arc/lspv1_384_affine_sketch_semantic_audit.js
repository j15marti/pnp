// LSPV-1/384 standalone deterministic witness producer. Node >=18; no imports.
const produce = function produce(){
 "use strict";
 let assertions=0, formulas=0, sat=0, unsat=0, witness=0, candidateReject=0, malformed=0, signControls=0, oddEven=[];
 function ok(b,s){assertions++;if(!b)throw Error("FAILED "+s)}
 function validate(n,cnf){if(!Number.isInteger(n)||n<0||n>12||!Array.isArray(cnf))throw Error("header");for(const c of cnf){if(!Array.isArray(c))throw Error("clause");for(const l of c)if(!Number.isInteger(l)||l===0||Math.abs(l)>n)throw Error("literal")}return true}
 function evalD(n,cnf,x){return cnf.every(c=>c.some(l=>{const bit=(x>>(Math.abs(l)-1))&1;return l>0?bit===1:bit===0}))}
 function gates(n,cnf){let g=[{op:"FALSE"},{op:"TRUE"}];const add=(op,a,b)=>{g.push({op,a,b});return g.length-1};const lit=(l)=>l>0?add("INPUT",Math.abs(l)-1):add("NOT",add("INPUT",Math.abs(l)-1));let f=1;for(const c of cnf){let v=0;for(const l of c)v=add("OR",v,lit(l));f=add("AND",f,v)}let out=add("AND",f,add("INPUT",n));return {g,out}}
 function evalG(bundle,x,n){const vals=[];for(let i=0;i<bundle.g.length;i++){let z=bundle.g[i],a=vals[z.a],b=vals[z.b];let value;switch(z.op){case"FALSE":value=0;break;case"TRUE":value=1;break;case"INPUT":value=(x>>z.a)&1;break;case"NOT":value=1-a;break;case"OR":value=a|b;break;case"AND":value=a&b;break;default:throw Error("corrupt gate")}vals.push(value)}return vals[bundle.out]}
 function trial(n,cnf){validate(n,cnf);const C=gates(n,cnf);let models=0,acceptedFactor=true,seen=[null,null],bad=null;for(let x=0;x<(1<<n);x++)if(evalD(n,cnf,x))models++;for(let bits=0;bits<(1<<(n+2));bits++){const x=bits&((1<<n)-1),z=(bits>>n)&1,y=(bits>>(n+1))&1;const expected=z&&evalD(n,cnf,x)?1:0;const value=evalG(C,bits,n);ok(expected===value,"circuit expansion");if(seen[y]===null)seen[y]={bits,value};else if(seen[y].value!==value){acceptedFactor=false;bad=[seen[y].bits,bits]}}
 ok(acceptedFactor===(models===0),"rank-one semantic factor iff UNSAT");ok(bad!==null || models===0,"counter-witness iff SAT");ok(acceptedFactor===(models===0),"zero-table equivalence iff UNSAT");if(bad){ok(((bad[0]>>(n+1))&1)===((bad[1]>>(n+1))&1),"witness same sketch");ok(evalG(C,bad[0],n)!==evalG(C,bad[1],n),"witness different output")}
 formulas++;if(models===0)unsat++;else{sat++;candidateReject++;witness++}
 return {models,bad,gates:C.g.length};
 }
 for(let n=1;n<=3;n++){let clauses=[];for(let a=0;a<(1<<n);a++){let c=[];for(let j=0;j<n;j++)c.push(((a>>j)&1)?-(j+1):j+1);clauses.push(c)}for(let mask=0;mask<(1<<(1<<n));mask++){let F=clauses.filter((c,i)=>mask&(1<<i));trial(n,F)}}
 const crafted=[
 [1,[[1],[-1]]],[2,[[1],[-1],[2]]],[2,[[1,2],[-1],[-2]]],
 [3,[[1],[-1,2],[-2,3],[-3]]],
 [3,[[1,2,3],[-1,-2,-3]]],
 [4,[[1],[-1,2],[-2,3],[-3,4],[-4]]],
 [0,[]],[0,[[]]],[2,[[1,-1],[2]]]
 ];
 for(const [n,cs] of crafted){trial(n,cs);signControls++}
 const invalid=[[-1,[]],[2,null],[2,[[0]]],[2,[[3]]],[2,[[1.5]]],[2,[false]],[1,[[NaN]]],[0,[[1]]],[2,[["1"]]],[2,[null]]];
 for(const [n,c] of invalid){let failed=false;try{validate(n,c)}catch(e){failed=true}ok(failed,"malformed rejection");malformed++}
 let rejected=false;try{evalG({g:[{op:"INVALID"}],out:0},0,1)}catch(e){rejected=true}ok(rejected,"corrupt circuit rejected");
 // K4 edge order 01,02,03,12,13,23, local XOR parity on each vertex.
 const incident=[[0,1,2],[0,3,4],[1,3,5],[2,4,5]];
 for(const charge of [[0,0,0,0],[1,0,0,0]]){let models=0;for(let x=0;x<64;x++){let valid=true;for(let v=0;v<4;v++){let bit=incident[v].reduce((s,e)=>s^((x>>e)&1),0);if(bit!==charge[v]){valid=false;break}}if(valid)models++}oddEven.push(models)}
 ok(oddEven[0]===8&&oddEven[1]===0,"K4 labels");
 return {result:"384_AFFINE_SKETCH_SEMANTIC_AUDIT",seed:null,exhaustive_full_width_n:[1,2,3],formulas, sat,unsat,witnesses:witness,candidate_zero_rejected:candidateReject,crafted_extra:crafted.length,malformed_rejected:malformed,corrupted_gate_rejected:1,k4_even_odd_models:oddEven,assertions,scope:"rank-one fresh-sketch semantic factor versus CNF UNSAT; finite controls only; not a proof of coNP-hardness"};
};
console.log(JSON.stringify(produce(),null,2));
