<script>
  import { onMount } from 'svelte';
  import NDK, { NDKEvent, NDKNip07Signer } from "@nostr-dev-kit/ndk";
  import ZAP from "../assets/images/ZAP.png";
  import { getZapEndpoint, makeZapRequest, useFetchImplementation } from '../utils/zapUtils.js';

  let events = [];
  let showModal = false;
  let currentLud16 = '';
  let zapAmount = '';
  let customZapComment = '';
  let customZapAmountMillisats = ''; // Amount in millisats
  let customZapAmountSats = ''; // Amount in sats
  const defaultZapAmounts = [5000, 10000, 20000, 50000];

  let ndk; // Define ndk in the component scope
  let nip07signer;

  onMount(async () => {
    nip07signer = new NDKNip07Signer();

    ndk = new NDK({
      explicitRelayUrls: [
        'wss://relay.damus.io',
      ],
      signer: nip07signer
    });

    await ndk.connect();
    console.log("connected");

    const subscription = ndk.subscribe({
      kinds: [0],
      limit: 45
    });

    subscription.on('event', (event) => {
      const eventData = JSON.parse(event.content);
      events = [...events, { ...eventData, id: event.id }];
    });
  });

  function showLud16(lud16) {
    currentLud16 = lud16;
    showModal = true;
  }

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
      const amountToSend = customZapAmountMillisats || zapAmount;
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

      const response = await fetch(`${callback}?amount=${amountToSend}&nostr=${JSON.stringify(zapRequest)}`);
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

  function closeModal() {
    showModal = false;
    currentLud16 = '';
    customZapAmountMillisats = ''; // Reset custom amount input in millisats
    customZapAmountSats = ''; // Reset custom amount input in sats
    zapAmount = ''; // Reset zap amount
    customZapComment = ''; // Reset custom comment
  }

  function setZapAmount(amount) {
    customZapAmountMillisats = amount.toString();
    customZapAmountSats = (amount / 1000).toFixed(0); // Convert to sats for UI
  }
</script>

<div class="event-container">
  {#if events.length > 0}
    {#each events as event (event.id)}
      <div class="event">
        <img src={event.picture} alt={event.name} width="50" height="50" />
        <div class="event-details">
          <div class="text-details">
            <p class="event-name">{event.name}</p>
            {#if event.about}
              <p class="event-about">{event.about}</p>
            {/if}
          </div>
          {#if event.lud16}
            <button on:click={() => showLud16(event.lud16)} class="zap-button" aria-label="Zap {event.name}">
              <img src={ZAP} alt="Zap pleb" width="30" height="30" aria-hidden="true" />
            </button>
          {/if}
        </div>
      </div>
    {/each}
  {:else}
    <p>No events available.</p>
  {/if}

  {#if showModal}
    <div class="modal" aria-modal="true" aria-labelledby="modal-title" role="dialog">
      <div class="modal-content">
        <span class="close" on:click={closeModal} aria-label="Close">&times;</span>
        <h2 id="modal-title" class="modal-title">Zap {currentLud16}</h2>
        <div class="zap-amounts">
          <p>Select Zap Amount:</p>
          {#each defaultZapAmounts as amount}
            <button on:click={() => setZapAmount(amount)}>{amount / 1000} sats</button>
          {/each}
        </div>
        <div class="custom-amount">
          <input type="number" bind:value={customZapAmountSats} placeholder="Custom Amount (sats)" min="1" on:input={() => customZapAmountMillisats = (customZapAmountSats * 1000).toString()} />
        </div>
        <div class="custom-amount">
          <input type="text" bind:value={customZapComment} placeholder="Add comment" />
        </div>
        <button class="send-button" on:click={handleZap}>Send Zap</button>
      </div>
    </div>
  {/if}
</div>



<style>
.event-container {
margin-top: 20px;
display: flex;
flex-direction: column;
gap: 10px;
width: 29em;
max-width: 30em;
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

  .event {
      background: #fff;
      border-radius: 10px;
      padding: 15px;
      display: flex;
      align-items: center;
      flex-wrap: wrap;
      transition: transform 0.3s, box-shadow 0.3s;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
      box-sizing: border-box;
  }

  .event:hover {
      transform: translateY(-5px);
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
  }

  .event img {
      border-radius: 50%;
      margin-right: 15px;
      transition: transform 0.3s;
  }

  .event img:hover {
      transform: scale(1.1);
  }

  .event-details {
      display: flex;
      flex: 1;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
  }

  .text-details {
      display: flex;
      flex-direction: column;
      flex: 1;
      min-width: 0; /* Prevent overflow */
  }

  .event-name {
      margin: 0;
      font-size: 1.2em;
      font-weight: bold;
      color: #333;
      word-wrap: break-word;
  }

  .event-about {
      margin: 5px 0 0;
      font-size: 0.9em;
      color: #666;
      word-wrap: break-word;
  }

  .zap-button {
      background: none;
      border: none;
      cursor: pointer;
      padding: 0;
      transition: transform 0.3s;
  }

  .zap-button img {
      display: block;
      transition: transform 0.3s;
  }

  .zap-button:hover img {
      transform: scale(1.2);
  }

  @media (max-width: 600px) {
      .event {
          flex-direction: column;
          text-align: center;
      }

      .event img {
          margin-right: 0;
          margin-bottom: 10px;
      }

      .event-details {
          justify-content: center;
      }

      .zap-button {
          margin-top: 10px;
      }
  }

  .modal {
    background: rgba(0, 0, 0, 0.5);
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }

  .modal-content {
    background: white;
    border-radius: 10px;
    padding: 20px;
    position: relative;
    width: 300px;
  }

  .close {
    position: absolute;
    top: 10px;
    right: 10px;
    font-size: 24px;
    cursor: pointer;
  }

  .modal-title {
    font-size: 20px;
    font-weight: bold;
    margin-bottom: 15px;
  }

  .zap-amounts {
    margin-bottom: 15px;
  }

  .zap-amounts button {
    margin-right: 10px;
    margin-bottom: 10px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    padding: 5px 10px;
    cursor: pointer;
  }

  .zap-amounts button:hover {
    background-color: #0056b3;
  }

  .custom-amount input {
    margin-bottom: 15px;
    padding: 5px;
    border-radius: 5px;
    border: 1px solid #ccc;
    width: 100%;
    box-sizing: border-box;
  }

  .send-button {
    background-color: #28a745;
    color: white;
    border: none;
    border-radius: 5px;
    padding: 10px;
    cursor: pointer;
    width: 100%;
  }

</style>
