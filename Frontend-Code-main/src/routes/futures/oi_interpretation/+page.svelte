<script lang="ts">
  import { page } from "$app/stores";
  import { graphql } from "$houdini";
  import DataTable, { Body, Cell, Head, Row } from "@smui/data-table";
  // import StrikePrice from "../../../components/StrikePrice.svelte";
  //import SymbolExpiryFilter from "../../../components/Symbol_Expiry_filter.svelte";
  import BuildUpStatus from "../../../components/BuildUpStatus.svelte";
  // import BuildupIndicator from "../../../components/Buildup_indicator.svelte";
  // import DataDownloader from "../../../components/DataDownloader.svelte";
  import FiltersInOneComponent from "./../../../components/FiltersInOneComponent.svelte";

  import { onMount } from "svelte";
  import ColoredCell from "../../../components/ColoredCell.svelte";
  

  let symbol_name;
  let expiry_date;
  let sort_obj;

  // let currentTime;F
  let variables = { ExpiryDate: {} };
  const options = { minimumFractionDigits: 2, maximumFractionDigits: 2 };

  // let strike;
  // let data_status;
  // let tableData = [];

  // getting yesterday date
  // var today = new Date();
  // var yesterday = new Date(today);
  // yesterday.setDate(today.getDate() - 1);

  // var max_date =
  //   yesterday.getFullYear() +
  //   "-" +
  //   (yesterday.getMonth() + 1).toString().padStart(2, "0") +
  //   "-" +
  //   yesterday.getDate().toString().padStart(2, "0");
  // max_date = "2023-2-21"

  // console.log(max_date);

  // console.log(yesterday.toLocaleDateString());

  // let data_pr_date=yesterday
  let ImportVariables;

  // Getting Symbols...
  // const symbol = graphql(`
  //   query Get_FutureIntradayOiChangeSymbol1 {
  //     fut_expiry_date(order_by: { expiry: asc }) {
  //       symbol
  //       expiry
  //     }
  //   }
  // `);

  const fut_oi_scan = graphql(`
    subscription Get_scan_data(
      $ExpiryDate: date
      $order_column: fut_oi_scan_order_by!
    ) {
      fut_oi_scan(
        where: { expiry: { _eq: $ExpiryDate } }
        order_by: [$order_column]
      ) {
        bucket
        expiry
        open_interest
        open_interest_15_min
        open_interest_1_hour
        open_interest_30_min
        open_interest_change
        open_interest_change_15_min
        open_interest_change_1_hour
        open_interest_change_30_min
        price
        price_15_min
        price_1_hour
        price_30_min
        price_change
        price_change_15_min
        price_change_1_hour
        price_change_30_min
        symbol
        open_interest_change_per
        open_interest_change_per_15_min
        open_interest_change_per_1_hour
        open_interest_change_per_30_min
      }
    }
  `);

  // $: fut_oi_scan.listen();

  // variables = { symbol: symbol_name, date_expiry: expiry_date };
  //   $: fut_oi_scan.listen(variables);

  // onMount(() => {
  //   symbol_name = ["NIFTY"];
  //   // variables = {
  //   //   symbol: "{%" + symbol_name + "%}",
  //   //   date_expiry: "{" + expiry_date[0] + "}",
  //   // };
  // // variables["date_expiry"] = "{" + expiry_date + "}";
  // variables["order_column"] = {"open_interest_change":"asc"};
  //   console.log("The Mounted Variables OI :- ", variables);
  //   // $: fut_oi_scan.listen(variables);
  // });

  // $: fut_oi_scan.listen(variables);

  async function filter_oi_breakup() {
    let sort_obj = ImportVariables.sort_obj;
    let expiry_date = ImportVariables.expiry_date_future;

    variables = { order_column: {} };
    variables["ExpiryDate"] = "{" + expiry_date + "}";
    variables["order_column"][sort_obj] = "asc";

    console.log(ImportVariables, variables);
    $: fut_oi_scan.listen(variables);
  }

  // let tableData = [];

  // let variables: { name: symbol_name; exprityDate: expiry_date };

  // export const _getStrickPriceVariables = () => {
  //     return {
  //         name: "NIFTY",
  //         exprityDate: "2023-02-09",
  //     };
  // };

  // Getting The Stricke Price List....
  // const getStrickePriceList = graphql(`
  //   query getStrickPrice($name: String!, $exprityDate: date!) {
  //     master_data(
  //       where: { name: { _eq: $name }, expiry: { _eq: $exprityDate } }
  //     ) {
  //       strike
  //       instrument_type
  //     }
  //   }
  // `);

  // getStrickePriceList.fetch({

  // });
  // let name = "NIFTY";
  // let exprityDate = "2023-02-09";

  // const data1 = getStrickePriceList({ name, exprityDate });

  // $: $fut_oi_scan?.fut_oi_scan, (currentTime = new Date());

  // let url = $page.route.id;

  // let items: oi_breakup[] = [];
  // items = intraday_oi_breakup;

  // ***********************Download Data***************************

  let tableHeader = [
    "symbol",
    "price",
    "price_15_min",
    "price_30_min",
    "price_1_hour",
    "price_change",
    "price_change_15_min",
    "price_change_30_min",
    "price_change_1_hour",
    "open_interest",
    "open_interest",
    "open_interest_15_min",
    "open_interest_30_min",
    "open_interest_1_hour",
    "open_interest_change",
    "open_interest_change_15_min",
    "open_interest_change_30_min",
    "open_interest_change_1_hour",
    "open_interest_change_per",
    "open_interest_change_per_15_min",
    "open_interest_change_per_1_hour",
    "open_interest_change_per_30_min"
  ];

  //   function downloaderData() {
  //     if ($fut_oi_scan?.fut_oi_scan_data) {
  //       tableData =
  //         // $fut_oi_scan?.fut_oi_scan_data;
  //         tableData =
  //           ($fut_oi_scan?.fut_oi_scan_data).map(
  //             (obj) => ({
  //               ...obj,
  //               Total_OI_Chg: parseFloat(0),
  //               Vwap: parseFloat(0),
  //               Iv: parseFloat(0),
  //             })
  //           );
  //     }
  //   }
  //   downloaderData();
  // ***********************Download Data***************************
