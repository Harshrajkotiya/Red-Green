<script >
    import Cell from "@smui/data-table/src/Cell.svelte";
    
    export let price_change;
    export let oi_change;
    
  </script>
  
  {#if price_change > 0 && oi_change > 0}
      <Cell class='text-center lb-color'>Long Buildup</Cell>
  {:else if price_change < 0 && oi_change > 0}
      <Cell class='text-center sc-color'>Short Covering</Cell>
  {:else if price_change > 0 && oi_change < 0}
      <Cell class='text-center lu-color'>Long Unwinding</Cell>
  {:else if price_change < 0 && oi_change < 0}
      <Cell class='text-center sb-color'>Short Buildup</Cell>
  {:else}
      <Cell class="text-center">-</Cell>
  {/if}
  