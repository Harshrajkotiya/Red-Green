<!-- <script>
    // /** @type {import('./$types').PageData} */
    // export let data;
</script> -->


<!-- <div class="container mt-4">
	<h4 class="font">
		{data.symbolData.info.symbol}
	</h4>
	<div style="display: flex;">
		<h3 class="font mt-3 me-2 text-muted">
			<b>{data.symbolData.marketStatus.last}</b>
		</h3>
		<span>
			{#if data.index.marketStatus.variation < 0}
				<h6 class="variationred font mt-3">
					{data.index.marketStatus.variation.toFixed(2)} ({data.index.marketStatus.percentChange}%)
					<span style="color: grey;">1D</span>
				</h6>
			{:else if data.index.marketStatus.variation > 0}
				<h6 class="variationgreen font mt-3">
					{data.index.marketStatus.variation.toFixed(2)} ({data.index.marketStatus.percentChange}% )
					<span style="color: grey;">1D</span>
				</h6>
			{/if}
		</span>
	</div>
	<div>
		<div style="display: flex;">
			<h5 class="me-1 mt-3">Performance</h5>
			<span class="mt-3">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					viewBox="0 0 24 24"
					fill="#7C7E8C"
					height="20"
					width="20"
					class="absolute-center stpp34InfoIcon "
					><path d="M0 0h24v24H0z" fill="none" /><path
						d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"
					/></svg
				>
			</span>
		</div>
		<div class="row mt-2">
			<div class="col-md-2">
				<p class="text-muted">Today's Low</p>
				<h5>{data.symbolData.priceInfo.intraDayHighLow.min}</h5>
			</div>
			<div class="col-md-5">
				<input
					style="width: 100%;"
					type="range"
					class="form-range mt-4"
					min={data.symbolData.priceInfo.intraDayHighLow.min}
					max={data.symbolData.priceInfo.intraDayHighLow.max}
					value={data.symbolData.priceInfo.intraDayHighLow.value}
					disabled
				/>
			</div>
			<div class="col-md-2">
				<p class="text-muted">Today's High</p>
				<h5>{data.symbolData.priceInfo.intraDayHighLow.max}</h5>
			</div>
			<div class="col-md-3">
				<p class="text-muted">Open Price</p>
				<h5>{data.symbolData.priceInfo.intraDayHighLow.value}</h5>
			</div>
		</div>
	</div>
	<div>
		<div class="row mt-4">
			<div class="col-md-2">
				<p class="text-muted">52W Low</p>
				<h5>{data.symbolData.priceInfo.weekHighLow.min}</h5>
			</div>
			<div class="col-md-5">
				<input
					style="width: 100%;"
					type="range"
					class="form-range mt-4"
					min={data.symbolData.priceInfo.weekHighLow.min}
					max={data.symbolData.priceInfo.weekHighLow.max}
					value={data.symbolData.priceInfo.previousClose}
					disabled
				/>
			</div>
			<div class="col-md-2">
				<p class="text-muted">52W High</p>
				<h5>{data.symbolData.priceInfo.weekHighLow.max}</h5>
			</div>
			<div class="col-md-2">
				<p class="text-muted">Previous Close</p>
				<h5>{data.symbolData.priceInfo.previousClose}</h5>
			</div>
		</div>
	</div>
</div> -->

<!-- <style>
	/* @import "../node_modules/bootstrap/scss/bootstrap"; */

	.font {
		font-family: 'Inter';

	}
	.variationred {
		color: red;
	}
	.variationgreen {
		color: green;
	}

	input[type='range']::-webkit-slider-thumb {
		border-radius: 0%;
		border-top: 10px solid transparent;
		border-left: 10px solid #3071a9;
		border-bottom: 10px solid transparent;
		transform: rotate(-90deg);
		background: transparent;
	}
</style> -->
