<script>
	import Ok from '$lib/components/atoms/popup/Ok.svelte';
	import { sendMessage } from '$lib/service/slackNotifier';
	import Button from '../atoms/button/button.svelte';
	import Ko from '../atoms/popup/Ko.svelte';

	let showModal = false;
	var regexEmail = /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/;
	let userMessage = '';
	let showPopupOk = false;
	let showPopupKo = false;

	function showModalFun() {
		showModal = !showModal;
		userMessage = '';
	}

	async function postMessage() {
		try {
			await sendMessage('Someone is interested to Nuvolaris Fantamaster: ' + userMessage);

			userMessage = '';
			showModalFun();
			showPopupOk = true;

			await new Promise((r) => setTimeout(r, 1500));

			showPopupOk = false;
		} catch (error) {
			console.log('Error while sending message', error);
			showPopupKo = true;
			showModalFun();
		}
	}
</script>

<button on:click={() => showModalFun()}>
	👉🏻 <b class="underline font-bold">clicca qui</b> 👈🏻
</button>

{#if showModal}
	<div class="fixed z-10 inset-0 flex items-center justify-center bg-black bg-opacity-50">
		<section class="relative rounded-3xl shadow-2xl w-4/5 bg-white">
			<div class="p-6 text-center sm:p-4">
				<h5 class="mt-2">
					Vuoi unirti al progetto? Inserisci la tua la mail e ti contatteremo al più presto!
				</h5>
				<div>
					<textarea
						class="m-4 p-2 w-4/5 border border-primary rounded-lg border-gray-200 shadow-sm sm:text-sm"
						rows="2"
						placeholder="Inserisci la tua mail..."
						bind:value={userMessage}
					/>
				</div>
				<div class="flex-auto">
					<div class="mt-2">
						<Button variant="accent" label="Annulla" onClick={showModalFun} />

						{#if regexEmail.test(userMessage)}
							<Button label="Conferma" onClick={postMessage} />
						{/if}
					</div>
				</div>
			</div>
		</section>
	</div>
{/if}

{#if showPopupOk}
	<div class="fixed z-10 inset-0 flex items-center justify-center bg-black bg-opacity-50">
		<div class="bg-opacity-85">
			<Ok bodyText="Ti contatteremo al più presto" />
		</div>
	</div>
{/if}

{#if showPopupKo}
	<div class="fixed z-10 inset-0 flex items-center justify-center bg-black bg-opacity-50">
		<div class="bg-opacity-85">
			<Ko bodyText="C'è stato un errore imprevisto" />
		</div>
	</div>
{/if}
