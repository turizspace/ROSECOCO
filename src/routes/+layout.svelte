<script>
    import Header from '../components/Header.svelte';
    import Footer from '../components/Footer.svelte';
    import Noteposter from '../components/Noteposter.svelte';
    import Shitposter from '../components/Shitposter.svelte';
    import { goto } from '$app/navigation';
    import { writable } from 'svelte/store';

    let menuOpen = writable(false);
</script>

<Header />

<div class="container">
    <nav class="left-tabs">
        <button class="hamburger" on:click={() => menuOpen.update(open => !open)}>
            &#9776;
        </button>
        <ul class:show={$menuOpen}>
            <li><a href="/" on:click="{(e) => { e.preventDefault(); goto('/'); }}">HOME</a></li>
            <li><a href="/adventure" on:click="{(e) => { e.preventDefault(); goto('/adventure'); }}">Adventure</a></li>
            <li><a href="/culture" on:click="{(e) => { e.preventDefault(); goto('/culture'); }}">Culture</a></li>
            <li><a href="/dining" on:click="{(e) => { e.preventDefault(); goto('/dining'); }}">Dining</a></li>
            <li><a href="/fantasy" on:click="{(e) => { e.preventDefault(); goto('/fantasy'); }}">Fantasy</a></li>
            <li><a href="/nightlife" on:click="{(e) => { e.preventDefault(); goto('/nightlife'); }}">Nightlife</a></li>
            <li><a href="/private" on:click="{(e) => { e.preventDefault(); goto('/private'); }}">Private</a></li>
            <li><a href="/shopping" on:click="{(e) => { e.preventDefault(); goto('/shopping'); }}">Shopping</a></li>
            <li><a href="/tours" on:click="{(e) => { e.preventDefault(); goto('/tours'); }}">Tours</a></li>
        </ul>

        <Noteposter class="noteposter" />
    </nav>

    <main class="content">
        <slot></slot>
    </main>

    <aside class="right-tabs">
        <ul>
            <li><a href="#" on:click="{(e) => { e.preventDefault(); goto('/'); }}">Highlights</a></li>
        </ul>
        <Shitposter class="shitposter" />
    </aside>
</div>

<Footer />

<style>
    .container {
        display: flex;
        min-height: calc(100vh - 4em); /* Adjusting height for header and footer */
    }

    .left-tabs, .right-tabs {
        flex: 0 0 12em; /* Fixed width for sidebars */
        background: linear-gradient(135deg, #f4f4f4, #e0e0e0); /* Light gradient background */
        padding: 1em;
        overflow-y: auto; /* Allow scrolling if content overflows */
    }

    .left-tabs {
        border-right: 1px solid #ddd; /* Border to separate left tabs from content */
    }

    .right-tabs {
        border-left: 1px solid #ddd; /* Border to separate right tabs from content */
    }

    .left-tabs ul, .right-tabs ul {
        list-style: none;
        padding: 0;
        margin: 0; /* Ensure no extra space around lists */
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
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }

    .left-tabs a:hover, .right-tabs a:hover {
        color: #fff;
        background: #ff6347; /* Tomato color on hover */
        transform: translateY(-2px);
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
    }

    .content {
        flex: 1; /* Takes remaining space */
        padding: 1em;
        display: flex;
        flex-direction: column;
        align-items: center; /* Center horizontally */
        margin-top: 2em; /* Add some top margin */
        overflow-y: auto; /* Allow scrolling if content overflows */
    }

    .content h1, .content p {
        text-align: center; /* Center text inside the content */
    }

    .hamburger {
        display: none;
        background: none;
        border: none;
        font-size: 2em;
        cursor: pointer;
    }

    @media (max-width: 768px) {
        .container {
            flex-direction: column; /* Stack sidebars and content vertically */
        }

        .left-tabs, .right-tabs {
            flex: 0 0 auto; /* Allow them to resize based on content */
            width: 100%;
            border: none; /* Remove borders for cleaner look */
            padding: 0;
        }

        .hamburger {
            display: block; /* Show hamburger menu on small screens */
            margin: 1em;
        }

        .left-tabs ul {
            display: none; /* Hide menu on small screens */
        }

        .left-tabs ul.show {
            display: block; /* Show menu when hamburger is clicked */
            background: linear-gradient(135deg, #f4f4f4, #e0e0e0); /* Light gradient background */
            padding: 1em;
            border-right: 1px solid #ddd; /* Border to separate left tabs from content */
        }

        .noteposter, .shitposter, .right-tabs {
            display: none; /* Hide Noteposter, Shitposter, and right-tabs on small screens */
        }

        .right-tabs {
            order: -1; /* Place right-tabs before content */
        }
    }
</style>
