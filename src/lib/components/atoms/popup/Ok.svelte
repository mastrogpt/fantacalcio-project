<script>
	export let bodyText = 'Everything ok';
</script>

<div role="alert" class="rounded-xl border border-primary bg-white p-4">
	<div class="flex items-start gap-2">
		<span class="text-green-600">
			<svg
				xmlns="http://www.w3.org/2000/svg"
				fill="none"
				viewBox="0 0 24 24"
				stroke-width="1.5"
				stroke="currentColor"
				class="h-5 w-5"
			>
				<path
					stroke-linecap="round"
					stroke-linejoin="round"
					d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
				/>
			</svg>
		</span>

		<div class="flex-1">
			<p class="mt-1 text-sm text-primary">{bodyText}</p>
		</div>
	</div>
</div>
