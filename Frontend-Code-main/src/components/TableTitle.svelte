<script lang="ts">
  import { last_update_timeStore } from "$houdini";
  import { graphql } from "graphql";

  // Getting Variable From The Page....
  export let title: string;
  // let update_time: Date; // If update_time not Get The Time It Will Take The Current Date And Time By Default....

  // Defining The Variables...
  const options = {
    day: "numeric",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    timeZone: "UTC"
  };


  const time = graphql(`
  subscription last_update_time {
      last_update_time {
        bucket
      }
    }
  `);

 $: time.listen()

</script>

<div class="d-flex justify-content-between align-items-center text-white">
  <h4 class="text-center flex-grow-1">{title}</h4>
  {#if $time?.last_update_time}
  <span class="updated-time text-white"
    >Last updated : {new Date($time?.last_update_time[0].bucket).toLocaleString('en-US', options)}</span
  >
{/if}
</div>

<style>
  .updated-time {
    font-family: "Roboto", "sans-serif";
    font-size: 16px;
    margin-right: 25px;
    text-align: right;
  }
</style>
