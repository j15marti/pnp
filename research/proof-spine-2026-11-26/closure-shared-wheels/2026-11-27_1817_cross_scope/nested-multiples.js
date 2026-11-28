function multiplyFusion(input,cap=700000){
 const start=Date.now();let work=0;const tick=(k=1)=>{work+=k;if(work>cap)throw Error("cap")};let a=new Map();const can=c=>[...new Set(c)].sort((x,y)=>x-y),key=c=>c.join(",");
 const root=[...new Map(input.map(c=>[key(can(c)),can(c)])).values()].filter(c=>!c.some(l=>c.includes(-l)));
 function UP(C,p=[]){let A=new Map(p),change=true;while(change){change=false;for(let c of C){let sat=false,free=[];for(let l of c){tick();let x=A.get(Math.abs(l));if(x===undefined)free.push(l);else if(x===+(l>0)){sat=true;break}}if(sat)continue;if(!free.length)return null;if(free.length===1){A.set(Math.abs(free[0]),+(free[0]>0));change=true}}}return A}
 function reduction(C,A){return [...new Map(C.filter(c=>!c.some(l=>A.get(Math.abs(l))===+(l>0))).map(c=>{let z=c.filter(l=>!A.has(Math.abs(l)));return[key(z),z]})).values()]}
 function bxor(a,b){for(let k of b){tick();if(a.has(k))a.delete(k);else a.add(k)}}
 function basisPoly(c,v){let p=new Set([0n]);for(let l of c){let b=1n<<BigInt(Math.abs(l)-1),q=new Set();for(let x of p){let y=x|b;bxor(q,[y]);if(l>0)bxor(q,[x])}p=q}if(v){let b=1n<<BigInt(v-1),q=new Set();for(let x of p)bxor(q,[x|b]);p=q}return p}
 function pop(x){let n=0;for(;x;x&=x-1n)n++;return n}
 function lead(p){let k=-1n,d=-1;for(let x of p){let j=pop(x);tick();if(j>d||j===d&&x>k){k=x;d=j}}return[k,d]}
 function direct(c,v){let positive=c.filter(l=>l>0),fixed=c.filter(l=>l<0).map(Math.abs);if(v)fixed.push(v);let s=new Set();for(let w=0;w<2**positive.length;w++){let vars=fixed.concat(positive.filter((l,i)=>w>>i&1)),m=0n;for(let j of vars)m|=1n<<BigInt(j-1);bxor(s,[m])}return s}
 let proof=[],gens=[],rows=[],stat={};try{
 a=UP(root);if(!a)return{status:"ROOT_UP_CONFLICT",work};rows=reduction(root,a);let G=[],basis=new Map(),known=new Set(rows.map(key)),out=[],quad=0,linear=0,tests=0;
 let scopes=rows.map(c=>[...new Set(c.map(Math.abs))]);let n=Math.max(0,...rows.flat().map(Math.abs));let neighbors=new Map();
 for(let i=0;i<rows.length;i++){let c=rows[i];if(c.length>3)continue;G.push({i,v:0});if(c.length>2)continue;let S=scopes[i],vs=new Set();for(let j=0;j<rows.length;j++){tick();let T=scopes[j];if(T.length<=3&&S.every(v=>T.includes(v)))for(let v of T)if(!S.includes(v))vs.add(v)}for(let v of vs)G.push({i,v})}
 gens=G;for(let g of G){let s=basisPoly(rows[g.i],g.v),p=new Set([G.indexOf(g)]);while(s.size){let [k,d]=lead(s);let B=basis.get(k);if(B){bxor(s,B.s);bxor(p,B.p);continue}basis.set(k,{s,p});if(d<=2){if(d===2)quad++;else linear++;let union=0n;for(let x of s)union|=x;let V=[];for(let j=1;j<=n;j++)if((union>>BigInt(j-1))&1n)V.push(j);if(V.length<=4){let t=new Set();for(let id of p){let h=G[id];bxor(t,direct(rows[h.i],h.v))}if(t.size!==s.size||[...t].some(x=>!s.has(x)))throw Error("polynomial replay");let bad=[];for(let w=0;w<2**V.length;w++){tests++;tick();let b=0n;V.forEach((v,i)=>{if(w>>i&1)b|=1n<<BigInt(v-1)});let val=0;for(let x of s)val^=+( (x&b)===x );if(val){let c=can(V.map((v,i)=>w>>i&1?-v:v));if(!known.has(key(c))){known.add(key(c));bad.push(c);out.push(c)}}}if(bad.length)proof.push({generators:[...p],polynomial:[...s].map(String),clauses:bad})}}
 break}}
 let u=UP(rows.concat(out));stat={generators:G.length,nontrivialMultiples:G.filter(g=>g.v).length,rank:basis.size,quadraticBasis:quad,linearBasis:linear,admitted:out.length,tests,extraForced:u===null?"CONFLICT":[...u],maxStoredBasis:basis.size};return{status:u===null?"UNSAT":"UNKNOWN",work,ms:Date.now()-start,rootPins:[...a],rows,gens,proof,stat};
 }catch(e){return{status:"UNKNOWN",reason:String(e),work,ms:Date.now()-start,rootPins:a?[...a]:[],rows,gens,proof,stat}}
}
function peerPrefix(chart,vars,proof,cap=400000){
 let F=chart.map(c=>c.slice()),index=new Map(vars.map((v,i)=>[v,i+1])),work=0,admitted=[],skipped=0,conflict=false;
 function up(C){let a=new Map(),again=true;while(again){again=false;for(let c of C){let free=[],sat=false;for(let l of c){if(++work>cap)throw Error("cap");let x=a.get(Math.abs(l));if(x===undefined)free.push(l);else if(x===+(l>0)){sat=true;break}}if(sat)continue;if(!free.length)return true;if(free.length===1){a.set(Math.abs(free[0]),+(free[0]>0));again=true}}}return false}
 try{for(let row of proof){let c=Array.isArray(row)?row:row.clause??row.c??row.lits;if(!Array.isArray(c)||c.some(l=>!index.has(Math.abs(l)))){skipped++;continue}let d=c.map(l=>Math.sign(l)*index.get(Math.abs(l)));if(up(F.concat(d.map(l=>[-l])))){F.push(d);admitted.push({original:c,dense:d});if(up(F)){conflict=true;break}}else skipped++}}catch(e){return{work,admitted,skipped,conflict,error:String(e)}}return{work,admitted,skipped,conflict}
}
