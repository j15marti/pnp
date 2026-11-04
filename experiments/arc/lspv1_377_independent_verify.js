"use strict";
// Self-contained, deterministic exhaustive verifier; Node.js 18+
const result = (function independent(){
  "use strict";
  let assertions=0;
  function check(x,s){assertions++;if(!x)throw Error("independent "+s);}
  function other(bits){
    if(!/^1[01]{2}/.test(bits))return "M";
    let tail=bits.substring(1),c=Number.parseInt(tail.substring(0,2),2);
    tail=tail.substring(2);
    const data=[];
    for(let j=0;j<c;j++){
      if(tail.length<2)return "M";
      const size=Number.parseInt(tail.substring(0,2),2);
      tail=tail.substring(2);
      if(tail.length<2*size)return "M";
      let cs=[];
      for(let k=0;k<size;k++){
        let pair=tail.substring(2*k,2*k+2);
        cs.push({variable:pair[0]==="0"?1:2,negated:pair[1]==="1"});
      }
      tail=tail.substring(2*size);
      data.push(cs);
    }
    if(tail.length)return "M";
    const assignment=[false,false,false];
    for(let a=0;a<2;a++)for(let b=0;b<2;b++){
      assignment[1]=a===1;assignment[2]=b===1;
      const success=data.every(clause=>clause.some(lit=>assignment[lit.variable]!==lit.negated));
      if(success)return "S";
    }
    return "U";
  }
  const truth={3:[1,0,14],5:[1,1,61],7:[5,2,248],9:[21,11,991],11:[97,59,3939],13:[217,291,15875]};
  let results=[];
  for(let N of Object.keys(truth).map(Number)){
    const tally=[0,0,0];
    for(let i=0;i<=N;i++)for(let k=0;k<(1<<i);k++){
      let s=i?k.toString(2).padStart(i,"0"):"";
      let label=other(s),index={S:0,U:1,M:2}[label];
      check(Number.isInteger(index),`partition ${s}`);
      tally[index]++;
    }
    for(let j=0;j<3;j++)check(tally[j]===truth[N][j],`count ${N} ${j}`);
    results.push({N,S:tally[0],U:tally[1],M:tally[2]});
  }
  // A separate parity-count check on K4 using explicit GF(2) incidence masks.
  const rows=[0b000111,0b011001,0b101010,0b110100];
  for(const [b,answer] of [[0,8],[1,0]]){
    let count=0;
    for(let a=0;a<64;a++){
      let ok=true;
      for(let i=0;i<4;i++){
        let z=a&rows[i];z^=z>>>3;z^=z>>>2;z^=z>>>1;
        if((z&1)!==(i===0?b:0)){ok=false;break;}
      }
      if(ok)count++;
    }
    check(count===answer,`K4 parity charge ${b}`);
  }
  check(other("100")==="S","empty formula");
  check(other("10100")==="U","empty clause");
  check(other("11001000101")==="U","signed opposing literals");
  check(other("11001000100")==="S","same-sign literals");
  check(other("1010")==="M","truncated clause");
  check(other("1000")==="M","bad suffix");
  return {kind:"independent parser with truth evaluation by explicit Boolean assignment",results,assertions,parity:"passed 8/0 K4"};
})();
console.log(JSON.stringify(result,null,2));
