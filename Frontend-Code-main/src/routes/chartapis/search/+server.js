/** @type {import('./$types').RequestHandler} */
export async function GET({ request,url }) {
    const query = url.searchParams.get('query')
    const limit = url.searchParams.get('limit')
    const type = url.searchParams.get('type')
  return new Response(JSON.stringify({"query":query,"limit":limit,"type":type}));
}
