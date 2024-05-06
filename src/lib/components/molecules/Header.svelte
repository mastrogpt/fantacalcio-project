<script>
	import logoMastroGPT from '$lib/assets/logoMastroGPT.svg';
	import { page } from '$app/stores';
	import VerticalMenu from '$lib/components/molecules/VerticalMenu.svelte';
	import Join from './JoinButton.svelte';
	import Youtube from '../atoms/icons/Youtube.svelte';
	import Github from '../atoms/icons/Github.svelte';
	import LinkedIn from '../atoms/icons/LinkedIn.svelte';
	import JoinButton from './JoinButton.svelte';

	$: route = $page.route.id;

	let showMenu = false;
</script>

<header class="z-50">
	<div class="mx-auto flex h-16 items-center gap-8 px-4 sm:px-6 lg:px-8">
		<a class="block text-teal-600" href="https://nuvolaris.io">
			<span class="sr-only">Home</span>
			<img src={logoMastroGPT} alt="Nuvolaris Logo" class="p-2 h-4 md:h-10 lg:h-12 xl:h-14" />
		</a>

		<div class="flex flex-1 items-center justify-end md:justify-between text-l font-bold">
			<nav aria-label="Global" class="hidden md:block">
				<ul class="flex items-center gap-6">
					<li>
						<a
							class="text-gray-500 transition hover:text-gray-500/75 {route == '/'
								? 'text-primary'
								: ''}"
							href="/"
						>
							Home
						</a>
					</li>

					<li>
						<a
							class="text-gray-500 transition hover:text-gray-500/75 {route == '/all'
								? 'text-primary'
								: ''}"
							href="/all "
						>
							Giocatori
						</a>
					</li>

					<li>
						<a
							class="text-gray-500 transition hover:text-gray-500/75 {route == '/comparator'
								? 'text-primary'
								: ''}"
							href="/comparator"
						>
							Comparatore
						</a>
					</li>

					<li>
						<a
							class="text-gray-500 transition hover:text-gray-500/75 {route == '/lineup'
								? 'text-primary'
								: ''}"
							href="/lineup"
						>
							Probabili formazioni
						</a>
					</li>
					<li>
						<a
							class="text-gray-500 transition hover:text-gray-500/75 {route == '/unavailable'
								? 'text-primary'
								: ''}"
							href="/unavailable "
						>
							Indisponibili
						</a>
					</li>

					{#if route?.includes('stats')}
						<li class="flex items-center">
							<a
								class="text-gray-500 transition hover:text-gray-500/75 {route?.includes('stats')
									? 'text-primary'
									: ''}"
								href="/lineup"
							>
								Player stats
							</a>
						</li>
					{/if}
				</ul>
			</nav>

			<div class="flex items-center gap-4">
				<div class="sm:flex sm:gap-4">
					<ul class="flex gap-3">
						<li class="ml-auto">
							<button>
								<JoinButton />
							</button>
						</li>

						<li>
							<a
								href="https://www.linkedin.com/company/nuvolaris-io/"
								rel="noreferrer"
								target="_blank"
								class="text-gray-700 transition hover:opacity-75"
							>
								<span class="sr-only">LinkedIn</span>

								<LinkedIn />
							</a>
						</li>

						<li>
							<a
								href="https://github.com/nuvolaris"
								rel="noreferrer"
								target="_blank"
								class="text-gray-700 transition hover:opacity-75"
							>
								<span class="sr-only">GitHub</span>

								<Github />
							</a>
						</li>
						<li>
							<a
								href="https://www.youtube.com/@nuvolarisio"
								rel="noreferrer"
								target="_blank"
								class="text-gray-700 transition hover:opacity-75"
							>
								<span class="sr-only">Youtube</span>

								<Youtube />
							</a>
						</li>
					</ul>
				</div>

				<button class="block mt-3 rounded bg-gray-100 p-2.5 text-primary transition md:hidden">
					<button on:click={() => (showMenu = !showMenu)}>
						<svg
							xmlns="http://www.w3.org/2000/svg"
							class="h-5 w-5"
							fill="none"
							viewBox="0 0 24 24"
							stroke="currentColor"
							stroke-width="2"
						>
							<path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16" />
						</svg>
						{#if showMenu}
							<VerticalMenu />
						{/if}
					</button>
				</button>
			</div>
		</div>
	</div>
	<div>
		<h1 class="text-xl mt-2 md:text-7xl text-center text-primary tracking-wider">
			AI Fantamaster
			<div class="text-primary text-xl md:text-3xl flex items-center justify-center">
				<a href="https://nuvolaris.io">
					<span class="mr-2 text-m"> by MastroGPT</span>

					<div class="inline-block align-middle">
						<img src={logoMastroGPT} alt="Nuvolaris Logo" class="h-10 md:h-10 lg:h-16 xl:h-20" />
					</div>
				</a>
			</div>
		</h1>
	</div>
</header>
