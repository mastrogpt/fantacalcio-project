<script>
	import { onMount, onDestroy } from 'svelte';
	import { fade, scale } from 'svelte/transition';

	export let modalContent;
	export let modalProps = {};
	export let toggleModal;
	export let title = '';

	const handleEscape = (event) => {
		if (event.key === 'Escape') {
			toggleModal();
		}
	};

	onMount(() => {
		document.body.style.overflow = 'hidden';
		window.addEventListener('keydown', handleEscape);
	});

	onDestroy(() => {
		document.body.style.overflow = ''; //
		window.removeEventListener('keydown', handleEscape);
	});

	const closeOnClickOutside = (event) => {
		if (event.target.classList.contains('modal')) {
			toggleModal();
		}
	};

	const handleKeyDown = (event) => {
		if (event.key === 'Enter' || event.key === ' ') {
			closeOnClickOutside(event);
		}
	};
</script>

{#if modalContent}
	<div
		class="modal"
		on:click={closeOnClickOutside}
		on:keydown={handleKeyDown}
		role="dialog"
		aria-modal="true"
		tabindex="-1"
		transition:fade
	>
		<div class="modal-container" transition:scale={{ duration: 300 }}>
			<div class="modal-header">
				{#if title}
					<h4>{title}</h4>
				{/if}

				<button class="close-button" on:click={toggleModal} aria-label="Close modal">
					<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24">
						<path
							d="M18.3 5.71a1 1 0 00-1.42-1.42L12 9.59 7.11 4.69A1 1 0 105.69 6.11L10.59 12l-4.9 4.89a1 1 0 101.42 1.42L12 14.41l4.89 4.89a1 1 0 001.42-1.42L13.41 12l4.89-4.89z"
						/>
					</svg>
				</button>
			</div>

			<div class="modal-content">
				<svelte:component this={modalContent} {...modalProps} />
			</div>
		</div>
	</div>
{/if}

<style>
	.modal {
		background-color: rgba(var(--dark), 0.4);
		position: fixed;
		display: flex;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		justify-content: center;
		align-items: center;
		z-index: 1000;
	}

	.modal-container {
		position: relative;
		background-color: white;
		padding: 2rem;
		border-radius: 0.5rem;
		box-shadow: 0 4px 6px rgba(var(--dark), 0.1);
		max-width: 90%;
		max-height: 90%;
		overflow-y: auto;
	}

	.modal-header {
		height: 3rem;
	}

	.close-button {
		position: absolute;
		top: 1rem;
		right: 1rem;
		background: transparent;
		border: none;
		cursor: pointer;
		transition: transform 0.2s;
	}

	.close-button:hover {
		transform: scale(1.2);
	}

	.close-button svg {
		fill: rgb(var(--dark));
	}

	.modal-content {
		display: flex;
		flex-direction: column;
	}
</style>
