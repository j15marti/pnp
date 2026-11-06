/* LSPV-3/444 source-level SAT/UNSAT controls, node script.js. Not native R_mix341. */
"use strict";
let checks=0;
function ok(x,s){checks++;if(!x)throw Error(s);}
function parse(src){const lines=src.trim().split("\n"),h=lines.shift().split(/\s+/);
 if(h[0]!=="p"||h[1]!=="cnf"||h.length!==4)throw Error("header");
 const n=Number(h[2]),m=Number(h[3]);if(m!==lines.length||n<1)throw Error("count");
 const c=lines.map(l=>{const a=l.trim().split(/\s+/).map(Number);if(a.pop()!==0||!a.length)throw Error("zero");
 if(a.some(x=>!Number.isInteger(x)||x===0||Math.abs(x)>n)||
 new Set(a.map(Math.abs)).size!==a.length)throw Error("literal");return a});return {n,c};
}
function source(n,c){return "p cnf "+n+" "+c.length+"\n"+c.map(x=>x.join(" ")+" 0\n").join("");}
function models(f){let k=0;for(let a=0;a<2**f.n;a++){
 const good=f.c.every(c=>c.some(l=>{const b=(a>>(Math.abs(l)-1))&1;return l>0?b===1:b===0;}));
 if(good)k++;
}return k;}
const edge=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
function tseitin(ch){let c=[];for(let v=0;v<4;v++){const I=edge.map((e,k)=>e.includes(v)?k:-1).filter(k=>k>=0);
 for(let w=0;w<8;w++){const parity=((w&1)^((w>>1)&1)^((w>>2)&1));
 if(parity===ch[v])continue;c.push(I.map((k,j)=>(w>>j)&1?-(k+1):k+1));}}
 return parse(source(6,c));}
function bphp(m,ell=2){const n=2**ell,c=[];for(let i=0;i<m;i++)for(let j=i+1;j<m;j++)for(let a=0;a<n;a++){
 const cl=[];for(const p of [i,j])for(let k=0;k<ell;k++)cl.push((a>>k)&1?-(p*ell+k+1):p*ell+k+1);c.push(cl);}
 return parse(source(m*ell,c));}
const odd=tseitin([1,0,0,0]),even=tseitin([0,0,0,0]),unsat=bphp(5),sat=bphp(4);
ok(odd.c.length===16&&even.c.length===16,"K4 source");
ok(models(odd)===0,"K4 odd UNSAT");ok(models(even)===8,"K4 even SAT");
for(let i=0;i<16;i++)ok(models({n:6,c:odd.c.filter((_,j)=>j!==i)})>0,"K4 clause essential");
ok(unsat.c.length===40&&models(unsat)===0,"bit-PHP UNSAT");
ok(sat.c.length===24&&models(sat)===24,"bit-PHP SAT");
let malformed=0;
const raw=source(6,odd.c);
for(const edit of [s=>s.replace("p cnf 6 16","p cnf 6 17"),
s=>s.replace("p cnf 6 16","p cnf 5 16"),
s=>s.replace(" 0\n"," 7 0\n"),
s=>s.replace(" 0\n"," 3\n"),
s=>s.replace(" 0\n"," 1 0\n"),
s=>s.replace("p cnf","p cxf")]){
 let rejected=false;try{parse(edit(raw))}catch{rejected=true}
 ok(rejected,"malformed accepted");malformed++}
console.log(JSON.stringify({result:"PASS",checks,malformed_rejected:malformed,
  K4_odd_models:0,K4_even_models:8,bitPHP_l2_m5_models:0,bitPHP_l2_m4_models:24,
  historical_native_checker:"not run"},null,2));
