function run(){
 const stat={gaussian:0,xor:0,mass:0,closureSweeps:0,pins:0,terms:0,rankTests:0,mergedBlocks:0,groupWords:0,liftProbes:0,referenceWords:0,assertions:0};
 const A=(x,msg)=>{stat.assertions++;if(!x)throw Error(msg)};
 const bit=i=>1n<<BigInt(i), pow=i=>1n<<BigInt(i);
 const parity=x=>{let p=0;while(x){x&=x-1n;p^=1}return p};
 function gauss(G){stat.gaussian++;let B=new Map();for(let [a,b] of G){while(a){let p=a&-a;if(!B.has(p)){B.set(p,[a,b]);break}let [v,w]=B.get(p);a^=v;b^=w;stat.xor++}if(!a&&b)return null}return B}
 function size(G,n){let b=gauss(G);return b===null?0n:pow(n-b.size)}
 function rows(f){return f.flatMap(t=>t[1].map(e=>e[0]))}
 function basis(R,G){let B=gauss(G), out=[];if(B===null)throw Error("inconsistent basis");for(let row of R){let a=row;while(a){let p=a&-a;if(!B.has(p)){B.set(p,[a,0]);out.push(row);break}a^=B.get(p)[0];stat.xor++}}return out}
 function mass(f,G,n){stat.mass++;let m=0n;for(let [c,E] of f)m+=c*size(G.concat(E),n);return m}
 function value(f,x){let m=0n;for(let [c,E] of f)if(E.every(([a,b])=>parity(a&x)===b))m+=c;return m}
 function close(F,G,n){G=G.slice();if(!size(G,n))return null;for(;;){stat.closureSweeps++;let changed=false;for(let f of F){if(mass(f,G,n)===0n)return null}
 for(let i=0;i<n&&!changed;i++){let e=[bit(i),0],h=[bit(i),1];if(!size(G.concat([e]),n)||!size(G.concat([h]),n))continue;for(let f of F){let v=mass(f,G.concat([e]),n);let w=mass(f,G.concat([h]),n);if(v===0n||w===0n){G.push(v===0n?h:e);stat.pins++;changed=true;break}}}
 if(!changed)return G}}
 function solveEq(G){let B=gauss(G);if(!B)return null;let x=0n;let K=[...B.keys()].sort((a,b)=>a>b?-1:a<b?1:0);for(let p of K){let [a,b]=B.get(p);if(parity(a&x)!==b)x|=p}return x}
 function group(F,Q,n,cap){let R=basis(F.flatMap(rows),Q),m=0n,first=null;
 if(F.length===1){m=mass(F[0],Q,n);return {m,R,F}}
 if(R.length>cap)return null;
 for(let w=0;w<2**R.length;w++){stat.groupWords++;let P=R.map((a,i)=>[a,(w>>i)&1]);let H=Q.concat(P),s=size(H,n),v=1n;for(let f of F)v*=mass(f,H,n)/s;m+=v*s;if(v>0n&&first===null)first=P}
 return {m,R,F,first}}
 function lift(g,Q,n){if(g.first!==undefined)return g.first;let P=[],H=Q.slice();for(let a of g.R){stat.liftProbes++;let e=[a,0],h=[a,1];let take=mass(g.F[0],H.concat([e]),n)>0n?e:h;P.push(take);H.push(take)}return P}
 function terminal(anchor,F,n,cap=7){let G=close([anchor,...F],[],n);if(G===null)return {m:0n,w:null};let total=0n,chosen=null,positive=anchor.every(t=>t[0]>0n);
 for(let [c,E] of anchor){if(!c)continue;stat.terms++;let Q=close(F,G.concat(E),n);if(Q===null)continue;let B=F.map(f=>[f]),rr=B.map(g=>basis(g.flatMap(rows),Q).length),joint=basis(F.flatMap(rows),Q).length;stat.rankTests++;
 if(rr.reduce((a,b)=>a+b,0)!==joint){B=[F];stat.mergedBlocks++}
 let gs=B.map(g=>group(g,Q,n,cap));if(gs.some(g=>g===null))return {m:null,w:null};let s=size(Q,n),num=s,den=1n;
 for(let g of gs){num*=g.m;den*=s}A(num%den===0n,"nonintegral term");let m=num/den;total+=c*m;if(positive&&m>0n&&chosen===null)chosen={Q,gs};
 }
 A(total>=0n,"negative total");let w=null;if(positive&&total>0n){A(chosen!==null,"missing chosen");let {Q,gs}=chosen;let P=gs.flatMap(g=>lift(g,Q,n));w=solveEq(Q.concat(P));A(w!==null&&value(anchor,w)>0n&&F.every(f=>value(f,w)>0n),"bad witness");}
 return {m:total,w}}
 const one=[[1n,[]]], reject=E=>[[1n,[]],[-1n,E]], word=(ids,w)=>ids.map((i,j)=>[bit(i),Number((BigInt(w)>>BigInt(j))&1n)]);
 const clause=(ids,w)=>reject(word(ids,w));
 const positiveClause=(ids,w)=>ids.map((i,j)=>[1n,[...word(ids.slice(0,j),w),[bit(i),1-Number((BigInt(w)>>BigInt(j))&1n)]]]);
 const nae=ids=>[[1n,[]],[-1n,word(ids,0)],[-1n,word(ids,7)]];
 const multiply=(a,b)=>a.flatMap(([c,E])=>b.map(([d,H])=>[c*d,E.concat(H)]));
 const ref=(anchor,F,n)=>{let m=0n;for(let x=0n;x<pow(n);x++){stat.referenceWords++;let p=value(anchor,x);for(let f of F)p*=value(f,x);m+=p}return m};
 const result={cube:{sat:0,unsat:0},fano:{sat:0,unsat:0,neighborCounts:[]},scale:[],controls:[]};
 for(let k=0;k<256;k++){let ids=[0,1,2], cs=Array.from({length:8},(_,w)=>w).filter(w=>(k>>w)&1),a=cs.length?positiveClause(ids,cs[0]):one,F=cs.slice(1).map(w=>clause(ids,w)),r=terminal(a,F,3),z=ref(a,F,3);A(r.m===z,"cube");result.cube[z>0n?"sat":"unsat"]++}
 const edges=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
 let owners=edges.flatMap(ids=>[[ids,0],[ids,7]]);
 for(let del=-1;del<14;del++){let a0=owners.filter((_,i)=>i!==del),a=positiveClause(...a0[0]),F=a0.slice(1).map(p=>clause(...p)),r=terminal(a,F,7),z=ref(a,F,7);A(r.m===z&&z===(del<0?0n:5n),"Fano");result.fano[z>0n?"sat":"unsat"]++;if(del>=0)result.fano.neighborCounts.push(String(z))}
 function modeCase(r,kind){let ids=Array.from({length:r},(_,i)=>i),modes=[0n,...ids.map(bit)],n=r+3*modes.length,a=modes.map(w=>[1n,word(ids,w)]),F=modes.map((w,j)=>{let p=nae([r+3*j,r+3*j+1,r+3*j+2]);if(kind==="neighbor"&&j===0)return p;let v=kind==="allSat"?pow(r)-1n:w;return multiply(reject(word(ids,v)),p)});return {n,a,F,modes}}
 for(let r of [2,4,8,16])for(let kind of ["root","neighbor","allSat"]){let {n,a,F,modes}=modeCase(r,kind),before=stat.terms,rb=stat.rankTests,mb=stat.mergedBlocks,z=kind==="root"?0n:6n**BigInt(r+1)*(kind==="neighbor"?1n:BigInt(r+1)),res=terminal(a,F,n);A(res.m===z,"mode");if(r===2)A(ref(a,F,n)===z,"mode ref");result.scale.push({r,n,kind,mass:String(res.m),terms:stat.terms-before,rankTests:stat.rankTests-rb,merged:stat.mergedBlocks-mb,witness:res.w!==null})}
 let F=[reject([[1n,0],[2n,0]]),reject([[4n,0],[8n,0]]),reject([[5n,0],[10n,0]])];
 let fail=terminal(one,F,4,0),pass=terminal(one,F,4,4);A(fail.m===null&&pass.m===6n&&ref(one,F,4)===6n,"pairwise rank trap");result.controls.push({name:"pairwise disjoint but globally dependent",capped:"UNKNOWN",mass:"6"});
 let a=[[1n,[[1n,0]]],[1n,[[2n,0]]]],res=terminal(a,[],2);A(res.m===4n&&ref(a,[],2)===4n,"overlap mass");result.controls.push({name:"overlapping positive cover",mass:"4",BooleanSupport:"3"});
 a=reject([[1n,0],[2n,0]]);F=[reject([[4n,0],[8n,0]])];res=terminal(a,F,4);A(res.m===9n&&ref(a,F,4)===9n&&res.w===null,"signed mass");result.controls.push({name:"signed anchor exact count (no lift)",mass:"9"});
 result.stat=stat;return result;
}
console.log(JSON.stringify(run(),null,2));
