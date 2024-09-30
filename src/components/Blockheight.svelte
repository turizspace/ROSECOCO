<!-- src/components/BlockHeight.svelte -->
<script lang="ts">
  import { onMount } from 'svelte';
  let blockHeight = 'Loading...'; // Initial block height

  // Fetch block height when the component is mounted
  onMount(async () => {
    fetchBlockHeight();
    // Refresh block height every 60 seconds
    setInterval(fetchBlockHeight, 60000);
  });

  async function fetchBlockHeight() {
    try {
      const response = await fetch('http://localhost:5000/block_height');
      const data = await response.json();
      blockHeight = data.block_height;
    } catch (error) {
      console.error('Error fetching block height:', error);
      blockHeight = 'Error'; // Set block height to 'Error' on error
    }
  }
</script>

<!-- Modern-looking block height component -->
<div class="block-height">
  <span class="icon">🔗</span> <!-- You can replace with your own icon -->
  <span class="text">Block Height: {blockHeight}</span>
</div>

<style>
  .block-height {
    display: flex;
    align-items: center;
    background-color: #f5f5f5;
    padding: 0.5rem 1rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  .icon {
    font-size: 1.5rem;
    margin-right: 0.5rem;
  }

  .text {
    font-size: 1rem;
    font-weight: bold;
  }
</style>
