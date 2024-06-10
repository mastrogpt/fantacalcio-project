<script>
	import { fly } from 'svelte/transition';

	let isOpen = false;
	const navItems = [
		{ label: 'Home', link: '/' },
		{ label: 'Chi siamo', link: '/about' },
		{ label: 'Giocatori', link: '/players' },
		{ label: 'Rose', link: '/composition' }
	];

	function toggleMenu() {
		isOpen = !isOpen;
	}
</script>

<nav class="relative flex items-center justify-between p-4">
	<a href="/" class="md:hidden text-white text-2xl font-bold z-20">
		<h2>FANTAQUALCOA</h2>
	</a>

	<button
		class="text-white text-2xl md:hidden z-20"
		aria-controls="navbar-menu"
		aria-expanded={isOpen}
		on:click={toggleMenu}
	>
		{isOpen ? '✖' : '☰'}
	</button>

	<div class="hidden md:flex flex-1 justify-center">
		<ul class="flex items-center space-x-8">
			{#each navItems.slice(0, Math.ceil(navItems.length / 2)) as navItem}
				<li class="menu-item">
					<a href={navItem.link} class="text-white relative hover:text-gray-300">{navItem.label}</a>
				</li>
			{/each}

			<li class="flex items-center menu-item px-12">
				<a href="/" class="text-white text-2xl font-bold z-20">
					<h2>FANTAQUALCOA</h2>
				</a>
			</li>

			{#each navItems.slice(Math.ceil(navItems.length / 2)) as navItem}
				<li class="menu-item">
					<a href={navItem.link} class="text-white relative hover:text-gray-300">{navItem.label}</a>
				</li>
			{/each}
		</ul>
	</div>

	{#if isOpen}
		<ul
			class="mobile-menu absolute top-20 left-0 w-full flex flex-col items-center space-y-4 py-4 md:hidden z-10"
			transition:fly={{ y: -100 }}
		>
			{#each navItems as navItem}
				<li class="menu-item">
					<a href={navItem.link} class="text-white">{navItem.label}</a>
				</li>
			{/each}
		</ul>
	{/if}
</nav>

<style>
	@tailwind components;
	@tailwind utilities;

	nav a::before {
		content: '';
		position: absolute;
		width: 0;
		height: 2px;
		bottom: -2px;
		left: 50%;
		transform: translateX(-50%);
		background-color: white;
		transition: width 0.3s;
	}

	nav a:hover::before,
	nav a:focus::before {
		width: 100%;
	}

	nav,
	ul {
		background: var(--primary);
	}

	.mobile-menu {
		background: rgb(var(--primary));
	}
</style>
