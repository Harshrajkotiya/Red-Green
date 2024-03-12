<script>
  import Speedometer from "./../components/speedometer.svelte";
  import { graphql } from "$houdini";
  // import { onMount } from "svelte";

  // onMount(() => {
  //     document.querySelector("html").style["background"] =
  //         "url('../../images/initial_bg_img.svg') fixed center no-repeat";
  //     document.querySelector("html").style["backgroundSize"] = "cover";

  //     document.body.style["background"] =
  //         "url('../../images/initial_bg_img.svg') fixed center no-repeat";
  //     document.body.style["backgroundSize"] = "cover";
  //     // return () =>  document.body.style;
  // });
  let stock;
  stock = 50;
  setTimeout(() => {
    stock -= 50;
    console.log("stock_value", stock);
  }, 3000);

  setTimeout(() => {
    stock += 30;
    console.log("stock_value", stock);
  }, 5000);

  const TopLoser = graphql(`
    subscription TopLoser {
      top_loser {
        price
        price_change
        symbol
      }
    }
  `);
  $: TopLoser.listen();

  const TopGainers = graphql(`
    subscription TopGainers {
      top_gainers {
        price
        price_change
        symbol
      }
    }
  `);
  $: TopGainers.listen();
  const currencies = graphql(`
    subscription top_currencies {
      top_currencies {
        currency_name
        inr_price
        usd_price
      }
    }
  `);
  $: currencies.listen();

  const CryptoAction = graphql(`
    subscription CryptoAction {
      crypto_action {
        day_1_change
        price_inr
        crypto_currency_name
      }
    }
  `);
  $: CryptoAction.listen();
</script>

<div class="container-fluid">
  <div class="row">
    <div class="col-md-3">
      <div class="table-outer-box">
        <h1 class="table-title text-center">Market Action</h1>
        <table class="table table-dark">
          <thead>
            <tr class="bg-head">
              <th scope="col">Index</th>
              <th scope="col">Price</th>
              <th scope="col">Change</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Nifty-50</td>
              <td>17,626.65</td>
              <td>131.65</td>
            </tr>
            <tr>
              <td>Nifty-50</td>
              <td>17,626.65</td>
              <td>131.65</td>
            </tr><tr>
              <td>Nifty-50</td>
              <td>17,626.65</td>
              <td>131.65</td>
            </tr><tr>
              <td>Nifty-50</td>
              <td>17,626.65</td>
              <td>131.65</td>
            </tr><tr>
              <td>Nifty-50</td>
              <td>17,626.65</td>
              <td>131.65</td>
            </tr>
            <tr>
              <td>Nifty-50</td>
              <td>17,626.65</td>
              <td>131.65</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="col-md-6">
      <div class="table-outer-box">
        <h1 class="table-title text-center">Market Movers</h1>

        <div class="d-flex">
          <table class="table table-dark me-2">
            <thead>
              <tr class="text-center text-success">
                <th colspan="3">Top Gainers</th>
              </tr>

              <tr class="bg-head">
                <th scope="col">Index</th>
                <th scope="col">Price</th>
                <th scope="col">Change</th>
              </tr>
            </thead>
            <tbody>
              {#if $TopGainers?.data?.top_gainers}
                {#each $TopGainers?.data?.top_gainers as gainers}
                  <tr>
                    <td>{gainers.symbol}</td>
                    <td>{gainers.price}</td>
                    <td>{gainers.price_change}</td>
                  </tr>
                {/each}
              {/if}
            </tbody>
          </table>

          <table class="table table-dark">
            <thead>
              <tr class="text-center text-danger">
                <th colspan="3">Top Loser</th>
              </tr>

              <tr class="bg-head">
                <th scope="col">Index</th>
                <th scope="col">Price</th>
                <th scope="col">Change</th>
              </tr>
            </thead>
            <tbody>
              {#if $TopLoser?.data?.top_loser}
                {#each $TopLoser?.data?.top_loser as loser}
                  <tr>
                    <td>{loser.symbol}</td>
                    <td>{loser.price}</td>
                    <td>{loser.price_change}</td>
                  </tr>
                {/each}
              {/if}
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div class="col-md-3">
      <div class="table-outer-box">
        <h1 class="table-title text-center">Market Action</h1>

        <table class="table table-dark">
          <thead>
            <tr class="bg-head">
              <th scope="col">Index</th>
              <th scope="col">Price</th>
              <th scope="col">Change</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Nifty-50</td>
              <td>17,626.65</td>
              <td>131.65</td>
            </tr>
            <tr>
              <td>Nifty-50</td>
              <td>17,626.65</td>
              <td>131.65</td>
            </tr><tr>
              <td>Nifty-50</td>
              <td>17,626.65</td>
              <td>131.65</td>
            </tr><tr>
              <td>Nifty-50</td>
              <td>17,626.65</td>
              <td>131.65</td>
            </tr><tr>
              <td>Nifty-50</td>
              <td>17,626.65</td>
              <td>131.65</td>
            </tr>
            <tr>
              <td>Nifty-50</td>
              <td>17,626.65</td>
              <td>131.65</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <div class="row">
    <div class="col-md-3">
      <div class="table-outer-box">
        <h1 class="table-title text-center">Currency</h1>

        <table class="table table-dark">
          <thead>
            <tr class="bg-head">
              <th scope="col">Currency</th>
              <th scope="col">Rupee</th>
              <th scope="col">US</th>
            </tr>
          </thead>
          <tbody>
            {#if $currencies?.data?.top_currencies}
              {#each $currencies?.data?.top_currencies as item}
                <tr>
                  <td>{item.currency_name}</td>
                  <td>{item.inr_price}</td>
                  <td>{item.usd_price}</td>
                </tr>
              {/each}
            {/if}
          </tbody>
        </table>
      </div>
    </div>

    <div class="col-md-6" style="text-align: -webkit-center">
      <Speedometer stock_per={stock} />
    </div>

    <div class="col-md-3">
      <div class="table-outer-box">
        <h1 class="table-title text-center">Crypto Action</h1>

        <table class="table table-dark">
          <thead>
            <tr class="bg-head">
              <th scope="col">Symbol</th>
              <th scope="col">Price</th>
              <th scope="col">Change</th>
            </tr>
          </thead>
          <tbody>
            {#if $CryptoAction?.data?.crypto_action}
              {#each $CryptoAction?.data?.crypto_action as crypto}
                <tr>
                  <td>{crypto.crypto_currency_name}</td>
                  <td>{crypto.price_inr}</td>
                  <td>{crypto.day_1_change}</td>
                </tr>
              {/each}
            {/if}
          </tbody>
        </table>
      </div>
    </div>
  </div>
</div>

<style>
  .table-dark {
    --bs-table-bg: none;
  }

  .table {
    border: 1px solid #373b3e;
  }

  .bg-head {
    background-color: #02373e;
  }

  .table > :not(:last-child) > :last-child > * {
    border-bottom-color: #373b3e;
  }

  .table-outer-box {
    margin: 10px 0px;
    padding: 20px;
    border: 1px solid #373b3e;
    border-radius: 6px;
  }

  .table-title {
    font-style: normal;
    font-weight: 600;
    font-size: 16px;
    line-height: 24px;
    color: #2acb41;
  }
</style>
