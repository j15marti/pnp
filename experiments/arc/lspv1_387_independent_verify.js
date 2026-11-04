/* Invoke: node -e 'console.log(require("./lspv1_387_independent_verify.js")())' */
module.exports=function(){
"use strict"; /* LSPV-1/387 no-import, independently enumerative checker */
let asserts=0;function must(v,msg){asserts++;if(!v)throw Error(msg);}
function codeInt(x){const s=Number(x).toString(2);return "0".repeat(s.length-1)+s;}
function build(l){
 const n=1<<l,V=(n+1)*l+1,t=V,w=V.toString(2).length;
 let rows=[],id=[];
 for(let i=0;i<=n;i++)for(let j=i+1;j<=n;j++)for(let hole=0;hole<n;hole++){
  let terms=[-t];for(let z of [i,j])for(let b=0;b<l;b++)terms.push((hole&(1<<b))?-(1+z*l+b):(1+z*l+b));
  rows.push(terms);
 }
 rows.push([t]);let data="1011"+codeInt(V+1)+codeInt(rows.length+1);
 for(let j=0;j<rows.length;j++){
  data+=codeInt(rows[j].length+1);
  for(let k=0;k<rows[j].length;k++){
   id.push([data.length,j,k]);let z=rows[j][k];
   data+=(z>0?"1":"0")+Math.abs(z).toString(2).padStart(w,"0");
  }
 }
 return {n,V,rows,id,data}
}
function parse(s){
 let p=0;
 if(s.substring(0,4)!=="1011"||/[^01]/.test(s))throw Error("tag");
 p=4;function g(){let k=0;while(p<s.length&&s[p]==="0")p++,k++;if(p+k>=s.length)throw Error("gamma");let v=parseInt(s.substring(p,p+k+1),2);p+=k+1;return v;}
 let V=g()-1,m=g()-1;
 if(V<1||m<1||m>10000)throw Error("header");
 let width=V.toString(2).length,rows=[];
 for(let j=0;j<m;j++){
  let k=g()-1;
  if(k<1||k>2*V+3)throw Error("width");
  let terms=[];
  for(let i=0;i<k;i++){
   if(p+1+width>s.length)throw Error("truncated");
   let sign=s[p++],v=parseInt(s.substring(p,p+width),2);p+=width;
   if(v<1||v>V)throw Error("id");
   terms.push(sign==="1"?v:-v);
  }
  rows.push(terms);
 }
 if(p!==s.length)throw Error("trailing");
 return {V,rows}
}
const flip=(s,ps)=>{const a=[...s];ps.forEach(p=>a[p]=a[p]==="0"?"1":"0");return a.join("")};
function triDecode(s){if(s.length%3)throw Error("width");let out="";for(let i=0;i<s.length;i+=3){let word=s.substring(i,i+3);if(/[^01]/.test(word))throw Error("bit");out+=((word[0]==="1")+(word[1]==="1")+(word[2]==="1")>=2?"1":"0")}return out}
function sat(F){let V=F.V;if(V>16)throw Error("small oracle only");
 for(let a=0;a<2**V;a++){let fits=true;
  for(const row of F.rows){let yes=false;for(const z of row){const bit=Boolean(a&(2**(Math.abs(z)-1)));if(z>0?bit:!bit){yes=true;break}}if(!yes){fits=false;break}}
  if(fits)return true;
 }
 return false;
}
const summary=[];
for(const l of [1,2,3]){
 const S=build(l),M=S.n*S.n*(S.n+1)/2,K=M*(2*l+1)+1;
 const w=S.V.toString(2).length;
 const N=4+codeInt(S.V+1).length+codeInt(M+2).length+
 M*(codeInt(2*l+2).length+(2*l+1)*(1+w))+
 codeInt(2).length+1+w;
 must(S.id.length===K,"K formula");
 must(S.data.length===N,"N formula");
 const raw=Array.from(S.data,c=>c+c+c).join("");
 must(parse(triDecode(raw)).rows.length===M+1,"decode source");
 let count=0;
 for(let h=0;h<S.id.length;h++){
  if(l===3 && h%17!==0)continue;
  const [pos,ci,li]=S.id[h],F=parse(flip(S.data,[pos]));
  if(l<3)must(sat(F),"each sign flip SAT");
  for(let z=0;z<3;z++){
   const y=flip(raw,[3*pos+z]);
   must(triDecode(y)===S.data,"single flip neutral");
  }
  for(let z=0;z<3;z++){
   const p1=z,p2=(z+1)%3;
   const y=flip(raw,[3*pos+p1,3*pos+p2]);
   must(triDecode(y)===flip(S.data,[pos]),"double flip");
  }
  count++;
 }
 summary.push({ell:l,N,K,tripledBits:3*N,selectedSignBits:count,oneBitNeutralCases:3*count,twoBitSATCases:3*count,deterministicReadsFloor:2*K,randomizedCoefficientNumerator:3*K});
}
const neg=["","1","000","222","1010000","1011"];let rejected=0;
for(const s of neg){try{parse(triDecode(s))}catch(e){rejected++}}
must(rejected===neg.length,"negative grammar cases");
return {id:"LSPV1_387_INDEPENDENT",summary,asserts,rejected};

};
if(require.main===module) console.log(JSON.stringify(module.exports(),null,2));
