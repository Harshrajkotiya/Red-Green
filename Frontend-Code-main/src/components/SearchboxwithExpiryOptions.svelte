<script lang="ts">
    import { createEventDispatcher, onMount } from "svelte";
    import { graphql } from "$houdini";

    export let current_expiry;
    export let result = "NIFTY";
    let selectedExpiry = "";
    let variables = { symbol_name: result };
    let searched = "";

    // console.log("hello");
    
    const dispatch = createEventDispatcher();
    const store = graphql(`
        query GetAlsymbol1($symbol_name: String!) {
            fut_expiry(
                distinct_on: symbol
                where: { symbol: { _ilike: $symbol_name } }
                limit: 7
            ) {
                symbol
            }
        }
    `);

    const getExpriDateBySymbol = graphql(`
        query getExpriDateBySymbol($symbol_name: String!) {
            opt_expiry(
                distinct_on: [expiry, symbol]
                where: { symbol: { _ilike: $symbol_name } }
            ) {
                symbol
                expiry
            }
        }
    `);

    export const _GetAlsymbol1Variables = () => {
        if (searched == "") {
            return { symbol_name: searched };
        } else {
            return { symbol_name: searched + "%" };
        }
    };

    export const symbol_search = () => {
        store.fetch({ variables: _GetAlsymbol1Variables() });
    };

    async function filter_date() {
        current_expiry = await $getExpriDateBySymbol?.data?.opt_expiry[0].expiry;
        dispatch("addSearchField");
    }

    onMount(async () => {
        await getExpriDateBySymbol.fetch({ variables });
        filter_date();
    });

    async function clearSearch(selected) {
        result = selected;
        filter_date();
        variables["symbol_name"] = result;
        await getExpriDateBySymbol.fetch({ variables });
        selectedExpiry;
        dispatch("addSearchField");
        store.data = [];
        searched = "";
        symbol_search();
        current_expiry = $getExpriDateBySymbol?.data?.opt_expiry[0].expiry;
    }

    const expiry_change = () => {
        dispatch("addSearchField");
    };
</script>

<!-- <div class="d-flex"> -->

<!-- Search box Implimentation -->

<div>
    <label class="my-2" style="color:azure">Symbol</label>
    <div class="row">
        <div class="input-group">
            <input
                class="inp-bg-color rounded-left-2 form-control"
                type="search"
                placeholder={result}
                id="myInput"
                bind:value={searched}
                on:input={symbol_search}
            />
        </div>
    </div>

    <div style="position:absolute; z-index: 99; width: 200px">
        {#if $store.data?.fut_expiry?.length > 0}
            <ul class="searchul" id="searchul">
                {#each $store?.data?.fut_expiry as item}
                    <div on:click={clearSearch(item.symbol)}>
                        <li class="searchli my-2 p-2 me-2">
                            {item.symbol}
                        </li>
                    </div>
                {/each}
            </ul>
        {/if}
    </div>
</div>

<!-- Expiry Dropdown -->

<div class="mx-4">
    <!-- svelte-ignore a11y-label-has-associated-control -->
    <label class="mt-2" style="color:azure;">Expiry Date</label>
    <select
        name="Symbol"
        class="form-select data-pick mt-2"
        style="background-color: black; color: white;"
        bind:value={current_expiry}
        on:change={expiry_change}
    >
        {#if $getExpriDateBySymbol?.data?.opt_expiry}
            {#each $getExpriDateBySymbol?.data?.opt_expiry as item }
                <option value={item.expiry}>{item.expiry}</option>
            {/each}
        {/if}
    </select>
</div>

<!-- </div> -->
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
