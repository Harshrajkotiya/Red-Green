<script lang="ts">
  import DataTable, {
    Head,
    Body,
    Row,
    Label,
    SortValue,
  } from "@smui/data-table";
  import IconButton from "@smui/icon-button";
  import Cell from "@smui/data-table/src/Cell.svelte";
  import { page } from "$app/stores";
  import { onMount } from "svelte";
  import { graphql } from "$houdini";
  import TableTitle from "../../../components/TableTitle.svelte";
  //   import SortFilter from "./../../../components/Sort_filter.svelte";
  //   import ExpiryDate from "../../../components/ExpiryDate.svelte";
  import FiltersInOneComponent from "./../../../components/FiltersInOneComponent.svelte";
  import ColoredCell from "../../../components/ColoredCell.svelte";
  import CellWithProgress from "../../../components/CellWithProgress.svelte";

  let url = $page.route.id;
  let sort_obj;
  let expiry_date = "";
  // let currentTime;
  // let sortDirection;
  let ImportVariables = new Array();
  let sort = "price_change";
  let variables = {};
  const options = { minimumFractionDigits: 2, maximumFractionDigits: 2 };

  // const expiry = graphql(`
  //     query GetOhlScanExpiryDate {
  //         features(
  //             distinct_on: expiry
  //             order_by: { expiry: asc }
  //             where: { ohl_status: { _neq: "none" } }
  //         ) {
  //             expiry
  //         }
  //     }
  // `);

  onMount(() => {
    // sort_obj = ImportVariables.sort_obj;
    expiry_date = ImportVariables.expiry_date_future;
    // variables = {};
    // variables.sort_object[sort] =
    //   sortDirection == "descending" ? "desc" : "asc";
    variables["date_expiry"] = "{" + expiry_date + "}";
    variables["order_column"] = { price_change: "asc" };
    console.log("mount method called from page", variables);
    $: ohlData.listen(variables);
    // $: openLow.listen(variables);
  });

  console.log("immort ", ImportVariables);

  // let variables = { sort_object: {} };
  // variables.sort_object[sort_obj] = sortDirection=="descending"?"desc":"asc";
  // variables["date_expiry"] = expiry_date;

  const ohlData = graphql(`
    subscription GetOHLData(
      $date_expiry: date
      $order_column: fut_ohl_scan_order_by!
    ) {
      fut_ohl_scan(
        where: { expiry: { _eq: $date_expiry } }
        order_by: [$order_column]
      ) {
        price
        high
        low
        open
        price_change
        symbol
        status
        price_change_per
      }
    }
  `);
  // $: ohlData.listen();

  // $: $ohlData?.features, (currentTime = new Date());
  // $: $openLow?.features, (currentTime = new Date());

  async function Sort() {
    // console.log(ImportVariables);

    sort_obj = ImportVariables.sort_obj;
    expiry_date = ImportVariables.expiry_date_future;

    variables = { order_column: {} };
    // variables.sort_object[sort] =
    //   sortDirection == "descending" ? "desc" : "asc";
    variables["date_expiry"] = "{" + expiry_date + "}";
    variables["order_column"][sort_obj] = "asc";
    console.log("variables", variables);
    $: ohlData.listen(variables);
    // $: openLow.listen(variables);
  }
</script>

