<script lang="ts">
	import { register } from 'swiper/element/bundle';
	import { fade } from 'svelte/transition';

	register();

	const sliderContainerCommonProps = {
		'space-between': 50,
		pagination: false,
		'slides-per-view': 'auto',
		loop: true,
		autoplay: {
			delay: 3500,
			disableOnInteraction: true,
			pauseOnMouseEnter: true
		}
	};
</script>

<div class="flex flex-col gap-[50px]">
	<swiper-container class="articles-slider-up" {...sliderContainerCommonProps} transition:fade>
		<swiper-slide>Slide 1</swiper-slide>
		<swiper-slide>Slide 2</swiper-slide>
		<swiper-slide>Slide 3</swiper-slide>
		<swiper-slide>Slide 4</swiper-slide>
		<swiper-slide>Slide 5</swiper-slide>
		<swiper-slide>Slide 6</swiper-slide>
		<swiper-slide>Slide 7</swiper-slide>
		<swiper-slide>Slide 8</swiper-slide>
		<swiper-slide>Slide 9</swiper-slide>
	</swiper-container>

	<swiper-container class="articles-slider-bottom" {...sliderContainerCommonProps} transition:fade>
		<swiper-slide>Slide 1</swiper-slide>
		<swiper-slide>Slide 2</swiper-slide>
		<swiper-slide>Slide 3</swiper-slide>
		<swiper-slide>Slide 4</swiper-slide>
		<swiper-slide>Slide 5</swiper-slide>
		<swiper-slide>Slide 6</swiper-slide>
		<swiper-slide>Slide 7</swiper-slide>
		<swiper-slide>Slide 8</swiper-slide>
		<swiper-slide>Slide 9</swiper-slide>
	</swiper-container>
</div>

<style>
	swiper-container {
		width: 100vw;
		height: 100%;
	}

	swiper-slide {
		text-align: center;
		font-size: 18px;
		background: #fff;
		display: flex;
		justify-content: center;
		align-items: center;
		width: 350px;
		height: 300px;
		border: solid 1px;
		border-radius: 20px;
		overflow: hidden;
	}
</style>
