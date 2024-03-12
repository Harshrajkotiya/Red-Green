<script lang="ts">
  import { Label } from "@smui/tab";
  import { page } from "$app/stores";
  import DataTable, { Body, Head, Row } from "@smui/data-table";
  import Cell from "@smui/data-table/src/Cell.svelte";
  import { onMount } from "svelte";
  import IconButton from "@smui/icon-button";

  import { graphql } from "$houdini";
  import BuildUpStatus from "../../../components/BuildUpStatus.svelte";
  import FiltersInOneComponent from "./../../../components/FiltersInOneComponent.svelte";
  import ColoredCell from "../../../components/ColoredCell.svelte";
  import TableTitle from "../../../components/TableTitle.svelte";
  import CellWithProgress from "../../../components/CellWithProgress.svelte";

  let expiry_date: string;
  let currentTime;
  let ImportVariables = new Array();
  // let variables = { symbol: {}, date_expiry: {} };
  let tableData = [];
  let sort = "price_chang";
  let sortDirection;
  let variables = { date_expiry: {} };
  const options = { minimumFractionDigits: 2, maximumFractionDigits: 2 };

  //   const expiry = graphql(`
  //   query GetdaywiseExpiry {
  //     future_expiry(distinct_on: expiry) {
  //       expiry
  //     }
  //   }
  // `);

  const daywise_summary = graphql(`
    subscription GetSpikesDayWisesummary(
      $ExpiryDate: date
      $order_column: today_fut_1_day_order_by!
    ) {
      today_fut_1_day(
        where: { expiry: { _eq: $ExpiryDate } }
        order_by: [$order_column]
      ) {
        symbol
        price
        price_change
        open_interest
        open_interest_change
        volume
        volume_change
        expiry
        price_change_per
        open_interest_change_per
        volume_change_per
      }
    }
  `);

  //   onMount(() => {
  //     variables = { sort_object: {} };
  //     variables.sort_object[sort] =
  //       sortDirection == "descending" ? "desc" : "asc";
  //     variables["date_expiry"] = expiry_date;
  //     // $: daywise_summary.listen(variables);
  //   });

  //   $: $daywise_summary?.today_fut_1_day, (currentTime = new Date());

  async function filter_daywise_oi_summary() {
    //   expiry_date = ImportVariables.expiry_date_future;
    //   variables = { sort_object: {} };
    //   variables.sort_object[sort] =
    //     sortDirection == "descending" ? "desc" : "asc";
    //   console.log("variables", variables);
    let sort_obj = ImportVariables.sort_obj;
    let expiry_date = ImportVariables.expiry_date_future;

    variables = { order_column: {} };
    // variables["ExpiryDate"] = "{"+expiry_date+"}";
    variables["ExpiryDate"] = "{" + expiry_date + "}";
    variables["order_column"][sort_obj] = "asc";
    // variables["symbol"] = `{${ImportVariables.symbol_name}}`;

    $: daywise_summary.listen(variables);
    // $: daywise_summary.listen(variables);
  }

  let url = $page.route.id;

  // ***********************Download Data***************************
  let tableHeader = [
    "Symbol",
    "Price",
    "price Chg%",
    "OI",
    "OI Chg%",
    "Volume",
    "Volume Chg%",
    "Buildup",
  ];
  // function downloaderData() {
  //     if ($daywise_summary?.today_fut_1_day) {
  //     $: tableData = $daywise_summary?.today_fut_1_day;
  //     // tableData = ($daywise_summary?.today_fut_1_day).map((obj) => ({
  //     //     ...obj,
  //     //     PCR: parseFloat(0),
  //     // }));
  //     }
  //     // console.log("ok got it at page * data :- ",$tableData,typeof($tableData));
  // }
  // downloaderData();
  // ***********************Download Data***************************
</script>

