<script lang="ts">
  import DataTable, { Head, Body, Row, Label } from "@smui/data-table";
  import Cell from "@smui/data-table/src/Cell.svelte";
  // import { page } from "$app/stores";
  // import { onMount } from "svelte";
  // import SymbolExpiryFilter from "../../../components/Symbol_Expiry_filter.svelte";
  import TableTitle from "../../../components/TableTitle.svelte";
  // import SearchboxwithExpiry from "./../../../components/SearchboxwithExpiry.svelte";
  import FiltersInOneComponent from "./../../../components/FiltersInOneComponent.svelte";
  import { graphql } from "$houdini";
  import { onMount } from "svelte";

  let expiry_date;
  let symbol_name;
  let variables = { symbol: {}, date_expiry: {} };
  let ImportVariables = new Array();
  const options = {minimumFractionDigits: 2, maximumFractionDigits: 2};


  const ce_ohl_scanner = graphql(`
    subscription ce_ohl_scanner($symbol: String, $date_expiry: date) {
      ce_ohl_scanner(
        where: { symbol: { _eq: $symbol }, expiry: { _eq: $date_expiry } }
      ) {
        expiry
        high
        low
        open
        open_interest_change
        price
        price_change
        status
        strike
        symbol
        volume_change
      }
    }
  `);

  const pe_ohl_scanner = graphql(`
    subscription pe_ohl_scanner($symbol: String, $date_expiry: date) {
      pe_ohl_scanner(
        where: { symbol: { _eq: $symbol }, expiry: { _eq: $date_expiry } }
      ) {
        expiry
        high
        low
        open
        open_interest_change
        price
        price_change
        status
        strike
        symbol
        volume_change
      }
    }
  `);

  // onMount(() => {
  //     variables["symbol"] = `{${ImportVariables.symbol_name}}`;
  //     variables["date_expiry"] = `{${ImportVariables.expiry_date}}`;
  //     $: ce_ohl_scanner.listen(variables);
  //     $: pe_ohl_scanner.listen(variables);
  // });

  async function filter_ohl_scan() {
    variables["symbol"] = ImportVariables.symbol_name;
    variables["date_expiry"] = ImportVariables.expiry_date;
    $: ce_ohl_scanner.listen(variables);
    $: pe_ohl_scanner.listen(variables);

    // symbol_name = ImportVariables.symbol_name;
    // expiry_date = ImportVariables.expiry_date;
    // variables = { symbol: symbol_name, date_expiry: expiry_date };
    // variables["symbol"] = `{${ImportVariables.symbol}}`;
    // variables["date_expiry"] = `{${ImportVariables.expiry_date}}`;
    // $: ce_ohl_scanner.listen(variables);
    // $: pe_ohl_scanner.listen(variables);
    // $: openLow_puts.listen(variables);
    // $: openHigh_puts.listen(variables);
    // $: openLow_calls.listen(variables);
    // $: openHigh_calls.listen(variables);
  }
</script>


