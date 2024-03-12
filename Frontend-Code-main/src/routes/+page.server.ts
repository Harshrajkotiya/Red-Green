// /** @type {import('./$types').PageServerLoad} */
// export async function load() {
// 	const url = "https://empty-paper-1552.fly.dev/operations/indices"

// 	const res = await fetch(url);
// 	const data = await res.json();
	
// 	if (res.ok) {
// 		return {
// 			cardData: data.data.nse_allindices.data

// 		};
// 	}

// 	return {
// 		status: 404,
// 		body: { error: 'Can not fetch recepies.' }
// 	};
// }
