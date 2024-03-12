<script lang="ts">
  import { graphql } from "$houdini";
  import DataTable, { Body, Cell, Head, Row } from "@smui/data-table";

  const vix = graphql(`
    subscription GetVIX {
      ind_vix {
        date
        open
        high
        low
        prev_close
        current
        change_per
      }
    }
  `);
  $: vix.listen();
</script>

<div class="container-fluid">
  <!-- heading -->
  <!-- <TableTitle title="India VIX Snapshot" update_time={currentTime} /> -->

  <div class="row mx-4">
    <!-- Vix Data Today -->
    <div class="col">
      <DataTable>
        <Head>
          <Row>
            <Cell colspan={6} class="text-center"  style="background:transparent;color:white">Today</Cell>
          </Row>
          <Row>
            <Cell class="text-center">Current</Cell>
            <Cell class="text-center">Open</Cell>
            <Cell class="text-center">High</Cell>
            <Cell class="text-center">Low</Cell>
            <Cell class="text-center">Prev. Close</Cell>
            <Cell class="text-center">% Change.</Cell>
          </Row>
        </Head>
        <Body>
          {#if $vix?.data?.ind_vix}
            {#each $vix?.data?.ind_vix as vixToday}
              <Row>
                <Cell>{vixToday.current}</Cell>
                <Cell>{vixToday.open}</Cell>
                <Cell>{vixToday.high}</Cell>
                <Cell>{vixToday.low}</Cell>
                <Cell>{vixToday.prev_close}</Cell>
                <Cell
                  class={Number(vixToday.change_per) <= 0
                    ? "red-color"
                    : "green-color"}>{vixToday.change_per}</Cell
                >
              </Row>
            {/each}
          {/if}
        </Body>
      </DataTable>
    </div>

    <!-- Vix Data Historical -->
    <!-- <div class="col">
        <DataTable>
          <Head>
            <Row>
              <Cell colspan={6} class="text-center">Historical</Cell>
            </Row>
            <Row>
              <Cell class="text-center">Previous Day</Cell>
              <Cell class="text-center">One Week Ago</Cell>
              <Cell class="text-center">One Month Age</Cell>
              <Cell class="text-center">52 Week High</Cell>
              <Cell class="text-center">52 Week Low</Cell>
              <Cell class="text-center">One Year Age</Cell>
            </Row>
          </Head>
          <Body>
            {#if $vix?.ind_vix}
              {#each $vix?.ind_vix as vixHistorical}
                <Row>
                  <Cell>{vixHistorical.previous_day}</Cell>
                  <Cell>{vixHistorical.one_week_ago}</Cell>
                  <Cell>{vixHistorical.one_month_ago}</Cell>
                  <Cell>{vixHistorical.week_52_high}</Cell>
                  <Cell>{vixHistorical.week_52_low}</Cell>
                  <Cell>{vixHistorical.one_year_age}</Cell>
                </Row>
                <Row>
                  <Cell
                    >{vixHistorical.previous_day_date.toLocaleString(
                      "en-US",
                      options
                    )}</Cell
                  >
                  <Cell
                    >{vixHistorical.one_week_ago_date.toLocaleString(
                      "en-US",
                      options
                    )}</Cell
                  >
                  <Cell
                    >{vixHistorical.one_month_ago_date.toLocaleString(
                      "en-US",
                      options
                    )}</Cell
                  >
                  <Cell
                    >{vixHistorical.week_52_high_date.toLocaleString(
                      "en-US",
                      options
                    )}</Cell
                  >
                  <Cell
                    >{vixHistorical.week_52_low_date.toLocaleString(
                      "en-US",
                      options
                    )}</Cell
                  >
                  <Cell
                    >{vixHistorical.one_year_age_date.toLocaleString(
                      "en-US",
                      options
                    )}</Cell
                  >
                </Row>
              {/each}
            {/if}
          </Body>
        </DataTable>
      </div> -->
  </div>
</div>
