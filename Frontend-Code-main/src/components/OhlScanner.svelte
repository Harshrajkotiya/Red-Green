<script >
    import Cell from "@smui/data-table/src/Cell.svelte";
    
    export let open;
    export let high;
    export let low;
    
  </script>
  
  {#if open === high}
      <Cell class='text-center green-color'>Open-High</Cell>
  {:else if open === low}
      <Cell class='text-center red-color'>Open-Low</Cell>
  {:else}
      <Cell>none</Cell>
  {/if}
  