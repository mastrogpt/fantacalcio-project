<script>
	import Header from '$lib/components/molecules/Header.svelte';
	import Footer from '$lib/components/molecules/footer/footer.svelte';
	import consoleMessage from '$lib/utils/consoleMessage';

	import '../app.css';
</script>

<Header />

<main>
	<slot />
</main>

<Footer />
