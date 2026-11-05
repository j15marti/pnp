// LSPV-1/427: finite parameter/encoding and output-growth scope checks.
// No execution of Braun's theorem, Cook's ER proof, or native R_mix341 verifier.
let checks=0;
const test=(assert,msg)=>{if(!assert)throw Error(msg);checks++};
const rows=[];
for(const ell of [1,2,3,4]){
 const n=2**ell,p=n+1,M=n*p*(p-1)/2;
 const m3=M*(2*ell-2||1);
 const vars=p*ell+M*Math.max(0,2*ell-3);
 const expectedRecovery=M*Math.max(0,2*ell-3);
 test(M===n*n*(n+1)/2,'pair count');
 test(m3>=M,'nonnegative chain');
 test(vars>=p*ell,'variable count');
 if(ell===2)test(M===40 && m3===80 && vars===50 && expectedRecovery===40,'ell2');
 if(ell===3)test(M===288 && m3===1152 && vars===891 && expectedRecovery===864,'ell3');
 rows.push({ell,holes:n,bitPHPClauses:M,chainFacets:m3,exactWidthThree:ell>=2,totalVariables:vars,strictRESRecoveryNodes:expectedRecovery});
}
// For arbitrary fixed polynomial exponent K, log L / (K log N) grows to infinity.
const K=10;
const ratios=[32,64,128,256].map(ell=>({ell,ratio:Number(2n**BigInt(ell))/(131072*K*ell**3)}));
for(let j=1;j<ratios.length;j++)test(ratios[j].ratio>ratios[j-1].ratio,'ratio must rise');
console.log(JSON.stringify({status:'PASS',status_scope:'finite arithmetic only, no theorem or native-byte verification',checks,rows,ratios},null,2));
