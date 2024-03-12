import { type RequestHandler, type ConstructorArgs, subscription } from "$houdini";
import { HoudiniClient } from "$houdini";
import { createClient as createWSClient } from "graphql-ws";

// For Query & Mutation
// async function fetchQuery({ fetch, text = "", variables = {} }: RequestHandler): Promise<any> {
//   const result = await fetch("https://hasura.derivedged.com/v1/graphql", {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/json",
//       "x-hasura-admin-secret": "R3cov3R*75"
//     },
//     body: JSON.stringify({
//       query: text,
//       variables,
//     }),
//   });
//   return await result.json();
// }

// Export the Houdini client
const client = new HoudiniClient({
  url: "https://hasura.derivedged.com/v1/graphql",
  // fetchQuery,
  fetchParams: (operation) => ({
    method: 'POST',
    headers: {
      "Content-Type": "application/json",
      "x-hasura-admin-secret": "R3cov3R*75",
    },
    body: JSON.stringify({
      query: operation.text,
      variables: operation.variables,
    }),
  }),
  plugins: [
    subscription(() =>
      createWSClient({
        url: "wss://hasura.derivedged.com/v1/graphql",
        connectionParams: {
          headers: {
            "Content-Type": "application/json",
            "x-hasura-admin-secret": "R3cov3R*75",
          },
        },
      })
    ),
  ],
} as ConstructorArgs);

export default client;