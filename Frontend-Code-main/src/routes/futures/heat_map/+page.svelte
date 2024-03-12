<script lang="ts">
  import { page } from "$app/stores";
  import { graphql } from "$houdini";
  import Tab, { Label } from "@smui/tab";
  import TabBar from "@smui/tab-bar";
  import { onMount } from "svelte";
  import TableTitle from "../../../components/TableTitle.svelte";
  // import BuildupIndicator from "../../../components/Buildup_indicator.svelte";
  // import SortFilter from "./../../../components/Sort_filter.svelte";
  // import ExpiryDate from "./../../../components/ExpiryDate.svelte";
  import FiltersInOneComponent from "./../../../components/FiltersInOneComponent.svelte";

  let active = "All";

  //   let url = $page.route.id;
  let sort_obj: string;
  let expiry_date: string;
  let currentTime;
  let ImportVariables = new Array();
  const sort_field_list = [
    { name: "price_change_per", label: "Price Change" },
    { name: "open_interest_change_per", label: "OI Change" },
  ];

  // const expiry = graphql(`
  //     query GetfeaturesExpiry {
  //         future_expiry(distinct_on: expiry) {
  //             expiry
  //         }
  //     }
  // `);

  // onMount(() => {
  //     variables = { sort_object: {} };
  //     variables.sort_object[sort_obj] = "desc";
  //     variables["date_expiry"] = expiry_date;
  //     // console.log("variables",variables);
  //     $: allHeatMap.listen();
  // });

  const allHeatMap = graphql(`
    subscription GetallHeatMap($date_expiry: date) {
      today_fut_1_day(where: { expiry: { _eq: $date_expiry } }) {
        price
        volume
        price_change
        symbol
        open
        low
        high
        open_interest_change
        price_change_per
      }
    }
  `);
  //   $: allHeatMap.listen();

  // const allHeatMap = graphql(`
  //     subscription GetallHeatMap(
  //         $sort_object: features_order_by!
  //         $date_expiry: date
  //     ) {
  //         features(
  //             order_by: [$sort_object]
  //             where: { expiry: { _eq: $date_expiry } }
  //         ) {
  //             name
  //             expiry
  //             close
  //             build_up_status
  //             price_change_per
  //             open_interest_change_per
  //         }
  //     }
  // `);
  let variables = { date_expiry: {} };
  //   variables.sort_object[sort_obj] = "desc";
  // variables["date_expiry"] = expiry_date;
  // console.log("variables",variables);

  // $: $allHeatMap?.features, (currentTime = new Date());

  // $: allHeatMap.listen(variables);

  async function Sort() {
    console.log(ImportVariables);
    // expiry_date = ImportVariables.expiry_date_future;
    // sort_obj = ImportVariables.sort_obj;

    // variables = { sort_object: {} };
    // variables.sort_object[sort_obj] = "desc";
    variables["date_expiry"] = `{${ImportVariables.expiry_date_future}}`;
    // console.log("variables",variables);
    $: allHeatMap.listen(variables);
  }
</script>


<div class="container-fluid">
</div>
<div>
  <!-- <div class="filter_indicator">
            <div>
                <ExpiryDate
                    bind:date={expiry_date}
                    on:addExpiryDate={Sort}
                    expiry_list={$expiry?.data?.future_expiry}
                />
            </div>
    
            <div>
                <SortFilter
                    bind:current_field={sort_obj}
                    on:addSortField={Sort}
                    sort_field={sort_field_list}
                />
            </div>
        </div> -->

  <!-- FiltersInOneComponent Filters -->
  <FiltersInOneComponent
    bind:ComponentExportableVarialbes={ImportVariables}
    on:MenuComponentChangeEvent={Sort}
    ImportableComponentList={["ExpiryDate", "BuildupIndicator"]}
    TableTitleFromPage={"Market Heatmap"}

  />

  <div class="tabs_bar">
    <TabBar
      tabs={[
        "All",
        "Long build-up",
        "Short Covering",
        "Long Unwinding",
        "Short build-up",
      ]}
      let:tab
      bind:active
    >
      <!-- Note: the `tab` property is required! -->
      <Tab {tab}>
        <Label>{tab}</Label>
      </Tab>
    </TabBar>
  </div>
