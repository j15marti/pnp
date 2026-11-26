function run(){
  let assertions=0, graphs=0, queries=0, yes=0, no=0, mutations=0, pairs=0, maxN=0;
  const assert=x=>{assertions++;if(!x)throw Error("failed "+assertions)};
  const b=n=>n.toString(2), frame=x=>"1".repeat(x.length)+"0"+x;
  function encode(rows,t,N){let p=frame(rows.map(r=>r.map(z=>frame(b(z))).join("")).join(""))+frame("")+frame(b(t));if(N!==undefined){assert(p.length<=N);p+="0".repeat(N-p.length)}return p}
  function decode(w){let p=0;function get(s,j){let z=j;while(s[z]==="1")z++;if(s[z]!=="0"||2*z+1-j>s.length)throw Error("frame");return[s.slice(z+1,2*z+1-j),2*z+1-j]}let a,x,t;[a,p]=get(w,p);[x,p]=get(w,p);[t,p]=get(w,p);assert(x===""&&/^0*$/.test(w.slice(p))&&/^(0|1[01]*)$/.test(t));let rows=[],j=0;while(j<a.length){let r=[];for(let i=0;i<8;i++){let y;[y,j]=get(a,j);assert(/^(0|1[01]*)$/.test(y));r.push(parseInt(y,2))}assert(r[0]!==1&&r[1]===0&&r[2]===0&&r[4]===0&&r[5]===0&&r[6]===2&&r[7]===2);rows.push(r)}let T=parseInt(t,2);assert(BigInt(T)<=BigInt(w.length)**2n);return{rows,T}}
  function reach(A,T){let n=A.length,R=Array.from({length:T+1},()=>Array.from({length:n},()=>Array(n).fill(false)));for(let u=0;u<n;u++)R[0][u][u]=true;for(let t=1;t<=T;t++)for(let u=0;u<n;u++)for(let v=0;v<n;v++)R[t][u][v]=R[t-1][u][v]||A[u].some((e,z)=>e&&R[t-1][z][v]);return R}
  function verify(A,R,W,mode){let n=A.length;for(let t=0;t<R.length;t++)for(let u=0;u<n;u++)for(let v=0;v<n;v++){let val=R[t][u][v];if(t<=1){let base=u===v||(t===1&&A[u][v]);if((mode!== "upper"&&val&&!base)||(mode!=="lower"&&!val&&base))return false;continue}let l=Math.floor(t/2),r=t-l;if(mode!=="upper"&&val){let z=W[t][u][v];if(!(z>=0&&z<n&&R[l][u][z]&&R[r][z][v]))return false}if(mode!=="lower"&&!val){for(let z=0;z<n;z++)if(R[l][u][z]&&R[r][z][v])return false}}return true}
  for(let mask=0;mask<512;mask++){
    let n=3,A=Array.from({length:n},(_,u)=>Array.from({length:n},(_,v)=>!!(mask&(1<<(3*u+v))))),R=reach(A,5);
    let W=R.map((mat,t)=>mat.map((row,u)=>row.map((val,v)=>t<2||!val?-1:Array.from({length:n},(_,z)=>z).find(z=>R[Math.floor(t/2)][u][z]&&R[t-Math.floor(t/2)][z][v]))));
    for(let mode of ["lower","upper","both"])assert(verify(A,R,W,mode));
    for(let t=0;t<6;t++)for(let u=0;u<n;u++)for(let v=0;v<n;v++){queries++;if(R[t][u][v])yes++;else no++;R[t][u][v]=!R[t][u][v];assert(!verify(A,R,W,"both"));mutations++;R[t][u][v]=!R[t][u][v]}
    graphs++;
    if(!A[1].some(Boolean)){
      let rows=[];for(let u of [0,2])for(let v=0;v<3;v++)if(A[u][v])rows.push([u,0,0,v,0,0,2,2]);
      let d=R.findIndex(mat=>mat[0][1]);if(d>0){let w0=encode(rows,d),w1=encode(rows,d-1,w0.length),p0=decode(w0),p1=decode(w1);assert(w0.length===w1.length);
        const sim=({rows,T})=>{let st=new Set([0]);for(let j=0;j<T&&!st.has(1);j++){let next=new Set();for(let r of rows)if(st.has(r[0]))next.add(r[3]);st=next}return st.has(1)};
        assert(sim(p0)&&!sim(p1));pairs++;maxN=Math.max(maxN,w0.length);
      }
    }
  }
  return {assertions,graphs,queries,yes,no,mutations,pairs,maxN,scope:"finite table verifier; not circuit-to-CNF compiler or production SAT evaluator"};
}
console.log(JSON.stringify(run(),null,2));
