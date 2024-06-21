<script>
	import { page } from '$app/stores';
	import Navbar from './navbar/navbar.svelte';

	$: route = $page.route.id;

	let showMenu = false;
</script>

<header class="bg-primary">
	<Navbar />
</header>
