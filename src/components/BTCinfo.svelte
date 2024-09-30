<!-- src/components/BitcoinCoreInfo.svelte -->
<script lang="ts">
  import { readable } from 'svelte/store';

  // Function to transform keys to sentence case and remove special characters
  const formatKey = (key: string) => {
    return key
      .replace(/_/g, ' ')
      .replace(/(?:^|\s)\S/g, function (a) {
        return a.toUpperCase();
      });
  };

  // Fetch functions for data stores
  const fetchData = (url: string, set: Function) => {
    fetch(url)
      .then(response => response.json())
      .then(data => {
        set(data);
      })
      .catch(error => {
        console.error(`Error fetching ${url}:`, error);
      });
  };

  // Store variables to hold fetched data
  const blockchainInfo = readable({}, (set) => fetchData('http://localhost:5000/blockchain_info', set));
  const mempoolInfo = readable({}, (set) => fetchData('http://localhost:5000/mempool_info', set));
  const miningInfo = readable({}, (set) => fetchData('http://localhost:5000/mining_info', set));
  const smartFee = readable({}, (set) => fetchData('http://localhost:5000/estimate_smart_fee/6', set));
</script>

<div class="bitcoin-core-info">
  <h2>Bitcoin Core Information</h2>

  <div class="info-item">
    <h3>Blockchain Info</h3>
    {#if Object.keys($blockchainInfo).length > 0}
      <div class="info-table">
        {#each Object.entries($blockchainInfo) as [key, value]}
          <div class="info-row">
            <div class="info-key">{formatKey(key)}</div>
            <div class="info-value">{value}</div>
          </div>
        {/each}
      </div>
    {:else}
      <p>Loading...</p>
    {/if}
  </div>

  <div class="info-item">
    <h3>Mempool Info</h3>
    {#if Object.keys($mempoolInfo).length > 0}
      <div class="info-table">
        {#each Object.entries($mempoolInfo) as [key, value]}
          <div class="info-row">
            <div class="info-key">{formatKey(key)}</div>
            <div class="info-value">{value}</div>
          </div>
        {/each}
      </div>
    {:else}
      <p>Loading...</p>
    {/if}
  </div>

  <div class="info-item">
    <h3>Mining Info</h3>
    {#if Object.keys($miningInfo).length > 0}
      <div class="info-table">
        {#each Object.entries($miningInfo) as [key, value]}
          <div class="info-row">
            <div class="info-key">{formatKey(key)}</div>
            <div class="info-value">{value}</div>
          </div>
        {/each}
      </div>
    {:else}
      <p>Loading...</p>
    {/if}
  </div>

  <div class="info-item">
    <h3>Estimated Smart Fee for 6 blocks</h3>
    {#if Object.keys($smartFee).length > 0}
      <div class="info-table">
        {#each Object.entries($smartFee) as [key, value]}
          <div class="info-row">
            <div class="info-key">{formatKey(key)}</div>
            <div class="info-value">{value}</div>
          </div>
        {/each}
      </div>
    {:else}
      <p>Loading...</p>
    {/if}
  </div>
</div>

<style>
  .bitcoin-core-info {
    background-color: #f9f9f9;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    font-family: Arial, sans-serif;
    max-width: 800px;
    margin: 0 auto;
    animation: fadeIn 1s ease-in-out;
  }

  @keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
  }

  .info-item {
    margin-bottom: 20px;
  }

  h2 {
    color: #2c3e50;
    font-size: 24px;
    text-align: center;
    margin-bottom: 20px;
  }

  h3 {
    color: #34495e;
    font-size: 20px;
    margin-bottom: 10px;
  }

  .info-table {
    display: grid;
    grid-template-columns: 1fr 2fr;
    background-color: #fff;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    margin-bottom: 20px;
  }

  .info-row {
    display: contents;
  }

  .info-key, .info-value {
    padding: 10px;
    border-bottom: 1px solid #eee;
    transition: background-color 0.3s ease;
  }

  .info-key {
    background-color: #f3f4f6;
    font-weight: bold;
    color: #2c3e50;
    text-transform: capitalize;
  }

  .info-value {
    background-color: #fff;
    color: #34495e;
  }

  .info-row:hover .info-key,
  .info-row:hover .info-value {
    background-color: #e2e8f0;
  }

  p {
    color: #999;
    text-align: center;
    margin: 20px 0;
  }
</style>
