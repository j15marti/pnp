function degreeLane(base,proof,D,cap=300000){
 let vars=[...new Set(base.flat().map(Math.abs))].sort((a,b)=>a-b),r=vars.length,ix=new Map(vars.map((x,i)=>[x,i])),mon=[],idx=new Map(),rank=0,ops=0,rows=0,terms=0,checks=0,generated=[],B=new Map(),history=[],result=null;
 function comb(start,k,a,out){if(!k){out.push(a);return}for(let i=start;i<=r-k;i++)comb(i+1,k-1,[...a,i],out)}
 let by=[];for(let d=0;d<=D;d++){let arr=[];comb(0,d,[],arr);by.push(arr);for(let a of arr){idx.set(a.join(","),mon.length);mon.push(a)}}
 const bit=i=>1n<<BigInt(i),head=x=>x.toString(2).length-1;
 function row(c,m){let p=[m];for(let l of c){let k=ix.get(Math.abs(l));let q=p.map(a=>[...new Set([...a,k])].sort((a,b)=>a-b));p=l>0?[...p,...q]:q}
 let x=0n;for(let a of p){let i=idx.get(a.join(","));if(i===undefined)throw Error("degree");terms++;x^=bit(i)}return x}
 function add(c,source){if(c.length>D)return;for(let d=0;d<=D-c.length;d++)for(let m of by[d]){if(++rows>cap)throw Error("cap");let x=row(c,m);let j=generated.length;generated.push({source,m,c});let support=bit(j);while(x){if(++ops>cap)throw Error("cap");if(x===1n){let check=0n,ids=[];for(let i=0;i<generated.length;i++)if(support&bit(i)){let g=generated[i];check^=row(g.c,g.m);ids.push({source:g.source,m:g.m.map(i=>vars[i])});checks++}if(check!==1n)throw Error("span");result={source,ids};return}let p=head(x),v=B.get(p);if(v){x^=v.x;support^=v.support}else{B.set(p,{x,support});rank++;break}}}}
 try{for(let i=0;i<base.length&&!result;i++)add(base[i],["base",i]);history.push({prefix:0,rank,rows,ops,hit:!!result});for(let i=0;i<proof.length&&!result;i++){if(!proof[i].length)break;add(proof[i],["learned",i]);history.push({prefix:i+1,rank,rows,ops,hit:!!result})}}catch(e){if(e.message!=="cap")throw e}
 return {D,r,dimension:mon.length,rank,ops,rows,terms,checks,history,result,peakBasisRows:B.size,generatedRows:generated.length,upperBasisBitSlots:B.size*(mon.length+generated.length)}
}
module.exports=degreeLane;
