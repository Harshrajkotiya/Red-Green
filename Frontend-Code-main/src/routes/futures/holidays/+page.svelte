<script lang="ts">
  import DataTable, { Head, Body, Row } from "@smui/data-table";
  import Cell from "@smui/data-table/src/Cell.svelte";
  import { graphql } from "$houdini";

  const holiday = graphql(`
    subscription GetHoliday {
      holiday {
        holiday
        day
        date
      }
    }
  `);
  $: holiday.listen();
</script>

<div class="container-fluid">
  <div style="display: flex;" class="p-2 mx-3">
    <!-- open-high value scanner table -->
    <DataTable table$aria-label="User list" style="width: 100%;" class="me-3">
      <Head>
        <Row>
          <Cell>Sr No.</Cell>
          <Cell>Holidays</Cell>
          <Cell>Date</Cell>
          <Cell>Day</Cell>
        </Row>
      </Head>
      <Body>
        {#if $holiday?.holiday}
          {#each $holiday?.holiday as item, index}
            <Row>
              <Cell>{index + 1}</Cell>
              <Cell>{item.holiday}</Cell>
              <Cell>{item.date}</Cell>
              <Cell>{item.day}</Cell>
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
