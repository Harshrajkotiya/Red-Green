<script lang="ts">
	// import TableTitle from './TableTitle.svelte';
    // Importing The Component & Packages....
    import SearchboxwithExpiry from "../components/SearchboxwithExpiry.svelte";
    import SearchboxwithExpiryOptions from "../components/SearchboxwithExpiryOptions.svelte";
    import BuildupIndicator from "./BuildupIndicator.svelte";
    import StrikePrice from "../components/StrikePrice.svelte";
    import ExpiryDate from "../components/ExpiryDate.svelte";
    import IntervalFilter from "./IntervalFilter.svelte";
    import SearchboxSymbol from "./SearchboxSymbol.svelte";
    // import LeatestHistoryRadio from "../components/Leatest_History_Radio.svelte";
    import DataDownloader from "../components/DataDownloader.svelte";
    import { graphql } from "$houdini";
    import { createEventDispatcher, onMount } from "svelte";
    import Sort_filter from "./SortFilter.svelte";
    import Collapse from "../components/collapse.svelte";
    import TableTitle from "../components/TableTitle.svelte";

    // Defining The Varialbes....
    // export let ComponentVarialbes = new Array();
    export let ComponentImportableVarialbes;
    export const ComponentExportableVarialbes = new Array();
    export let SortFilterData = new Array();
    export let ImportableComponentList = new Array();
    export let fileName: string;
    export let tableData;
    export let tableHeader = new Array();
    export let isDownloadableData = true;
    export let IsOptionSearchBoxAndExpiry = false;
    export let isDefaultNifty = false;
    export let TableTitleFromPage: string;
    let expiry_date;
    let expiry_date_future;
    let symbol_name;
    let strike;
    const variables = new Object();
    let sort_field_list = new Array();
    const interval_list = [
        { name: "futures_3_min", label: "3min" },
        { name: "futures_5_min", label: "5min" },
        { name: "futures_15_min", label: "15min" },
        { name: "futures_30_min", label: "30min" },
        { name: "futures_1_hour", label: "1hour" },
    ];
    let sort_obj: string;
    let interval_obj: string;
    const dispatch = createEventDispatcher();

    // Getting The SortFilter Data Minimal or All Data...
    if (SortFilterData.includes("minimal")) {
        // Minimal Sort Filter List...
        sort_field_list = [
            { name: "open_interest_change_per", label: "OI Change" },
            { name: "price_change_per", label: "Price Change %" },
            { name: "price_change", label: "price Change" },
            { name: "symbol", label: "Symbol" },
        ];
    } else if (SortFilterData.includes("intradayOiBreakUp")) {
        sort_field_list = [ 
            { name: "price_change", label: "price Change" },
            { name: "price", label: "Price" },
            { name: "open_interest", label: "OI" },
            { name: "open_interest_change", label: "OI Change" },
            { name: "volume", label: "Volume" },
            { name: "volume_change", label: "Volume Change" },
        ];


    } else if (SortFilterData.includes("oiSpikes")) {
        sort_field_list = [ 
            { name: "price_change", label: "price Change" },
            { name: "price", label: "Price" },
            { name: "symbol", label: "Symbol" },
            { name: "open_interest", label: "OI" },
            { name: "open_interest_change", label: "OI Change" },
            { name: "volume", label: "Volume" },
            { name: "volume_change", label: "Volume Change" },
        ];

    } else if (SortFilterData.includes("minimal_at_heat_map_future")) {
        sort_field_list = [
            { name: "open_interest_change_per", label: "OI Change" },
            { name: "price_change_per", label: "Price Change" },
        ];
    }else if (SortFilterData.includes("minimal_at_heat_map_future")) {
        sort_field_list = [
            { name: "open_interest_change_per", label: "OI Change" },
            { name: "price_change_per", label: "Price Change" },
        ];
    } else if (SortFilterData.includes("maximal_at_OI_spikes_future")) {
        sort_field_list = [
            { name: "open_interest_change_per", label: "OI Change %" },
            { name: "volume_change_per", label: "Volume Change %" },
            { name: "price_change_per", label: "Price Change %" },
            { name: "symbol", label: "Symbol" },
            { name: "open_interest", label: "OI" },
            { name: "open_interest_change", label: "OI Change" },
            { name: "price", label: "Price" },
            { name: "volume", label: "Volume" },
            { name: "volume_change_per", label: "Volume Change %" },
        ];
    } else if (SortFilterData.includes("fieldListAtOHLScannerAtFutures")) {
        sort_field_list = [
            { name: "price_change_per", label: "Price Change %" },
            { name: "price_change", label: "price Change" },
            { name: "symbol", label: "Symbol" },
        ];
    } else {
        // Full List
        sort_field_list = [
            { name: "open_interest_change", label: "OI Change" },
            { name: "symbol", label: "Symbol" },
            { name: "price", label: "Price" },
            { name: "price_change", label: "Price Change" },
            { name: "open_interest", label: "OI" },
        ];
    }

    // console.log("the consoles of the FiltersInOneComponent");
    // console.log("Importable Components Are :- ", ImportableComponentList);

    // Executing The Graphql Queryies.....
    // if(ImportableComponentList.includes("SearchboxwithExpiry"))
    // {
    // const symbol = graphql(`
    //     query GetSymbolAndExpiryDate {
    //         opt_expiry_date(order_by: { expiry: asc }) {
    //             expiry
    //             symbol
    //         }
    //     }
    // `);
    //  }

    // expiry Dates For Futures...
    const expiry = graphql(`
        query GetfeaturesExpiryDate {
            fut_expiry(
                order_by: { expiry: asc }
                where: { symbol: { _neq: "{FINNIFTY}" } }
            ) {
                expiry
                symbol
            }
        }
    `);

    // expiry Date For Options...
    const expiry_symbol_in_option = graphql(`
        query expiry_symbol_in_option {
            opt_expiry(distinct_on: [expiry, symbol]) {
                expiry
                symbol
            }
        }
    `);

    // Method Call After Mounting the Page...
    onMount(async () => {
        // console.log("Component Mount AT FILTERES :- ");
        setFuturesExpiryDate();
        setSortFilterChange();
        IntervalFilterChange();
        ExpityDateChange();
        SymbolChange();
        if (ImportableComponentList.includes("StrikePrice")) {
            setVariables();
        }
    });

    // On SearchBox Component Change Event...
    const SearchboxwithExpiryChange = () => {
        // console.log(symbol_name,expiry_date,expiry_date[0]);
        ComponentExportableVarialbes["symbol_name"] = symbol_name;
        ComponentExportableVarialbes["expiry_date"] = expiry_date;
        variables.symbol = symbol_name;
        variables.date_expiry = expiry_date;
        dispatch("MenuComponentChangeEvent");
    };

    const SearchboxwithExpiryChangeAtOptions = () => {
        ComponentExportableVarialbes["symbol_name"] = symbol_name;
        ComponentExportableVarialbes["expiry_date"] = expiry_date;
        variables.symbol = symbol_name;
        variables.date_expiry = expiry_date;
        dispatch("MenuComponentChangeEvent");
    };

    // Setup Of Variables (Symbol & ExpiryDate)....
    const setVariables = async () => {
        await expiry_symbol_in_option.fetch();
        let indexOfNifty = $expiry_symbol_in_option?.data?.opt_expiry.findIndex(
            (e) => e.symbol == "NIFTY"
        );
        variables.symbol = "NIFTY";
        variables.date_expiry = ComponentExportableVarialbes.expiry_date;
        console.log("variables At Filters  is :- ",variables);
    };

    // SetUp of The Futures Expiry Date....
    const setFuturesExpiryDate = async () => {
        await expiry.fetch();
        if ($expiry?.data?.fut_expiry) {
            ExpityDateChange();
        }
    };

    // Setup Of The Sort Filters....
    const setSortFilterChange = async () => {
        sort_obj = sort_field_list[0].name;
        SortFilterChange();
    };

    // On ExpityDate Component Change Event...
    const ExpityDateChange = () => {
        ComponentExportableVarialbes["expiry_date_future"] = expiry_date_future;
        dispatch("MenuComponentChangeEvent");
    };

    // On SortFilter Component Change Event...
    const SortFilterChange = () => {
        console.log(sort_obj);

        ComponentExportableVarialbes["sort_obj"] = sort_obj;
        dispatch("MenuComponentChangeEvent");
    };

    // On IntervalFilter Component Change Event...
    const IntervalFilterChange = () => {
        ComponentExportableVarialbes["interval_obj"] = interval_obj;

        dispatch("MenuComponentChangeEvent");
    };

    // On IntervalFilter Component Change Event...
    const SymbolChange = () => {
        // console.log("the Symbols Are :: ", symbol_name);
        ComponentExportableVarialbes["symbol_name"] = symbol_name;
        dispatch("MenuComponentChangeEvent");
    };

    // console.log("last Comment of Filters Component");
