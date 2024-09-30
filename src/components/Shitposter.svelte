<!-- App.svelte -->
<script>
  import { onMount } from 'svelte';
  import NDK, { NDKEvent, NDKNip07Signer } from "@nostr-dev-kit/ndk";
  import { writable } from 'svelte/store';

  let input = writable('');
  let detail = writable('');
  let title = writable('');
  let summary = writable('');
  let geolocation = writable('');
  let location = writable('');
  let price = writable('');
  let currency = writable('BTC');
  let frequency = writable('weekly');
  let image = writable('');
  let nip07signer;

  onMount(async () => {});

  const onSubmit = async (event) => {
    event.preventDefault();

    nip07signer = new NDKNip07Signer();

    const ndk = new NDK({
      explicitRelayUrls: ["wss://relay.primal.net", "wss://relay.snort.social"],
      signer: nip07signer
    });
    await ndk.connect();
    console.log("mounted");

    const ndkEvent = new NDKEvent(ndk);
    ndkEvent.kind = 30402;
    ndkEvent.content = $input;
    ndkEvent.tags = [
      ["d", $detail],
      ["t", $detail.toUpperCase()],
      ["title", $title],
      ["summary", $summary],
      ['image', $image, "756x1008"],
      ["g", $geolocation],
      ["location", $location],
      ["price", $price, $currency, $frequency],
    ];
    await ndk.publish(ndkEvent);

    console.log(ndkEvent);
  };
</script>

<div>
  <h2 class="text-h3 text-white mb-12">Share what you have to offer to clients.</h2>
  <form on:submit={onSubmit}>
    <input
      type="text"
      placeholder="Title"
      class="w-full p-12 rounded"
      bind:value={$title}
    />
    <input
      type="text"
      placeholder="Describe the experiences you can create for clients."
      class="w-full p-12 rounded"
      bind:value={$input}
    />
    <input
      type="text"
      placeholder="Summary"
      class="w-full p-12 rounded"
      bind:value={$summary}
    />
    <input
      type="text"
      placeholder="Tag"
      class="w-full p-12 rounded"
      bind:value={$detail}
    />
    <input
      type="text"
      placeholder="Ping from map"
      class="w-full p-12 rounded"
      bind:value={$geolocation}
    />
    <input
      type="text"
      placeholder="Location"
      class="w-full p-12 rounded"
      bind:value={$location}
    />
    <input
      type="text"
      placeholder="Price"
      class="w-full p-12 rounded"
      bind:value={$price}
    />
    <input
      type="text"
      placeholder="Currency"
      class="w-full p-12 rounded"
      bind:value={$currency}
    />
    <input
      type="text"
      placeholder="Frequency"
      class="w-full p-12 rounded"
      bind:value={$frequency}
    />
    <input
      type="text"
      placeholder="Image URL"
      class="w-full p-12 rounded"
      bind:value={$image}
    />    <p>Paste an image link preferably from nostr.build</p>
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
</style>
