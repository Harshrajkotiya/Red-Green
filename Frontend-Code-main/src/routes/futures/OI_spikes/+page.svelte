<script lang="ts">
  import SearchboxSymbol from "../../../components/SearchboxSymbol.svelte";
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
  import SortFilter from "../../../components/SortFilter.svelte";
  import ExpiryDate from "../../../components/ExpiryDate.svelte";
  import TableTitle from "../../../components/TableTitle.svelte";
  //   import DataDownloader from "../../../components/DataDownloader.svelte";
  import FiltersInOneComponent from "./../../../components/FiltersInOneComponent.svelte";
  import ColoredCell from "../../../components/ColoredCell.svelte";
  import CellWithProgress from "../../../components/CellWithProgress.svelte";

  let sort = "price_change";
  let symbol_name;
  // let expiry_date;
  let search_object = "";
  let currentTime;
  // let expiry_date = "";
  let variables = { ExpiryDate: {} };

  let ImportVariables = new Array();
  const options = { minimumFractionDigits: 2, maximumFractionDigits: 2 };

  //   const sort_field_list = [
  //     { name: "volume_change_per", label: "Volume Change %" },
  //     { name: "price_change_per", label: "Price Change %" },
  //     { name: "open_interest_change_per", label: "OI Change %" },
  //     { name: "symbol", label: "Symbol" },
  //     { name: "open_interest", label: "OI" },
  //     { name: "open_interest_change", label: "OI Change" },
  //     { name: "close", label: "Price" },
  //     { name: "volume", label: "Volume" },
  //     { name: "volume_change_per", label: "Volume Change %" },
  //   ];

  //   const expiry = graphql(`
  //     query GetfeaturesEdatespikes {
  //       future_expiry(distinct_on: expiry, order_by: { expiry: asc }) {
  //         expiry
  //       }
  //     }
  //   `);

  const spikes = graphql(`
    subscription GetSpikes(
      $ExpiryDate: date
      $order_column: today_fut_1_day_order_by!
    ) {
      today_fut_1_day(
        where: { expiry: { _eq: $ExpiryDate } }
        order_by: [$order_column]
      ) {
        expiry
        open_interest
        open_interest_change
        price
        volume
        price_change
        symbol
        volume_change
        price_change_per
        open_interest_change_per
        volume_change_per
      }
    }
  `);

  // $: spikes.listen();

  // const spikes = graphql(`
  //     subscription GetSpikes(
  //         $sort_object: features_order_by!
  //         $date_expiry: date
  //         $search_symbol: String!
  //     ) {
  //         features(
  //             order_by: [$sort_object]
  //             where: {
  //                 expiry: { _eq: $date_expiry }
  //                 name: { _ilike: $search_symbol }
  //             }
  //         ) {
  //             name
  //             close
  //             price_change
  //             price_change_per
  //             open_interest
  //             open_interest_change
  //             open_interest_change_per
  //             open_interest_change_value
  //             volume
  //             volume_change_per
  //         }
  //     }
  // `);

  //   variables.sort_object[sort_obj] = "desc";
  //   variables["date_expiry"] = expiry_date;
  //   variables["search_symbol"] = "%%";

  onMount(() => {
    // variables = { sort_object: {} };
    // variables.sort_object[sort_obj] = "desc";
    // variables["date_expiry"] = expiry_date;
    // variables["search_symbol"] = "%%";
    // $: spikes.listen(variables);
  });

  //   $: $spikes?.features, (currentTime = new Date());

  async function Sort() {
    let sort_obj = ImportVariables.sort_obj;
    let expiry_date = ImportVariables.expiry_date_future;
    // let expiry_date = ImportVariables.expiry_date;
    // expiry_date = ImportVariables.expiry_date_future;

    variables = { order_column: {} };
    variables["ExpiryDate"] = "{" + expiry_date + "}";
    variables["order_column"][sort_obj] = "asc";
    // variables["symbol"] = `{NIFTY}`;

    // variables["date_expiry"] = `{${ImportVariables.expiry_date_future}}`;

    // expiry_date = ImportVariables.expiry_date_future;
    // sort_obj = ImportVariables.sort_obj;
    // search_object = ImportVariables.symbol_name;

    // variables = { sort_object: {} };
    // variables.sort_object[sort_obj] = "desc";
    // variables["date_expiry"] = expiry_date;

    // if (search_object == "") {
    //   variables["search_symbol"] = "%%";
    // } else {
    //   variables["search_symbol"] = search_object;
    // }
    // console.log("variables", variables);
    $: spikes.listen(variables);
  }

  let url = $page.route.id;
  // ***********************Download Data***************************

  let tableData = [];
  let tableHeader = [
    "Symbol",
    "Price",
    "Price chg",
    "Price chg(%)",
    "OI",
    "OI Chg",
    "OI Chg(%)",
    "Volume",
    "Volume Chg(%)",
    "OI Chg(Value)",
  ];

  // function downloaderData() {
  //     tableData = ($spikes?.features || []).map((obj) => ({
  //         ...obj,
  //         open_interest_change_value: parseFloat(
  //             (obj.open_interest_change * obj.close)?.toFixed(2)
  //         ),
  //     }));
  // }

  // ***********************Download Data***************************