<div class="container-fluid" style="width: 100%;">
  <div class="d-flex" style="justify-content: end">
    <!-- ***********************Download Data*************************** -->
    <!-- <DataDownloader
      {tableData}
      {tableHeader} 
      {downloaderData}
      fileName={`Options Chain`} /> -->
    <!-- ***********************Download Data*************************** -->
  </div>

  <!-- FiltersInOneComponent Filters -->
  <FiltersInOneComponent
    bind:ComponentExportableVarialbes={ImportVariables}
    on:MenuComponentChangeEvent={filter_ohl_scan}
    ImportableComponentList={["SearchboxwithExpiry"]}
    TableTitleFromPage={"Options Open-High / Open-Low Scan"}

    IsOptionSearchBoxAndExpiry="true"
  />
  <!-- <div class="filter_indicator"> 
    <div class="d-flex mb-3" style="justify-content:space-around;">
            {#if $symbol?.data?.option_expiry}
            <SearchboxwithExpiry bind:current_expiry={expiry_date} bind:result={symbol_name} on:addSearchField={filter_ohl_scan} symbol_list = {$symbol?.data?.option_expiry}/>
            {/if}
      </div>
  </div> -->

  <!-- Open High -->
  <DataTable style="width: 100%; color: white; ">
    <Head>
      <Row>
        <Cell style="text-align: center;background:transparent;color:white"
          >Open-High</Cell
        >
      </Row>
    </Head>
  </DataTable>

  <div class="d-flex" style="width: 100%;">
    <div style="width: 50%;">
      <DataTable class="col-12">
        <Head>
          <Row>
            <Cell style=" text-align: center;">Call</Cell>
          </Row>
        </Head>
      </DataTable>
    </div>
    <div style="width: 50%; margin-left: 2%;">
      <DataTable class="col-12">
        <Head>
          <Row>
            <Cell style="text-align: center;"
              >Put</Cell
            >
          </Row>
        </Head>
      </DataTable>
    </div>
  </div>

  <div style="display: flex; overflow-y: hidden;">
    <!-- open-high value scanner table -->

    <DataTable
      stickyHeader
      style="width: 50%; height: 65vh; overflow-y: auto; background-color: transparent !important;"
      class="me-3"
    >
      <Head>
        <Row>
          <Cell class="fixed-col">Symbol</Cell>
          <Cell>Open</Cell>
          <Cell>High</Cell>
          <!-- <Cell>Latest High</Cell> -->
          <Cell>LTP</Cell>
          <Cell>Change</Cell>
          <Cell numeric columnId="price_change_per">
            <!-- <IconButton class="material-icons">arrow_upward</IconButton> -->
            <Label>Change%</Label>
          </Cell>
        </Row>
      </Head>
      <Body>
        {#if $ce_ohl_scanner?.data?.ce_ohl_scanner}
          {#each $ce_ohl_scanner?.data?.ce_ohl_scanner as item}
            {#if item.status != "high"}
              <Row>
                <Cell
                  >{item.symbol + "-" + item.strike + "-C-" + item.expiry}</Cell
                >
                <Cell>{item.open?.toFixed(2)}</Cell>
                <Cell>{item.high?.toFixed(2)}</Cell>
                <Cell>{item.price?.toLocaleString(options)}</Cell>
                <Cell>{item.price_change?.toFixed(2)}</Cell>
                <Cell numeric>{item.price_change?.toFixed(2)}</Cell>
              </Row>
            {/if}
          {/each}
        {/if}
      </Body>
    </DataTable>
    <!-- open-low value scanner table -->

    <DataTable
      stickyHeader
      style="width: 50%;  height: 65vh; overflow-y: auto; background-color: transparent !important;"
    >
      <Head>
        <Row>
          <Cell sortable={false}>Symbol</Cell>
          <Cell>Open</Cell>
          <Cell>High</Cell>
          <!-- <Cell>Latest Low</Cell> -->
          <Cell>LTP</Cell>
          <Cell>Change</Cell>
          <!-- <Cell columnId="price_change_per"> -->
          <!-- <IconButton class="material-icons"
                            >arrow_upward</IconButton
                        > -->
          <!-- <Label>Change%</Label> -->
          <!-- </Cell> -->
          <Cell>Change%</Cell>
        </Row>
      </Head>
      <Body>
        {#if $ce_ohl_scanner?.data?.ce_ohl_scanner}
          {#each $ce_ohl_scanner?.data?.ce_ohl_scanner as item}
            {#if item.status != "high"}
              <Row>
                <Cell
                  >{item.symbol + "-" + item.strike + "-C-" + item.expiry}</Cell
                >
                <Cell>{item.open?.toFixed(2)}</Cell>
                <Cell>{item.high?.toFixed(2)}</Cell>
                <Cell>{item.price?.toLocaleString(options)}</Cell>
                <Cell>{item.price_change?.toFixed(2)}</Cell>
                <Cell numeric>{item.price_change?.toFixed(2)}</Cell>
              </Row>
            {/if}
          {/each}
        {/if}
      </Body>
    </DataTable>
  </div>

  <DataTable
    style="width: 100%; color: white; align-items: center; margin-top: 1%;"
  >
    <Head>
      <Row>
        <Cell style="text-align: center;background:transparent;color:white">Open-Low</Cell>
      </Row>
    </Head>
  </DataTable>

  <!-- Open LOW -->
  <div class="d-flex" style="width: 100%;">
    <div style="width: 50%;">
      <DataTable class="col-12">
        <Head>
          <Row>
            <Cell style=" text-align: center;">Call</Cell>
          </Row>
        </Head>
      </DataTable>
    </div>
    <div style="width: 50%; margin-left: 2%;">
      <DataTable class="col-12">
        <Head>
          <Row>
            <Cell style="text-align: center;">Put</Cell>
          </Row>
        </Head>
      </DataTable>
    </div>
  </div>

  <div style="display: flex; overflow-y: hidden;">
    <!-- open-high value scanner table -->

    <DataTable
      stickyHeader
      style="width: 50%; height: 65vh; overflow-y: auto; background-color: transparent !important;"
      class="me-3"
    >
      <Head>
        <Row>
          <Cell class="fixed-col">Symbol</Cell>
          <Cell>Open</Cell>
          <Cell>High</Cell>
          <!-- <Cell>Latest High</Cell> -->
          <Cell>LTP</Cell>
          <Cell>Change</Cell>
          <Cell numeric columnId="price_change_per">
            <!-- <IconButton class="material-icons">arrow_upward</IconButton> -->
            <Label>Change%</Label>
          </Cell>
        </Row>
      </Head>
      <Body>
        {#if $ce_ohl_scanner?.data?.ce_ohl_scanner}
          {#each $ce_ohl_scanner?.data?.ce_ohl_scanner as item}
            {#if item.status != "low"}
              <Row>
                <Cell
                  >{item.symbol + "-" + item.strike + "-C-" + item.expiry}</Cell
                >
                <Cell>{item.open?.toLocaleString(options)}</Cell>
                <Cell>{item.high?.toLocaleString(options)}</Cell>
                <Cell>{item.price?.toLocaleString(options)}</Cell>
                <Cell>{item.price_change?.toLocaleString(options)}</Cell>
                <Cell numeric>{item.price_change?.toFixed(2)}</Cell>
              </Row>
            {/if}
          {/each}
        {/if}
      </Body>
    </DataTable>
    <!-- open-low value scanner table -->

    <DataTable
      stickyHeader
      style="width: 50%;  height: 65vh; overflow-y: auto; background-color: transparent !important;"
    >
      <Head>
        <Row>
          <Cell sortable={false}>Symbol</Cell>
          <Cell>Open</Cell>
          <Cell>High</Cell>
          <!-- <Cell>Latest Low</Cell> -->
          <Cell>LTP</Cell>
          <Cell>Change</Cell>
          <Cell>Change%</Cell>
        </Row>
      </Head>
      <Body>
        {#if $ce_ohl_scanner?.data?.ce_ohl_scanner}
          {#each $ce_ohl_scanner?.data?.ce_ohl_scanner as item}
            {#if item.status != "low"}
              <Row>
                <Cell
                  >{item.symbol + "-" + item.strike + "-C-" + item.expiry}</Cell
                >
                <Cell>{item.open?.toLocaleString(options)}</Cell>
                <Cell>{item.high?.toLocaleString(options)}</Cell>
                <Cell>{item.price?.toLocaleString(options)}</Cell>
                <Cell>{item.price_change?.toLocaleString(options)}</Cell>
                <Cell numeric>{item.price_change?.toFixed(2)}</Cell>
              </Row>
            {/if}
          {/each}
        {/if}
      </Body>
    </DataTable>
  </div>
</div>
