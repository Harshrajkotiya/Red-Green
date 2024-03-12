<script>
    import { createEventDispatcher } from "svelte";
    export let interval_field;
    export let current_field;
  
    const dispatch = createEventDispatcher();
  
    const selectIntervalEvent = () => {
      dispatch("addIntervalField");
    };
  </script>
  
  <div>
    <label class="mt-2" for="interval_field" style="color:azure">Interval</label>
    <select
      id="interval_field"
      name="interval_field"
      class="form-select data-pick mt-2"
      style="background-color: black; color: white;"
      bind:value={current_field}
      on:change={selectIntervalEvent}
    >
      <option value={interval_field[0].name} selected>
        {interval_field[0].label}
      </option>
      {#each interval_field.slice(1) as interval}
        <option value={interval.name}>{interval.label}</option>
      {/each}
    </select>
  </div>
  
  <style>
    .data-pick {
      max-width: 200px;
      width: 200px;
      font-size: small;
      min-width: 150px;
      background-color: var(--bg-dark);
      color: white;
      height: 35px;
    }
  </style>
  