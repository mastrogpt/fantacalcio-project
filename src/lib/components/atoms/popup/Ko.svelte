<script>
	export let bodyText = 'Something went wrong';
</script>

<div role="alert" class="rounded-xl border border-primary bg-white p-4">
	<div class="flex items-start gap-2">
		<span class="text-red-600">
			<svg
				xmlns="http://www.w3.org/2000/svg"
				fill="none"
				viewBox="0 0 24 24"
				stroke-width="1.5"
				stroke="currentColor"
				class="w-5 h-5"
			>
				<path
					stroke-linecap="round"
					stroke-linejoin="round"
					d="M12 9v3.75m9-.75a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 3.75h.008v.008H12v-.008Z"
				/>
			</svg>
		</span>

		<div class="flex-1">
			<p class="mt-1 text-sm text-primary">{bodyText}</p>
		</div>
	</div>
</div>
