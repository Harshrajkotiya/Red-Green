<script lang="ts">
    import { createEventDispatcher, onMount } from "svelte";
    import { graphql } from "$houdini";

    export let symbol_list;
    export let current_expiry;
    // export let isDefaultNifty = false;
    export let result = "NIFTY";

    // if(isDefaultNifty)
    // {
    //     result = "NIFTY";
    // }

    let unique_expiry = [];

    let searched = "";

    const dispatch = createEventDispatcher();
    const store = graphql(`
        query GetAlsymbol($symbol_name: String!) {
            fut_expiry(
                distinct_on: symbol
                where: { symbol: { _ilike: $symbol_name } }
                limit: 7
            ) {
                symbol
            }
        }
    `);

    export const _GetAlsymbolVariables = () => {
        if (searched == "") {
            return { symbol_name: searched };
        } else {
            return { symbol_name: searched + "%" };
        }
    };

    export const symbol_search = () => {
        store.fetch({ variables: _GetAlsymbolVariables() });
    };

    let today = new Date();
    let nextTwoMonths = new Date(
        new Date().getFullYear(),
        new Date().getMonth() + 3,
        1
    );

    async function filter_date() {
        unique_expiry = [];
        symbol_list.forEach((item) => {
            if (item.symbol == result) {
                unique_expiry.push(item.expiry);
            }
        });

        current_expiry = unique_expiry[0];
        // console.log(current_expiry);
        if (result != "") {
            dispatch("addSearchField");
        }
    }

    onMount(() => filter_date());

    function clearSearch(selected) {
        result = selected;
        // current_symbol = selected;
        filter_date();
        // console.log("call");

        dispatch("addSearchField");
        store.data = [];
        searched = "";
        symbol_search();
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
        <option value={unique_expiry[0]} selected> {unique_expiry[0]} </option>
        {#each unique_expiry.slice(1) as expiry}
            <option value={expiry}>{expiry}</option>
        {/each}
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
