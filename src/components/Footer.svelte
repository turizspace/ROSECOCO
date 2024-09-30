<!-- src/components/Footer.svelte -->
<script lang="ts">
  import BlockHeight from './BlockHeight.svelte'; // Import the BlockHeight component
  import logoSrc1 from "./orangeicon.png";
  import logoSrc from "./rosecoco_landscape.png";
</script>

<footer class="footer">
    <img class="logo-icon" src={logoSrc1} alt="ROSECOCOiconLogo">
    <img class="logo-text" src={logoSrc} alt="ROSECOCOtextLogo">
    <BlockHeight />
</footer>

<style>
    .footer {
        display: flex;
        align-items: center;
        justify-content: center;
        border-top: 1px solid #e7e7e7;
        background: #f8f8f8; /* Optional: Add a background color */
        width: 100%;
        flex-shrink: 0;
    }

    .logo-icon {
        width: 0.9em;
        height: auto;
        margin-right: 1em;
    }

    .logo-text {
        width: 6em;
        height: auto;
    }

    /* Reset margin-right for the last image */
    .footer img:last-child {
        margin-right: 0;
    }
</style>