</script>

<TableTitle title={TableTitleFromPage} />

<div class="container-fluid mt-3">
    <Collapse />
</div>

<div class="d-flex mb-3 justify-content-center">
    <!-- Options Symbols & Expiry Date -->
    {#if ImportableComponentList.includes("SearchboxwithExpiry")}
        {#if IsOptionSearchBoxAndExpiry}

            <!-- {#if $expiry_symbol_in_option?.data?.opt_expiry} -->
                <SearchboxwithExpiryOptions
                    bind:current_expiry={expiry_date}
                    bind:result={symbol_name}
                    on:addSearchField={SearchboxwithExpiryChangeAtOptions}
                />
            <!-- {/if} -->
        {:else if $expiry?.data?.fut_expiry}
            <SearchboxwithExpiry
                bind:current_expiry={expiry_date}
                bind:result={symbol_name}
                on:addSearchField={SearchboxwithExpiryChange}
                symbol_list={$expiry?.data?.fut_expiry}
            />
        {/if}
        <!-- {#if IsOptionSearchBoxAndExpiry}
            {#if $expiry_symbol_in_option?.data?.opt_expiry}
                <SearchboxwithExpiryOptions
                    bind:current_expiry={expiry_date}
                    bind:result={symbol_name}
                    on:addSearchField={SearchboxwithExpiryChange}
                    symbol_list={$expiry_symbol_in_option?.data?.opt_expiry}
                />
            {/if}
        {:else if $expiry?.data?.fut_expiry}
            <SearchboxwithExpiry
                bind:current_expiry={expiry_date}
                bind:result={symbol_name}
                on:addSearchField={SearchboxwithExpiryChange}
                symbol_list={$expiry?.data?.fut_expiry}
            />
        {/if} -->
    {/if}
    <!-- <h1>{variables.date_expiry}</h1> -->

    <!-- Depends On The OPtions's Symbols & Expiry -->
    {#if ImportableComponentList.includes("StrikePrice")}
        {#if variables.date_expiry}
            <StrikePrice
                stock_obj={variables}
                bind:selected_strike={strike}
                strike_status="Strike Price"
            />
            <!-- <div class="text-white">{Object.values(variables)}</div> -->
        {/if}
    {/if}

    <!-- Radio Buttons Latest & Historical -->
    {#if ImportableComponentList.includes("DataFiltersLatestHistorical")}
        <!-- <div class="d-flex mx-3 mt-4">
              <input
                  type="radio"
                  id="leatest"
                  name="stockData"
                  value="leatest"
                  checked
              />
              <label class="text-white my-auto mx-2" for="leatest"
                  >Leatest Data</label
              ><br />
          </div>
          <div class="d-flex mx-3 mt-4">
              <input
                  type="radio"
                  id="historical"
                  name="stockData"
                  value="historical"
              />
              <label class="text-white my-auto mx-2" for="historical"
                  >Historical Data</label
              ><br />
          </div> -->
        <!-- <LeatestHistoryRadio /> -->
    {/if}

    <!-- List of Stock name (Symbol) -->
    {#if ImportableComponentList.includes("SearchboxSymbol")}
        <SearchboxSymbol
            bind:result={symbol_name}
            on:addSearchField={SymbolChange}
        />
    {/if}

    {#if ImportableComponentList.includes("SortFilter")}
        <Sort_filter
            sort_field={sort_field_list}
            bind:current_field={sort_obj}
            on:addSortField={SortFilterChange}
        />
    {/if}

    <!-- Futures Expiry Date -->
    {#if ImportableComponentList.includes("ExpiryDate")}
        {#if $expiry?.data?.fut_expiry}
            <ExpiryDate
                bind:date={expiry_date_future}
                on:addExpiryDate={ExpityDateChange}
                expiry_list={$expiry?.data?.fut_expiry}
            />
        {/if}
    {/if}

    <!-- Sort Filter Which has Getting data from the ===>>> sort_field_list see above at variable declarations and Creates the select box -->
    <!-- {#if ImportableComponentList.includes("SortFilter")}
          <SortFilter
              bind:current_field={sort_obj}
              on:addSortField={SortFilterChange}
              sort_field={sort_field_list}
          />
      {/if} -->

    <!-- IntervalFilter Filter Which has Getting data from the ===>>> interval_list see above at variable declarations and Creates the select box -->
    {#if ImportableComponentList.includes("IntervalFilter")}
        <IntervalFilter
            bind:current_field={interval_obj}
            on:addIntervalField={IntervalFilterChange}
            interval_field={interval_list}
        />
    {/if}

    <!-- Specifications Of BuidupStatus's Color Which Color Is What For And Full Form Of Indicates -->
    {#if ImportableComponentList.includes("BuildupIndicator")}
        <BuildupIndicator />
    {/if}

    {#if isDownloadableData}
        <DataDownloader {tableData} {tableHeader} {fileName} />
    {/if}

    
</div>
