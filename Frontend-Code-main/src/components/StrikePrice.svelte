<script>
  // Importing The Required Packages....
  import { graphql } from "$houdini";
  import { createEventDispatcher, onMount } from "svelte";

  export let stock_obj;
  let selected_strike;
  export let strike_status;
  let variables = {}

  console.log("strike price ",stock_obj);
  const dispatch = createEventDispatcher();

  // Graphql Query...
  const strike = graphql(`
    query Getstrikeprice($symbol: String!, $expiry: date!) 
    {
      pre_2_day_minute_data(
        distinct_on: strike_price
          where: { symbol: { _eq: $symbol }, expiry: { _eq: $expiry } }
        ) {
          strike_price
        }
    }
  `);

    //create function for make variable object
    export const _GetstrikepriceVariables =  () => {
      console.log("inside variable");
      return {symbol: stock_obj.symbol ,expiry: stock_obj.date_expiry};
    };

    
    // Fetcing The Data From Database...
    export const fetch_date = async () => {
        // console.log("fetch date trigger");
        // console.log("The Variable Are Here :- ", stock_obj.symbol);
        variables.symbol = stock_obj.symbol;
        variables.expiry = stock_obj.date_expiry;
        // console.log("passing var", _GetstrikepriceVariables());
        $: strike.fetch({variables});
      
      // selected_strike = await $strike?.data?.last_week_minute_data[0].strike_price;
    };


    const change_obj = async () => {
      await fetch_date()
      // selected_strike = await $strike?.data?.last_week_minute_data[1].strike_price;
    }

    // Updating The Stricke Price When the Symbol And Expiry Date Change...
    const change_strike = async () => {
      dispatch("addstrikeprice");
      fetch_date()
      // selected_strike = await $strike.data.last_week_minute_data[0].strike_price;
    };
  
    // Calling Mounting Function...
    // onMount( () => {
    //   // if(!Object.values(stock_obj))
    //     // console.log("In Fetch Data...", stock_obj)
    //     // fetch_date();
    //   });
      $: stock_obj, change_obj()
      
</script>

<div class="col-md-1">
  <!-- {selected_strike=$strike.data.master_data[0].strike} -->
  <label class="text-white m-2"> {strike_status}</label>
  {#if $strike?.data?.last_week_minute_data}
    <select
      name="Strike Price"
      class="form-select data-pick text-white"
      style="background-color: black; border-color: #4f5159"
      bind:value={selected_strike}
      on:change={change_strike}
    >
      <option value={$strike.data.last_week_minute_data[0].strike_price} selected>
        {$strike.data.last_week_minute_data[0].strike_price}
      </option>
      {#each $strike.data.last_week_minute_data.slice(1) as item}
        <option value={item.strike_price}> {item.strike_price} </option>
      {/each}
    </select>
  {/if}
</div>
