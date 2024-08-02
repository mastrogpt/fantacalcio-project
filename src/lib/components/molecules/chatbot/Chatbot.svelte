<script lang="ts">
	import { onMount } from 'svelte';
	import anime from 'animejs';
	import ChatbotIcon from '$lib/components/atoms/icons/ChatbotIcon.svelte';
	import { chatMessage, isChatOpen } from '$lib/store/store';

	let message = '';
	let isOpen = false;

	onMount(() => {
		// Subscribing to the stores
		const unsubscribeMessage = chatMessage.subscribe((value) => {
			message = value;
		});

		const unsubscribeChatOpen = isChatOpen.subscribe((value) => {
			isOpen = value;
		});

		// Clean up subscription on component destroy
		return () => {
			unsubscribeMessage();
			unsubscribeChatOpen();
		};
	});

	function toggleChat() {
		isOpen = !isOpen;
		isChatOpen.set(isOpen);
	}

	function sendMessage(message) {
		//console.log('🔎 [Chatbot][message] =>', message);
		// Implementa la logica per inviare un messaggio
	}

	console.log('🔎 [Chatbot][message] =>', message);
</script>

<ChatbotIcon onClick={toggleChat} />

{#if isOpen}
	<div class={`chat-window ${isOpen ? 'show' : ''}`}>
		<div class="chat-header">
			<h2>Chat Fantacalcio</h2>
			<button on:click={() => isChatOpen.set(false)}>Chiudi</button>
		</div>
		<div class="chat-body">
			{#if message}
				<p>{message}</p>
			{/if}
		</div>

		<div class="chat-input">
			<input type="text" placeholder="Scrivi un messaggio..." />
			<button>Invia</button>
		</div>
	</div>
{/if}

<style>
	.chat-window {
		position: fixed;
		bottom: 20px;
		right: 20px;
		width: 300px;
		background: white;
		box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
		border-radius: 5px;
		overflow: hidden;
		z-index: 1000;
	}
	.chat-header {
		background: #10987d;
		color: white;
		padding: 10px;
		display: flex;
		justify-content: space-between;
		align-items: center;
	}
	.chat-body {
		padding: 10px;
		max-height: 200px;
		overflow-y: auto;
	}
	.chat-input {
		display: flex;
		padding: 10px;
	}
	.chat-input input {
		flex: 1;
		padding: 5px;
		border: 1px solid #ddd;
		border-radius: 3px;
	}
	.chat-input button {
		margin-left: 5px;
		background: #10987d;
		color: white;
		border: none;
		padding: 5px 10px;
		border-radius: 3px;
	}
</style>
