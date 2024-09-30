<script lang="ts">
    import logoSrc1 from "./orangeicon.png";
    import logoSrc from "./rosecoco_landscape.png";
</script>

<header class="header">
    <img class="logo-icon" src={logoSrc1} alt="ROSECOCOiconLogo">
    <img class="logo-text" src={logoSrc} alt="ROSECOCOtextLogo">
</header>

<style>
    .header {
        display: flex;
        align-items: center;
        justify-content: center;
        background: #f8f8f8; /* Optional: Add a background color */
        width: 100%;
        border-bottom: 0.1em solid #e7e7e7; /* Optional: Add a bottom border */
    }

    .logo-icon {
        width: 2.8em; /* 45px equivalent */
        height: auto;
        margin-right: 1em;
    }

    .logo-text {
        width: 18em; /* 300px equivalent */
        height: auto;
    }

    /* Reset margin-right for the last image */
    .header img:last-child {
        margin-right: 0;
    }
</style>