<div class="container-fluid" style="width: 100%;">

  <!-- FiltersInOneComponent Filters -->

  <FiltersInOneComponent
    bind:ComponentExportableVarialbes={ImportVariables}
    on:MenuComponentChangeEvent={Sort}
    ImportableComponentList={["ExpiryDate", "SortFilter"]}
    TableTitleFromPage={"Futures Open-High / Open-Low Scanner"}
    SortFilterData={"fieldListAtOHLScannerAtFutures"}
  />

  <!-- dropdown manu -->
  <!-- <div class="d-flex mb-3" style="justify-content: center;">
        <div class="mx-4">
            <SortFilter
                bind:current_field={sort_obj}
                on:addSortField={Sort}
                sort_field={sort_field_list}
            />
        </div>

        <div class="mx-4">
            <ExpiryDate
                bind:date={expiry_date}
                on:addExpiryDate={Sort}
                expiry_list={$expiry?.data?.features}
            />
        </div>
    </div> -->

  <div class="d-flex" style="width: 100%;">
    <div style="width: 50%;">
      <DataTable class="col-12">
        <Head>
          <Row>
            <Cell style="text-align: center;background:transparent;color:white"
              >Open-High</Cell
            >
          </Row>
        </Head>
      </DataTable>
    </div>
    <div style="width: 50%; margin-left: 2%;">
      <DataTable class="col-12">
        <Head>
          <Row>
            <Cell style="text-align: center;background:transparent;color:white"
              >Open-Low</Cell
            >
          </Row>
        </Head>
      </DataTable>
    </div>
  </div>

  <div style="display: flex;">
    <!-- open-high value scanner table -->
    <DataTable
      sortable
      bind:sort
      on:SMUIDataTable:sorted={Sort}
      stickyHeader
      style="width: 50%; height: 750px; background-color: transparent !important; overflow-y: auto;"
      class="me-3"
    >
      <Head>
        <Row>
          <Cell columnId="symbol">
            <Label>Symbol</Label>
            <IconButton class="material-icons">arrow_upward</IconButton>
          </Cell>

          <Cell columnId="open">
            <Label>Open</Label>
            <IconButton class="material-icons">arrow_upward</IconButton>
          </Cell>
          <Cell columnId="high">
            <Label>High</Label>
            <IconButton class="material-icons">arrow_upward</IconButton>
          </Cell>
          <!-- <Cell>Latest High</Cell> -->
          <Cell columnId="price">
            <Label>LTP</Label>
            <IconButton class="material-icons">arrow_upward</IconButton>
          </Cell>
          <Cell columnId="price_change">
            <Label>Change</Label>
            <IconButton class="material-icons">arrow_upward</IconButton>
          </Cell>
          <Cell sortable={false}>
            <Label>Change%</Label>
            <IconButton class="material-icons">arrow_upward</IconButton>
          </Cell>
        </Row>
      </Head>
      <Body>
        {#if $ohlData?.data?.fut_ohl_scan}
          {#each $ohlData?.data?.fut_ohl_scan as item}
            {#if item.status === "high"}
              <Row>
                <Cell>{item.symbol}</Cell>
                <Cell>{item.open?.toFixed(2)}</Cell>
                <Cell>{item.high?.toFixed(2)}</Cell>
                <!-- <Cell>{item.price?.toLocaleString(options)}</Cell> -->
                <CellWithProgress
                  value={item.price.toLocaleString(options)}
                  percentage={item.price_change_per?.toFixed(4)}
                />
                <ColoredCell
                  value={item.price_change == undefined ||
                  isNaN(item.price_change)
                    ? 0
                    : item.price_change?.toFixed(2)}
                />
                <ColoredCell
                  isPer={true}
                  value={item.price_change_per?.toFixed(4)}
                />
              </Row>
            {/if}
          {/each}
        {/if}
      </Body>
    </DataTable>
    <!-- open-low value scanner table -->
    <DataTable
      stickyHeader
      style="width: 50%; height: 750px; background-color: transparent !important; overflow-y: auto;"
    >
      <Head>
        <Row>
          <Cell>Symbol</Cell>
          <Cell>Open</Cell>
          <Cell>Low</Cell>
          <!-- <Cell>Latest Low</Cell> -->
          <Cell>LTP</Cell>
          <Cell>Change</Cell>
          <Cell>
            <!-- <IconButton class="material-icons">arrow_upward</IconButton> -->
            Change%
          </Cell>
          <!-- <Cell>Change%</Cell> -->
        </Row>
      </Head>
      <Body>
        {#if $ohlData?.data?.fut_ohl_scan}
          {#each $ohlData?.data?.fut_ohl_scan as item}
            {#if item.status === "low"}
              <Row>
                <Cell>{item.symbol}</Cell>
                <Cell>{item.open?.toFixed(2)}</Cell>
                <Cell>{item.low?.toFixed(2)}</Cell>
                <!-- <Cell>{item.price?.toLocaleString(options)}</Cell> -->
                <CellWithProgress
                  value={item.price.toLocaleString(options)}
                  percentage={item.price_change_per?.toFixed(4)}
                />
                <ColoredCell
                  value={item.price_change == undefined ||
                  isNaN(item.price_change)
                    ? 0
                    : item.price_change?.toFixed(2)}
                />
                <ColoredCell
                  isPer={true}
                  value={item.price_change_per?.toFixed(4)}
                />
              </Row>
            {/if}
          {/each}
        {/if}
      </Body>
    </DataTable>
  </div>
</div>
