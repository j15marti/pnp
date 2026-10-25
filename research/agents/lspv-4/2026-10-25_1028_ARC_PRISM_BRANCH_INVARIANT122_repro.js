// ARC-PRISM-BRANCH-INVARIANT122. Deterministic Node/V8 standalone.
"use strict";
function ok(x,msg){if(!x)throw Error(msg||"assertion");}
function prism(k){
 const inc=Array.from({length:2*k},()=>[]),edges=[];
 function edge(a,b){const id=edges.length+1;edges.push([a,b]);inc[a].push(id);inc[b].push(id);}
 for(let i=0;i<k;i++)edge(i,(i+1)%k);
 for(let i=0;i<k;i++)edge(k+i,k+(i+1)%k);
 for(let i=0;i<k;i++)edge(i,k+i);
 ok(inc.every(v=>v.length===3));return {inc,edges};
}
function cnf(g,b){
 let cs=[];
 for(let v=0;v<g.inc.length;v++)for(let a=0;a<8;a++){
  const bits=[a>>2&1,a>>1&1,a&1];
  if((bits[0]^bits[1]^bits[2])!==b[v])
   cs.push(g.inc[v].map((id,j)=>bits[j]?-id:id));
 }
 return cs;
}
function maxid(cs){return Math.max(0,...cs.flat().map(Math.abs));}
function encode(cs){
 let n=maxid(cs),w=Math.max(1,Math.ceil(Math.log2(n+1)));
 function h(x){let q=x.toString(2);return "1".repeat(q.length)+"0"+q;}
 let s="10011010"+h(n)+h(cs.length);
 for(const c of cs){
  ok(c.length===3&&new Set(c.map(Math.abs)).size===3,"proper CNF");
  for(const x of c)s+=(x<0?"1":"0")+Math.abs(x).toString(2).padStart(w,"0");
 }
 return s;
}
function decode(s){
 let p=0;ok(s.slice(0,8)==="10011010","magic");p=8;
 function h(){let n=0;while(s[p]==="1"){n++;p++;}ok(s[p++]==="0"&&n>0,"header");let v=parseInt(s.slice(p,p+n),2);p+=n;return v;}
 let n=h(),m=h(),w=Math.max(1,Math.ceil(Math.log2(n+1))),cs=[];
 for(let i=0;i<m;i++){
  let c=[];for(let j=0;j<3;j++){
   let sign=s[p++]==="1",id=parseInt(s.slice(p,p+w),2);p+=w;ok(id>0&&id<=n);c.push(sign?-id:id);
  }
  ok(new Set(c.map(Math.abs)).size===3);cs.push(c);
 }
 ok(p===s.length,"EOF");return cs;
}
function lift(cs,id,value){
 let out=[],next=maxid(cs)+1;
 for(const c of cs){
  if(c.some(x=>Math.abs(x)===id&&(x>0)===value))continue;
  let a=c.filter(x=>Math.abs(x)!==id);
  ok(a.length>=2&&a.length<=3,"unit or contradiction");
  if(a.length===3)out.push(a);
  else{let h=next++;out.push([a[0],a[1],h],[a[0],a[1],-h]);}
 }
 return out;
}
function balanced(cs){
 let d=new Map();
 for(const c of cs)for(const x of c){
  let id=Math.abs(x);if(!d.has(id))d.set(id,[0,0]);d.get(id)[x<0?1:0]++;
 }
 return [...d.values()].every(z=>z[0]===z[1]);
}
function linear(g,charges,fixed){
 let n=g.edges.length,rows=[];
 for(let v=0;v<g.inc.length;v++){
  let row=Array(n+1).fill(0);for(const e of g.inc[v])row[e-1]=1;row[n]=charges[v];rows.push(row);
 }
 for(const [id,val] of fixed){
  let row=Array(n+1).fill(0);row[id-1]=1;row[n]=val?1:0;rows.push(row);
 }
 let pivot=[],r=0;
 for(let c=0;c<n;c++){
  let j=r;while(j<rows.length&&!rows[j][c])j++;if(j===rows.length)continue;
  [rows[j],rows[r]]=[rows[r],rows[j]];
  for(let h=0;h<rows.length;h++)if(h!==r&&rows[h][c])
   for(let t=c;t<=n;t++)rows[h][t]^=rows[r][t];
  pivot.push(c);r++;
 }
 if(rows.slice(r).some(row=>row[n]===1))return null;
 let a=Array(n+1).fill(false);
 for(let i=0;i<pivot.length;i++)a[pivot[i]+1]=!!rows[i][n];
 return a;
}
function truth(cs,a){return cs.every(c=>c.some(x=>a[Math.abs(x)]===(x>0)));}
function dpll(cs){
 function run(f,a){
  for(;;){
   let change=false,out=[];
   for(const c of f){
    if(c.some(x=>a.has(Math.abs(x))&&a.get(Math.abs(x))===(x>0)))continue;
    let z=c.filter(x=>!a.has(Math.abs(x)));if(!z.length)return false;
    if(z.length===1){let id=Math.abs(z[0]),v=z[0]>0;if(a.has(id)&&a.get(id)!==v)return false;if(!a.has(id)){a.set(id,v);change=true;}}
    out.push(z);
   }
   f=out;if(!change)break;
  }
  if(!f.length)return true;
  let id=Math.abs(f[0][0]);
  for(const val of [false,true]){let b=new Map(a);b.set(id,val);if(run(f,b))return true;}
  return false;
 }
 return run(cs,new Map());
}
function audit(){
 const raw={id:"ARC-PRISM-BRANCH-INVARIANT122",seed:null,mode:"deterministic exhaustive two branch choices at k=3,4,6,8",cases:[],
  assertions:0,grandchildren:0,roundtrip_bits:0,explicit_unchanged_scratch_writes:0,dpll_root_checks:0,physical_flmv_trace:false};
 function check(p,m){raw.assertions++;ok(p,m);}
 for(const k of [3,4,6,8]){
  let g=prism(k),E=g.edges.length,M=8*k;
  for(const charge of [0,1]){
   let b=Array(2*k).fill(0);b[0]=charge;const sat=charge===0;
   let root=cnf(g,b),s0=encode(root),p0=decode(s0);
   check(JSON.stringify(root)===JSON.stringify(p0),"root serialization");
   check(root.length===M&&balanced(root),"root parity balance");
   check(Boolean(linear(g,b,[]))===sat,"root parity");
   if(k<=4){check(dpll(root)===sat,"root DPLL");raw.dpll_root_checks++;}
   let one=0,two=0,min1=Infinity,max1=0,min2=Infinity,max2=0;
   for(let e=1;e<=E;e++)for(const v of [false,true]){
    let c1=lift(p0,e,v),s1=encode(c1),p1=decode(s1);raw.roundtrip_bits+=s1.length;
    check(JSON.stringify(c1)===JSON.stringify(p1),"first child exact");
    check(c1.length===M,"first clause count");
    check(balanced(c1),"first sign balance");
    check(Boolean(linear(g,b,[[e,v]]))===sat,"first label");
    one++;min1=Math.min(min1,s1.length/s0.length);max1=Math.max(max1,s1.length/s0.length);
    for(const x of [...new Set(c1.flat().map(Math.abs))])for(const w of [false,true]){
     let c2=lift(p1,x,w),s2=encode(c2),p2=decode(s2);raw.roundtrip_bits+=s2.length;
     check(JSON.stringify(c2)===JSON.stringify(p2),"second child exact");
     check(c2.length===M,"second clause count");
     let fixed=[[e,v]];if(x<=E)fixed.push([x,w]);
     let a=linear(g,b,fixed);check(Boolean(a)===sat,"second label");
     if(a){
      let witness=Array(maxid(c2)+1).fill(false);
      for(let j=1;j<=E;j++)witness[j]=a[j];witness[x]=w;
      check(truth(c2,witness),"second SAT witness");
     }
     let scratch=0;
     for(let j=0;j<c2.length;j++){if(scratch===0)raw.explicit_unchanged_scratch_writes++;scratch=0;}
     two++;raw.grandchildren++;
     min2=Math.min(min2,s2.length/s0.length);max2=Math.max(max2,s2.length/s0.length);
    }
   }
   raw.cases.push({k,label:sat?"SAT":"UNSAT",root_variables:E,root_clauses:M,root_bits:s0.length,
    first_children:one,second_children:two,first_over_root:[min1,max1],second_over_root:[min2,max2]});
  }
 }
 return raw;
}
if(typeof process!=="undefined"&&typeof require!=="undefined"&&require.main===module)
 console.log(JSON.stringify(audit(),null,2));
