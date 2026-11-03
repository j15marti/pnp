// LSPV-2 347 diagnostic ENUM_ARITY replay. No dependency, Node >=16.
'use strict';
function ok(x,m){if(!x)throw Error(m)}
function val(c,a){return c.some(l=>Boolean((a>>(Math.abs(l)-1))&1)===(l>0))}
function count(f){let q=0;for(let a=0;a<2**f.n;a++)q+=f.c.every(c=>val(c,a));return q}
function minimum(f){ok(count(f)===0,'SAT');let ids=f.c.map((_,i)=>i);if(ids.every(j=>count({n:f.n,c:f.c.filter((_,i)=>i!==j)})>0))return ids;
 let best=ids;for(let s=1;s<2**ids.length;s++){const sel=ids.filter(i=>(s>>i)&1);if(sel.length>=best.length)continue;if(count({n:f.n,c:sel.map(i=>f.c[i])})===0)best=sel}return best}
function cert(f,S){return {rule:'ENUM_ARITY',sources:S,weight:S.length-1,rows:Array.from({length:2**f.n},(_,a)=>{let j=S.find(i=>!val(f.c[i],a));ok(j!==undefined,'SAT uncovered');return j})}}
function verify(f,p){ok(Number.isInteger(f.n)&&f.n>=0&&f.n<=10,'n');ok(Array.isArray(f.c)&&f.c.length<=16,'clauses');for(const c of f.c){ok(Array.isArray(c),'array');for(let l of c)ok(Number.isInteger(l)&&l!==0&&Math.abs(l)<=f.n,'literal')}
 ok(p.rule==='ENUM_ARITY'&&p.sources.length>=2&&new Set(p.sources).size===p.sources.length,'sources');
 ok(p.weight===p.sources.length-1&&p.rows.length===2**f.n,'weight/rows');
 let checks=0;for(let a=0;a<p.rows.length;a++){let j=p.rows[a];ok(p.sources.includes(j)&&!val(f.c[j],a),'invalid row');checks+=f.c[j].length}return checks}
const G={n:4,c:[[-3,1,4],[-1,2],[1,3],[-4,-3],[-2,-1,3],[-2,4]]};
const H={n:7,c:[[1],...Array.from({length:6},(_,i)=>[-i-1,i+2]),[-7]]};
const B={n:3,c:[ [1,2],[-1,-2],[1,3],[-1,-3],[2,3],[-2,-3] ]};
const E={n:4,c:[[-1,2],[1,-2],[-2,3],[2,-3],[-3,4],[3,-4],[1],[-4]]};
const T=(odd)=>{let ed=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],cs=[];for(let v=0;v<4;v++){let u=ed.map((e,i)=>e.includes(v)?i+1:0).filter(Boolean);for(let a=0;a<8;a++){let pc=(a.toString(2).split('1').length-1)%2;if(pc!==(v===0&&odd?1:0))cs.push(u.map((l,i)=>(a>>i&1)?-l:l))}}return {n:6,c:cs}};
let results={cases:[],satModels:{}};for(const [name,f] of [['G342',G],['Horn7',H],['BPHP2',B],['OddK4',T(true)],['Equality4',E],['UnitClash',{n:1,c:[[1],[-1]]}]]){let S=minimum(f),p=cert(f,S),literalChecks=verify(f,p);results.cases.push({name,n:f.n,m:f.c.length,mu:S.length,cost:p.weight,rows:p.rows.length,literalChecks});}
for(const [name,f] of [['EvenK4',T(false)],['G342Flipped',{n:4,c:[[3,1,4],...G.c.slice(1)]}],['HornFlipped',{n:7,c:[...H.c.slice(0,-1),[7]]}],['EqualityFlipped',{n:4,c:[...E.c.slice(0,-1),[4]]}]]){results.satModels[name]=count(f);ok(count(f)>0,name)}
console.log(JSON.stringify(results,null,2));