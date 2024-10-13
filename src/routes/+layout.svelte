<script>
    import Header from '../components/Header.svelte';
    import Footer from '../components/Footer.svelte';
    import Noteposter from '../components/Noteposter.svelte';
    import Shitposter from '../components/Shitposter.svelte';
    import { writable } from 'svelte/store';
    import { goto } from '$app/navigation';

    let menuOpen = writable(false);
    let showShitposterModal = writable(false);

    // Function to toggle modal visibility
    function toggleShitposterModal() {
        showShitposterModal.update(current => !current);
    }
</script>

<Header />

<div class="container">
    <nav class="left-tabs">
    <button class="hamburger" on:click={() => menuOpen.update(open => !open)}>
        &#9776;
    </button>
    <ul class:show={$menuOpen}>
        <li><a href="/" on:click="{(e) => { e.preventDefault(); goto('/'); menuOpen.set(false); }}">HOME</a></li>
        <li><a href="/adventure" on:click="{(e) => { e.preventDefault(); goto('/adventure'); menuOpen.set(false); }}">Adventure</a></li>
        <li><a href="/culture" on:click="{(e) => { e.preventDefault(); goto('/culture'); menuOpen.set(false); }}">Culture</a></li>
        <li><a href="/dining" on:click="{(e) => { e.preventDefault(); goto('/dining'); menuOpen.set(false); }}">Dining</a></li>
        <li><a href="/fantasy" on:click="{(e) => { e.preventDefault(); goto('/fantasy'); menuOpen.set(false); }}">Fantasy</a></li>
        <li><a href="/nightlife" on:click="{(e) => { e.preventDefault(); goto('/nightlife'); menuOpen.set(false); }}">Nightlife</a></li>
        <li><a href="/private" on:click="{(e) => { e.preventDefault(); goto('/private'); menuOpen.set(false); }}">Private</a></li>
        <li><a href="/shopping" on:click="{(e) => { e.preventDefault(); goto('/shopping'); menuOpen.set(false); }}">Shopping</a></li>
        <li><a href="/tours" on:click="{(e) => { e.preventDefault(); goto('/tours'); menuOpen.set(false); }}">Tours</a></li>
    </ul>

    <Noteposter class="noteposter" />
    </nav>


    <main class="content">
        <slot />
    </main>

    <!-- Right tabs content (Shitposter component only on smaller screens or modal) -->
    <div class="right-tabs">
        <!-- Shitposter visible on large screens -->
        <Shitposter class="shitposter" />
        <!-- Shitposter visible only when modal is toggled on small screens -->
        {#if $showShitposterModal}
            <Shitposter class="modal-shitposter" />
        {/if}
    </div>

    <!-- Floating Button for Small Screens -->
    <button class="floating-btn" on:click={toggleShitposterModal}>+</button>

    <!-- Modal for Shitposter -->
    {#if $showShitposterModal}
        <div class="modal-overlay" on:click={toggleShitposterModal}>
            <div class="modal-content" on:click|stopPropagation>
                <Shitposter class="modal-shitposter" />
                <button class="close-btn" on:click={toggleShitposterModal}>X</button>
            </div>
        </div>
    {/if}
</div>

<Footer />

<style>
    .container {
        display: flex;
        flex-direction: row;
    }

    .left-tabs, .right-tabs {
        flex: 0 0 10em;
        background: linear-gradient(135deg, #f4f4f4, #e0e0e0);
        padding: 1em;
        overflow-y: auto;
    }

    .left-tabs, .right-tabs {
        border-right: 1px solid #ddd;
    }

    .left-tabs ul, .right-tabs ul {
        list-style: none;
        padding: 0;
        margin: 0;
    }

    .left-tabs li, .right-tabs li {
        margin-bottom: 0.5em;
    }

    .left-tabs a, .right-tabs a {
        display: block;
        padding: 0.5em 1em;
        text-decoration: none;
        color: #333;
        background: #fff;
        border-radius: 5px;
        transition: all 0.3s ease;
    }

    .left-tabs a:hover, .right-tabs a:hover {
        color: #fff;
        background: #ff6347;
        transform: translateY(-2px);
    }

    .content {
        flex: 1;
        padding: 1em;
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-top: 0.2em;
        overflow-y: auto;
    }

    .hamburger {
        display: none;
        background: none;
        border: none;
        font-size: 2em;
        cursor: pointer;
    }

    .floating-btn {
        display: none;
        position: fixed;
        bottom: 20px;
        right: 20px;
        background-color: #ff6347;
        color: white;
        border: none;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        font-size: 30px;
        cursor: pointer;
    }

    .modal-overlay {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: rgba(0, 0, 0, 0.5);
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .modal-content {
        background: white;
        padding: 2em;
        border-radius: 8px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
        position: relative;
    }

    .close-btn {
        position: absolute;
        top: 10px;
        right: 10px;
        background-color: #ff6347;
        color: white;
        border: none;
        border-radius: 50%;
        width: 30px;
        height: 30px;
        font-size: 18px;
        cursor: pointer;
    }

    /* Mobile Styling */
    @media (max-width: 768px) {
        .container {
            flex-direction: column;
        }

        .left-tabs, .right-tabs {
            flex: 0 0 auto;
            width: 100%;
            border: none;
            padding: 0;
        }

        .hamburger {
            display: block;
        }

        .left-tabs ul {
            display: none;
        }

        .left-tabs ul.show {
            display: block;
        }

        .floating-btn {
            display: block;
        }

        .right-tabs {
            display: none; /* Hide right tabs on mobile */
        }

        /* Show Shitposter only in modal on mobile */
        .modal-shitposter {
            display: block;
        }
    }

    /* Large Screen - Keep Shitposter visible in right-tabs */
    @media (min-width: 769px) {
        .right-tabs {
            display: block; /* Show right tabs on larger screens */
        }

        .floating-btn {
            display: none; /* Hide floating button on large screens */
        }

        .modal-shitposter {
            display: none; /* Keep Shitposter hidden in modal on large screens */
        }

        .shitposter {
            display: block; /* Show Shitposter in right-tabs on large screens */
        }
    }
</style>
