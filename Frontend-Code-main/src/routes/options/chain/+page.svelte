<script lang="ts">
  //import Button from "@smui/button";
  import { onMount } from "svelte";
  import DataTable, { Head, Body, Row, Cell } from "@smui/data-table";
  import { page } from "$app/stores";
  import { graphql } from "$houdini";
  import TableTitle from "../../../components/TableTitle.svelte";
  import BuildUpStatus from "../../../components/BuildUpStatus.svelte";

  import FiltersInOneComponent from "./../../../components/FiltersInOneComponent.svelte";
  import ColoredCell from "../../../components/ColoredCell.svelte";
  // import SearchboxwithExpiry from "./../../../components/SearchboxwithExpiry.svelte";
  // import BuildupIndicator from "../../../components/Buildup_indicator.svelte";
  // import DataDownloader from "../../../components/DataDownloader.svelte";

  let url = $page.route.id;
  let currentTime;
  let tableData = [];
  let variables ={symbol: "", date_expiry:""};
  let expiry_date;
  let symbol_name;
  let ImportVariables = new Array();
  const options = {minimumFractionDigits: 2, maximumFractionDigits: 2};



  const option_chain = graphql(`
    subscription Option_chain($symbol: String, $date_expiry:date ) {
      options_chain(limit: 100 where: {symbol: {_eq: $symbol}, expiry: {_eq: $date_expiry}}){
    bucket
    ce_high
    ce_low
    ce_open
    ce_open_interest
    ce_open_interest_change
    ce_price
    ce_price_change
    ce_volume
    ce_volume_change
    expiry
    pe_high
    pe_low
    pe_open
    pe_open_interest
    pe_open_interest_change
    pe_price
    pe_price_change
    pe_volume
    pe_volume_change
    strike
    symbol
  }
    }
  `);

// $: option_chain.listen();


//   $: $option_chain?.options_chain, (currentTime = new Date());

  // onMount( async () => {
  //   await ImportVariables.symbol_name
  //   await ImportVariables.expiry_date
  //   variables["symbol"] =  `{${ImportVariables.symbol_name}}`;
  //   variables["date_expiry"] = `{${ImportVariables.expiry_date}}`;
  //   // variables = { symbol: symbol_name, date_expiry: expiry_date };
  //   $: option_chain.listen(variables);
  //   console.log(variables);
  // });

  async function filter_oi_chain() {
    
    console.log(ImportVariables);
    // variables["symbol"] = "{"+ImportVariables.symbol_name+"}";
    // variables["date_expiry"] = "{"+ImportVariables.expiry_date+"}";
    variables = { symbol: ImportVariables.symbol_name, date_expiry: ImportVariables.expiry_date };
    $: option_chain.listen(variables);
  }

//   variables = { symbol: symbol_name, date_expiry: expiry_date };

  // ***********************Download Data***************************

  let tableHeader = [
    "ce_build_up_status",
    "ce_trend",
    "es_time_field",
    "ce_oi_chg",
    "ce_oi",
    "ce_volume",
    "ce_ltp",
    "ce_strike_price",
    "pe_ltp",
    "pe_volume",
    "pe_oi",
    "pe_oi_chg",
    "pcr_oi",
    "pcr_volume",
    "ps_time_field",
    "pe_trend",
    "pe_build_up_status",
    "ce_change_pts",
    "pe_change_pts",
  ];
  // function downloaderData() {
  //   if ($option_chain?.options_chain) {
  //     tableData = $option_chain?.options_chain;
  //     // tableData = ($option_chain?.options_chain).map((obj) => ({
  //     //   ...obj,
  //     //   pe_change_pts: parseFloat(0),ce_change_pts: parseFloat(0)
  //     // }));
  //   }
  // }
  // downloaderData();
  // ***********************Download Data***************************
</script>

