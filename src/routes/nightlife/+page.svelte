<script>
    import '../../styles/layout.css';
</script>

<section class="the-section">
    <div class="image-container">
        <img src="/tabimages/nightlife.png" alt="Adventure Image" />
    </div>

    <div class="text-content">
        <h2>Nightlife Awaits</h2>
        <p>Discover exciting lifestyles and experiences that will take your breath away.</p>

        <div class="cta-container">
            <p>Stay tuned for more thrilling adventures coming your way!</p>
            <button class="cta-button" on:click="{() => alert('You will be notified soon!')}">Join the Nightlife List</button>
        </div>
    </div>
</section>
