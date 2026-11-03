'use strict';
// LSPV-1 REVERSIBLE-REPRESENTATION-TRAP373, finite exhaustive controls.
function assert(q,msg){if(!q)throw Error(msg)}
function valid(F){return F!==null&&typeof F==='object'&&Number.isSafeInteger(F.n)&&
 F.n>=0&&Array.isArray(F.clauses)&&F.clauses.every(c=>Array.isArray(c)&&
 c.every(x=>Number.isSafeInteger(x)&&x!==0&&Math.abs(x)<=F.n))}
function PHP(h){
 assert(Number.isInteger(h)&&h>=1&&h<=100,'PHP parameter');
 let cs=[];const id=(i,j)=>i*h+j+1;
 for(let i=0;i<h+1;i++){let c=[];for(let j=0;j<h;j++)c.push(id(i,j));cs.push(c)}
 for(let j=0;j<h;j++)for(let i=0;i<h+1;i++)for(let k=i+1;k<h+1;k++)
 cs.push([-id(i,j),-id(k,j)]);
 return {n:h*(h+1),clauses:cs}
}
function isPHP(F){
 if(!valid(F)||F.n<2)return false;
 const h=Math.floor((Math.sqrt(1+4*F.n)-1)/2);
 if(h*(h+1)!==F.n||h<1||h+1>F.clauses.length)return false;
 if((h+1)+h*h*(h+1)/2!==F.clauses.length)return false;
 const p=PHP(h);
 return F.clauses.every((c,i)=>c.length===p.clauses[i].length&&
 c.every((x,j)=>x===p.clauses[i][j]));
}
function encode(F){
 if(!valid(F))return F;
 const z=F.n+1,cs=F.clauses.map(c=>c.slice());cs.push([z]);
 if(isPHP(F))cs.push([-z]);
 return {n:z,clauses:cs}
}
function decode(G){
 if(!valid(G))return G;
 const z=G.n,cs=G.clauses;
 if(z===0||cs.length===0)throw Error('nonimage');
 let tail;
 if(cs.length>=2&&cs.at(-1).length===1&&cs.at(-1)[0]===-z&&
 cs.at(-2).length===1&&cs.at(-2)[0]===z)tail=2;
 else if(cs.at(-1).length===1&&cs.at(-1)[0]===z)tail=1;
 else throw Error('bad suffix');
 const F={n:z-1,clauses:cs.slice(0,-tail).map(c=>c.slice())};
 if(!valid(F)||JSON.stringify(encode(F))!==JSON.stringify(G))
 throw Error('nonimage/corrupt');
 return F
}
function models(F){
 assert(valid(F)&&F.n<=13,'finite exhaustive oracle only');
 let ans=0;
 for(let a=0;a<2**F.n;a++)
 if(F.clauses.every(c=>c.some(l=>(l>0)===Boolean(a&(1<<(Math.abs(l)-1))))))ans++;
 return ans
}
function oneResolution(F,p){
 return valid(F)&&Number.isSafeInteger(p)&&p>0&&
 F.clauses.some(c=>c.length===1&&c[0]===p)&&
 F.clauses.some(c=>c.length===1&&c[0]===-p)
}
function K4(odd){
 const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],cs=[];
 for(let v=0;v<4;v++){
 const local=edges.map((e,i)=>e.includes(v)?i+1:null).filter(x=>x!==null);
 const b=(odd&&v===0)?1:0;
 for(let a=0;a<8;a++){
 const parity=((a>>0)&1)^((a>>1)&1)^((a>>2)&1);
 if(parity===b)continue;
 cs.push(local.map((x,i)=>(a&(1<<i))?-x:x))
 }}return {n:6,clauses:cs}
}
function main(){
 let checks=0;const check=(b,s)=>{checks++;assert(b,s)};
 const fixtures=[];
 for(let h=1;h<=3;h++){
 const F=PHP(h),G=encode(F),z=G.n;
 check(isPHP(F),'PHP recognized');
 check(JSON.stringify(decode(G))===JSON.stringify(F),'inverse');
 check(G.clauses.length===F.clauses.length+2,'append');
 check(G.clauses.slice(0,-2).every((c,i)=>
 JSON.stringify(c)===JSON.stringify(F.clauses[i])),'prefix');
 check(oneResolution(G,z),'unit resolution');
 check(!oneResolution(F,z),'original pivot unavailable');
 check(!oneResolution(G,z+1),'bad pivot');
 check(models(F)===0&&models(G)===0,'UNSAT both');
 const M=JSON.parse(JSON.stringify(F));M.clauses.at(-1)[0]*=-1;
 const sat=models(M);
 check(sat>0,'SAT polarity neighbor');
 check(!isPHP(M),'neighbor not recognized');
 check(JSON.stringify(decode(encode(M)))===JSON.stringify(M),'neighbor inverse');
 check(models(encode(M))===sat,'neighbor preserved');
 fixtures.push({family:'PHP',h,variables:F.n,clauses:F.clauses.length,
 source_json_characters:JSON.stringify(F).length,
 encoded_json_characters:JSON.stringify(G).length,
 source_models:0,encoded_models:0,mutant_models:sat,
 encoded_resolution_minimum:1});
 }
 for(const [name,F] of [
 ['SAT_unit',{n:1,clauses:[[1]]}],
 ['SAT_mixed',{n:2,clauses:[[1,2],[-1,2]]}],
 ['UNSAT_units',{n:1,clauses:[[1],[-1]]}],
 ['UNSAT_empty',{n:0,clauses:[[]]}],
 ['SAT_empty',{n:0,clauses:[]}],
 ['TSEITIN_even',K4(false)],['TSEITIN_odd',K4(true)]])
 {
 const G=encode(F),a=models(F),b=models(G);
 check(!isPHP(F),'nonPHP');
 check(JSON.stringify(decode(G))===JSON.stringify(F),'inverse');
 check(a===b,'source projection');
 if(name==='TSEITIN_even')check(a===8,'K4 even models');
 if(name==='TSEITIN_odd')check(a===0,'K4 odd UNSAT');
 fixtures.push({family:name,variables:F.n,clauses:F.clauses.length,
 source_models:a,encoded_models:b});
 }
 const bad=[null,'bad',{n:-1,clauses:[]},{n:1,clauses:[[0]]},
 {n:1,clauses:[[2]]},{n:1,clauses:'wrong'},
 {n:1,clauses:[['1']]},{n:1,clauses:[[1.2]]},{n:'1',clauses:[[1]]}];
 for(const x of bad){
 check(!valid(x),'malformed');
 check(encode(x)===x,'malformed unchanged');
 check(decode(encode(x))===x,'malformed inverse');
 }
 const corrupt=[{n:3,clauses:[[1],[-2]]},
 {n:3,clauses:[[1],[3],[-3]]},{n:4,clauses:[[3],[-4]]}];
 for(const x of corrupt){let rejected=false;try{decode(x)}catch(e){rejected=true}
 check(rejected,'corrupt proof/payload');}
 return {experiment:'REVERSIBLE_REPRESENTATION_TRAP373',
 controls:'finite source labels, exhaustive truth evaluator',
 deterministic:true,random_seed:null,assertions:checks,
 malformed_rejected:bad.length,corrupt_rejected:corrupt.length,
 fixtures,scope:'Haken exponential theorem external; JSON size numbers finite only'}
}
if(typeof module!=='undefined'){
 module.exports={PHP,isPHP,encode,decode,valid,models,oneResolution,main};
 if(require.main===module)console.log(JSON.stringify(main(),null,2));
}