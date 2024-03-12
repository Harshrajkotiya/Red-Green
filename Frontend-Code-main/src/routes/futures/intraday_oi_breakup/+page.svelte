<script lang="ts">
  import DataTable, {
    Head,
    Body,
    Row,
  } from "@smui/data-table";
  import Cell from "@smui/data-table/src/Cell.svelte";
  import { page } from "$app/stores";
  import { graphql } from "$houdini";
  import FiltersInOneComponent from "../../../components/FiltersInOneComponent.svelte";
  import ColoredCell from "../../../components/ColoredCell.svelte";

  let expiry_date: string;
  let symbol_name: string;
  // let variables;
  let sort_obj;
  let variables = { symbol: {}, date_expiry: {} };

  let interval_obj: string;
  let currentTime;
  let ImportVariables = new Array();
  const options = { minimumFractionDigits: 2, maximumFractionDigits: 2 };
  // let sort
  let GetintradayData;
  // let interval_list = [
  //   { name: "fut_today_3_min", label: "3min" },
  //   { name: "fut_today_5_min", label: "5min" },
  //   { name: "fut_today_15_min", label: "15min" },
  //   { name: "fut_today_30_min", label: "30min" },
  //   { name: "fut_today_1_hour", label: "1hour" },
  // ];

  // const symbol = graphql(`
  //   query Get_futureintradaySymbol  {
  //     future_expiry(distinct_on: expiry, order_by: { expiry: asc }) {
  //       expiry
  //     }
  //   }
  // `);

  const Mypageload = () => {
    interval_obj = ImportVariables.interval_obj;
    console.log(interval_obj);

    switch (interval_obj) {
      case "futures_5_min":
        GetintradayData = graphql(`
          subscription min5Data(
            $date_expiry: date
            $symbol: String
            $order_column: p2_fut_today_5_min_order_by!
          ) {
            future_data: p2_fut_today_5_min(
              where: { symbol: { _eq: $symbol }, expiry: { _eq: $date_expiry } }
              order_by: [$order_column]
            ) {
              bucket
              open_interest
              open_interest_change
              price
              price_change
              price_change_per
              volume
              open_interest_change_per
            }
          }
        `);
        break;

      case "futures_15_min":
        GetintradayData = graphql(`
          subscription min15Data(
            $date_expiry: date
            $symbol: String
            $order_column: p2_fut_today_15_min_order_by!
          ) {
            future_data: p2_fut_today_15_min(
              where: { symbol: { _eq: $symbol }, expiry: { _eq: $date_expiry } }
              order_by: [$order_column]
            ) {
              bucket
              open_interest
              open_interest_change
              price
              price_change
              price_change_per
              volume
              open_interest_change_per
            }
          }
        `);
        break;

      case "futures_30_min":
        GetintradayData = graphql(`
          subscription min30Data(
            $date_expiry: date
            $symbol: String
            $order_column: p2_fut_today_30_min_order_by!
          ) {
            future_data: p2_fut_today_30_min(
              where: { symbol: { _eq: $symbol }, expiry: { _eq: $date_expiry } }
              order_by: [$order_column]
            ) {
              bucket
              open_interest
              open_interest_change
              price
              price_change
              price_change_per
              volume
              open_interest_change_per
            }
          }
        `);
        break;

      case "futures_1_hour":
        GetintradayData = graphql(`
          subscription hour1Data(
            $date_expiry: date
            $symbol: String
            $order_column: p2_fut_today_1_hour_order_by!
          ) {
            future_data: p2_fut_today_1_hour(
              where: { symbol: { _eq: $symbol }, expiry: { _eq: $date_expiry } }
              order_by: [$order_column]
            ) {
              bucket
              open_interest
              open_interest_change
              price
              price_change
              price_change_per
              volume
              open_interest_change_per
            }
          }
        `);
        break;

      default:
        GetintradayData = graphql(`
          subscription GetOiBreakup(
            $date_expiry: date
            $order_column: p2_fut_today_3_min_order_by!
            $symbol: String
          ) {
            future_data_3min: p2_fut_today_3_min(
              where: { symbol: { _eq: $symbol }, expiry: { _eq: $date_expiry } }
              order_by: [$order_column]
            ) {
              bucket
              open_interest
              open_interest_change
              price
              price_change
              price_change_per
              volume
              open_interest_change_per
            }
          }
        `);
        break;
    }
    sort_obj = ImportVariables.sort_obj;
    symbol_name = ImportVariables.symbol_name;
    expiry_date = ImportVariables.expiry_date;
    variables = {
      date_expiry: expiry_date,
      symbol: symbol_name,
      order_column: {},
    };

    variables["order_column"][sort_obj] = "asc";

    $: GetintradayData.listen(variables);
  };

  // onMount(() => {
  //   symbol_name = "NIFTY";
  //   // expiry_date = ImportVariables.expiry_date_future;
  //   // variables = { date_expiry: "{"+expiry_date+"}", symbol: "{"+symbol_name+"}" };
  //   Mypageload();
  // });

  $: $GetintradayData, (currentTime = new Date());

  let url = $page.route.id;

  // ***********************Download Data***************************

  let tableData = [];
  let tableHeader = [
    "Time",
    "OI",
    "Total OI Chg(%)",
    "Day High",
    "Day Low",
    "Price",
    "Price Chg",
    "Volume",
    "OI Chg(%)",
    "Build Up",
    // "VWAP",
    // "IV",
    // "PCR",
  ];

  // function downloaderData() {
  //     if ($GetintradayData) {
  //         tableData = ($GetintradayData?.future_data || []).map((obj) => ({
  //             ...obj,
  //             // VWAP: 0,
  //             // IV: 0,
  //             // PCR: 0,
  //         }));
  //     }

  // }

  // ***********************Download Data***************************