</div>

<div class="box-container">
  {#if $allHeatMap?.data?.today_fut_1_day}
    {#each $allHeatMap?.data?.today_fut_1_day as stock}
      {#if active == "All"}
        {#if stock.price_change > 0 && stock.open_interest_change > 0}
          <div class="box lb-color">
            <p class="name_lable">{stock.symbol}</p>
            <p class="stock_data">
              {stock.price_change_per?.toFixed(4)} %
            </p>
            <p class="stock_data">{stock.price}</p>
          </div>
        {:else if stock.price_change < 0 && stock.open_interest_change > 0}
          <div class="box sb-color">
            <p class="name_lable">{stock.symbol}</p>
            <p class="stock_data">
              {stock.price_change_per?.toFixed(4)} %
            </p>
            <p class="stock_data">{stock.price}</p>
          </div>
        {:else if stock.price_change > 0 && stock.open_interest_change < 0}
          <div class="box sc-color">
            <p class="name_lable">{stock.symbol}</p>
            <p class="stock_data">
              {stock.price_change_per?.toFixed(4)} %
            </p>
            <p class="stock_data">{stock.price}</p>
          </div>
        {:else if stock.price_change < 0 && stock.open_interest_change < 0}
          <div class="box lu-color">
            <p class="name_lable">{stock.symbol}</p>
            <p class="stock_data">
              {stock.price_change_per?.toFixed(4)} %
            </p>
            <p class="stock_data">{stock.price}</p>
          </div>
        {/if}
      {/if}

      {#if active == "Long build-up"}
        {#if stock.price_change > 0 && stock.open_interest_change > 0}
          <div class="box lb-color">
            <p class="name_lable">{stock.symbol}</p>
            <p class="stock_data">
              {stock.price_change_per?.toFixed(4)} %
            </p>
            <p class="stock_data">{stock.price}</p>
          </div>
        {/if}
      {:else if active == "Short build-up"}
        {#if stock.price_change < 0 && stock.open_interest_change > 0}
          <div class="box sb-color">
            <p class="name_lable">{stock.symbol}</p>
            <p class="stock_data">
              {stock.price_change_per?.toFixed(4)} %
            </p>
            <p class="stock_data">{stock.price}</p>
          </div>
        {/if}
      {:else if active == "Short Covering"}
        {#if stock.price_change > 0 && stock.open_interest_change < 0}
          <div class="box sc-color">
            <p class="name_lable">{stock.symbol}</p>
            <p class="stock_data">
              {stock.price_change_per?.toFixed(4)} %
            </p>
            <p class="stock_data">{stock.price}</p>
          </div>
        {/if}
      {:else if active == "Long Unwinding"}
        {#if stock.price_change < 0 && stock.open_interest_change < 0}
          <div class="box lu-color">
            <p class="name_lable">{stock.symbol}</p>
            <p class="stock_data">
              {stock.price_change_per?.toFixed(4)} %
            </p>
            <p class="stock_data">{stock.price}</p>
          </div>
        {/if}
      {/if}
    {/each}
  {/if}
</div>

<style>
  .filter_indicator {
    display: flex;
    justify-content: space-around;
  }

  .box {
    border-radius: 3px;
    padding: 10px;
    width: 150px;
    height: 100px;
    border: 1px solid gray;
    text-align: center;
  }

  .form-option {
    font-size: larger;
    border-radius: 6px;
  }

  .box-container {
    display: flex;
    flex-wrap: wrap;
    margin: 20px 40px;
    justify-content: flex-start;
  }

  .stock_data {
    line-height: 14px;
    font-size: 12px;
    color: white;
  }

  .name_lable {
    line-height: 20px;
    color: white;
    font-weight: 600;
  }

  .data-pick {
    max-width: 250px;
    width: 200px;

    min-width: 150px;
    background-color: var(--bg-dark);
    color: white;
    height: 40px;
  }
</style>
