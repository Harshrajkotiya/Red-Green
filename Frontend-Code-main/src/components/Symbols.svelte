<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import { graphql } from "$houdini";
    export let result = "NIFTY";

    let searched = "";

    const dispatch = createEventDispatcher();
    // const store = graphql(`
    //     query GetAllFuturesAtComponentsymbol($symbol_name: String!) {
    //         future_expiry(
    //             distinct_on: name
    //             where: { name: { _ilike: $symbol_name } }
    //         ) {
    //             name
    //         }
    //     }
    // `);

    export const _GetAllFuturesAtComponentsymbolVariables = () => {
        if (searched == "") {
            return { symbol_name: searched };
        } else {
            return { symbol_name: searched + "%" };
        }
    };

    export const symbol_search = () => {
        store.fetch({ variables: _GetAllFuturesAtComponentsymbolVariables() });
    };

    function clearSearch(selected: string) {
        result = selected;
        dispatch("addSearchField");
        store.data = [];
        searched = "";
        symbol_search();
    }
</script>

<div class="mx-2">
    <!-- Search box Implimentation -->
    <div>
        <label class="my-2" style="color:azure">Symbol</label>
        <div class="row">
            <div class="input-group">
                <input
                    class="inp-bg-color rounded-left-2 form-control"
                    data-bs-toggle="collapse"
                    href="#collapse"
                    aria-expanded="false"
                    aria-controls="collapseExample"
                    type="search"
                    placeholder={result}
                    id="myInput"
                    bind:value={searched}
                    on:input={symbol_search}
                />
            </div>
        </div>

        <div
            class="collapse"
            id="collapse"
            style="position:absolute; z-index: 99; width: 200px"
        >
            {#if $store.data?.future_expiry?.length > 0}
                <ul class="searchul" id="searchul">
                    {#each $store?.data?.future_expiry as item}
                        <div on:click={clearSearch(item.name)}>
                            <li class="searchli my-2 p-2 me-2">
                                {item.name}
                            </li>
                        </div>
                    {/each}
                </ul>
            {/if}
        </div>
    </div>
</div>

<style>
    .data-pick {
        max-width: 200px;
        width: 200px;
        font-size: small;
        min-width: 150px;
        background-color: var(--bg-dark);
        color: white;
        height: 35px;
    }
    :root {
        --font-color: white;
        --bg-dark: #141822;
    }

    #myInput {
        /* background-position: 10px 12px;
		background-repeat: no-repeat;
		width: 100%;
		font-size: 16px;
		padding: 12px 20px 12px 40px;
		border: 1px solid #ddd;
		margin-bottom: 12px; */
        /* color:#1e1f4b; */
        font-weight: 400;
        font-size: 14px;
        line-height: 24px;
        font-family: "Inter senserif";
    }
    .data-pick {
        max-width: 200px;
        width: 200px;
        font-size: small;
        min-width: 150px;
        background-color: black;
        color: white;
        height: 35px;
    }
    .inp-bg-color {
        background: var(--bg-dark);
        color: var(--font-color);
    }

    #searchul {
        list-style-type: none;
        padding: 0;
        margin: 0;
        display: block;
        padding: 4px 0px 4px 8px;
        height: auto;
        background: var(--bg-dark);
        box-shadow: 0px 15px 6px rgba(0, 0, 0, 0.01),
            0px 8px 5px rgba(0, 0, 0, 0.05), 0px 4px 4px rgba(0, 0, 0, 0.09),
            0px 1px 2px rgba(0, 0, 0, 0.1), 0px 0px 0px rgba(0, 0, 0, 0.1);
        border-radius: 6px;
    }
    .searchul li {
        color: var(--font-color);
        list-style-type: none;

        height: auto;
        font-weight: 600;
    }
    .searchul a {
        text-decoration: none;
        color: var(--font-color);
    }

    .searchul span {
        color: var(--font-color);
        font-size: 12px;
        font-weight: 300;
    }

    .searchul div:hover {
        background-color: #141822;
        border-left: 3px solid #02373e;
        border-radius: 5px;
    }
</style>
