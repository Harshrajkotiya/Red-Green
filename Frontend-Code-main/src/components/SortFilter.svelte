<script lang="ts">
    import { createEventDispatcher } from "svelte";
    export let sort_field;
    export let current_field = sort_field[0].name;
    const dispatch = createEventDispatcher();

    const sorting_field = () => {
        dispatch("addSortField");
    };
</script>

<div class="mx-3">
    <label class="mt-2" for="Sort" style="color:azure">Sort</label>
    <select
        id="Sort"
        name="Sort"
        class="form-select data-pick mt-2"
        style="background-color: black; color: white;"
        bind:value={current_field}
        on:change={sorting_field}
    >
        <option value={sort_field[0].name} selected>
            {sort_field[0].label}
        </option>
        {#each sort_field.slice(1) as sort_data}
            <option value={sort_data.name}>{sort_data.label}</option>
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
