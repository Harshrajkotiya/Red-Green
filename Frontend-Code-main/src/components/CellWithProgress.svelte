<script>
    import Cell from "@smui/data-table/src/Cell.svelte";

    export let value = 0.0;
    export let percentage = 0.0;
    /**
     * @type {String}
     */
    let colorCode = percentage >= 0 ? "#2d8747" : "#d33242";
    
    console.log(colorCode);
</script>

<Cell>
    <div class="progress" style="background-color: rgb(21 24 33) !important;">
        <div
            class="progress-bar"
            style="background-color: {colorCode} !important; width: {Math.abs(
                percentage > 100 ? 100 : percentage
            )}%"
        >
            <div style="position: absolute; color: white;">
                {value}
            </div>
        </div>
    </div>
    
</Cell>
