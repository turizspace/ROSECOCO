<script>
import { onMount, onDestroy } from 'svelte';
import NDK from "@nostr-dev-kit/ndk";
import Icon from '@iconify/svelte'; // Ensure you have this installed
import { getZapEndpoint, makeZapRequest } from '../utils/zapUtils.js';



let eventsKind1 = [];
let profiles = {};
let isLoading = true;

let ndk;
let subscriptionKind1;
let subscriptionKind0;

let events = [];
let showModal = false;
let currentLud16 = '';
let customZapComment = '';
let customZapAmountMillisats = ''; // Amount in millisats
const defaultZapAmounts = [5000, 10000, 20000, 50000];

onMount(async () => {
  try {
    // Initialize NDK with the signer
    ndk = new NDK({
      explicitRelayUrls: [
        'wss://relay.snort.social',
        'wss://relay.primal.net',
        'wss://nostr-02.dorafactory.org',
        'wss://relay.snort.social',
        'wss://relay.damus.io',
        'wss://relay.nostrplebs.com',
        'wss://nos.lol',
        'wss://relay.primal.net'
      ],
    });

    // Connect to the relay
    await ndk.connect();
    console.log("Connected to relay");

    // Subscribe to events of kind 1
    subscriptionKind1 = ndk.subscribe({
      kinds: [30402],

    });

    // Handle incoming events of kind 1
    subscriptionKind1.on('event', (event) => {
      eventsKind1 = [...eventsKind1, event];
      isLoading = false; // Stop loading once the first event is received
    });

    // Subscribe to events of kind 0
    subscriptionKind0 = ndk.subscribe({
      kinds: [0],

    });

    // Handle incoming events of kind 0
    subscriptionKind0.on('event', (event) => {
      try {
        const profile = JSON.parse(event.content); // Parse the content field
        profiles[event.pubkey] = profile; // Store the parsed profile data
        // Check if lud16 is present in profile
        if (profile.lud16) {
        }
      } catch (error) {
        console.error("Error parsing profile content:", error);
      }
    });

    // Handle subscription errors
    subscriptionKind1.on('error', (error) => {
      console.error("Subscription error (Kind 1):", error);
    });

    subscriptionKind0.on('error', (error) => {
      console.error("Subscription error (Kind 0):", error);
    });

  } catch (error) {
    console.error("Error during onMount:", error);
  }
});

onDestroy(() => {
  // Clean up subscriptions and connections when the component is destroyed
  if (subscriptionKind1) {
  }

  if (subscriptionKind0) {
  }

  if (ndk) {
  }
});

// Open the modal
function openModal(lud16) {
  currentLud16 = lud16;
  showModal = true;
}

// Close the modal
function closeModal() {
  showModal = false;
  customZapComment = '';
  customZapAmountMillisats = '';
}

// Function to send zaps
async function handleZap() {
  if (!ndk) {
    console.error('NDK is not defined');
    return;
  }

  const metadata = {
    content: JSON.stringify({
      lud16: currentLud16,
      comment: customZapComment // Include the comment in the metadata
    })
  };
  const callback = await getZapEndpoint(metadata);

  if (callback) {
    const amountToSend = customZapAmountMillisats; // Amount in millisats
    if (!amountToSend) {
      console.error('Please enter a zap amount.');
      return;
    }

    const zapRequest = makeZapRequest({
      profile: currentLud16,
      event: null,
      amount: amountToSend,
      comment: customZapComment, // Include the comment in the zap request
      relays: ['wss://relay.damus.io'],
    });

    const response = await fetch(`${callback}?amount=${amountToSend}`);
    const { pr: invoice } = await response.json();

    console.log('Invoice:', invoice);

    try {
      // Check if WebLN is available
      if (window.webln) {
        await window.webln.enable(); // Request permission to use WebLN
        await window.webln.sendPayment(invoice); // Send payment using WebLN
        console.log('Payment sent successfully via WebLN!');
      } else {
        console.error('WebLN not available.'); // Provide fallback if WebLN is unavailable
        alert('WebLN not available. Please ensure you have a WebLN-enabled browser extension.');
      }
    } catch (err) {
      console.error('WebLN error:', err);
      alert('Failed to send payment via WebLN.');
    }

  } else {
    console.error('Failed to get zap endpoint.');
  }

  closeModal();
}

// Function to get image URLs from event.tags
function getImageUrls(tags) {
  return tags
    .filter(tag => tag[0] === 'image')
    .map(tag => tag[1]);
}

// Function to find image URLs in event.content
function extractImageUrls(content) {
  const imageUrlRegex = /https?:\/\/[^\s]+(?:\.jpg|\.jpeg|\.png|\.gif)/gi;
  return content.match(imageUrlRegex) || [];
}

function getPrice(tags) {
  const priceTag = tags.find(tag => tag[0] === 'price');
  return priceTag ? `${priceTag[1]} ${priceTag[2]}` : 'Price not available';
}
</script>

