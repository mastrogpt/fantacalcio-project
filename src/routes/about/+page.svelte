<script lang="ts">
	import Loader from '$lib/components/atoms/Loader.svelte';
	import { getAiPresentationFromBackend } from '$lib/service/aiPresentation';
	import { onMount } from 'svelte';
	import JoinButton from '$lib/components/molecules/JoinButton.svelte';

	let aiPresentation: string;
	let aiPresentationWritingEffect: string = '';
	let isLoading = false;

	async function showMessage() {
		for (let i = 0; i < aiPresentation.length; i++) {
			aiPresentationWritingEffect = aiPresentation.substring(0, i + 1);
			await sleep(25);
		}
	}

	function sleep(ms: number) {
		return new Promise((resolve) => setTimeout(resolve, ms));
	}

	async function getAiPresentation() {
		isLoading = true;
		aiPresentation = await getAiPresentationFromBackend();
		showMessage();
		isLoading = false;
	}

	onMount(async () => {
		await getAiPresentation();
	});

	export function draggable(node) {
		let pos1 = 0,
			pos2 = 0,
			pos3 = 0,
			pos4 = 0;

		function dragMouseDown(e) {
			e.preventDefault();
			pos3 = e.clientX;
			pos4 = e.clientY;
			document.onmouseup = closeDragElement;
			document.onmousemove = elementDrag;
		}

		function elementDrag(e) {
			e.preventDefault();
			pos1 = pos3 - e.clientX;
			pos2 = pos4 - e.clientY;
			pos3 = e.clientX;
			pos4 = e.clientY;
			node.style.top = `${node.offsetTop - pos2}px`;
			node.style.left = `${node.offsetLeft - pos1}px`;
		}

		function closeDragElement() {
			document.onmouseup = null;
			document.onmousemove = null;
		}

		node.onmousedown = dragMouseDown;

		return {
			destroy() {
				node.onmousedown = null;
			}
		};
	}
</script>

