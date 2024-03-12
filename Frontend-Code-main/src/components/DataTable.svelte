<script lang="ts">
  import DataTable, { Head, Body, Row, Cell } from "@smui/data-table";
  import ColoredCell from "./ColoredCell.svelte";
  //   import Cell from "@smui/data-table/src/Cell.svelte";
  // import {stock_data} from '../data/stock_table';

  //   type stock_data = {
  //   symbol: string,
  // 	price: number,
  // 	price_change: number,
  // 	oi: number,
  // 	oi_change: number,
  // };

  export let items;
  export let name;
  const options = {minimumFractionDigits: 2, maximumFractionDigits: 2};


  // items = stock_data;
</script>

<!-- <h1>{name}</h1> -->

<div class="table_content p-2">
  <DataTable
    stickyHeader
    table$aria-label="User list"
    style="width:100%; height:50vh; overflow-y:auto;background: transparent;"
  >
    <Head>
      <Row
        ><Cell
          colSpan="5"
          style="text-align-last: center; font-weight:bolder; background-color: transparent; color:white"
          >{name}</Cell
        >
      </Row>
      <!-- {#each items as item} -->

      <!-- {#if name==="Long Buildup" } -->
      <!-- {#if item.price_change > 0 && item.open_interest_change > 0} -->
      <Row>
        <Cell>Symbol</Cell>
        <Cell>Price</Cell>
        <Cell>Price Chg(%)</Cell>
        <Cell>OI</Cell>
        <Cell>OI Chg(%)</Cell>
      </Row>
      <!-- {/if} -->
      <!-- {:else if name==="Short Buildup" }
        {#if item.price_change < 0 && item.open_interest_change < 0}
        <Row>
            <Cell>Symbol</Cell>
            <Cell>Price</Cell>
            <Cell>Price Chg(%)</Cell>
            <Cell>OI</Cell>
            <Cell>OI Chg(%)</Cell>
          </Row>
         {/if} 
        {:else if name==="Long Unwinding" }
        {#if item.price_change > 0 && item.open_interest_change < 0}
        <Row>
            <Cell>Symbol</Cell>
            <Cell>Price</Cell>
            <Cell>Price Chg(%)</Cell>
            <Cell>OI</Cell>
            <Cell>OI Chg(%)</Cell>
          </Row>
          {/if}
        {:else if name==="Short Covering" }
        {#if item.price_change < 0 && item.open_interest_change > 0}
        <Row>
            <Cell>Symbol</Cell>
            <Cell>Price</Cell>
            <Cell>Price Chg(%)</Cell>
            <Cell>OI</Cell>
            <Cell>OI Chg(%)</Cell>
          </Row>
         {/if} 
        {:else}
          <Cell></Cell>
        {/if}
        {/each} -->
    </Head>
    <Body>
      {#each items as item}
        {#if item.price_change > 0 && item.open_interest_change > 0 && name === "Long Buildup"}
          <Row>
            <Cell>{item.symbol[0]}</Cell>
            <Cell>{item.price.toLocaleString(options)}</Cell>
            <ColoredCell
              isPer={true}
              value={parseFloat(
                ((item.price_change / item.price) * 100)?.toFixed(4)
              )}
            />
            <Cell>{item.open_interest.toLocaleString(options)}</Cell>
            <ColoredCell
              isPer={true}
              value={parseFloat(
                (
                  (item.open_interest_change / item.open_interest) *
                  100
                )?.toFixed(4)
              )}
            />
          </Row>
        {/if}
        {#if item.price_change < 0 && item.open_interest_change < 0 && name === "Short Buildup"}
          <Row>
            <Cell>{item.symbol[0]}</Cell>
            <Cell>{item.price.toLocaleString(options)}</Cell>
            <ColoredCell
              isPer={true}
              value={parseFloat(
                ((item.price_change / item.price) * 100)?.toFixed(4)
              )}
            />
            <Cell>{item.open_interest.toLocaleString(options)}</Cell>
            <ColoredCell
              isPer={true}
              value={parseFloat(
                (
                  (item.open_interest_change / item.open_interest) *
                  100
                )?.toFixed(4)
              )}
            />
          </Row>
        {/if}
        {#if item.price_change > 0 && item.open_interest_change < 0 && name === "Long Unwinding"}
          <Row>
            <Cell>{item.symbol[0]}</Cell>
            <Cell>{item.price.toLocaleString(options)}</Cell>
            <ColoredCell
              isPer={true}
              value={parseFloat(
                ((item.price_change / item.price) * 100)?.toFixed(4)
              )}
            />
            <Cell>{item.open_interest.toLocaleString(options)}</Cell>
            <ColoredCell
              isPer={true}
              value={parseFloat(
                (
                  (item.open_interest_change / item.open_interest) *
                  100
                )?.toFixed(4)
              )}
            />
          </Row>
        {/if}
        {#if item.price_change < 0 && item.open_interest_change > 0 && name === "Short Covering"}
          <Row>
            <Cell>{item.symbol[0]}</Cell>
            <Cell>{item.price.toLocaleString(options)}</Cell>
            <ColoredCell
              isPer={true}
              value={parseFloat(
                ((item.price_change / item.price) * 100)?.toFixed(4)
              )}
            />
            <Cell>{item.open_interest.toLocaleString(options)}</Cell>
            <CustomCell
              isPer={true}
              value={parseFloat(
                (
                  (item.open_interest_change / item.open_interest) *
                  100
                )?.toFixed(4)
              )}
            />
          </Row>
        {/if}
      {/each}
    </Body>

    <!-- <LinearProgress
        indeterminate
        bind:closed={loaded}
        aria-label="Data is being loaded..."
        slot="progress"
      /> -->
  </DataTable>
</div>

<style>
  .table_content {
    width: 50%;
    min-width: 500px;
  }
</style>
