<script>
    import Login from "./Login.svelte";
    import { graphql } from "$houdini";
    import { page } from "$app/stores";
    import { onMount } from "svelte";
    import { navigating } from "$app/stores";
    import DataTable, { Head, Body, Row, Cell } from "@smui/data-table";

    var searched = "";

    export const _searchQueryVariables = () => {
        return { searched_string: searched };
    };

    async function Search() {
        if (searched == "") {
            store.fetch({ variables: { searched_string: searched } });
        } else {
            store.fetch({ variables: { searched_string: searched + "%" } });
        }
    }

    const store = graphql(`
        query searchQuery($searched_string: String!) {
            fut_expiry(
                distinct_on: symbol
                limit: 7
                order_by: { symbol: asc }
                where: { symbol: { _ilike: $searched_string } }
            ) {
                symbol
                expiry
            }
        }
    `);

    // const store = graphql(`
    //     query searchQuery($searched_string: String!) {
    //         master_data(
    //             distinct_on: name
    //             limit: 7
    //             order_by: { name: asc }
    //             where: {
    //                 _or: [
    //                     { name: { _ilike: $searched_string } }
    //                     { tradingsymbol: { _ilike: $searched_string } }
    //                 ]
    //             }
    //         ) {
    //             name
    //             tradingsymbol
    //             expiry
    //             segment
    //             instrument_type
    //         }
    //     }
    // `);(
    // const store = Array();
    function clearSearch() {
        searched = "";
        store.data = [];

        Search();
    }

    function LoginSignupPage() {
        console.log("click meeee.............");
    }

    let linkColor;
    let btnClick = false;
    onMount(() => {
        linkColor = document.querySelectorAll(".nav-link");
        nav_selection($page.route.id);
    });

    const nav_selection = (location) => {
        console.log(location);
        if (location.startsWith("/home")) {
            linkColor.forEach((l) => l.classList.remove("selected"));
            document.getElementById("home")?.classList.add("selected");
            console.log("home");
        } else if (location.startsWith("/options")) {
            linkColor.forEach((l) => l.classList.remove("selected"));
            document.getElementById("options")?.classList.add("selected");
            console.log("options");
        } else if (location.startsWith("/futures")) {
            linkColor.forEach((l) => l.classList.remove("selected"));
            document.getElementById("futures")?.classList.add("selected");
            console.log("futures");
        }
    };
    let url = $page.route.id;

    $: if ($navigating) {
        nav_selection($navigating.to?.route.id);
    }
</script>

