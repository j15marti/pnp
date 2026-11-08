"use strict";
/* LSPV-3/493: exact local-factor closure for Pang q=2 one-hot cubic Tseitin.
   This is a DISTINCT SOURCE/AND3/XOR semantic fragment, not the historical parser. */
function must(x,why){if(!x)throw Error(why);}
function graph(name){
 if(name==="K4"){let a=[];for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)a.push([i,j]);return [4,a];}
 if(name==="K33"){let a=[];for(let i=0;i<3;i++)for(let j=3;j<6;j++)a.push([i,j]);return [6,a];}
 if(name==="CUBE"){let a=[];for(let i=0;i<8;i++)for(let j=i+1;j<8;j++)if((i^j).toString(2).replace(/0/g,"").length===1)a.push([i,j]);return [8,a];}
 if(name==="PETERSEN"){let a=[];for(let i=0;i<5;i++){a.push([i,(i+1)%5], [i+5,((i+2)%5)+5],[i,i+5]);}return [10,a];}
 throw Error("unknown graph");
}
function source(h,ee,odd){
 let inc=Array.from({length:h},()=>[]),out=[];
 for(let e=0;e<ee.length;e++){let [u,v]=ee[e];inc[u].push(e);inc[v].push(e);out.push([2*e+1,2*e+2],[-2*e-1,-2*e-2]);}
 must(inc.every(x=>x.length===3),"degree");
 for(let v=0;v<h;v++)for(let k=0;k<8;k++){
   let z=[k&1,(k>>1)&1,(k>>2)&1];
   if((z[0]^z[1]^z[2])!==(odd&&v===0?1:0))
     out.push(inc[v].map((e,j)=>-(2*e+z[j]+1)));
 }
 return out;
}
function makeFactor(c){
 let s=[...new Set(c.map(Math.abs))].sort((a,b)=>a-b);
 let t=0;
 for(let k=0;k<(1<<s.length);k++)if(c.some(l=>(((k>>s.indexOf(Math.abs(l)))&1)===Number(l>0))))t|=1<<k;
 return {s,t};
}
function key(f){return f.s.join(",")+":"+f.t;}
function conj(a,b){
 let s=[...new Set([...a.s,...b.s])].sort((u,v)=>u-v);
 must(s.length<=3,"AND3 support >3");
 let t=0;
 for(let k=0;k<(1<<s.length);k++){
   function evalF(f){let j=0;for(let i=0;i<f.s.length;i++)j|=((k>>s.indexOf(f.s[i]))&1)<<i;return (f.t>>j)&1;}
   t|=(evalF(a)&evalF(b))<<k;
 }
 return {s,t};
}
function factors(src){
 let m=new Map(src.map(c=>{let f=makeFactor(c);return [key(f),f]})),joins=0,iterations=0;
 for(;;){
   let arr=[...m.values()], added=0;
   for(let i=0;i<arr.length;i++)for(let j=i+1;j<arr.length;j++){
     if(new Set([...arr[i].s,...arr[j].s]).size>3)continue;
     joins++;
     let f=conj(arr[i],arr[j]),k=key(f);
     if(!m.has(k)){m.set(k,f);added++;}
   }
   iterations++;
   if(!added)break;
   must(iterations<=5,"unexpected factor-closure growth");
 }
 return {list:[...m.values()],joins,iterations};
}
function affine(f){
 let out=[];
 for(let a=0;a<(1<<f.s.length);a++)for(let rhs=0;rhs<2;rhs++){
   let same=true;
   for(let k=0;k<(1<<f.s.length);k++)
     if(((f.t>>k)&1)!==Number(((k&a).toString(2).replace(/0/g,"").length%2)===rhs))same=false;
   if(same){
     let mask=0;
     for(let j=0;j<f.s.length;j++)if(a>>j&1)mask|=1<<(f.s[j]-1);
     out.push([mask,rhs]);
   }
 }
 return out;
}
function models(E,clauses){
 let count=0;
 for(let a=0;a<(1<<E);a++){
   let bits=Array(2*E+1).fill(0);
   for(let e=0;e<E;e++){bits[2*e+1]=1-((a>>e)&1);bits[2*e+2]=(a>>e)&1;}
   if(clauses.every(c=>c.some(l=>bits[Math.abs(l)]===Number(l>0))))count++;
 }
 return count;
}
function run(){
 let results=[],checks=0;
 for(let name of ["K4","K33","CUBE","PETERSEN"]){
   let [h,ee]=graph(name),E=ee.length;
   must(E*2===3*h,"not cubic");checks++;
   let odd=source(h,ee,true),even=source(h,ee,false);
   must(odd.length===7*h,"source clause count");checks++;
   must(models(E,odd)===0,"odd source SAT");checks++;
   let em=models(E,even);
   must(em===(1<<(E-h+1)),"even model count");checks++;
   let closure=factors(odd);
   must(closure.list.length===4*h+3*E,"factor closure mismatch");checks++;
   let rows=new Map();
   for(let f of closure.list)for(let [mask,rhs] of affine(f))rows.set(mask+"/"+rhs,[mask,rhs]);
   must(rows.size===E,"unexpected affine row");checks++;
   for(let e=0;e<E;e++){must(rows.has((3<<(2*e))+"/1"),"missing edge row");checks++;}
   let r=[...rows.values()];
   for(let z=0;z<(1<<E);z++){
     let mask=0,rhs=0;
     for(let e=0;e<E;e++)if(z>>e&1){mask^=r[e][0];rhs^=r[e][1];}
     must(!(mask===0&&rhs===1),"derived contradiction");checks++;
   }
   results.push({name,vertices:h,edges:E,onehotVariables:2*E,originalClauses:odd.length,oddModels:0,evenModels:em,factorClosure:closure.list.length,newEdgeFactors:E,distinctAffineRows:E,spanSize:1<<E,pairChecks:closure.joins,refutation:false});
 }
 let corrupt=0;
 for(let fn of [
   ()=>must(factors(source(...graph("K4"),true)).list.length===35,"bad closure"),
   ()=>conj(makeFactor([1,2,3]),makeFactor([4,5])),
   ()=>must(affine(makeFactor([1,2,3])).length>0,"forged row"),
   ()=>must(source(...graph("K4"),false).length===27,"corrupted source count")
 ]){try{fn();}catch(e){corrupt++;}}
 must(corrupt===4,"corruption acceptance");checks+=4;
 return {status:"PASS",checks,rejectedControls:corrupt,model:"Separate source-factor AND3, exact local affine alias and global XOR; NO historical RES/DEF/LOCAL or parser claims",results};
}
if(typeof require==="function"&&typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(run(),null,2));
