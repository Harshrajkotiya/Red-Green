<script>
  import { onMount } from "svelte";
  import {widget}from "../../../charting_library/charting_library.esm"
  import {UDFCompatibleDatafeed}from "../../../datafeeds/udf/lib/udf-compatible-datafeed"

  onMount(()=>{
    const gg = new widget({
            container: 'chartContainer',
            locale: 'en',
            library_path: '/charting_library/',
            datafeed: new UDFCompatibleDatafeed("/chartapis"),
            symbol: 'NIFTY',
            interval: '1D',
            fullscreen: true,
            debug: true
        })
  })
</script>

<div id = "chartContainer" />