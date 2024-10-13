<script>
  import { onMount } from 'svelte';
  import NDK, { NDKEvent, NDKNip07Signer } from "@nostr-dev-kit/ndk";
  import { writable } from 'svelte/store';

  let input = writable('');
  let warning = writable('');
  let nip07signer;

  onMount(async () => {
    // Try to initialize the signer
    try {
      nip07signer = new NDKNip07Signer();
    } catch (error) {
      warning.set('Signer not available. Please check your NDK setup.');
    }
  });

  const onSubmit = async (event) => {
    event.preventDefault();

    if (!nip07signer) {
      warning.set('Signer not available. Cannot proceed with posting.');
      return;
    }

    const ndk = new NDK({
      explicitRelayUrls: [
      'wss://relay.snort.social',
      'wss://relay.damus.io',
      'wss://relay.nostrplebs.com',
      'wss://nos.lol',
      'wss://relay.primal.net'
      ],
      signer: nip07signer
    });
    await ndk.connect();

    console.log("connected");

    // Create a new NDK event
    const ndkEvent = new NDKEvent(ndk);

    // Create a post
    ndkEvent.kind = 1;
    ndkEvent.content = $input;

    try {

    await ndk.publish(ndkEvent);

    console.log("POSTED", ndkEvent);
    console.log("Your post has been Zapvertised!!");

    } catch (error) {
      warning.set('Failed to sign the event. Please try again.');
      console.error('Error signing the event:', error);
    }
  };
</script>

<div>
  <h2 class="text-h3 text-white mb-12">Post a note to the Nostrverse.</h2>
  {#if $warning}
    <div class="warning">{$warning}</div>
  {/if}
  <form on:submit={onSubmit}>
    <input
      type="text"
      placeholder="Shitpost more."
      class="w-full p-12 rounded"
      bind:value={$input}
    />
    <div class="flex justify-end">
      <button type="submit">
        Publish
      </button>
    </div>
  </form>
</div>

<style>
  div {
    margin-top: 20px;
  }

  input {
    margin-top: 10px;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
  }

  button {
    padding: 10px 20px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }

  button:hover {
    background-color: #0056b3;
  }

  .warning {
    color: red;
    margin-bottom: 10px;
  }
</style>
