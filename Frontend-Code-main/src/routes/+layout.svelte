<script lang="ts">
    import Navbar from "../components/Navbar.svelte";
    // import Marquee from "../components/marquee.svelte";
    // import Sidemanu from "../components/Sidemanu.svelte";
    import { page } from "$app/stores";
    import type { PageData } from "./$types";
    import Footer from "../components/Footer.svelte";

    export let data: PageData;
</script>

{#if $page.route.id == "/"}
    <!-- <Marquee /> -->
    <div style="width:-webkit-fill-available; ">
        <Navbar />
        <slot />
    </div>
{:else}
    <div style="width:-webkit-fill-available; ">
        <Navbar />
        <slot />
    </div>
{/if}
<Footer />
