"use strict";
function run(){
 const seed=20261103;let r=seed,checks=0,sat=0,unsat=0,gates=0,malformed=0;
 function assert(x,m){checks++;if(!x)throw Error("FAIL:"+m)}
 function rnd(n){r=(Math.imul(r,1664525)+1013904223)>>>0;return r%n}
 function flip(x){return {i:x.i,s:!x.s}}
 function lit(x,v){if(!Number.isInteger(x.i)||x.i<0||x.i>=v.length||typeof x.s!=="boolean")throw Error("literal");return v[x.i]^(x.s?1:0)}
 function parse(gs,o){if(!o||!Number.isInteger(o.i)||o.i<0||o.i>gs.length||typeof o.s!=="boolean")throw Error("output");for(let k=0;k<gs.length;k++){let g=gs[k];if(!g||g.i!==k+1)throw Error("id");for(let x of [g.a,g.b])if(!x||!Number.isInteger(x.i)||x.i<0||x.i>=g.i||typeof x.s!=="boolean")throw Error("edge");}return true}
 function original(ns,a){const v=a.slice();for(let n of ns){const x=v[n.a];v.push(n.op==="NOT"?1-x:n.op==="AND"?(x&v[n.b]):n.op==="OR"?(x|v[n.b]):NaN);}return v.at(-1)}
 function compiled(ns,a){const v=a.map(x=>({i:0,s:!x})),gs=[];for(let n of ns){let x=v[n.a];if(n.op==="NOT"){v.push(flip(x));continue;}let y=v[n.b],i=gs.length+1;if(n.op==="AND"){gs.push({i,a:x,b:y});v.push({i,s:false})}else if(n.op==="OR"){gs.push({i,a:flip(x),b:flip(y)});v.push({i,s:true})}else throw Error("op")}return {gs,o:v.at(-1)}}
 function gatesEval(gs,o){parse(gs,o);let v=[1];for(let g of gs)v.push(lit(g.a,v)&lit(g.b,v));return lit(o,v)}
 function cnf(gs,o,b){const cs=[[1]];for(let g of gs){const A=(g.a.s?-1:1)*(g.a.i+1),B=(g.b.s?-1:1)*(g.b.i+1),z=g.i+1;cs.push([-z,A],[-z,B],[z,-A,-B]);}const y=(o.s?-1:1)*(o.i+1);cs.push([b?y:-y]);return cs}
 function count(cs,k){let total=0;for(let a=0;a<2**k;a++){let good=true;for(let c of cs){let yes=false;for(let x of c){const b=(a>>(Math.abs(x)-1))&1;if((x>0&&b)||(x<0&&!b)){yes=true;break;}}if(!yes){good=false;break;}}if(good)total++;}return total}
 const fixed=[
 [{op:"AND",a:0,b:1}], [{op:"OR",a:0,b:1}],
 [{op:"NOT",a:0},{op:"NOT",a:3}],
 [{op:"AND",a:0,b:1},{op:"NOT",a:3},{op:"OR",a:4,b:2}],
 [{op:"OR",a:0,b:1},{op:"AND",a:3,b:2},{op:"OR",a:4,b:0}],
 [{op:"AND",a:0,b:1},{op:"AND",a:0,b:1},{op:"OR",a:3,b:4}]
 ];
 for(let j=0;j<160;j++){const ns=[];for(let k=0;k<5;k++){const op=["AND","OR","NOT"][rnd(3)],q=3+k;ns.push(op==="NOT"?{op,a:rnd(q)}:{op,a:rnd(q),b:rnd(q)});}fixed.push(ns)}
 for(const ns of fixed)for(let mask=0;mask<8;mask++){const a=[mask&1,(mask>>1)&1,(mask>>2)&1],b=original(ns,a),{gs,o}=compiled(ns,a);assert(parse(gs,o),"parse");assert(gatesEval(gs,o)===b,"truth");const n1=count(cnf(gs,o,1),gs.length+1),n0=count(cnf(gs,o,0),gs.length+1);assert(n1===b,"SAT side");assert(n0===1-b,"UNSAT side");sat+=n1+n0;unsat+=(n1===0)+(n0===0);gates+=gs.length;}
 const bad=[
 {gs:[{i:2,a:{i:0,s:false},b:{i:0,s:false}}],o:{i:1,s:false}},
 {gs:[{i:1,a:{i:1,s:false},b:{i:0,s:false}}],o:{i:1,s:false}},
 {gs:[{i:1,a:{i:3,s:false},b:{i:0,s:false}}],o:{i:1,s:false}},
 {gs:[{i:1,a:{i:0,s:"bad"},b:{i:0,s:false}}],o:{i:1,s:false}},
 {gs:[{i:1,a:{i:-1,s:false},b:{i:0,s:false}}],o:{i:1,s:false}},
 {gs:[{i:1,a:{i:0,s:false},b:{i:0,s:false}}],o:{i:2,s:false}},
 {gs:[{i:1,a:{i:0,s:false},b:{i:0,s:false}}],o:{i:1,s:1}},
 {gs:[{i:1,a:{i:0,s:false},b:null}],o:{i:1,s:false}},
 {gs:[{i:1,a:{i:0,s:false},b:{i:0,s:false}},{i:2,a:{i:3,s:false},b:{i:0,s:false}}],o:{i:2,s:false}}
 ];
 for(const x of bad){let rej=false;try{parse(x.gs,x.o)}catch(e){rej=true}assert(rej,"malformed");malformed++}
 const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
 function tseitin(ch){let n=0;for(let a=0;a<64;a++){let ok=true;for(let v=0;v<4;v++){let p=0;for(let i=0;i<6;i++)if(edges[i].includes(v))p^=(a>>i)&1;if(p!==ch[v]){ok=false;break}}if(ok)n++}return n}
 const parity=[tseitin([0,0,0,0]),tseitin([1,0,0,0])];assert(parity[0]===8&&parity[1]===0,"parity");
 return {status:"COMPUTATIONAL",seed,source_cases:fixed.length*8,forced_label_CNF_cases:fixed.length*16,checks,sat,unsat,gates,malformed_rejected:malformed,k4_even_odd:parity,tool:"node >=18 standard builtins; deterministic, no dependencies"};
}
if (require.main===module) console.log(JSON.stringify(run(),null,2));
module.exports=run;
