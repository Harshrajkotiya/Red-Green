<script>
  import Cell from "@smui/data-table/src/Cell.svelte";

  export let value = 0.0;
  export let isPer = false;
</script>

{#if value > 0}
  <Cell class="text-success">+{value} {isPer ? "%" : ""}</Cell>
{:else if value == 0}
  <Cell class="text-success">0.00 {isPer ? "%" : ""}</Cell>
{:else}
  <Cell class="text-danger">{value} {isPer ? "%" : ""}</Cell>
{/if}


<style>
    .mdc-data-table__cell {
            background-color: #141822;
        }
</style>
