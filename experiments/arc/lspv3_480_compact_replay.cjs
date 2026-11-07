'use strict';
// LSPV3/480: finite direct enumeration, independently of /341 native checker.
let cases=0,affine=0,projections=0,bad=0;
const assert=(x,m)=>{if(!x)throw Error(m)};
const pop=x=>{let s=0;while(x){x&=x-1;s++}return s};
function audit(n,k,sign,branch){
  let fixed=0,ones=0,b=branch;
  for(let j=0;j<k;j++){let t=b%3;b=(b-t)/3;if(t){fixed|=1<<j;if(t===2)ones|=1<<j}}
  let sat=[],hit=false,r=0;
  for(let j=0;j<k;j++){
    if(!(fixed&(1<<j)))r++;
    else if(((ones>>j)&1)===((sign>>j)&1))hit=true;
  }
  let mode=hit?'TAUTOLOGY':r===0?'EMPTY':'RESIDUAL';
  for(let x=0;x<(1<<n);x++){
    if((x&fixed)!==ones)continue;
    let yes=false;for(let j=0;j<k;j++)if(((x>>j)&1)===((sign>>j)&1)){yes=true;break}
    if(yes)sat.push(x);
  }
  if(mode==='RESIDUAL'&&r>=2){
    for(let mask=1;mask<(1<<n);mask++){
      if(mask&fixed)continue;
      let seen=0;for(const x of sat)seen|=1<<((pop(x&mask))%2);
      assert(seen===3,'false original affine rule');affine++;
    }
  }
  if(mode==='RESIDUAL'&&r>=4){
    for(let mask=0;mask<(1<<n);mask++){
      if((mask&fixed)||pop(mask)>3)continue;
      const set=new Set(sat.map(x=>x&mask));
      assert(set.size===2**pop(mask),'false local projection');projections++;
    }
  }
  return mode;
}
const modes={RESIDUAL:0,TAUTOLOGY:0,EMPTY:0};
for(let n=2;n<=5;n++)for(let k=2;k<=n;k++)for(let sign=0;sign<(1<<k);sign++)for(let branch=0;branch<3**k;branch++){
  modes[audit(n,k,sign,branch)]++;cases++;
}
assert(cases===11160&&modes.RESIDUAL===1688&&modes.TAUTOLOGY===9368&&modes.EMPTY===104,'controls');
assert(affine===10944&&projections===3888,'independent control counts');
const x=0b0010;assert(((x&15)!==0)&&((x&1)===0),'OR4 does not imply x1');
const y=0b11;assert((y!==0)&&pop(y)%2===0,'OR2 not XOR parity');
console.log(JSON.stringify({cases,affine,projections,modes,negative_controls:2,status:'PASS: restricted OR-locality theorem controls; historical checker NOT executed'},null,2));
