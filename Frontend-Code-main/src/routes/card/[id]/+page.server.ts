/** @type {import('./$types').PageServerLoad} */
export async function load({ params }) {
	const url = `https://www.nseindia.com/api/equity-stockIndices?index=${params.id}`;

	const res = await fetch(url);
	const results = await res.json();
	debugger;
	console.log('results', results);

	if (res.ok) {
		return {
			index: results
		};
	}

	return {
		status: 404,
		body: { error: 'Can not fetch recepies.' }
	};
}
