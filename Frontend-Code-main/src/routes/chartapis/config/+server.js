import { json } from '@sveltejs/kit';
 
/** @type {import('./$types').RequestHandler} */
export async function GET({ request }) {
  return new Response(JSON.stringify({
    supported_resolutions: ['1', '5', '15', '30', '60', '1D', '1W', '1M'],
    supports_group_request: false,
    supports_marks: false,
    supports_search: true,
    supports_timescale_marks: false,
}))
}