<style>
  /* Loading spinner */
  .loading {
    font-size: 18px;
    color: #007bff;
    margin-bottom: 10px;
    font-weight: bold;
    text-align: center;
  }

  /* Main content card styling */
  .content-card {
    margin-top: 20px;
    display: flex;
    flex-direction: column;
    gap: 20px;
    width: 100%;
    max-width: 30em;
    margin: 0 auto;
    padding: 20px;
    background: #f8f9fa;
    border-radius: 12px;
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
    box-sizing: border-box;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
  }

  .content-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15);
  }

  /* Profile card styling */
  .profile-card {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 20px;
  }

  .profile-card img {
    border-radius: 50%;
    width: 80px;
    height: 80px;
    object-fit: cover;
  }

  .profile-card div {
    display: flex;
    flex-direction: column;
  }

  .profile-card h3 {
    margin: 0;
    font-size: 20px;
    font-weight: 600;
    color: #333;
  }

  .profile-card p {
    margin: 0;
    font-size: 14px;
    color: #777;
  }

  /* Zap button */
  .zap-button {
    background-color: #f7d74e;
    border: none;
    border-radius: 8px;
    padding: 10px 18px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    transition: background-color 0.3s ease;
  }

  .zap-button:hover {
    background-color: #f5c141;
  }

  .zap-button:active {
    transform: scale(0.98);
  }

  .zap-icon {
    margin-left: 8px;
  }

  /* Preformatted text */
  .content-card pre {
    white-space: pre-wrap;
    word-break: break-word;
    font-size: 14px;
    color: #444;
    padding: 12px;
    background: #f0f1f3;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  /* Image gallery */
  .image-gallery {
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
    justify-content: center;
  }

  .image-gallery img {
    width: 100%;
    max-width: 200px;
    height: auto;
    border-radius: 8px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
  }

  /* Modal styling */
  .modal {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 100;
  }

  .modal-content {
    background: white;
    padding: 20px;
    border-radius: 12px;
    width: 320px;
    max-width: 90%;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease;
  }

  .modal-content h3 {
    font-size: 20px;
    font-weight: 600;
    margin-bottom: 16px;
    color: #333;
  }

  .modal-content label {
    font-size: 14px;
    color: #666;
    margin-top: 12px;
  }

  .modal-content input,
  .modal-content textarea {
    width: 100%;
    padding: 10px;
    margin-top: 6px;
    font-size: 14px;
    border: 1px solid #ccc;
    border-radius: 8px;
    background: #f9f9f9;
    box-sizing: border-box;
  }

  .modal-content textarea {
    height: 100px;
  }

  .modal-content button {
    background-color: #f7d74e;
    border: none;
    border-radius: 8px;
    padding: 12px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    width: 100%;
    margin-top: 20px;
    transition: background-color 0.3s ease;
  }

  .modal-content button:hover {
    background-color: #f5c141;
  }

  .modal-content .close {
    position: absolute;
    top: 10px;
    right: 10px;
    font-size: 24px;
    cursor: pointer;
    color: #333;
  }
</style>

<div>
  {#if isLoading}
    <div class="loading">Loading events...</div>
  {/if}

  {#if eventsKind1.length > 0}
    {#each eventsKind1 as event (event.id)}
      {#if profiles[event.pubkey]}
        <div class="content-card">
          <div class="profile-card">
            <img src={profiles[event.pubkey].picture || 'https://via.placeholder.com/80'} alt="Profile Picture">
            <div>
              <h3>{profiles[event.pubkey].name || 'Unknown'}</h3>
              <p>{profiles[event.pubkey].about || 'No bio available'}</p>
            </div>
          </div>
          <pre>{event.content}</pre>
          <div class="image-gallery">
            {#each getImageUrls(event.tags) as imageUrl}
              <img src={imageUrl} alt="Image from event">
            {/each}
          </div>
          <div>
            <span>{getPrice(event.tags)}</span>
            <button class="zap-button" on:click={() => openModal(profiles[event.pubkey].lud16)}>
              Zap <Icon icon="mdi:zap" class="zap-icon" />
            </button>
          </div>
        </div>
      {/if}
    {/each}
  {/if}

  {#if showModal}
    <div class="modal" on:click={closeModal}>
      <div class="modal-content" on:click|stopPropagation>
        <span class="close" on:click={closeModal}>&times;</span>
        <h3>Send a Zap</h3>
        <label for="zap-amount">Amount (in millisats):</label>
        <input type="number" id="zap-amount" bind:value={customZapAmountMillisats} placeholder="e.g., 5000">
        <label for="zap-comment">Comment:</label>
        <textarea id="zap-comment" bind:value={customZapComment} placeholder="Your comment..."></textarea>
        <button on:click={handleZap}>Send Zap</button>
      </div>
    </div>
  {/if}
</div>