</script>

<div class="container-fluid">
  <FiltersInOneComponent
    bind:ComponentExportableVarialbes={ImportVariables}
    on:MenuComponentChangeEvent={Mypageload}
    tableData={$GetintradayData?.future_data}
    ImportableComponentList={[
      "SearchboxwithExpiry",
      "IntervalFilter",
      "SortFilter",
    ]}
    SortFilterData={["intradayOiBreakUp"]}
    TableTitleFromPage={"Futures Intraday OI Breakup"}
  />

  <!-- <div class="d-flex" style="justify-content: center">
        <div class="d-flex mb-3 me-auto">
            <div class="mx-4">
                <SearchboxSymbol
                    bind:result={symbol_name}
                    on:addSearchField={Mypageload}
                />
            </div>

            <ExpiryDate
                bind:date={expiry_date}
                on:addExpiryDate={Mypageload}
                expiry_list={$symbol?.data?.future_expiry}
            />

            <div class="mx-2">
                <IntervalFilter
                    bind:current_field={interval_obj}
                    on:addIntervalField={Mypageload}
                    interval_field={interval_list}
                />
            </div>
        </div> -->
  <!-- <div class="d-flex" style="justify-content: center">
    <div class="d-flex mb-3 me-auto">
      <div class="mx-2">
        <IntervalFilter
          bind:current_field={interval_obj}
          on:addIntervalField={Mypageload}
          interval_field={interval_list}
        />
      </div>
    </div>
  </div> -->
  <!-- ***********************Download Data*************************** -->
  <!-- <DataDownloader
      {tableData}
      {tableHeader}
      {downloaderData}
      fileName={`Intraday OI Breakup_${symbol_name}_${expiry_date}_${interval_obj}`}
    /> -->
  <!-- ***********************Download Data*************************** -->
  <!-- </div> -->

  <div style="display: flex;" class="p-2 mx-3">
    <!-- open-high value scanner table -->
    <DataTable table$aria-label="User list" style="width: 100%;" class="me-3">
      <Head>
        <Row>
          <Cell>Time</Cell>
          <Cell>OI</Cell>
          <Cell>OI Chg</Cell>
          <Cell>OI Chg %</Cell>
          <!-- <Cell>Day High</Cell> -->
          <!-- <Cell>Day Low</Cell> -->
          <Cell>Price</Cell>
          <Cell>Price Chg</Cell>
          <Cell>Volume</Cell>
          <!-- <Cell>Buildup</Cell> -->
        </Row>
      </Head>
      <Body>
        {#if $GetintradayData?.data?.future_data}
          {#each $GetintradayData?.data?.future_data as item}
            <Row>
              <Cell>{item.bucket.slice(11, 16)}</Cell>
              <!-- <Cell
                >{new Date(item.bucket).toLocaleTimeString("en-IN", {
                  hour: "2-digit",
                  minute: "2-digit",
                  timeZone: "Asia/Kolkata",
                })}</Cell
              > -->
              <!-- <Cell>{item.open_interest}</Cell> -->
              <CellWithProgress
              value={item.open_interest.toLocaleString(options)}
              percentage={item.open_interest_change_per?.toFixed(4)}
          />
              <Cell
                >{item.open_interest_change == null
                  ? 0
                  : item.open_interest_change}</Cell
              >
              <ColoredCell
                isPer={true}
                value={item.open_interest_change_per?.toFixed(4)}
              />
              <CellWithProgress
                            value={item.price.toLocaleString(options)}
                            percentage={item.price_change_per?.toFixed(4)}
                        />
              <Cell>{item.price_change == null ? 0 : item.price_change}</Cell>
              <Cell>{item.volume}</Cell>
              <!-- <BuildUpStatus build_up_status={item.build_up_status} /> -->
            </Row>
          {/each}
        {:else if $GetintradayData?.data?.future_data_3min}
          {#each $GetintradayData?.data?.future_data_3min as item}
            {#if $GetintradayData?.data?.future_data_3min[0] !== item || item.bucket.slice(11, 16) === "15:30"}
              <Row>
                <Cell>{item.bucket.slice(11, 16)}</Cell>
                <!-- <Cell
                >{new Date(item.bucket).toLocaleTimeString("en-IN", {
                  hour: "2-digit",
                  minute: "2-digit",
                  timeZone: "Asia/Kolkata",
                })}</Cell
              > -->
                <Cell>{item.open_interest.toLocaleString(options)}</Cell>
                <ColoredCell
                  value={item.open_interest_change == undefined ||
                  item.open_interest_change == null ||
                  isNaN(item.open_interest_change)
                    ? 0
                    : item.price_change?.toLocaleString(options)}
                />

                <ColoredCell
                  isPer={true}
                  value={item.open_interest_change_per?.toFixed(4)}
                />

                <Cell>{item.price.toLocaleString(options)}</Cell>
                <ColoredCell
                  value={item.price_change == undefined ||
                  item.price_change == null ||
                  isNaN(item.price_change)
                    ? 0
                    : item.price_change?.toLocaleString(options)}
                />

                <Cell>{item.volume.toLocaleString(options)}</Cell>
                <!-- <BuildUpStatus build_up_status={item.build_up_status} /> -->
              </Row>
            {/if}
          {/each}
        {/if}
      </Body>
    </DataTable>
  </div>
</div>

<style>
  .radio_lab {
    font-family: "Roboto", "sans-serif";
    font-style: normal;
    font-weight: 400;
    font-size: 13px;
    line-height: 24px;
    color: #ebebeb;
  }
</style>