<div class="container-fluid">
  <!-- FiltersInOneComponent Filters -->
  <FiltersInOneComponent
    bind:ComponentExportableVarialbes={ImportVariables}
    on:MenuComponentChangeEvent={filter_daywise_oi_summary}
    ImportableComponentList={["ExpiryDate", "SortFilter", "BuildupIndicator"]}
    TableTitleFromPage={"Daywise Price and OI Summary"}
    SortFilterData={["minimalAtSummaryFuture"]}
  />

  <!-- <BuildupIndicator /> -->
  <!-- dropdown manu -->
  <!-- <div class="d-flex mb-3" style="justify-content: center;">
          <div class="mx-4">
              <SortFilter
                  bind:current_field={sort_obj}
                  on:addSortField={filter_daywise_oi_summary}
                  sort_field={sort_field_list}
              />
          </div>
  
          <div>
              <ExpiryDate
                  bind:date={expiry_date}
                  on:addExpiryDate={filter_daywise_oi_summary}
                  expiry_list={$expiry?.data?.future_expiry}
              />
          </div> -->

  <!-- ***********************Download Data*************************** -->
  <!-- <DataDownloader
              {tableData}
              {tableHeader}
              {downloaderData}
              fileName={`Daywise Price & OI Details_${expiry_date}`}
          /> -->
  <!-- ***********************Download Data*************************** -->
  <!-- </div> -->

  <div>
    <!-- open-high value scanner table -->
    <DataTable
      sortable
      stickyHeader
      style="width: 100%; height: 750px; background-color: transparent !important;"
    >
      <Head>
        <Row>
          <Cell columnId="name">
            <Label>Summary</Label>
            <IconButton class="material-icons">arrow_upward</IconButton>
          </Cell>
          <Cell columnId="close">
            <Label>Price</Label>
            <IconButton class="material-icons">arrow_upward</IconButton>
          </Cell>

          <Cell columnId="price_change_per">
            <Label>Price Chg (%)</Label>
            <IconButton class="material-icons">arrow_upward</IconButton>
          </Cell>
          <Cell columnId="open_interest">
            <Label>OI</Label>
            <IconButton class="material-icons">arrow_upward</IconButton>
          </Cell>
          <Cell columnId="open_interest_change_per">
            <Label>OI Chg (%)</Label>
            <IconButton class="material-icons">arrow_upward</IconButton>
          </Cell>
          <Cell columnId="volume">
            <Label>Volume</Label>
            <IconButton class="material-icons">arrow_upward</IconButton>
          </Cell>
          <Cell columnId="volume_change_per">
            <Label>Volume Chg (%)</Label>
            <IconButton class="material-icons">arrow_upward</IconButton>
          </Cell>
          <Cell columnId="build_up_status">
            <Label>Buildup</Label>
            <IconButton class="material-icons">arrow_upward</IconButton>
          </Cell>
        </Row>
      </Head>
      <Body>
        {#if $daywise_summary?.data?.today_fut_1_day}
          {#each $daywise_summary?.data?.today_fut_1_day as item}
            <Row>
              <Cell>{item.symbol}</Cell>
              <CellWithProgress
                value={item.price.toLocaleString(options)}
                percentage={item.price_change_per?.toFixed(4)}
              />
              <ColoredCell
                isPer={true}
                value={item.price_change_per?.toFixed(4)}
              />
              <CellWithProgress
                value={item.open_interest.toLocaleString(options)}
                percentage={item.open_interest_change_per?.toFixed(4)}
              />
              <ColoredCell
                isPer={true}
                value={item.open_interest_change_per?.toFixed(4)}
              />

              <CellWithProgress
                value={item.volume.toLocaleString(options)}
                percentage={item.volume_change_per?.toFixed(4)}
              />
              <ColoredCell
                isPer={true}
                value={item.volume_change_per?.toFixed(4)}
              />

              <!-- <Cell>Buildup</Cell> -->
              <BuildUpStatus
                price_change={item.price_change}
                oi_change={item.open_interest_change}
              />
            </Row>
          {/each}
        {/if}
      </Body>
    </DataTable>
  </div>
</div>
