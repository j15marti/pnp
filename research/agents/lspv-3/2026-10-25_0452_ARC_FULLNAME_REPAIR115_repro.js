"use strict";
function run(){
 let S={run_id:"ARC-FULLNAME-REPAIR115",seed:null,checks:0,sat_calls:0,dpll_nodes:0,roundtrips:0,visible_contexts:0,full_pin_queries:0,stage_cases:[],label_preserving_twolevel:[],large_lengths:[],errors:0,FLMV_steps_measured:false};
 function ck(x,m){S.checks++;if(!x){S.errors++;throw Error(m)}}
 function alloc(n){return {n}};
 function fresh(a){return ++a.n}
 function xor(u,v,w){let C=[];for(let k=0;k<8;k++){let p=k>>2&1,q=k>>1&1,r=k&1;if(r!==(p^q))C.push([p?-u:u,q?-v:v,r?-w:w])}return C}
 function pin(l,a){let p=fresh(a),q=fresh(a);return [[l,p,q],[l,p,-q],[l,-p,q],[l,-p,-q]]}
 function or2(u,v,a){let x=fresh(a);return [[u,v,x],[u,v,-x]]}
 function mod(b,u){let a=alloc(b),z=[],w=[],R=[],Q=[];
   for(let i=0;i<=b;i++)z.push(fresh(a));
   R.push(...pin(-z[0],a),...pin(-z[b],a));
   for(let i=0;i<b;i++)R.push(...xor(z[i],i+1,z[i+1]));
   for(let i=0;i<=b;i++)w.push(fresh(a));
   Q.push(...pin(-w[0],a));
   for(let i=0;i<b;i++)Q.push(...xor(w[i],i+1,w[i+1]));
   let q=fresh(a);Q.push(...or2(q,w[b],a));
   for(let i=0;i<b;i++)Q.push(...or2(-q,u[i]?i+1:-(i+1),a));
   return {R,Q,F:[...R,...Q],n:a.n};
 }
 function pack(C,n){let m=C.length,h=Math.floor(Math.log2(2*Math.max(n,m)+1))+1;
   const field=x=>x.toString(2).padStart(h,"0");
   let v="1".repeat(h)+"0"+field(n)+field(m);
   for(let c of C){ck(c.length===3&&new Set(c.map(Math.abs)).size===3,"proper clause");
     for(let l of c){ck(Math.abs(l)>0&&Math.abs(l)<=n,"identifier");v+=field(2*(Math.abs(l)-1)+(l<0?1:0))}}
   ck(v.length===1+(3+3*m)*h,"length");return v}
 function unpack(v){let h=0;while(v[h]==="1")h++;
   if(!h||v[h]!=="0")throw Error("bad unary");
   let n=parseInt(v.slice(h+1,2*h+1),2),m=parseInt(v.slice(2*h+1,3*h+1),2);
   if(h!==Math.floor(Math.log2(2*Math.max(n,m)+1))+1||v.length!==1+(3+3*m)*h)throw Error("bad header/length");
   let C=[],p=3*h+1;for(let i=0;i<m;i++){let c=[];
     for(let j=0;j<3;j++){let z=parseInt(v.slice(p,p+h),2);p+=h;let x=Math.floor(z/2)+1;if(x>n)throw Error("bad name");c.push(z%2?-x:x)}
     if(new Set(c.map(Math.abs)).size!==3)throw Error("not proper");C.push(c)}
   return {C,n}
 }
 function rd(C,n){let bits=pack(C,n),p=unpack(bits);
   ck(p.n===n&&JSON.stringify(p.C)===JSON.stringify(C),"serialization mismatch");S.roundtrips++;
   return {C:p.C,n:p.n,bits}
 }
 function sat(C){S.sat_calls++;
   function go(A){S.dpll_nodes++;A={...A};
     while(true){let live=[],units=[];
       for(let c of C){let yes=false,empty=[];for(let l of c){let x=Math.abs(l);
          if(x in A){if(A[x]===(l>0)){yes=true;break}}else empty.push(l)}
          if(yes)continue;if(!empty.length)return false;live.push(empty);
          if(empty.length===1)units.push(empty[0])}
       if(!live.length)return true;
       if(units.length){let change=false;
          for(let l of units){let x=Math.abs(l),val=l>0;if(x in A){if(A[x]!==val)return false}else{A[x]=val;change=true}}
          if(change)continue}
       let x=Math.abs(live[0][0]);return go({...A,[x]:false})||go({...A,[x]:true});
     }}
   return go({});
 }
 function contexts(b,n){let arr=[{name:"empty",C:[],n}],a=alloc(n);
    arr.push({name:"single_pin",C:pin(-1,a),n:a.n});a=alloc(n);
    arr.push({name:"padded_2SAT",C:or2(1,-2,a),n:a.n});a=alloc(n);
    let y=fresh(a);arr.push({name:"affine",C:[...xor(1,2,y),...pin(-y,a)],n:a.n});a=alloc(n);
    let v=[fresh(a),fresh(a),fresh(a)],C=[];
    for(let k=0;k<8;k++)C.push(v.map((x,i)=>(k>>(2-i)&1)?-x:x));
    arr.push({name:"private_unsat",C,n:a.n});a=alloc(n);
    C=[];for(let i=1;i<b;i++)C.push(...pin(-i,a));
    arr.push({name:"all_but_one",C,n:a.n});return arr;
 }
 function stage(b,n){let a=alloc(n),h=Math.ceil(b/2),z=[fresh(a)],one=[];
    one.push(...pin(-z[0],a));
    for(let i=0;i<h;i++){z.push(fresh(a));one.push(...xor(z[i],i+1,z[i+1]))}
    let n1=a.n,two=[];
    for(let i=h;i<b;i++){z.push(fresh(a));two.push(...xor(z[i],i+1,z[i+1]))}
    two.push(...pin(-z[b],a));return {one,two,n1,n2:a.n};
 }
 for(let b of [3,4,5,6]){
  let y=Array(b).fill(0),z=Array(b).fill(0);z[b-1]=1;
  let A=mod(b,y),B=mod(b,z),pA=rd(A.F,A.n),pB=rd(B.F,B.n);
  ck(pA.bits.length===pB.bits.length,"matched length");
  ck([...pA.bits].filter((v,i)=>v!==pB.bits[i]).length===2,"matched signs");
  ck(JSON.stringify(A.F.map(c=>c.map(Math.abs)))===JSON.stringify(B.F.map(c=>c.map(Math.abs))),"matched support");
  for(let [label,u,M] of [["SAT",y,A],["UNSAT",z,B]]){
   ck(M.n===4*b+10&&M.R.length===4*b+8&&M.Q.length===6*b+6,"module metadata");
   let root=rd(M.F,M.n);ck(sat(root.C)===(label==="SAT"),"root label");
   for(let H of contexts(b,M.n)){
      let names=new Set(H.C.flat().map(Math.abs).filter(x=>x<=b));
      ck(names.size<b,"name omitted");
      let expect=sat(H.C);
      for(let key of ["R","Q"]){ck(sat(rd([...M[key],...H.C],H.n).C)===expect,"visibility");S.visible_contexts++}}
   let H=stage(b,M.n),one=rd([...M.Q,...H.one],H.n1),two=rd([...one.C,...H.two],H.n2);
   ck(sat(one.C),"first child SAT");ck(sat(two.C)===(label==="SAT"),"second child exact");
   ck(two.bits.length>one.bits.length,"child size grows");
   S.stage_cases.push({b,label,root_N:root.bits.length,first_N:one.bits.length,second_N:two.bits.length,n0:M.n,n1:H.n1,n2:H.n2,m0:M.F.length,m1:one.C.length,m2:two.C.length});
   // Real, independently label-preserving two-level fallback.
   // FIRST: Q plus a complete fresh even-parity chain, hence parent-equivalent.
   // SECOND: append proper CNF equality linking original x1 to a new copy y.
   // Every new private auxiliary is disjoint from all source and previous IDs.
   let a=alloc(H.n2),yc=fresh(a),pa=fresh(a),qa=fresh(a);
   let eq=[[-1,yc,pa],[-1,yc,-pa],[1,-yc,qa],[1,-yc,-qa]];
   let valid2=rd([...two.C,...eq],a.n);
   ck(sat(valid2.C)===(label==="SAT"),"hereditary second label");
   ck(two.bits.length===root.bits.length,"first legitimate child equals root length");
   ck(valid2.bits.length>two.bits.length,"second legitimate child grows");
   S.label_preserving_twolevel.push({b,label,N_root:root.bits.length,
     N_child1:two.bits.length,N_child2:valid2.bits.length,
     n_child1:H.n2,n_child2:a.n,m_child1:two.C.length,m_child2:valid2.C.length,
     original_source_names_preserved:true});
   if(b<=4)for(let k=0;k<(1<<b);k++){let w=Array.from({length:b},(_,i)=>k>>i&1),a=alloc(M.n),P=[];
      for(let i=0;i<b;i++)P.push(...pin(w[i]?i+1:-(i+1),a));
      ck(sat(rd([...M.Q,...P],a.n).C)===(w.reduce((x,y)=>x^y,0)===1||w.every((x,i)=>x===u[i])),"complete pin");
      S.full_pin_queries++;
   }
  }
 }
 for(let b of [8,16,32,64,128]){let M=mod(b,Array(b).fill(0)),H=stage(b,M.n),
    n0=rd(M.F,M.n).bits.length,n1=rd([...M.Q,...H.one],H.n1).bits.length,
    n2=rd([...M.Q,...H.one,...H.two],H.n2).bits.length;
    ck(n2>n1,"asymptotic child growth");
    S.large_lengths.push({b,N0:n0,N1:n1,N2:n2,ratio:n2/n0})}
 let p=mod(3,[0,0,0]),bad=pack(p.F,p.n).slice(0,-1),rejected=false;
 try{unpack(bad)}catch(e){rejected=true}ck(rejected,"invalid header rejection");
 S.status="COMPUTATIONAL finite audit; symbolic restricted theorems independent-review pending";
 return S;
}
if(typeof module!=="undefined"&&typeof require!=="undefined"&&require.main===module)
 console.log(JSON.stringify(run(),null,2));
