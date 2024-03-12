<script lang="ts">
    import { createEventDispatcher, onMount } from "svelte";
    import { graphql } from "$houdini";
    import { Input } from "postcss";

    // export let symbol_list;
    // export let current_expiry;
    // export let isDefaultNifty = false;
    export let result = "";

    // if(isDefaultNifty)
    // {
    //     result = "NIFTY";
    // }

    // onMount(()=>{})
    let searched = "";

    const dispatch = createEventDispatcher();
    const store = graphql(`
        query Getsymbol($symbol_name: String!) {
            fut_expiry(
                distinct_on: symbol
                where: { symbol: { _ilike: $symbol_name } }
                limit: 7
            ) {
                symbol
            }
        }
    `);

    export const _GetsymbolVariables = () => {
        if (searched == result || searched == "") {
            return { symbol_name: searched };
        } else {
            return { symbol_name: searched + "%" };
        }
    };

    // if (searched == ""){

    // }

    export const symbol_search = () => {
        store.fetch({ variables: _GetsymbolVariables() });
    };

    onMount(() => {
        let mydiv = document.getElementById("drop1");

        let myinput = document.getElementById("myinput");
        myinput.addEventListener("focus", () => {
            mydiv.style.display = "block";
            console.log("cll");
        });

        myinput.addEventListener("keyup", (event) => {
            if (event.key === "Backspace" && searched == "" && result != "") {
                console.log("event call");

                clearSearch(searched);
            }
        });

        // filter_date();
    });

    // if( searched == ""){
    //     clearSearch("")
    // }
    function clearSearch(selected) {
        result = selected;
        // current_symbol = selected;
        console.log(selected);
        dispatch("addSearchField");
        store.data = [];
        let mydiv = document.getElementById("drop1");
        if (selected != "") {
            mydiv.style.display = "none";
        }
        // searched = "";
        symbol_search();
        searched = result;
    }

    // let mydiv = document.getElementById("drop1")
    // let myinput = document.getElementById("myinput")
</script>

<!-- <div class="d-flex"> -->

<!-- Search box Implimentation -->

<div>
    <label class="my-2" style="color:azure">Symbol</label>
    <div class="input-group">
        <input
            class="inp-bg-color rounded-left-2 form-control"
            type="search"
            placeholder="search"
            id="myinput"
            bind:value={searched}
            on:input={symbol_search}
        />
        <!-- <button on:click={clearSearch("")}> -->

        <span class="input-group-append">
            <div class="btn border-left-0 myborder">
                <i class="fa fa-search" style="color:#ced4da" />
            </div>
        </span>
    </div>

    <div
        id="drop1"
        style="display: none ; position:absolute; z-index: 99; width: 200px"
    >
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
    .myborder {
        border: 1px solid #ced4da;
        border-left-style: none;
        border-bottom-left-radius: 0;
        border-top-left-radius: 0;
    }

    #myinput {
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
        border-right-style: none;
        background-color: transparent;
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