<div class="container-fluid" style="width: 100%;">
  <!-- <TableTitle  /> -->
  <div class="d-flex" style="justify-content: end">
    <!-- ***********************Download Data*************************** -->
    <!-- <DataDownloader
      {tableData}
      {tableHeader}
      {downloaderData}
      fileName={`Options Chain`}
        /> -->
    <!-- ***********************Download Data*************************** -->
  </div>
  <!-- FiltersInOneComponent Filters -->
  <FiltersInOneComponent
    bind:ComponentExportableVarialbes={ImportVariables}
    on:MenuComponentChangeEvent={filter_oi_chain}
    tableData={$option_chain?.options_chain}
    ImportableComponentList={["SearchboxwithExpiry","BuildupIndicator"]}
    TableTitleFromPage={"Options Chain"}
    IsOptionSearchBoxAndExpiry="true"
  />

  <!-- <div class="filter_indicator">
        <div class="d-flex mb-3" style="justify-content:space-around;">
            {#if $symbol?.data?.option_expiry}
                <SearchboxwithExpiry
                    bind:current_expiry={expiry_date}
                    bind:result={symbol_name}
                    on:addSearchField={filter_oi_chain}
                    symbol_list={$symbol?.data?.option_expiry}
                />
            {/if}
        </div>

        <BuildupIndicator />
    </div> -->

  <div class="d-flex">
    <DataTable style="width: 49.5%;">
      <Head>
        <Row>
          <Cell colSpan= '8' style="text-align: center;background:transparent;color:white">Calls</Cell>
        </Row>
        <Row>
          <Cell>Build Up</Cell>
          <!-- <Cell>Trend</Cell> -->
          <Cell>Time</Cell>
          <Cell>OI Chg</Cell>
          <Cell>OI</Cell>
          <Cell>Volume</Cell>
          <Cell>Chg(pts)</Cell>
          <Cell>LTP</Cell>
          <Cell>Strike Price</Cell>
        </Row>
      </Head>
      <Body>
        {#if $option_chain?.data?.options_chain}
          {#each $option_chain?.data?.options_chain as item}
            <Row>
              <BuildUpStatus price_change={item.ce_price_change} oi_change= {item.ce_open_interest}  />
              <!-- <Cell>{item.ce_trend}</Cell> -->
              <Cell
                >{new Date(item.bucket).toLocaleTimeString(
                  "en-GB"
                )}</Cell
              >
              <Cell>{item.ce_open_interest_change.toLocaleString(options)}</Cell>
              <Cell>{item.ce_open_interest.toLocaleString(options)}</Cell>
              <Cell>{item.ce_volume.toLocaleString(options)}</Cell>
              <Cell>{item.ce_price_change.toLocaleString(options)}</Cell>
              <Cell>{item.ce_price.toLocaleString(options)}</Cell>
              <Cell>{item.strike.toLocaleString(options)}</Cell>
            </Row>
          {/each}
        {/if}
      </Body>
    </DataTable>
    <DataTable style="width: 49.5%; margin-left: 1%;">
      <Head>
        <Row>
          <Cell colSpan= '7' style="text-align: center;background:transparent;color:white">Puts</Cell>
        </Row>
        <Row>
       
          <Cell>LTP</Cell>
          <Cell>Chg(pts)</Cell>
          <Cell>Volume</Cell>
          <Cell>OI</Cell>
          <Cell>OI Chg</Cell>
          <!-- <Cell>PCR-OI</Cell> -->
          <!-- <Cell>PCR-Vol</Cell> -->
          <Cell>Time</Cell>
          <!-- <Cell>Trend</Cell> -->
          <Cell>Build Up</Cell>
        </Row>
      </Head>
      <Body>
        {#if $option_chain?.data?.options_chain}
          {#each $option_chain?.data?.options_chain as item}
            <Row>
             
              <Cell>{item.pe_price.toLocaleString(options)}</Cell>
              <Cell>{item.pe_price_change.toLocaleString(options)}</Cell>
              <Cell>{item.pe_volume_change.toLocaleString(options)}</Cell>
              <Cell>{item.pe_open_interest.toLocaleString(options)}</Cell>
              <Cell>{item.pe_open_interest_change.toLocaleString(options)}</Cell>
             
              <Cell
              >{new Date(item.bucket).toLocaleTimeString(
                "en-GB"
              )}</Cell
            >
              <!-- <Cell>{item.pe_trend}</Cell> -->
              <BuildUpStatus price_change={item.pe_price_change} oi_change= {item.pe_open_interest_change}  />
            </Row>
          {/each}
        {/if}
      </Body>
    </DataTable>
  </div>
</div>

<style>
  .filter_indicator {
    display: flex;
    justify-content: space-around;
  }
</style>
