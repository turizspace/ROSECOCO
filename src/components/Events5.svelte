<script>
import { onMount, onDestroy } from 'svelte';
import NDK from "@nostr-dev-kit/ndk";
import Icon from '@iconify/svelte'; // Ensure you have this installed

let eventsKind1 = [];
let profiles = {};
let isLoading = true;

let ndk;
let subscriptionKind1;
let subscriptionKind0;

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
      authors: ['06830f6cb5925bd82cca59bda848f0056666dff046c5382963a997a234da40c5',
      '8097a42ccf7806cc1af5fda269048be1972167c6c6516a211616e6c1da0f15e6',
      'd7c6d014b342815ba29c48f3449e4f0073df84f4ad580ae173538041a6abb6b8',
      '9cb3545c36940d9a2ef86d50d5c7a8fab90310cc898c4344bcfc4c822ff47bca',
      'd662c10fcdb2b990cb13f9e934f4798d9bd0991979d03aaa052ccb6478d039af',
      'f4db5270bd991b17bea1e6d035f45dee392919c29474bbac10342d223c74e0d0']
    });

    // Handle incoming events of kind 1
    subscriptionKind1.on('event', (event) => {
      console.log("Kind 1 event received:", event);
      eventsKind1 = [...eventsKind1, event];
      isLoading = false; // Stop loading once the first event is received
    });

    // Subscribe to events of kind 0
    subscriptionKind0 = ndk.subscribe({
      kinds: [0],
      authors: ['06830f6cb5925bd82cca59bda848f0056666dff046c5382963a997a234da40c5',
      '8097a42ccf7806cc1af5fda269048be1972167c6c6516a211616e6c1da0f15e6',
      'd7c6d014b342815ba29c48f3449e4f0073df84f4ad580ae173538041a6abb6b8',
      '9cb3545c36940d9a2ef86d50d5c7a8fab90310cc898c4344bcfc4c822ff47bca',
      'd662c10fcdb2b990cb13f9e934f4798d9bd0991979d03aaa052ccb6478d039af',
      'f4db5270bd991b17bea1e6d035f45dee392919c29474bbac10342d223c74e0d0']
    });

    // Handle incoming events of kind 0
    subscriptionKind0.on('event', (event) => {
      try {
        const profile = JSON.parse(event.content); // Parse the content field
        profiles[event.pubkey] = profile; // Store the parsed profile data
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

function handleZap(lud16) {
  alert(`Zap address: ${lud16}`);
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
</script>

<style>
.loading {
  font-size: 18px;
  color: #007bff;
  margin-bottom: 10px;
}

.content-card {
margin-top: 20px;
display: flex;
flex-direction: column;
gap: 10px;
width: 22em;
max-width: 24em;
margin: 0 auto;
padding: 20px;
background: #f8f9fa;
border-radius: 10px;
box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
box-sizing: border-box;
overflow: hidden; /* Prevent overflow of modal */
word-wrap: break-word; /* Prevent text overflow */
word-break: break-word; /* Force break long words */
white-space: normal; /* Ensure text wraps inside container */
}

.profile-card {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
}

.profile-card img {
  border-radius: 50%;
  width: 80px;
  height: 80px;
  margin-right: 16px;
}

.profile-card div {
  display: flex;
  flex-direction: column;
}

.profile-card h3 {
  margin: 0;
  font-size: 18px;
}

.profile-card p {
  margin: 0;
  font-size: 14px;
  color: #666;
}

.zap-button {
  background-color: #f7d74e;
  border: none;
  border-radius: 4px;
  padding: 8px 16px;
  font-size: 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
  margin-top: 8px;
}

.zap-button:hover {
  background-color: #f5c141;
}

.zap-icon {
  margin-left: 8px;
}

.content-card pre {
  white-space: pre-wrap;
  word-break: break-word;
}

.image-gallery {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 16px;
}

.image-gallery img {
  max-width: auto;
  height: 254px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
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
            </div>
          </div>

          <pre>{event.content}</pre>

          {#if getImageUrls(event.tags).length > 0}
            <div class="image-gallery">
              {#each getImageUrls(event.tags) as image}
                <img src={image} alt="Event Image">
              {/each}
            </div>
          {/if}

          {#if extractImageUrls(event.content).length > 0}
            <div class="image-gallery">
              {#each extractImageUrls(event.content) as image}
                <img src={image} alt="Event Image">
              {/each}
            </div>
          {/if}

          <p>Posted on: {new Date(event.created_at * 1000).toLocaleString()}</p>
        </div>
      {/if}
    {/each}
  {/if}
</div>
