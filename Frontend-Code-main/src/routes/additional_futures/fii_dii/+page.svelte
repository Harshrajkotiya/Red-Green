<script>
  import Body from "@smui/data-table/src/Body.svelte";
  import Cell from "@smui/data-table/src/Cell.svelte";
  import DataTable from "@smui/data-table/src/DataTable.svelte";
  import Head from "@smui/data-table/src/Head.svelte";
  import Row from "@smui/data-table/src/Row.svelte";
  import TableTitle from "../../../components/TableTitle.svelte";

  let currentTime = new Date()
</script>

<div>
  <TableTitle update_time={currentTime} title="FII & DII TRADING ACTIVITY" />
</div>

<DataTable style="width: 100%;">
  <Head>
    <Row>
      <Cell style="text-align: center;" class="col-6">FII RS CRORES</Cell>
      <Cell style="text-align: center;" class="col-6">DII RS CRORES</Cell>
    </Row>
  </Head>
</DataTable>

<DataTable style="width: 100%;">
  <Head>
    <Row>
      <Cell>Date</Cell>
      <Cell>Gross Purchase</Cell>
      <Cell>Gross Sales</Cell>
      <Cell>Net Purchase / Sales</Cell>
      <Cell>Gross Purchase</Cell>
      <Cell>Gross Sales</Cell>
      <Cell>Net Purchase / Sales</Cell>
    </Row>
  </Head>
  <Body>
    {#each fii_dii_Data as i}
      <Row>
        <Cell>{i.Date}</Cell>
        <Cell>{i["Gross Purchase FII"]}</Cell>
        <Cell>{i["Gross Sales FII"]}</Cell>
        <Cell>{i["Net Purchase / Sales FII"]}</Cell>
        <Cell>{i["Gross Purchase"]}</Cell>
        <Cell>{i["Gross Sales"]}</Cell>
        <Cell>{i["Net Purchase / Sales"]}</Cell>
      </Row>
    {/each}
  </Body>
</DataTable>