</script>

<div class="container-fluid">


  <!-- FiltersInOneComponent Filters -->
  <FiltersInOneComponent
    bind:ComponentExportableVarialbes={ImportVariables}
    on:MenuComponentChangeEvent={Sort}
    ImportableComponentList={["ExpiryDate", "SortFilter"]}
    SortFilterData={["oiSpikes"]}
    TableTitleFromPage={"OI / OI Chg / Volume Spikes Scan"}
  />

  <!-- dropdown manu -->
  <!-- <div class="d-flex" style="justify-content: center">
        <div class="d-flex mb-3 me-auto">
            <div class="mx-4">
                <SearchboxSymbol
                    bind:result={search_object}
                    on:addSearchField={Sort}
                />
            </div>
            <div class="mx-4">
                <SortFilter
                    bind:current_field={sort_obj}
                    on:addSortField={Sort}
                    sort_field={sort_field_list}
                />
            </div>
            <div class="mx-2">
                <ExpiryDate
                    bind:date={expiry_date}
                    on:addExpiryDate={Sort}
                    expiry_list={$expiry?.data?.future_expiry}
                />
            </div>
        </div> -->

  <!-- ***********************Download Data*************************** -->
  <!-- <DataDownloader tableData={tableData} tableHeader={tableHeader} downloaderData={downloaderData} fileName={`Volume & OI Spikes_${expiry_date}`}/> -->
  <!-- ***********************Download Data*************************** -->

  <!-- radio button -->
  <!-- <div class='d-flex mx-5'> -->

  <!-- <div class="mx-3 mt-4">
                <input
                    class="form-check-input"
                    type="radio"
                    name="flexRadioDefault"
                    id="one"
                    checked
                />
                <label class="radio_lab py-1" style="" for="one"> Latest </label>
            </div>

            <div class="mx-3 mt-4">
                <input
                    class="form-check-input"
                    type="radio"
                    name="flexRadioDefault"
                    id="two"
                />
                <label class="radio_lab py-1" style="" for="two">
                    Historical
                </label>
            </div> -->

  <!-- datefield -->
  <!-- <div class="input-append date">
                <input type="text" class="span2"><span class="add-on"><i class="icon-th"></i></span>
        </div> -->
  <!-- </div> -->

  <div style="display: flex;">
    <!-- open-high value scanner table -->
    <DataTable
      stickyHeader
      style="width: 100%; overflow-y: auto; height: 750px; background-color: transparent !important;"
    >
      <Head>
        <Row>
          <Cell>Symbol</Cell>
          <Cell>Price</Cell>
          <Cell>Price chg</Cell>
          <Cell>Price chg%</Cell>
          <Cell>OI</Cell>
          <Cell>OI chg</Cell>
          <Cell>OI chg%</Cell>
          <!-- <Cell>OI chg Value</Cell> -->
          <Cell>Volume</Cell>
          <Cell>Volume chg%</Cell>
        </Row>
      </Head>
      <Body>
        {#if $spikes?.data?.today_fut_1_day}
          {#each $spikes?.data?.today_fut_1_day as item}
            <Row>
              <Cell>{item.symbol}</Cell>
              <CellWithProgress
                value={item.price.toLocaleString(options)}
                percentage={item.price_change_per?.toFixed(4)}
              />
              <Cell>{item.price_change?.toFixed(2)}</Cell>
              <ColoredCell
                isPer={true}
                value={item.price_change_per?.toFixed(4)}
              />
              <CellWithProgress
                value={item.open_interest.toLocaleString(options)}
                percentage={item.open_interest_change_per?.toFixed(4)}
              />
              <Cell>{item.open_interest_change?.toFixed(2)}</Cell>
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
            </Row>
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
  span {
    color: white;
    text-decoration: underline;
    cursor: pointer;
  }
</style>
