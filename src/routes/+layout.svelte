<script>
	import Header from '$lib/components/molecules/Header.svelte';
	import Footer from '$lib/components/molecules/footer/footer.svelte';
	import Widget from '$lib/components/widget/Widget.svelte';
	import consoleMessage from '$lib/utils/consoleMessage';

	import '../app.css';
</script>

<Header />

<main>
	<slot />

	<Widget />
</main>

<Footer />
