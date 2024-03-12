<script lang="ts">
    import { createEventDispatcher } from "svelte";
    export let expiry_list;
    export let date;
    const dispatch = createEventDispatcher();
    let nif_exp=[];  



    // let today = new Date();
    // let nextTwoMonths = new Date(new Date().getFullYear(), new Date().getMonth() + 3, 1);
    // console.log("in the expiry", expiry_list);

    let unique_expiry = [];
    expiry_list.forEach((item) => {
        if (!unique_expiry.includes(item.expiry)) {
            unique_expiry.push(item.expiry);
            
        }
        if (item.symbol == "NIFTY"){ 
                nif_exp.push(item.expiry)
            }
    });

    // console.log(nif_exp);
    
    date = nif_exp[0];
    const expiry_change = () => {
        dispatch("addExpiryDate");
    };

    // onMount(() => {
    //     dispatch("addExpiryDate");
    // });

    // console.log("this is ok", unique_expiry);
</script>

<!-- {#if unique_expiry != []} -->

<div class="mx-3">
    <label class="mt-2" for="expiryDate" style="color:azure">Expiry Date</label>
    <select
        id="expiryDate"
        name="expiryDate"
        class="form-select data-pick mt-2"
        style="background-color: black; color: white;"
        bind:value={date}
        on:change={expiry_change}
    >
        <option value={unique_expiry[0]} selected >
            {unique_expiry[0]}
        </option>
        {#each unique_expiry.slice(1) as expiry_date}
            <option value={expiry_date}>{expiry_date}</option>
        {/each}
    </select>
</div>

<!-- {/if} -->

<!-- <h1>{unique_expiry[0].expiry}</h1> -->
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
</style>
