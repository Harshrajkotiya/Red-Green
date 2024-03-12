<script lang="ts">
  import { page } from "$app/stores";
  import DataTable, {
    Body,
    Head,
    Row,
    Label,
    SortValue,
  } from "@smui/data-table";
  import IconButton from "@smui/icon-button";

  import Cell from "@smui/data-table/src/Cell.svelte";
  import { graphql } from "$houdini";
  import { onMount } from "svelte";
  import BuildUpStatus from "../../../components/BuildUpStatus.svelte";
  import TableTitle from "../../../components/TableTitle.svelte";
  import DataDownloader from "../../../components/DataDownloader.svelte";
  // import BuildupIndicator from "../../../components/Buildup_indicator.svelte";
  // import SymbolExpiryFilter from "../../../components/Symbol_Expiry_filter.svelte";
  import FiltersInOneComponent from "./../../../components/FiltersInOneComponent.svelte";
  import ColoredCell from "../../../components/ColoredCell.svelte";
  import CellWithProgress from "../../../components/CellWithProgress.svelte";

  let expiry_date;
  let symbol_name;
  let variables = { symbol: {}, date_expiry: {} };
  let currentTime;
  let ImportVariables = new Array();
  let tableData;
  let sortDirection;
  let sort = "bucket";

  //   const symbol = graphql(`
  //       query Get_daywiseSymbol {
  //           future_expiry(order_by: { expiry: asc }) {
  //               name
  //               expiry
  //           }
  //       }
  //   `);

  const daywise_details = graphql(`
  subscription GetSpikesDayWise($ExpiryDate: date $order_column: today_fut_1_day_order_by!) {
    today_fut_1_day(where: { expiry: { _eq: $ExpiryDate } }order_by: [$order_column]) {
        bucket
        expiry
        open_interest
        open_interest_change
        price
        price_change
        symbol
        volume
        volume_change
        price_change_per
        open_interest_change_per
        volume_change_per
      }
    }
  `);

  // $: daywise_details.listen();

  //   variables = { symbol: symbol_name, date_expiry: expiry_date };

  // onMount(() => {
  //   //   console.log("IMP VARS :- ", ImportVariables);
  //   // symbol_name = ImportVariables.symbol_name;
  //   // expiry_date = ImportVariables.expiry_date_future;
  //   // variables = { sort_object: {} };
  //   // variables.sort_object[sort] =
  //   //   sortDirection == "descending" ? "desc" : "asc";
  //   variables["symbol"] = symbol_name;
  //   variables["date_expiry"] = expiry_date;
  //   $: daywise_details.listen(variables);
  // });

  //   $: $daywise_details?.daywise_oi_futures, (currentTime = new Date());

  async function filter_oi_break_up() {
    //   console.log("IMP VARS SORT :- ", ImportVariables);

    // symbol_name = ImportVariables.symbol_name;
    // expiry_date = ImportVariables.expiry_date_future;

    // variables = { sort_object: {} };
    // variables.sort_object[sort] =
    //     sortDirection == "descending" ? "desc" : "asc";
    // variables["symbol"] = symbol_name;
    // variables["date_expiry"] = expiry_date;
    console.log(ImportVariables);
    

    let sort_obj = ImportVariables.sort_obj;
    let expiry_date = ImportVariables.expiry_date_future;

    variables = {order_column:{} };
    variables["ExpiryDate"] = expiry_date;
    variables["order_column"][sort_obj] = "asc";
    // variables["symbol"] = "{NIFTY/}";

    // variables["symbol"] = ImportVariables.symbol_name;
    // variables["date_expiry"] = `{${ImportVariables.expiry_date}}`;
    $: daywise_details.listen(variables);
  }

  let url = $page.route.id;

  const options = {minimumFractionDigits: 2, maximumFractionDigits: 2};

  // ***********************Download Data***************************

  let tableHeader = [
    "Date",
    "Price",
    "price Chg%",
    "OI",
    "OI Chg%",
    "Volume",
    "Volume Chg%",
    "Buildup",
  ];

  //     function downloaderData() {
  //     if ($daywise_details?.daywise_oi_futures) {
  //       $: tableData = $daywise_details?.daywise_oi_futures;
  //     //   tableData = ($daywise_details?.daywise_oi_futures).map((obj) => ({
  //     //     ...obj,
  //     //     PCR: parseFloat(0),
  //     //   }));
  //     }
  //     console.log("ok got it at page * data :- ",$tableData,typeof($tableData));
  //     // return tableData;
  //   }
  //   downloaderData();
  // ***********************Download Data***************************
</script>



<div class="container-fluid" style="width: 100%;">
  <!-- FiltersInOneComponent Filters -->
  <FiltersInOneComponent
    bind:ComponentExportableVarialbes={ImportVariables}
    on:MenuComponentChangeEvent={filter_oi_break_up}
    ImportableComponentList={["ExpiryDate","SortFilter","BuildupIndicator"]}
    TableTitleFromPage={"Daywise Price & OI Details"}

  />

  <!-- <div class="d-flex" style="justify-content: center">
          <div class="d-flex mb-1 me-auto gap-3">
              {#if $symbol?.data}
                  <SymbolExpiryFilter
                      bind:current_symbol={symbol_name}
                      bind:current_expiry={expiry_date}
                      symbol_list={$symbol?.data?.future_expiry}
                      on:addSymbolField={filter_oi_break_up}
                  />
              {/if}
              <BuildupIndicator />
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

  <div style="display: flex;">
    <!-- open-high value scanner table -->

    <DataTable
      sortable
      stickyHeader
      style="width: 100%; height: 750px; overflow-y: auto; background-color: transparent !important;"
    >
      <Head style="color: #FFD166;">
        <Row >
          <Cell columnId="bucket">
            <Label>Date</Label>
            <IconButton class="material-icons">arrow_upward</IconButton>
          </Cell>
          <Cell columnId="close">
            <Label>Price</Label>
            <IconButton class="material-icons">arrow_upward</IconButton>
          </Cell>
          <Cell columnId="price_change_per">
            <Label>Price Chg%</Label>
            <IconButton class="material-icons">arrow_upward</IconButton>
          </Cell>
          <Cell columnId="open_interest">
            <Label>OI</Label>
            <IconButton class="material-icons">arrow_upward</IconButton>
          </Cell>
          <Cell columnId="open_interest_change_per">
            <Label>OI Chg%</Label>
            <IconButton class="material-icons">arrow_upward</IconButton>
          </Cell>
          <Cell columnId="volume">
            <Label>Volume</Label>
            <IconButton class="material-icons">arrow_upward</IconButton>
          </Cell>
          <Cell columnId="volume_change_per">
            <Label>Volume Chg%</Label>
            <IconButton class="material-icons">arrow_upward</IconButton>
          </Cell>
          <Cell class="text-center" sortable={false}>
            <Label>Buildup</Label>
          </Cell>
        </Row>
      </Head>
      <Body>
        {#if $daywise_details?.data?. today_fut_1_day}
          {#each $daywise_details?.data?. today_fut_1_day as item}
            <Row>
              <Cell
                >{new Date(item.bucket).toISOString().slice(0, 10)}</Cell
              >
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
              <!-- <Cell>BuildUp</Cell> -->
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
