<script>
	export let href = '#';
	export let text = 'Download';
	/**
	 * @type {(() => void) | null}
	 */
	export let clickAction = null;

	export function handleClick() {
		if (clickAction) {
			console.log('clicked');
			clickAction();
		}
	}
</script>

<a
	class="group inline-block rounded-full bg-gradient-to-r from-primary via-secondary to-secondary p-[2px] hover:text-white focus:outline-none focus:ring active:text-opacity-75"
	{href}
	on:click={() => handleClick()}
>
	<span
		class="block rounded-full bg-white px-8 py-3 text-sm font-medium group-hover:bg-transparent"
	>
		{text}
	</span>
</a>
