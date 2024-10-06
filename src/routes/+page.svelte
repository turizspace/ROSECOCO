<script>
    import Header from '../components/Header.svelte';
    import Footer from '../components/Footer.svelte';
    import Events from '../components/Events5.svelte';
    import Noteposter from '../components/Noteposter.svelte';
    import Shitposter from '../components/Shitposter.svelte';

</script>


<div class="container">


    <main class="content">
        <h1>Welcome to Rosecoco</h1>
        <p>The right place to find exactly what you are looking for!</p>
        <Events />
    </main>
</div>


<style>
    .container {
        display: flex;
        min-height: calc(100vh - 4em); /* Adjusting height for header and footer */
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

    @media (max-width: 768px) {
        .container {
            flex-direction: column; /* Stack sidebars and content vertically */
        }
    }
</style>
