/// <references types="houdini-svelte">

/** @type {import('houdini').ConfigFile} */
const config = {
    watchSchema: {
		url: "https://hasura.derivedged.com/v1/graphql",
		headers: {
			"x-hasura-admin-secret": "R3cov3R*75"
		}
	},
    "plugins": {
        "houdini-svelte": {
        }
    },
  
    scalars: {
        // the name of the scalar we are configuring
        DateTime: {
            // the corresponding typescript type
            type: 'Date',
            // turn the api's response into that type
            unmarshal(val) {
                return new Date(val)
            },
            // turn the value into something the API can use
            marshal(date) {
                return date.getTime()
            }
        }
    }
}

export default config