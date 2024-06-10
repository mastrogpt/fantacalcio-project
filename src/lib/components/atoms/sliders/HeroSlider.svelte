<script lang="ts">
	import { fade } from 'svelte/transition';
	import { register } from 'swiper/element/bundle';
	import Button from '../button/button.svelte';

	register();
</script>

<swiper-container
	class="swiper-hero"
	pagination={{
		dynamicBullets: true,
		clickable: true
	}}
	effect="coverflow"
	centeredSlides={true}
	slides-per-view="auto"
	autoplay={{
		delay: 5000,
		disableOnInteraction: true,
		pauseOnMouseEnter: true
	}}
	coverflowEffect={{
		rotate: 100,
		stretch: 0,
		depth: 100,
		modifier: 1,
		slideShadows: false
	}}
	transition:fade
>
	<swiper-slide class="max-[600px]:flex-col-reverse">
		<div class="flex flex-col text-left justify-start hero-text gap-10">
			<div class="flex flex-col gap-4">
				<h2>
					Benvenuto su br
					<b class="text-accent">fantaqualcoa</b>
				</h2>

				<p>Il tuo assistente AI per il fantacalcio.</p>
			</div>

			<Button label="scopri Chi siamo!" onClick={console.log} variant="accent" />
		</div>

		<div class="hero-image">
			<img src="https://swiperjs.com/demos/images/nature-3.jpg" loading="lazy" />
		</div>
	</swiper-slide>

	<swiper-slide class="max-[600px]:flex-col-reverse">
		<div class="flex flex-col text-left justify-start hero-text gap-10">
			<div class="flex flex-col gap-4">
				<h2>
					Benvenuto su br
					<b class="text-accent">fantaqualcoa</b>
				</h2>

				<p>Il tuo assistente AI per il fantacalcio.</p>
			</div>

			<Button label="scopri Chi siamo!" onClick={console.log} variant="accent" />
		</div>

		<div class="hero-image">
			<img src="https://swiperjs.com/demos/images/nature-3.jpg" loading="lazy" />
		</div>
	</swiper-slide>

	<swiper-slide class="max-[600px]:flex-col-reverse">
		<div class="flex flex-col text-left justify-start hero-text gap-10">
			<div class="flex flex-col gap-4">
				<h2>
					Benvenuto su br
					<b class="text-accent">fantaqualcoa</b>
				</h2>

				<p>Il tuo assistente AI per il fantacalcio.</p>
			</div>

			<Button label="scopri Chi siamo!" onClick={console.log} variant="accent" />
		</div>

		<div class="hero-image">
			<img src="https://swiperjs.com/demos/images/nature-3.jpg" loading="lazy" />
		</div>
	</swiper-slide>

	<swiper-slide class="max-[600px]:flex-col-reverse">
		<div class="flex flex-col text-left justify-start hero-text gap-10">
			<div class="flex flex-col gap-4">
				<h2>
					Benvenuto su br
					<b class="text-accent">fantaqualcoa</b>
				</h2>

				<p>Il tuo assistente AI per il fantacalcio.</p>
			</div>

			<Button label="scopri Chi siamo!" onClick={console.log} variant="accent" />
		</div>

		<div class="hero-image">
			<img src="https://swiperjs.com/demos/images/nature-3.jpg" loading="lazy" />
		</div>
	</swiper-slide>
</swiper-container>

<style>
	.swiper-hero {
		width: 100%;
		height: 80vh;
	}

	swiper-container {
		width: 100%;
		padding-bottom: 50px;
	}

	swiper-slide {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 100%;
		border-radius: 20px;
		overflow: hidden;
		background-position: center;
		background-size: cover;
		padding: 0 2rem;
	}

	swiper-slide .hero-text,
	swiper-slide .hero-image {
		display: flex;
		flex: 1;
	}

	swiper-slide .hero-image {
		align-items: center;
		justify-content: center;
	}

	swiper-slide img {
		display: block;
		object-fit: cover;
		height: 450px;
		border-radius: 20px;
	}
</style>
