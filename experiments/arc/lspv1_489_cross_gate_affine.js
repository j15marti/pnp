'use strict';
// Independent AND affine cross-coupling exhaustive verifier; NOT a native R_mix341 checker.
const run=function(){
  'use strict';
  const pop32=v=>{v-=((v>>>1)&0x55555555);v=(v&0x33333333)+((v>>>2)&0x33333333);return Math.imul((v+(v>>>4))&0x0f0f0f0f,0x01010101)>>>24;};
  const results=[];
  for(let g=1;g<=3;g++){
    const n=2*g, nf=1<<(n+1), mask=Array.from({length:g},()=>Array(nf));
    for(let i=0;i<g;i++)for(let a=0;a<nf;a++){
      let lo=0,hi=0;
      for(let x=0;x<(1<<n);x++){
        let z=(a>>>1)&x, parity=0;while(z){parity^=1;z&=z-1;}
        const predicted=(a&1)^parity, actual=((x>>>(2*i))&1)&((x>>>(2*i+1))&1);
        if(predicted===actual){if(x<32)lo|=(1<<x);else hi|=(1<<(x-32));}
      }
      mask[i][a]=[lo>>>0,hi>>>0];
    }
    const cross=arr=>arr.some((a,i)=>arr.some((b,j)=>i!==j&&(((a>>>1)&(3<<(2*j)))!==0)));
    let max=0,nmax=0,cmax=0,ncmax=0,example=null;
    function visit(a){
      let lo=0xffffffff,hi=0xffffffff;
      for(let i=0;i<g;i++){lo&=mask[i][a[i]][0];hi&=mask[i][a[i]][1];}
      const cnt=pop32(lo)+pop32(hi),bad=cross(a);
      if(cnt>max){max=cnt;nmax=1;}else if(cnt===max)nmax++;
      if(bad){if(cnt>cmax){cmax=cnt;ncmax=1;example=a.slice();}else if(cnt===cmax)ncmax++;}
    }
    if(g===1)for(let a=0;a<nf;a++)visit([a]);
    if(g===2)for(let a=0;a<nf;a++)for(let b=0;b<nf;b++)visit([a,b]);
    if(g===3)for(let a=0;a<nf;a++)for(let b=0;b<nf;b++)for(let c=0;c<nf;c++)visit([a,b,c]);
    if(max!==3**g||nmax!==4**g|| (g>=2 && cmax!==7*3**(g-2)))throw Error("theorem controls failed g="+g);
    results.push({g,affine_maps:nf**g,max_agreement:max,number_of_maximizers:nmax,cross_coupled_max:g>=2?cmax:null,cross_maximizers:g>=2?ncmax:null,cross_witness:example});
  }
  let small=0;
  for(let x=0;x<16;x++){const u=x&1,v=(x>>>1)&1,s=(x>>>2)&1,t=(x>>>3)&1;if((u&v)===0&&(s&t)===u)small++;}
  if(small!==7)throw Error("seven assignment witness falsified");
  // Adversarial controls check that the implausibly strong candidate claims are rejected.
  const rejected=[results[1].cross_coupled_max<8, results[2].cross_coupled_max<27,
     results[2].number_of_maximizers===64,small===7];
  if(!rejected.every(Boolean))throw Error("negative control failed");
  return {title:"LSPV1_489_CROSS_AFFINE_PENALTY",status:"COMPUTATIONAL finite exhaustive g=1,2,3; asymptotic proof in report; not R_mix341",
     semantics:"Boolean independent AND gate outputs vs arbitrary affine vector predictors over all 2g original inputs",
     results,explicit_witness:{g:2,A1:"0",A2:"u1",agreeing_inputs:7},
     rejected_false_claims:["cross-coupled g2 can agree on >=8","cross-coupled g3 can attain 27","some cross-coupled map globally maximizes"],verifier:"Standalone JS g<=3, complete enumeration"};
};
if(typeof module!=='undefined'&&require.main===module)console.log(JSON.stringify(run(),null,2));
if(typeof module!=='undefined')module.exports=run;
