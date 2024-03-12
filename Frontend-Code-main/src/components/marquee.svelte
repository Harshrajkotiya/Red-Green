<script lang="ts">
    import type { indicesResponseData } from "../wundergraph/models";
    export let indices: indicesResponseData["postgres_db_findManyindices_ticks"] =
        [];
    console.log(indices);
</script>

<div class="main_marquee">
    <!-- svelte-ignore a11y-distracting-elements -->
    <marquee
        loop="infinite"
        onmouseover="this.stop();"
        onmouseout="this.start();"
    >
        <div class="mar_line">
            {#each indices as stock}
                <a href={`/stock_detail/${stock.instrument_token}`}>
                    <div class="stock_item">
                        <div class="s_symbol">
                            {stock.master_data.trading_symbol}
                        </div>

                        {#if stock.change < 0}
                            <div class="s_symbol mx-2 text-danger">
                                <p class="s_pchangedown">{stock.last_price}</p>
                            </div>

                            <div class="arrow_sign">
                                <svg
                                    class="keyboarddoublearrow"
                                    xmlns="http://www.w3.org/2000/svg"
                                    width="15"
                                    height="15"
                                    viewBox="0 0 10 12"
                                    fill="none"
                                >
                                    <path
                                        d="M5 12L0 7L1.062 5.938L5 9.875L8.938 5.938L10 7L5 12ZM5 6.062L0 1.062L1.062 0L5 3.938L8.938 0L10 1.062L5 6.062Z"
                                        fill="red"
                                    />
                                </svg>
                            </div>

                            <div class="s_pchange mx-3">
                                <p class="s_pchangedown">
                                    {stock.change} %
                                </p>
                            </div>
                        {:else if stock.change >= 0}
                            <div class="s_symbol mx-2 text-white">
                                {stock.last_price}
                            </div>
                            <div class="arrow_sign">
                                <svg
                                    class="keyboarddoublearrow"
                                    xmlns="http://www.w3.org/2000/svg"
                                    width="15"
                                    height="15"
                                    viewBox="0 0 10 12"
                                    fill="none"
                                >
                                    <path
                                        d="M5 12L0 7L1.062 5.938L5 9.875L8.938 5.938L10 7L5 12ZM5 6.062L0 1.062L1.062 0L5 3.938L8.938 0L10 1.062L5 6.062Z"
                                        fill="green"
                                        transform="scale(1,-1) translate(0,-11)"
                                    />
                                </svg>
                            </div>

                            <div class="s_pchange mx-3">
                                <p class="s_pchangeup">
                                    {stock.change} %
                                </p>
                            </div>
                        {/if}
                    </div>
                </a>
            {/each}
        </div>
    </marquee>
</div>

<style>
    a {
        text-decoration: none;
    }

    .stock_item {
        display: flex;
    }

    .s_pchange {
        margin: 5px;
    }

    .arrow_sign {
        margin-right: 20px;
        margin: 6px;
    }

    .s_pchangeup {
        padding-right: 10px;
        font-size: 14px;
        font-weight: 600;
        color: green;
        font-family: "Roboto", sans-serif;
    }

    .s_pchangedown {
        font-weight: 600;

        padding-right: 10px;
        font-size: 14px;
        color: red;
        font-family: "Roboto", sans-serif;
    }

    .mar_line {
        height: 30px;
        display: flex;
        top: 0;
        width: max-content;
        /* left: 0; */
    }

    .main_marquee {
        background-color: #000000;
        height: 30px;
        top: 0;
    }

    .s_symbol {
        font-family: "Roboto", sans-serif;
        font-weight: 400;
        font-size: 13px;
        margin: 5px 10px;
        line-height: 20px;
        color: rgba(255, 255, 255, 1);
    }

    .bounding-box-4 {
        position: absolute;
        width: 20px;
        height: 20px;
        top: 0px;
        background: rgba(217, 217, 217, 1);
    }

    .keyboarddoublearrow {
        position: absolute;
        width: 20px;
        height: 20px;
        padding: 2px;
    }

    .bounding-box-6 {
        position: absolute;
        width: 15px;
        height: 15px;
        top: 5px;
        background: rgba(217, 217, 217, 1);
    }
</style>
