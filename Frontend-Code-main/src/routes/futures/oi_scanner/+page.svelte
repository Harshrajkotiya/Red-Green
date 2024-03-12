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
  // let currentTime;F
  let variables;
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

  // const options_intraday_oi_breakup = graphql(`
  //   subscription Get_scan_data($symbol: _varchar!, $date_expiry: date) {
  //     fut_oi_scan(
  //       where: { symbol: { _eq: $symbol }, expiry: { _eq: $date_expiry } }
  //     ) {
  //       symbol
  //       ltp
  //       ltp_15_min
  //       ltp_30_min
  //       ltp_60_min
  //       price_change
  //       price_change_15_min
  //       price_change_30_min
  //       price_change_60_min
  //       open_interest
  //       open_interest_15_min
  //       open_interest_30_min
  //       open_interest_60_min
  //       open_interest_change
  //       open_interest_change_15_min
  //       open_interest_change_30_min
  //       open_interest_change_60_min
  //     }
  //   }
  // `);

  // variables = { symbol: symbol_name, date_expiry: expiry_date };
  $: options_intraday_oi_breakup.listen(variables);

  onMount(() => {
    symbol_name = ["NIFTY"];
    variables = {
      symbol: "{%" + symbol_name + "%}",
      date_expiry: "{" + expiry_date[0] + "}",
    };
    console.log("The Mounted Variables OI :- ", variables);
    $: options_intraday_oi_breakup.listen(variables);
  });

  // $: options_intraday_oi_breakup.listen(variables);

  async function filter_oi_breakup() {
    // strike = "";
    symbol_name = ImportVariables.symbol_name;
    expiry_date = ImportVariables.expiry_date;
    variables = {
      symbol: "{" + symbol_name + "}",
      date_expiry: "{" + expiry_date[0] + "}",
    };
    console.log(variables);
    $: options_intraday_oi_breakup.listen(variables);
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

  // $: $options_intraday_oi_breakup?.fut_oi_scan, (currentTime = new Date());

  // let url = $page.route.id;

  // let items: oi_breakup[] = [];
  // items = intraday_oi_breakup;

  // ***********************Download Data***************************

  let tableHeader = [
    "symbol",
    "ltp",
    "ltp_15_min",
    "ltp_30_min",
    "ltp_60_min",
    "price_change",
    "price_change_15_min",
    "price_change_30_min",
    "price_change_60_min",
    "open_interest",
    "open_interest",
    "open_interest_15_min",
    "open_interest_30_min",
    "open_interest_60_min",
    "open_interest_change",
    "open_interest_change_15_min",
    "open_interest_change_30_min",
    "open_interest_change_60_min",
  ];

  function downloaderData() {
    if ($options_intraday_oi_breakup?.options_intraday_oi_breakup_data) {
      tableData =
        // $options_intraday_oi_breakup?.options_intraday_oi_breakup_data;
        tableData =
          ($options_intraday_oi_breakup?.options_intraday_oi_breakup_data).map(
            (obj) => ({
              ...obj,
              Total_OI_Chg: parseFloat(0),
              Vwap: parseFloat(0),
              Iv: parseFloat(0),
            })
          );
    }
  }
  downloaderData();
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
    tableData={$options_intraday_oi_breakup?.fut_oi_scan}
    {tableHeader}
    isDownloadableData={false}
    fileName={`Futures OI Interpretation_${expiry_date}`}
    ImportableComponentList={[
      "SearchboxwithExpiry",
      // "BuildupIndicator",
      // "StrikePrice",
    ]}
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
        <Cell class="text-wrap" colspan={2}>Symbol</Cell>
        <Cell class="text-wrap">Price</Cell>
        <Cell class="text-wrap">Price Change</Cell>
        <Cell class="text-wrap">Price Change %</Cell>
        <Cell class="text-wrap">Open Interest</Cell>
        <Cell class="text-wrap">Open Interest Change</Cell>
        <Cell class="text-wrap">Open Interest Change %</Cell>
        <Cell class="text-wrap">BIDP</Cell>
      </Row>
    </Head>
    <Body>
      {#if $options_intraday_oi_breakup?.fut_oi_scan}
        {#each $options_intraday_oi_breakup?.fut_oi_scan as oi_data}
          <Row>
            <Cell class="border border_color" rowspan={4}>{oi_data.symbol}</Cell
            >
            <Cell class="orange_text-color">Today</Cell>
            <Cell>{oi_data.ltp}</Cell>
            <ColoredCell
              value={oi_data.price_change == undefined ||
              isNaN(oi_data.price_change)
                ? 0
                : oi_data.price_change?.toFixed(2)}
            />

            <Cell
              class={(oi_data.price_change / oi_data.ltp) * 100 < 0
                ? "text-danger"
                : "text-success"}
              >{((oi_data.price_change / oi_data.ltp) * 100)?.toFixed(2)}</Cell
            >

            <Cell>{oi_data.open_interest?.toFixed(2)}</Cell>
            <Cell
              class={oi_data.open_interest_change < 0
                ? "text-danger"
                : "text-success"}
              >{oi_data.open_interest_change?.toFixed(2)}</Cell
            >
            <Cell
              class={(oi_data.open_interest_change / oi_data.open_interest) *
                100 <
              0
                ? "text-danger"
                : "text-success"}
              >{(
                (oi_data.open_interest_change / oi_data.open_interest) *
                100
              )?.toFixed(2)}</Cell
            >
            <BuildUpStatus
              price_change={oi_data.price_change}
              oi_change={oi_data.open_interest_change}
            />
          </Row>
          <Row>
            <Cell class="text-light_pink">Last 15 Min</Cell>
            <Cell>{oi_data.ltp_15_min}</Cell>
            <Cell
              class={oi_data.price_change_15_min < 0
                ? "text-danger"
                : "text-success"}
              >{oi_data.price_change_15_min?.toFixed(2)}</Cell
            >
            <Cell
              class={(oi_data.price_change_15_min / oi_data.ltp_15_min) * 100 <
              0
                ? "text-danger"
                : "text-success"}
              >{(
                (oi_data.price_change_15_min / oi_data.ltp_15_min) *
                100
              )?.toFixed(2)}</Cell
            >
            <Cell>{oi_data.open_interest_15_min?.toFixed(2)}</Cell>

            <Cell
              class={oi_data.open_interest_change_15_min < 0
                ? "text-danger"
                : "text-success"}
              >{oi_data.open_interest_change_15_min?.toFixed(2)}</Cell
            >

            <Cell
              class={(oi_data.open_interest_change_15_min /
                oi_data.open_interest_15_min) *
                100 <
              0
                ? "text-danger"
                : "text-success"}
              >{(
                (oi_data.open_interest_change_15_min /
                  oi_data.open_interest_15_min) *
                100
              )?.toFixed(2)}</Cell
            >
            <BuildUpStatus
              price_change={oi_data.price_change_15_min}
              oi_change={oi_data.open_interest_change_15_min}
            />
          </Row>
          <Row>
            <Cell class="text-success">Last 30 Min</Cell>
            <Cell>{oi_data.ltp_30_min}</Cell>
            <Cell
              class={oi_data.price_change_30_min < 0
                ? "text-danger"
                : "text-success"}
              >{oi_data.price_change_30_min?.toFixed(2)}</Cell
            >
            <Cell
              class={(oi_data.price_change_30_min / oi_data.ltp_30_min) * 100 <
              0
                ? "text-danger"
                : "text-success"}
              >{(
                (oi_data.price_change_30_min / oi_data.ltp_30_min) *
                100
              )?.toFixed(2)}</Cell
            >
            <Cell>{oi_data.open_interest_30_min?.toFixed(2)}</Cell>
            <Cell
              class={oi_data.open_interest_change_30_min < 0
                ? "text-danger"
                : "text-success"}
              >{oi_data.open_interest_change_30_min?.toFixed(2)}</Cell
            >

            <Cell
              class={(oi_data.open_interest_change_30_min /
                oi_data.open_interest_30_min) *
                100 <
              0
                ? "text-danger"
                : "text-success"}
              >{(
                (oi_data.open_interest_change_30_min /
                  oi_data.open_interest_30_min) *
                100
              )?.toFixed(2)}</Cell
            >
            <BuildUpStatus
              price_change={oi_data.price_change_30_min}
              oi_change={oi_data.open_interest_change_30_min}
            />
          </Row>
          <Row>
            <Cell class="text-primary">Last 60 Min</Cell>
            <Cell>{oi_data.ltp_60_min}</Cell>
            <Cell
              class={oi_data.price_change_60_min < 0
                ? "text-danger"
                : "text-success"}
              >{oi_data.price_change_60_min?.toFixed(2)}</Cell
            >
            <Cell
              class={(oi_data.price_change_60_min / oi_data.ltp_60_min) * 100 <
              0
                ? "text-danger"
                : "text-success"}
              >{(
                (oi_data.price_change_60_min / oi_data.ltp_60_min) *
                100
              )?.toFixed(2)}</Cell
            >
            <Cell>{oi_data.open_interest_60_min?.toFixed(2)}</Cell>
            <Cell
              class={oi_data.open_interest_change_60_min < 0
                ? "text-danger"
                : "text-success"}
              >{oi_data.open_interest_change_60_min?.toFixed(2)}</Cell
            >

            <Cell
              class={(oi_data.open_interest_change_60_min /
                oi_data.open_interest_60_min) *
                100 <
              0
                ? "text-danger"
                : "text-success"}
              >{(
                (oi_data.open_interest_change_60_min /
                  oi_data.open_interest_60_min) *
                100
              )?.toFixed(2)}</Cell
            >
            <BuildUpStatus
              price_change={oi_data.price_change_60_min}
              oi_change={oi_data.open_interest_change_60_min}
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
