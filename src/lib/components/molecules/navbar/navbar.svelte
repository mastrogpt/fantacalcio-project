<script lang="ts">
	import { page } from '$app/stores';
	import { onMount } from 'svelte';

	let isOpen = false;
	let currentPath = '';
	let prova = '';

	function toggleMenu() {
		isOpen = !isOpen;
	}

	function scrollToSection(event) {
		event.preventDefault();
		const targetId = event.currentTarget.getAttribute('href').substring(1);
		const targetElement = document.getElementById(targetId);

		console.log('🔎 [navbar][targetId] =>', targetId);
		console.log('🔎 [navbar][targetElement] =>', targetElement);

		if (targetElement) {
			targetElement.scrollIntoView({ behavior: 'smooth' });
		}
	}

	onMount(() => {
		const unsubscribe = page.subscribe(($page) => {
			currentPath = $page.url.href;
		});
		return () => unsubscribe();
	});
</script>

<nav class="bg-primary text-white shadow-lg">
	<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
		<div class="flex justify-between h-16 items-center">
			<a href="/" class="flex-shrink-0 flex items-center">
				<h2 class="text-2xl font-bold">FantaAICalcio</h2>
			</a>
			<div class="hidden md:flex md:space-x-8">
				<a
					href="/"
					class={`nav-link text-lg font-medium hover:text-accent transition duration-300 ease-in-out ${currentPath === $page.url.origin + '/' ? 'active' : ''}`}
					>Home</a
				>
				<!-- <a
					href="/about"
					class={`nav-link text-lg font-medium hover:text-accent transition duration-300 ease-in-out ${currentPath === $page.url.origin + '/about' ? 'active' : ''}`}
					>Chi siamo</a
				> -->
				<a
					href="/#players"
					class={`nav-link text-lg font-medium hover:text-accent transition duration-300 ease-in-out ${currentPath === $page.url.origin + '/#players' ? 'active' : ''}`}
					>Giocatori</a
				>
				<a
					href="/#composition"
					class={`nav-link text-lg font-medium hover:text-accent transition duration-300 ease-in-out ${currentPath === $page.url.origin + '/#composition' ? 'active' : ''}`}
					>Formazioni</a
				>
			</div>
			<div class="-mr-2 flex md:hidden">
				<button
					on:click={toggleMenu}
					class="inline-flex items-center justify-center p-2 rounded-md text-white hover:text-accent focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white"
				>
					<svg
						class="h-6 w-6"
						xmlns="http://www.w3.org/2000/svg"
						fill="none"
						viewBox="0 0 24 24"
						stroke="currentColor"
						aria-hidden="true"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M4 6h16M4 12h16m-7 6h7"
						/>
					</svg>
				</button>
			</div>
		</div>
	</div>

	<div class={`md:hidden ${isOpen ? 'block' : 'hidden'}`}>
		<div class="px-4 pt-2 pb-3 space-y-1">
			<a
				href="/"
				class={`nav-link block text-lg font-medium hover:text-accent transition duration-300 py-2 ease-in-out ${currentPath === $page.url.origin + '/' ? 'active' : ''}`}
				>Home</a
			>
			<a
				href="/about"
				class={`nav-link block text-lg font-medium hover:text-accent transition duration-300 py-2 ease-in-out ${currentPath === $page.url.origin + '/about' ? 'active' : ''}`}
				>Chi siamo</a
			>
			<a
				href="/#players"
				class={`nav-link block text-lg font-medium hover:text-accent transition duration-300 py-2 ease-in-out ${currentPath === $page.url.origin + '/#players' ? 'active' : ''}`}
				>Giocatori</a
			>
			<a
				href="/#composition"
				class={`nav-link block text-lg font-medium hover:text-accent transition duration-300 py-2 ease-in-out ${currentPath === $page.url.origin + '/#composition' ? 'active' : ''}`}
				>Formazioni</a
			>
		</div>
	</div>
</nav>

<style>
	.nav-link {
		transition: all 0.3s ease;
	}

	.nav-link.active {
		color: rgb(var(--accent));
		font-weight: bold;
	}
</style>