</script>

<div class="container" style="width: 100%;">
  <!-- <TableTitle title="Options Intraday OI Breakup" /> -->

  <div class="d-flex" style="justify-content: end">
    <!-- ***********************Download Data*************************** -->
    <!-- <DataDownloader
        {tableData}
        {tableHeader}
        {downloaderData}
        fileName={`Options Intraday OI Breakup`}
      /> -->
    <!-- ***********************Download Data*************************** -->
  </div>

  <!-- FiltersInOneComponent Filters -->
  <FiltersInOneComponent
    bind:ComponentExportableVarialbes={ImportVariables}
    on:MenuComponentChangeEvent={filter_oi_breakup}
    ImportableComponentList={["ExpiryDate", "SortFilter", "BuildupIndicator"]}
    TableTitleFromPage={"Oi Interpretation"}
  />

  <!-- {#if $symbol?.data?.option_expiry}
        <SearchboxwithExpiry
            bind:current_expiry={expiry_date}
            bind:result={symbol_name}
            on:addSearchField={filter_oi_breakup}
            symbol_list={$symbol?.data?.option_expiry}
        />
  
        {#if variables}
            <StrikePrice bind:selected_strike={strike} stock_obj={variables} />
        {/if}
    {/if} -->

  <!-- <div class="filter_indicator">
        <div class="d-flex mb-3" style="justify-content:space-around;">
            {#if $symbol?.data?.option_expiry}
                <SearchboxwithExpiry
                    bind:current_expiry={expiry_date}
                    bind:result={symbol_name}
                    on:addSearchField={filter_oi_breakup}
                    symbol_list={$symbol?.data?.option_expiry}
                />
  
                {#if variables}
                    <StrikePrice
                        bind:selected_strike={strike}
                        stock_obj={variables}
                    />
                {/if}
            {/if} -->

  <!-- <div /> -->
  <!-- <BuildupIndicator /> -->
  <!-- <h1>{strike}</h1> -->
  <!-- </div>
    </div> -->

  <DataTable class="d-flex border border-color">
    <Head>
      <Row>
        <Cell colspan={2}>Symbol</Cell>
        <Cell>Price</Cell>
        <Cell>Price Change</Cell>
        <Cell>Price Change %</Cell>
        <Cell>Open Interest</Cell>
        <Cell>Open Interest Change</Cell>
        <Cell>Open Interest Change %</Cell>
        <Cell class="text-center">BIDP</Cell>
      </Row>
    </Head>
    <Body>
      {#if $fut_oi_scan?.data?.fut_oi_scan}
        {#each $fut_oi_scan?.data?.fut_oi_scan as oi_data}
          <Row>
            <Cell class="border border_color" rowspan={4}>{oi_data.symbol}</Cell
            >
            <Cell class="orange_text-color">Today</Cell>
            <Cell>{oi_data.price.toLocaleString(options)}</Cell>

            <ColoredCell
              value={oi_data.price_change == undefined ||
              isNaN(oi_data.price_change)
                ? 0
                : oi_data.price_change?.toLocaleString(options)}
            />
            <!-- <ColoredCell
              isPer={true}
              value={parseFloat(
                ((oi_data.price_change / oi_data.price) * 100)?.toFixed(4)
              )}
            /> -->

            <ColoredCell
              isPer={true}
              value={oi_data.price_change_per?.toFixed(4)}
            />

            <Cell>{oi_data.open_interest?.toLocaleString(options)}</Cell>
            <!-- <Cell
              class={oi_data.open_interest_change < 0
                ? "text-danger"
                : "text-success"}
              >{oi_data.open_interest_change?.toFixed(2)}</Cell
            > -->

            <ColoredCell
              value={oi_data.open_interest_change == undefined ||
              isNaN(oi_data.open_interest_change)
                ? 0
                : oi_data.open_interest_change?.toLocaleString(options)}
            />

            <ColoredCell
              isPer={true}
              value={oi_data.open_interest_change_per?.toFixed(4)}
            />

            <BuildUpStatus
              price_change={oi_data.price_change}
              oi_change={oi_data.open_interest_change}
            />
          </Row>
          <Row>
            <Cell class="text-light_pink">Last 15 Min</Cell>
            <Cell>{oi_data.price_15_min.toLocaleString(options)}</Cell>
            <ColoredCell
              value={oi_data.price_change_15_min == undefined ||
              isNaN(oi_data.price_change_15_min)
                ? 0
                : oi_data.price_change_15_min?.toLocaleString(options)}
            />
            <ColoredCell
              isPer={true}
              value={oi_data.price_change_per_15_min?.toFixed(4)}
            />

            <Cell>{oi_data.open_interest_15_min?.toLocaleString(options)}</Cell>
            <ColoredCell
              value={oi_data.open_interest_change_15_min == undefined ||
              isNaN(oi_data.open_interest_change_15_min)
                ? 0
                : oi_data.open_interest_change_15_min?.toLocaleString(options)}
            />
            <ColoredCell
              isPer={true}
              value={oi_data.open_interest_change_per_15_min?.toFixed(4)}
            />
            <BuildUpStatus
              price_change={oi_data.price_change_15_min}
              oi_change={oi_data.open_interest_change_15_min}
            />
          </Row>
          <Row>
            <Cell class="text-success">Last 30 Min</Cell>
            <Cell>{oi_data.price_30_min.toLocaleString(options)}</Cell>
            <ColoredCell
              value={oi_data.price_change_30_min == undefined ||
              isNaN(oi_data.price_change_30_min)
                ? 0
                : oi_data.price_change_30_min?.toLocaleString(options)}
            />

            <ColoredCell
              isPer={true}
              value={oi_data.price_change_per_30_min?.toFixed(4)}
            />
            <Cell>{oi_data.open_interest_30_min?.toLocaleString(options)}</Cell>
            <ColoredCell
              value={oi_data.open_interest_change_30_min == undefined ||
              isNaN(oi_data.open_interest_change_30_min)
                ? 0
                : oi_data.open_interest_change_30_min?.toLocaleString(options)}
            />
            <ColoredCell
              isPer={true}
              value={oi_data.open_interest_change_per_30_min?.toFixed(4)}
            />
            <BuildUpStatus
              price_change={oi_data.price_change_30_min}
              oi_change={oi_data.open_interest_change_30_min}
            />
          </Row>
          <Row>
            <Cell class="text-primary">Last 60 Min</Cell>
            <Cell>{oi_data.price_1_hour.toLocaleString(options)}</Cell>
            <ColoredCell
              value={oi_data.price_change_1_hour == undefined ||
              isNaN(oi_data.price_change_1_hour)
                ? 0
                : oi_data.price_change_1_hour?.toLocaleString(options)}
            />
            <ColoredCell
              isPer={true}
              value={oi_data.price_change_per_1_hour?.toFixed(4)}
            />

            <Cell>{oi_data.open_interest_1_hour?.toLocaleString(options)}</Cell>
            <ColoredCell
              value={oi_data.open_interest_1_hour == undefined ||
              isNaN(oi_data.open_interest_1_hour)
                ? 0
                : oi_data.open_interest_1_hour?.toLocaleString(options)}
            />
            <ColoredCell
              isPer={true}
              value={oi_data.open_interest_change_per_1_hour?.toFixed(4)}
            />

            <BuildUpStatus
              price_change={oi_data.price_change_1_hour}
              oi_change={oi_data.open_interest_change_1_hour}
            />
          </Row>
        {/each}
      {/if}
    </Body>
  </DataTable>
</div>

<style>
  .container {
    max-width: 95vw;
  }

  .datepicker {
    height: 35px;
    background-color: black;
    color: white;
    width: 200px;
  }
  input[type="date"]::-webkit-calendar-picker-indicator {
    filter: invert(1); /* Invert the color */
  }
</style>
