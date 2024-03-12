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
    let sort_obj 
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
  
    async function filter_oi_breakup() {
      interval_obj = ImportVariables.interval_obj;
      // console.log(interval_obj);
  
      switch (interval_obj) {
        case "5_min":
          GetintradayData = graphql(`
            subscription oiBreak_ce_5_min($date_expiry: date, $symbol: String $order_column:p2_opt_ce_today_5_min_order_by!) {
                option_ce_data: p2_opt_ce_today_5_min(
                where: { symbol: { _eq: $symbol }, expiry: { _eq: $date_expiry } }
                order_by: [$order_column]
              ) {
                bucket
                open_interest
                open_interest_change
                price
                price_change
                volume
              }
            }
          `);
          break;
  
        case "15_min":
          GetintradayData = graphql(`
            subscription oiBreak_ce_15_min($date_expiry: date, $symbol: String $order_column:p2_opt_ce_today_15_min_order_by!) {
                option_ce_data: p2_opt_ce_today_15_min(
                where: { symbol: { _eq: $symbol }, expiry: { _eq: $date_expiry } }
                order_by: [$order_column]
              ) {
                bucket
                open_interest
                open_interest_change
                price
                price_change
                volume
              }
            }
          `);
          break;
  
        case "30_min":
          GetintradayData = graphql(`
            subscription oiBreak_ce_30_min($date_expiry: date, $symbol: String  $order_column:p2_opt_ce_today_30_min_order_by!) {
                option_ce_data: p2_opt_ce_today_30_min(
                where: { symbol: { _eq: $symbol }, expiry: { _eq: $date_expiry } }
                order_by: [$order_column]
              ) {
                bucket
                open_interest
                open_interest_change
                price
                price_change
                volume
              }
            }
          `);
          break;
  
        case "1_hour":
          GetintradayData = graphql(`
            subscription oiBreak_ce_1_hour($date_expiry: date, $symbol: String, $order_column:p2_opt_ce_today_1_hour_order_by!) {
                option_ce_data: p2_opt_ce_today_1_hour(
                where: { symbol: { _eq: $symbol }, expiry: { _eq: $date_expiry } }
                order_by: [$order_column]
              ) {
                bucket
                open_interest
                open_interest_change
                price
                price_change
                volume
              }
            }
          `);
          break;
  
        default:
          GetintradayData = graphql(`
            subscription oiBreak_ce_3_min(
              $date_expiry: date
              $order_column: p2_opt_ce_today_3_min_order_by!
              $symbol: String
            ) {
              option_ce_data: p2_opt_ce_today_3_min(
                where: { symbol: { _eq: $symbol }, expiry: { _eq: $date_expiry } }
                order_by: [$order_column]
              ) {
                bucket
                open_interest
                open_interest_change
                price
                price_change
                volume
              }
            }
          `);
          break;
      }
      sort_obj = ImportVariables.sort_obj;
      symbol_name = ImportVariables.symbol_name;
      expiry_date = ImportVariables.expiry_date;
      variables = {
        date_expiry:  expiry_date,
        symbol: symbol_name ,
        order_column:{}
      };
      
      variables["order_column"][sort_obj] = "asc";
  
      // $: GetintradayData.listen(variables);
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
  

<!-- <TableTitle title="Options Intraday OI Breakup" /> -->

<div class="container" style="width: 100%;">
    <!-- FiltersInOneComponent Filters -->
    <FiltersInOneComponent
        bind:ComponentExportableVarialbes={ImportVariables}
        on:MenuComponentChangeEvent={filter_oi_breakup}
        ImportableComponentList={[
            "SearchboxwithExpiry",
            "BuildupIndicator",
            "StrikePrice",
        ]}
    />

    <DataTable class="d-flex border border-color">
        <Head>
            <Row>
                <Cell class="text-wrap">Time</Cell>
                <Cell class="text-wrap">OI</Cell>
                <Cell class="text-wrap">OI Chg</Cell>
                <Cell class="text-wrap">OI Chg%</Cell>
                <Cell class="text-wrap">Price</Cell>
                <Cell class="text-wrap">Price Chg</Cell>
                <Cell class="text-wrap">Volume</Cell>
                <Cell class="text-wrap">BIDP</Cell>
                <Cell class="text-wrap">PCR</Cell>
                <Cell class="text-wrap">Total OI</Cell>
                <Cell class="text-wrap">Total Price</Cell>
                <Cell class="text-wrap">OI</Cell>
                <Cell class="text-wrap">OI Chg</Cell>
                <Cell class="text-wrap">OI Chg%</Cell>
                <Cell class="text-wrap">Price</Cell>
                <Cell class="text-wrap">Price Chg</Cell>
                <Cell class="text-wrap">Volume</Cell>
                <Cell class="text-wrap">BIDP</Cell>
            </Row>
        </Head>
        <Body>
            <!-- {#if $options_intraday_oi_breakup?.p2_pe_ce_details}
                {#each $options_intraday_oi_breakup?.p2_pe_ce_details as oi_data}
                    <Row>
                        <Cell
                            >{new Date(oi_data.bucket)
                                .toISOString()
                                .slice(11, 16)}</Cell
                        >
                        <Cell>{oi_data.ce_oi?.toFixed(2)}</Cell>
                        <Cell>{oi_data.ce_oi_chg?.toFixed(2)}</Cell>
                        <Cell
                            >{(
                                (oi_data.ce_oi_chg / oi_data.ce_oi) *
                                100
                            )?.toFixed(2)}</Cell
                        >

                        <Cell class="red-color"
                            >{oi_data.ce_price?.toFixed(2)}</Cell
                        >
                        <Cell>{oi_data.ce_price_chg?.toFixed(2)}</Cell>
                        <Cell>{oi_data.ce_volume?.toFixed(2)}</Cell>
                        <BuildUpStatus
                            price_change={oi_data.ce_price_chg}
                            oi_change={oi_data.ce_oi_chg}
                        />
                        <Cell class="yellow-color border-1 text-dark font-bold"
                            >{(oi_data.pe_oi / oi_data.ce_oi)?.toFixed(2)}</Cell
                        >
                        <Cell class="yellow-color border-1 text-dark font-bold"
                            >{(oi_data.pe_oi + oi_data.ce_oi)?.toFixed(2)}</Cell
                        >
                        <Cell class="yellow-color border-1 text-dark font-bold"
                            >{(oi_data.pe_price + oi_data.ce_price)?.toFixed(
                                2
                            )}</Cell
                        >
                        <Cell>{oi_data.pe_oi?.toFixed(2)}</Cell>
                        <Cell>{oi_data.pe_oi_chg?.toFixed(2)}</Cell>
                        <Cell
                            >{(
                                (oi_data.pe_oi_chg / oi_data.pe_oi) *
                                100
                            )?.toFixed(2)}</Cell
                        >

                        <Cell class="green-color"
                            >{oi_data.pe_price?.toFixed(2)}</Cell
                        >
                        <Cell>{oi_data.pe_price_chg?.toFixed(2)}</Cell>
                        <Cell>{oi_data.pe_volume?.toFixed(2)}</Cell>
                        <BuildUpStatus
                            price_change={oi_data.pe_price_chg}
                            oi_change={oi_data.pe_oi_chg}
                        />
                    </Row>
                {/each}
            {/if} -->
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