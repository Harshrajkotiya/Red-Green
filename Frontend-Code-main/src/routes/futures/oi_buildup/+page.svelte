<script lang="ts">
    import Data_table from "../../../components/DataTable.svelte";
    import { page } from "$app/stores";
    // import { onMount } from "svelte";
    import { graphql } from "$houdini";
    // import ExpiryDate from "../../../components/ExpiryDate.svelte";
    // import SortFilter from "./../../../components/Sort_filter.svelte";
    // import TableTitle from "../../../components/TableTitle.svelte";
    import FiltersInOneComponent from "../../../components/FiltersInOneComponent.svelte";
    import SearchboxSymbol from "../../../components/SearchboxSymbol.svelte";

    // Declaring The Variables...
    let ImportVariables;
    let variables = { _date_expiry: {} };

  // onMount(() => {
  //     // variables["date_expiry"] = expiry_date;
  //     // console.log("variables", variables);
  //     // $: buildup_data.listen(variables);
  //     console.log("mount Method Is called !!");
  //     // Sort();
  // });

  let buildup_data;

  async function Sort() {
    variables = {};
    // if (ImportVariables.symbol_name == undefined) {
    buildup_data = graphql(`
      subscription GetBuildupData($date_expiry: date) {
        today_fut_1_day(
          where: { expiry: { _eq: $date_expiry } }
          order_by: { price_change: desc }
        ) {
          symbol
          price
          open_interest
          open_interest_change
          price_change
          price_change_per
        }
      }
    `);
    // } else if (ImportVariables.symbol_name != "") {
    //     buildup_data = graphql(`
    //         subscription GetBuildupDatasym(
    //             $date_expiry: date
    //             $symbol_name: String
    //         ) {
    //             today_fut_1_day(
    //                 where: {
    //                     expiry: { _eq: $date_expiry }
    //                     symbol: { _eq: $symbol_name }
    //                 }
    //                 order_by: { price_change: desc }
    //             ) {
    //                 symbol
    //                 price
    //                 open_interest
    //                 open_interest_change
    //                 price_change
    //                 price_change_per
    //             }
    //         }
    //     `);
    // }

    // console.log("imported Variables are :- ", ImportVariables);
    // variables.date_expiry["date_expiry"] =
    // ImportVariables.expiry_date_future;
    variables["date_expiry"] = ImportVariables.expiry_date_future;

    // if (
    //     ImportVariables.symbol_name != "" &&
    //     ImportVariables.symbol_name != undefined
    // ) {
    //     variables["symbol_name"] = `${ImportVariables.symbol_name}`;
    // }
    // console.log(" Vars :- ", variables);

    $: buildup_data.listen(variables);
    //   $: shortBuildUp.listen(variables);
    //   $: shortCovering.listen(variables);
    //   $: longUnWinding.listen(variables);
  }
</script>

<div class="container-fluid">
  <!-- Filters -->
  <!-- <h1>gopljdfg</h1> -->
  <!-- <SearchboxSymbol bind:result= {symbol} on:addSearchField={Sort}/> -->

  <FiltersInOneComponent
    bind:ComponentExportableVarialbes={ImportVariables}
    on:MenuComponentChangeEvent={Sort}
    ImportableComponentList={["ExpiryDate", "SortFilter", "SearchboxSymbol"]}
    TableTitleFromPage={"Futures OI Buildup"}
  />
  {#if $buildup_data?.data?.today_fut_1_day}
    <div class="table_block">
      <Data_table
        items={$buildup_data?.data?.today_fut_1_day}
        name="Long Buildup"
      />

      <!-- {#if $shortBuildUp?.features} -->
      <Data_table
        items={$buildup_data?.data?.today_fut_1_day}
        name="Short Buildup"
      />
      <!-- {/if} -->
    </div>

    <div class="table_block">
      <!-- {#if $shortCovering?.features} -->
      <Data_table
        items={$buildup_data?.data?.today_fut_1_day}
        name="Short Covering"
      />
      <!-- {/if} -->
      <!-- {#if $longUnWinding?.features} -->
      <Data_table
        items={$buildup_data?.data?.today_fut_1_day}
        name="Long Unwinding"
      />
      <!-- {/if} -->
    </div>
  {/if}
</div>

<style>
  :root {
    --bg-dark: #141822;
    --light-col: white;
  }

  .mrg {
    margin: 0px 100px;
  }

  hr {
    border: 1px solid white;
  }

  .loc_me {
    font-family: "Roboto", "sans-serif";
    font-style: normal;
    font-weight: 600;
    font-size: 13px;
    line-height: 16px;
    color: #7a7a7a;
  }

  .head_loc {
    font-family: "Roboto", "sans-serif";
    font-style: normal;
    font-weight: 500;
    font-size: 10.52px;
    line-height: 16px;
    color: #ffffff;
  }

  .page_heading {
    font-family: "Roboto", "sans-serif";
    font-style: normal;
    font-weight: 700;
    font-size: 24px;
    line-height: 29px;
    color: #ffffff;
  }
  .drop_label {
    font-family: "Roboto", "sans-serif";
    font-style: normal;
    font-weight: 400;
    font-size: 12px;
    line-height: 20px;
    color: #f5f5f5;
  }

  .dropdown_btn {
    background: var(--bg-dark);
    box-sizing: border-box;
    padding: 0px 16px;
    width: 235.48px;
    height: 40px;
    border: 1px solid rgba(184, 184, 184, 0.2);
    border-radius: 6px;
    color: #ffffff;
  }
  .table_block {
    display: flex;
  }

  .radio_lab {
    font-family: "Roboto", "sans-serif";
    font-style: normal;
    font-weight: 400;
    font-size: 13px;
    line-height: 24px;
    color: #ebebeb;
  }
  .form-check-input {
    width: 24px;
    height: 24px;
  }

  .sub-btn {
    box-sizing: border-box;
    /* Font/Base button size */
    height: 40px;
    font-family: "Roboto", "sans-serif";
    font-style: normal;
    font-weight: 600;
    font-size: 13px;
    line-height: 16px;
    border: 1px solid rgba(0, 0, 0, 0.1);
    border-radius: 6px;
  }

  .data-pick {
    max-width: 250px;
    min-width: 150px;
    background-color: var(--bg-dark);
    color: var(--light-col);
    height: 40px;
  }

  @media only screen and (max-width: 1100px) {
    .table_block {
      display: block;
      width: full;
      text-align: -webkit-center;
    }
  }
</style>
