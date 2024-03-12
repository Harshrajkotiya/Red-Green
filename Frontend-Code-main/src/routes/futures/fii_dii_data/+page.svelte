<script lang="ts">
  import DataTable, { Head, Body, Row } from "@smui/data-table";
  import Cell from "@smui/data-table/src/Cell.svelte";
  import { graphql } from "$houdini";

  const fii_dii = graphql(`
    subscription GetFii_Dii {
      fii_dii_data {
        category
        date
        net_value
        sell_value
        buy_value
      }
    }
  `);
  $: fii_dii.listen();
</script>

<div class="container-fluid">
  <div style="display: flex;" class="p-2 mx-3">
    <!-- open-high value scanner table -->
    <DataTable table$aria-label="User list" style="width: 100%;" class="me-3">
      <Head>
        <Row>
          <Cell>Category</Cell>
          <Cell>Date</Cell>
          <Cell>Buy Value</Cell>
          <Cell>Sell Value</Cell>
          <Cell>Net Value</Cell>
        </Row>
      </Head>
      <Body>
        {#if $fii_dii?.data?.fii_dii_data}
          {#each $fii_dii?.data?.fii_dii_data as item}
            <Row>
              <Cell>{item.category}</Cell>
              <Cell>{item.date}</Cell>
              <Cell>{item.buy_value}</Cell>
              <Cell>{item.sell_value}</Cell>
              <Cell>{item.net_value}</Cell>
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
</style>
