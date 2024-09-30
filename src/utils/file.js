import NDK from "@nostr-dev-kit/ndk";
let events;

// Create an asynchronous function to handle the async operations
async function {

    // Create a new NDK instance with explicit relays
    const ndk = new NDK({
        explicitRelayUrls: [
            'wss://relay.primal.net',
        ],
    });

    // Connect to the relay
    await ndk.connect();
    console.log("connected");

    // Subscribe to events
    const subscription = ndk.subscribe({
        kinds: [0],
        limit: 45,
        closeOnEose: false
    });

    // Handle received events
    subscription.on('event', (event) => {
        console.log(event);
    });
}

// Call the main function to execute the code
