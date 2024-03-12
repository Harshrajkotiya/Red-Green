

/** @type {import('./$types').PageServerLoad} */

export async function load({params}) {
  let response = await fetch("https://empty-paper-1552.fly.dev/operations/nifty50");
  let mydata = await response.json();
  mydata = mydata.data.nse_nifty50.data
  const res = mydata.find(x => x.symbol == params.id);
  return res;
}








