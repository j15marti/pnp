"use strict";
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){let x=a%b;a=b;b=x}return a}
class Q{constructor(a,b=1n){a=BigInt(a);b=BigInt(b);if(!b)throw Error("den");if(b<0n){a=-a;b=-b}const g=gcd(a,b);this.a=a/g;this.b=b/g;}
add(o){return new Q(this.a*o.b+o.a*this.b,this.b*o.b)}
sub(o){return new Q(this.a*o.b-o.a*this.b,this.b*o.b)}
mul(o){return new Q(this.a*o.a,this.b*o.b)}
div(o){return new Q(this.a*o.b,this.b*o.a)}
lt(o){return this.a*o.b<o.a*this.b}
str(){return this.a+"/"+this.b}}
const one=new Q(1),zero=new Q(0);
function runSingle(ca,cb){
 let c=new Q(ca,cb),f=one,power=one,best=zero,bestK=0,vals=[];
 for(let k=1;k<=200;k++){
  f=c.mul(f).div(one.add(f));
  power=power.div(c);
  let term=one.div(f).sub(c).div(new Q(k)), d=term.lt(power)?term:power;
  if(best.lt(d)){best=d;bestK=k}
  vals.push({k,f:f.str(),d:d.str(),power:power.str()});
  // Future j >= k+1 satisfy d_j <= c^-j <= c^-(k+1).
  const tail=power.div(c);
  if(best.a>0n&&tail.lt(best)){
   return {c:c.str(),d_star:best.str(),best_k:bestK,
      terms:vals,certified_all_future_k_at_least:k+1,tail_upper:tail.str(),
      strict_space_test_half:new Q(1,2).lt(best)};
  }
 }
 throw Error("missing tail");
}
function run(){return [ [6,5],[241,200],[7,5],[3,2],[8,5] ].map(x=>runSingle(...x))}
if(typeof require!=="undefined"&&require.main===module)process.stdout.write(JSON.stringify(run(),null,2)+"\n");