<div class="hero w-full flex flex-col items-center">
	<div class="content">
		<h1 class="title">Chi siamo</h1>
		<p class="description">
			Siamo sviluppatori di software, amanti del calcio, delle statistiche e delle innovazioni.
			<br/> Attraverso questo progetto, vogliamo offrire ai Fantallenatori di tutta Italia un consigliere fidato, un AI che somigli all'amico a cui chiedere consiglio il giovedì sera davanti ad una birra su che calciatore schierare o su chi comprare all'asta. 
			L'amico che ne sa, ma che non pretende di aver sempre ragione, perché il fantacalcio è arte e improvvisazione, oltre che strategia. E noi, oltre i buoni consigli, vogliamo portare fortuna!
			
			
			<br/> <i> Usiamo Nuvolaris come piattaforma, il serverless come filosofia. Se vuoi unirti a noi, clicca qui </i>
			<p class="text-2xl">👇🏻
		</p>
		<JoinButton/>
		<div class="ai-text">
			{#if aiPresentation}
				<p>{aiPresentationWritingEffect}</p>
			{:else}
				<Loader />
			{/if}
		</div>
	</div>
	<svg class="football-icon" viewBox="0 0 400 400" fill="none" xmlns="http://www.w3.org/2000/svg">
		<path
			d="M341.864 340.816C377.776 304.64 400 254.872 400 200C400 145.176 377.824 95.456 341.976 59.296C341.84 59.144 341.8 58.96 341.656 58.816C341.536 58.704 341.384 58.664 341.264 58.552C305.056 22.392 255.096 0 200 0C144.864 0 94.872 22.424 58.656 58.632C58.568 58.712 58.456 58.736 58.368 58.824C58.256 58.936 58.224 59.08 58.12 59.192C22.216 95.36 0 145.136 0 200C0 310.28 89.72 400 200 400C255.144 400 305.144 377.568 341.352 341.36C341.44 341.28 341.544 341.248 341.632 341.176C341.736 341.072 341.776 340.92 341.864 340.816ZM16.2 208H111.608C109.76 251.224 93.056 291.736 63.904 323.712C35.832 292.848 18.112 252.448 16.2 208ZM63.912 76.296C93.072 108.272 109.76 148.76 111.608 192H16.2C18.112 147.56 35.832 107.152 63.912 76.296ZM383.8 192H288.392C290.232 148.76 306.936 108.264 336.096 76.296C364.168 107.152 381.88 147.56 383.8 192ZM272.192 192H208V16.2C252.904 18.136 293.688 36.224 324.664 64.816C292.464 99.832 274.056 144.456 272.192 192ZM192 192H127.808C125.952 144.456 107.544 99.832 75.352 64.816C106.32 36.224 147.096 18.136 192 16.2V192ZM127.808 208H192V383.8C147.088 381.872 106.312 363.768 75.336 335.184C107.536 300.16 125.944 255.528 127.808 208ZM208 208H272.192C274.048 255.536 292.448 300.16 324.656 335.184C293.68 363.776 252.904 381.864 208 383.8V208ZM288.392 208H383.8C381.888 252.448 364.168 292.848 336.096 323.712C306.936 291.736 290.232 251.24 288.392 208Z"
			fill="black"
		/>
	</svg>
	<svg class="football-icon" viewBox="0 0 400 400" fill="none" xmlns="http://www.w3.org/2000/svg">
		<path
			d="M341.864 340.816C377.776 304.64 400 254.872 400 200C400 145.176 377.824 95.456 341.976 59.296C341.84 59.144 341.8 58.96 341.656 58.816C341.536 58.704 341.384 58.664 341.264 58.552C305.056 22.392 255.096 0 200 0C144.864 0 94.872 22.424 58.656 58.632C58.568 58.712 58.456 58.736 58.368 58.824C58.256 58.936 58.224 59.08 58.12 59.192C22.216 95.36 0 145.136 0 200C0 310.28 89.72 400 200 400C255.144 400 305.144 377.568 341.352 341.36C341.44 341.28 341.544 341.248 341.632 341.176C341.736 341.072 341.776 340.92 341.864 340.816ZM16.2 208H111.608C109.76 251.224 93.056 291.736 63.904 323.712C35.832 292.848 18.112 252.448 16.2 208ZM63.912 76.296C93.072 108.272 109.76 148.76 111.608 192H16.2C18.112 147.56 35.832 107.152 63.912 76.296ZM383.8 192H288.392C290.232 148.76 306.936 108.264 336.096 76.296C364.168 107.152 381.88 147.56 383.8 192ZM272.192 192H208V16.2C252.904 18.136 293.688 36.224 324.664 64.816C292.464 99.832 274.056 144.456 272.192 192ZM192 192H127.808C125.952 144.456 107.544 99.832 75.352 64.816C106.32 36.224 147.096 18.136 192 16.2V192ZM127.808 208H192V383.8C147.088 381.872 106.312 363.768 75.336 335.184C107.536 300.16 125.944 255.528 127.808 208ZM208 208H272.192C274.048 255.536 292.448 300.16 324.656 335.184C293.68 363.776 252.904 381.864 208 383.8V208ZM288.392 208H383.8C381.888 252.448 364.168 292.848 336.096 323.712C306.936 291.736 290.232 251.24 288.392 208Z"
			fill="black"
		/>
	</svg>
	<svg class="football-icon" viewBox="0 0 400 400" fill="none" xmlns="http://www.w3.org/2000/svg">
		<path
			d="M341.864 340.816C377.776 304.64 400 254.872 400 200C400 145.176 377.824 95.456 341.976 59.296C341.84 59.144 341.8 58.96 341.656 58.816C341.536 58.704 341.384 58.664 341.264 58.552C305.056 22.392 255.096 0 200 0C144.864 0 94.872 22.424 58.656 58.632C58.568 58.712 58.456 58.736 58.368 58.824C58.256 58.936 58.224 59.08 58.12 59.192C22.216 95.36 0 145.136 0 200C0 310.28 89.72 400 200 400C255.144 400 305.144 377.568 341.352 341.36C341.44 341.28 341.544 341.248 341.632 341.176C341.736 341.072 341.776 340.92 341.864 340.816ZM16.2 208H111.608C109.76 251.224 93.056 291.736 63.904 323.712C35.832 292.848 18.112 252.448 16.2 208ZM63.912 76.296C93.072 108.272 109.76 148.76 111.608 192H16.2C18.112 147.56 35.832 107.152 63.912 76.296ZM383.8 192H288.392C290.232 148.76 306.936 108.264 336.096 76.296C364.168 107.152 381.88 147.56 383.8 192ZM272.192 192H208V16.2C252.904 18.136 293.688 36.224 324.664 64.816C292.464 99.832 274.056 144.456 272.192 192ZM192 192H127.808C125.952 144.456 107.544 99.832 75.352 64.816C106.32 36.224 147.096 18.136 192 16.2V192ZM127.808 208H192V383.8C147.088 381.872 106.312 363.768 75.336 335.184C107.536 300.16 125.944 255.528 127.808 208ZM208 208H272.192C274.048 255.536 292.448 300.16 324.656 335.184C293.68 363.776 252.904 381.864 208 383.8V208ZM288.392 208H383.8C381.888 252.448 364.168 292.848 336.096 323.712C306.936 291.736 290.232 251.24 288.392 208Z"
			fill="black"
		/>
	</svg>
</div>

<style>
	.hero {
		color: white;
		padding: 60px 20px;
		position: relative;
		overflow: hidden;
	}

	.content {
		position: relative;
		z-index: 10;
		text-align: center;
		padding: 20px;
	}

	.title {
		font-size: 2rem;
		font-weight: bold;
		margin-bottom: 10px;
	}

	.subtitle {
		font-size: 1.25rem;
		margin-bottom: 20px;
	}

	.description {
		font-size: 1rem;
		max-width: 800px;
		margin: 0 auto 20px;
		line-height: 1.6;
	}

	.ai-text {
		font-size: 1rem;
		font-weight: bold;
		padding: 20px;
		background: rgba(31, 41, 55, 0.85);
		border-radius: 10px;
		margin: 0 auto;
		max-width: 800px;
	}

	.football-icon {
		position: absolute;
		width: 50px;
		height: 50px;
		opacity: 0.5;
		cursor: grab;
		animation: float 4s ease-in-out infinite;
		opacity: 0.1;
	}

	.football-icon:nth-child(1) {
		top: 20%;
		left: 10%;
		animation-delay: 0s;
	}

	.football-icon:nth-child(2) {
		top: 40%;
		left: 80%;
		animation-delay: 1s;
	}

	.football-icon:nth-child(3) {
		top: 70%;
		left: 30%;
		animation-delay: 2s;
	}

	@keyframes float {
		0% {
			transform: translate(0px, 10px);
		}
		50% {
			transform: translate(-20px, -20px);
		}
		100% {
			transform: translate(0px, 0px);
		}
	}

	@media (min-width: 1024px) {
		.title {
			font-size: 3rem;
		}

		.subtitle {
			font-size: 1.75rem;
		}

		.description,
		.ai-text {
			font-size: 1.25rem;
		}
	}
</style>
