<script>
	import { page } from '$app/stores';
	import logoMastroGPT from '$lib/assets/logoMastroGPT.svg';
	import VerticalMenu from '$lib/components/molecules/VerticalMenu.svelte';
	import Github from '../atoms/icons/Github.svelte';
	import LinkedIn from '../atoms/icons/LinkedIn.svelte';
	import Youtube from '../atoms/icons/Youtube.svelte';
	import JoinButton from './JoinButton.svelte';
	import Navbar from './navbar/navbar.svelte';

	$: route = $page.route.id;

	let showMenu = false;
</script>

<header class="bg-primary">
	<Navbar />
</header>
