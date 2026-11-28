function canon(c){return [...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b)}

function twoDemand(C,U,sameOnly=false,cap=1000000,max=8){
 const M={candidatePairs:0,subsets:0,conflicts:0,rupVisits:0,found:0,duplicate:0,alreadyRup:0},keys=new Map(C.map((c,i)=>[canon(c).join(","),i])),out=[],seen=new Set(keys.keys()),scope=c=>c.map(Math.abs).sort((a,b)=>a-b).join(",");
 function cost(){return M.candidatePairs+M.subsets+M.conflicts+M.rupVisits}
 outer:for(let i=0;i<C.length;i++)for(let j=i+1;j<C.length;j++){if(++M.candidatePairs>cap||cost()>cap)break outer;let a=C[i],b=C[j];if(a.length<2||b.length<2||a.length>4||b.length>4||a.some(l=>b.includes(l))||sameOnly&&scope(a)!==scope(b))continue;
 for(let w=1;w<2**a.length;w++){M.subsets++;let X=a.filter((l,k)=>w>>k&1),Y=[],pairs=[];for(let l of b){let why=[],ok=true;for(let q of X){M.conflicts++;let id=q===-l?-1:keys.get(canon([-q,-l]).join(","));if(id===undefined){ok=false;break}why.push([q,l,id])}if(ok){Y.push(l);pairs.push(...why)}}if(!Y.length)continue;let c=canon(a.filter(l=>!X.includes(l)).concat(b.filter(l=>!Y.includes(l)))),k=c.join(",");if(c.length>3||c.some(l=>c.includes(-l)))continue;if(seen.has(k)){M.duplicate++;continue}seen.add(k);let w0={n:0},p=new Map(c.map(l=>[Math.abs(l),+(l<0)]));if(!U.scalar(C,p,w0)){M.alreadyRup++;M.rupVisits+=w0.n;continue}M.rupVisits+=w0.n;out.push({i,j,X,Y,clause:c,pairs});M.found++;if(out.length>=max||cost()>cap)break outer}}
 return {M:{...M,total:cost()},out,complete:cost()<=cap&&out.length<max};
}

function verifyCut(C,s){let a=C[s.i],b=C[s.j];if(!a||!b||!s.X.length||!s.Y.length||!s.X.every(x=>a.includes(x))||!s.Y.every(x=>b.includes(x)))throw Error("demand");let expected=canon(a.filter(l=>!s.X.includes(l)).concat(b.filter(l=>!s.Y.includes(l))));if(expected.join(",")!==s.clause.join(","))throw Error("boundary");let work=0;for(let x of s.X)for(let y of s.Y){work++;if(x===-y)continue;if(!C.some(c=>c.length===2&&c.includes(-x)&&c.includes(-y)))throw Error("conflict missing")}return{ok:true,work};}
module.exports={twoDemand,verifyCut};