<nav class="navbar navbar-expand-lg p-0" id="Navbar">
    <div class="container">
        <a class="navbar-brand" href="/"
            ><img
                src="../images/new_logo_derivedged.png"
                alt="logo-red-green-traders-cafe"
                style="width: 100%;
                  height: 4vh;"
                class="img-fluid"
            /></a
        >
        <!-- Search Box Start -->
        {#if url === "/"}
            <div class="mx-4" style="width:30vw">
                <div class="row">
                    <div class="input-group col-md-4">
                        <input
                            class="form-control inp-bg-color border-right-0"
                            type="search"
                            placeholder="Search stocks"
                            id="myInput"
                            autocomplete="off"
                            bind:value={searched}
                            on:input={Search}
                        />
                        <span class="input-group-append">
                            <div class="btn border-left-0 myborder">
                                <i class="fa fa-search" style="color:#ced4da" />
                            </div>
                        </span>
                    </div>
                </div>

                <div style="position:absolute; z-index: 99; width:30vw">
                    {#if $store.data?.fut_expiry?.length > 0}
                        <ul class="searchul" id="searchul">
                            {#each $store.data.fut_expiry as item}
                                <a
                                    class="searchlink"
                                    href={`/symbol/${item.symbol}`}
                                    on:click={clearSearch}
                                >
                                    <div
                                        class="d-flex"
                                        style="justify-content:space-between"
                                    >
                                        <li class="searchli my-2 p-2 me-2">
                                            {item.symbol} <br /><span />
                                        </li>
                                        <!-- <li class="searchli my-2 p-2 me-2">
                                            {item.symbol} <br /><span
                                                >{item.tradingsymbol}</span
                                            >
                                        </li> -->
                                        <!-- {#if item.instrument_type == "EQ"}
                                            <li class="searchli my-2 p-2 me-2">
                                                {item.segment}
                                            </li>
                                        {:else} -->
                                        <li class="searchli my-2 p-2 me-2">
                                            {item.expiry} <br />
                                        </li>
                                        <!-- <li class="searchli my-2 p-2 me-2">
                                            {item.expiry} <br />
                                            <span>{item.expiry}</span>
                                        </li> -->
                                        <!-- {/if} -->
                                    </div>
                                </a>
                            {/each}
                        </ul>
                    {/if}
                </div>
            </div>
        {/if}
        <!-- Search Box Ends -->
        <!-- Top menu bar -->
        <!-- {#if url === "/"}
          <div class="collapse navbar-collapse" id="navbarSupportedContent">
              <ul class="navbar-nav mr-auto">
                  <li class="nav-item active">
                      <a
                          data-sveltekit-reload
                          class="nav-link mx-2 selected"
                          href="#"
                          id="home"
                          >Home <span class="sr-only">(current)</span></a
                      >
                  </li>
                  <li class="nav-item">
                      <a
                          class="nav-link mx-2"
                          data-bs-toggle="modal"
                          data-bs-target="#exampleModalCenter">About Us</a
                      >
                  </li>
                  <li class="nav-item">
                      <a
                          data-sveltekit-reload
                          class="nav-link mx-2"
                          href="#"
                          id="home">Contact Us</a
                      >
                  </li>
                  <li class="nav-item">
                      <a
                          data-sveltekit-reload
                          class="nav-link mx-2"
                          href="#"
                          id="home">Pricing</a
                      >
                  </li>
                  <li class="nav-item">
                      <a
                          data-sveltekit-reload
                          class="nav-link mx-2"
                          href="#"
                          id="home">Support</a
                      >
                  </li>
              </ul>
          </div> -->
        {#if url != "/"}
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav mr-auto">
                    <li class="nav-item active">
                        <a
                            data-sveltekit-reload
                            class="nav-link mx-2 selected"
                            href="/home"
                            id="home"
                            >Home <span class="sr-only">(current)</span></a
                        >
                    </li>

                    <li class="dropdown mx-2">
                        <a
                            class="dropdown-toggle nav-link"
                            id="futures"
                            data-bs-toggle="dropdown"
                        >
                            Futures
                        </a>
                        <ul class="dropdown-menu">
                            <li>
                                <a
                                    data-sveltekit-reload
                                    class="dropdown-item"
                                    href="/futures/oi_buildup">OI BUILDUP</a
                                >
                            </li>
                            <li>
                                <a
                                    data-sveltekit-reload
                                    class="dropdown-item"
                                    href="/futures/oi_interpretation"
                                    >OI INTERPRETATION</a
                                >
                            </li>
                            <li>
                                <a
                                    data-sveltekit-reload
                                    class="dropdown-item"
                                    href="/futures/intraday_oi_breakup"
                                    >OI BREAKUP</a
                                >
                            </li>
                            <li>
                                <a
                                    data-sveltekit-reload
                                    class="dropdown-item"
                                    href="/futures/ohl_scanner">O=H, O=L</a
                                >
                            </li>
                            <li>
                                <a
                                    data-sveltekit-reload
                                    class="dropdown-item"
                                    href="/futures/daywise_price_oi_details"
                                    >DAY WISE PRICE & OI DETAILS</a
                                >
                            </li>
                            <li>
                                <a
                                    data-sveltekit-reload
                                    class="dropdown-item"
                                    href="/futures/daywise_price_oi_summary"
                                    >DAY WISE PRICE & OI SUMMARY</a
                                >
                            </li>
                            <li>
                                <a
                                    data-sveltekit-reload
                                    class="dropdown-item"
                                    href="/futures/OI_spikes"
                                    >VOLUME/ OI/ OI CHANGE SPIKES</a
                                >
                            </li>
                            <li>
                                <a
                                    data-sveltekit-reload
                                    class="dropdown-item"
                                    href="/futures/heat_map"
                                    >SECTOR WISE HEAT MAP</a
                                >
                            </li>
                            <li>
                                <a
                                    data-sveltekit-reload
                                    class="dropdown-item"
                                    href="/futures/vix">VIX</a
                                >
                            </li>
                        </ul>
                    </li>

                    <li class="dropdown mx-2">
                        <a
                            class="dropdown-toggle nav-link"
                            id="options"
                            data-bs-toggle="dropdown"
                            style="cursor: pointer;"
                        >
                            Options
                        </a>
                        <ul class="dropdown-menu">
                            <li>
                                <a
                                    data-sveltekit-reload
                                    class="dropdown-item"
                                    href="/options/chain">OPTIONS CHAIN</a
                                >
                            </li>
                            <li>
                                <a
                                    data-sveltekit-reload
                                    class="dropdown-item"
                                    href="/options/options_ohl_scanner"
                                    >O=H, O=L</a
                                >
                            </li>
                            <li>
                                <a
                                    data-sveltekit-reload
                                    class="dropdown-item"
                                    href="/options/options_snapshot"
                                    >OI SNAPSHOT</a
                                >
                            </li>
                            <li>
                                <a
                                    data-sveltekit-reload
                                    class="dropdown-item"
                                    href="/options/intraday_oi_breakup"
                                    >OPTIONS OI BREAKUP</a
                                >
                            </li>
                            <li>
                                <a
                                    data-sveltekit-reload
                                    class="dropdown-item"
                                    href="/options/PE_CE_OI_Difference"
                                    >TOTAL PE CE OI DIFFERENCE</a
                                >
                            </li>
                        </ul>
                    </li>

                    <li class="dropdown mx-2">
                        <a
                            data-sveltekit-reload
                            class="dropdown-toggle nav-link"
                            id="add_features"
                            data-bs-toggle="dropdown"
                            style="cursor: pointer;"
                        >
                            Additional features
                        </a>
                        <ul class="dropdown-menu">
                            <li>
                                <a class="dropdown-item" href="#"
                                    >CONNECTING DOTS</a
                                >
                            </li>
                            <li>
                                <a
                                    class="dropdown-item"
                                    href="../../futures/fii_dii_data"
                                    >FII/DII DATA</a
                                >
                            </li>
                            <li>
                                <a class="dropdown-item" href="#"
                                    >PATICIPATE WISE OI</a
                                >
                            </li>
                            <li>
                                <a
                                    class="dropdown-item"
                                    href="../../futures/holidays"
                                    data-bs-toggle="modal"
                                    data-bs-target="#marketHolidaysModal"
                                    >MARKET HOLIDAYS</a
                                >
                            </li>
                        </ul>
                    </li>

                    <li class="dropdown mx-2">
                        <a
                            data-sveltekit-reload
                            class="dropdown-toggle nav-link"
                            id="strategies"
                            data-bs-toggle="dropdown"
                            style="cursor: pointer;"
                        >
                            Strategies
                        </a>
                        <ul class="dropdown-menu">
                            <li>
                                <a class="dropdown-item" href="#"
                                    >STRADDLE SNAPSHOT</a
                                >
                            </li>
                            <li>
                                <a class="dropdown-item" href="#"
                                    >STRADDLE CHARTS(OIP)</a
                                >
                            </li>
                            <li>
                                <a class="dropdown-item" href="#"
                                    >STRANGLE CHARTS(OIP)</a
                                >
                            </li>
                            <li>
                                <a class="dropdown-item" href="#"
                                    >STRADDLE WATCH</a
                                >
                            </li>
                            <li>
                                <a class="dropdown-item" href="#"
                                    >STRADDLE CHARTS PLUS</a
                                >
                            </li>
                            <li>
                                <a class="dropdown-item" href="#"
                                    >STRADDLE COMBO</a
                                >
                            </li>
                            <li>
                                <a class="dropdown-item" href="#"
                                    >SPREAD CHART</a
                                >
                            </li>
                            <li>
                                <a class="dropdown-item" href="#">BUTTERFLY</a>
                            </li>
                            <li>
                                <a class="dropdown-item" href="#"
                                    >IRON CONDOR/FLY</a
                                >
                            </li>
                            <li>
                                <a class="dropdown-item" href="#"
                                    >DOUBLE CALENDER/DIAGONAL</a
                                >
                            </li>
                        </ul>
                    </li>

                    <li class="dropdown mx-2">
                        <a
                            data-sveltekit-reload
                            class="dropdown-toggle nav-link"
                            id="scanners"
                            data-bs-toggle="dropdown"
                            style="cursor: pointer;"
                        >
                            Scanners
                        </a>
                        <ul class="dropdown-menu">
                            <li>
                                <a class="dropdown-item" href="#"
                                    >FUTURE NEAR MAX OI</a
                                >
                            </li>
                            <li>
                                <a class="dropdown-item" href="#">OI SUPPORT</a>
                            </li>
                            <li>
                                <a class="dropdown-item" href="#"
                                    >NIFTY 50 OI CHANGE%</a
                                >
                            </li>
                            <li>
                                <a class="dropdown-item" href="#"
                                    >MARKET MOVERS</a
                                >
                            </li>
                            <li>
                                <a class="dropdown-item" href="#"
                                    >OI SUPRT(NIFTY AND BANK)</a
                                >
                            </li>
                            <li>
                                <a class="dropdown-item" href="#">NR4 AND NR7</a
                                >
                            </li>
                            <li>
                                <a class="dropdown-item" href="#"
                                    >GOLDEN CROSSSOVER</a
                                >
                            </li>
                        </ul>
                    </li>

                    <li class="nav-item active">
                        <a
                            data-sveltekit-reload
                            class="nav-link mx-2 selected"
                            href="#"
                            >Other
                        </a>
                    </li>
                </ul>
            </div>
        {/if}
        <!-- End Top menu bar -->

        <!-- Search bar -->

        <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <form class="d-flex p-2 flex-grow-1" style="justify-content:right">
                <!-- Login Button -->
                <a
                    href=""
                    data-bs-toggle="modal"
                    data-bs-target="#staticBackdrop"
                    on:click={LoginSignupPage}
                >
                <button type="button" class="btn btn-success">Get Started</button>
                </a>
                <!-- login End -->
            </form>
        </div>

        <!-- Login Modal -->
        <!-- <div
      class="modal fade"
      id="staticBackdrop"
      tabindex="-1"
      aria-labelledby="staticBackdropLabel"
    >
      <div class="modal-dialog">
        <div class="modal-content_update">
          <Login />
        </div>
      </div>
    </div> -->
        <div
            class="modal fade"
            id="staticBackdrop"
            data-backdrop="static"
            tabindex="-1"
            role="dialog"
            aria-labelledby="exampleModalLabel"
            aria-hidden="true"
        >
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-body">
                        <Login />
                    </div>
                </div>
            </div>
        </div>
        <!-- Login Modal Ends -->

        <!-- Modal Market Holidays Page -->
        <div
            class="modal fade bd-example-modal-lg"
            id="marketHolidaysModal"
            tabindex="-1"
            role="dialog"
            aria-labelledby="marketHolidaysModalTitle"
            aria-hidden="true"
        >
            <div
                class="modal-dialog modal-dialog-centered modal-lg modal-dialog-scrollable"
                role="document"
            >
                <div class="modal-content">
                    <div class="modal-header text-center">
                        <h5
                            class="modal-title w-100"
                            id="exampleModalLongTitle"
                        >
                            Market Holiday
                        </h5>
                    </div>
                    <!-- <div class="modal-body text-center">
                        <DataTable class="w-100">
                            <Head>
                                <Row>
                                    <Cell>Sr. No.</Cell>
                                    <Cell>Date</Cell>
                                    <Cell>Day</Cell>
                                    <Cell>Description</Cell>
                                </Row>
                            </Head>
                            <Body>
                                {#each holidayList as holiday}
                                    <Row>
                                        <Cell>{holiday.Sr_no}</Cell>
                                        <Cell>{holiday.tradingDate}</Cell>
                                        <Cell>{holiday.weekDay}</Cell>
                                        <Cell>{holiday.description}</Cell>
                                    </Row>
                                {/each}
                            </Body>
                        </DataTable>
                    </div> -->
                </div>
            </div>
        </div>
        <!-- Model Over -->
    </div>
</nav>

<style>
    :root {
        --font-color: white;
        --bg-dark: #141822;
    }
    #myInput {
        /* background-position: 10px 12px;
  background-repeat: no-repeat;
  width: 100%;
  font-size: 16px;
  padding: 12px 20px 12px 40px;
  border: 1px solid #ddd;
  margin-bottom: 12px; */
        /* color:#1e1f4b; */
        font-weight: 400;
        font-size: 14px;
        line-height: 24px;
        font-family: "Inter senserif";
        border-right-style: none;
        background-color: transparent;
    }
    #searchul {
        list-style-type: none;
        padding: 0;
        margin: 0;
        display: block;
        padding: 4px 0px 4px 8px;
        height: auto;
        background: var(--bg-dark);
        box-shadow: 0px 15px 6px rgba(0, 0, 0, 0.01),
            0px 8px 5px rgba(0, 0, 0, 0.05), 0px 4px 4px rgba(0, 0, 0, 0.09),
            0px 1px 2px rgba(0, 0, 0, 0.1), 0px 0px 0px rgba(0, 0, 0, 0.1);
        border-radius: 6px;
    }
    .searchli {
        padding: 1px;
        cursor: pointer;
    }
    .searchul li {
        color: var(--font-color);
        list-style-type: none;

        height: auto;
        font-weight: 600;
    }
    .searchul a {
        text-decoration: none;
        color: var(--font-color);
    }

    .searchul span {
        color: var(--font-color);
        font-size: 12px;
        font-weight: 300;
    }

    .searchul div:hover {
        background-color: #141822;
        border-left: 3px solid #02373e;
        border-radius: 5px;
    }
    .inp-bg-color {
        /* width: 40vw; */
        /* gap: 10px; */
        /* height: 40px; */
        /* padding: 0px 5px 0px 10px; */
        /* background: #2a2e39; */
        color: var(--font-color);
    }

    .navbar-nav li:hover > .dropdown-menu {
        display: block;
    }

    .navbar-expand-lg {
        background: transparent;
    }

    .modal-content {
        background: transparent;
        /* height: 0; */
    }

    /* .modal-dialog {
      width: 0%;
  } */

    .container,
    .container-lg,
    .container-md,
    .container-sm,
    .container-xl,
    .container-xxl {
        max-width: 95vw;
    }

    .dropdown-item {
        color: white;
    }

    a {
        text-decoration: none;
    }

    .nav-link {
        height: 24px;

        font-family: Arial, Helvetica, sans-serif;
        font-style: normal;
        font-weight: 500;
        font-size: 16px;
        line-height: 24px;
        /* identical to box height, or 150% */
        display: flex;
        align-items: center;
        /* Color/White/60 */
        color: rgba(255, 255, 255, 0.6);
    }

    .dropdown-menu {
        background-color: rgb(153, 151, 151);
    }

    .dropdown {
        width: auto;
    }

    .navbar-collapse {
        justify-content: center;
        max-width: fit-content;
    }

    .selected {
        color: #2acb41;
        height: 24px;
        font-weight: 700;
        font-size: 16px;
        line-height: 24px;
    }

    .dropdown-item:hover {
        background-color: #2acb41;
        border-radius: 6px;
    }

    .myborder {
        border: 1px solid #ced4da;
        border-left-style: none;
        border-bottom-left-radius: 0;
        border-top-left-radius: 0;
    }
</style>
