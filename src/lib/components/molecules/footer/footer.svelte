
<div class="footer">
	<div class="footer-content flex justify-between">
		<div class="footer-section">
			<h2 class="footer-title text-primary">FantaAICalcio</h2>
			<a href="mailto:info@nuvolaris.io" class="footer-email">info@nuvolaris.io
			</a>
		</div>
		<div class="footer-section align-end justify-end text-right">
			<h2 class="footer-title">Quick Links</h2>
			<ul class="footer-links">
				<li><a href="/"> Home</a></li>
				<li>  <a href="/about"> Chi siamo </a>
				</li>
				<li><a href="/#players">Giocatori</a></li>
				<li><a href="/#composition">Probabili formazioni</a></li>
			</ul>
		</div>
		
	</div>
	<div class="footer-bottom flex space-x-0">
		<div class="footer-social">
			<a href="https://www.linkedin.com/company/nuvolaris-io/" class="social-icon">in</a>
			<a href="https://x.com/NuvolarisIO" class="social-icon">t</a>
		</div>

		<div class="text-center">
			<p>A product of <br /> <span class="footer-brand">
				
				<a href="https://mastrogpt.nuvolaris.dev/"> Mastrogpt </a></span></p>
		</div>

		<div>
			<p>© 2024. All rights reserved</p>
		</div>
	</div>
</div>

<style>
	.footer {
		background-color: #ffd700;
		padding: 20px;
		color: black;
	}

	.footer-content {
		display: flex;
		flex-wrap: wrap;
		justify-content: space-between;
		align-items: flex-start;
	}

	.footer-section {
		flex: 1 1 30%;
		margin: 10px;
	}

	.footer-title {
		font-size: 1.5em;
	}

	.footer-email {
		color: black;
		text-decoration: none;
	}

	.footer-links {
		list-style: none;
		padding: 0;
	}

	.footer-links li {
		margin: 5px 0;
	}

	.footer-links a {
		color: black;
		text-decoration: none;
	}

	.footer-subscribe {
		display: flex;
		align-items: center;
	}

	.footer-input {
		padding: 10px;
		border: none;
		flex: 1;
	}

	.footer-button {
		background-color: rgb(var(--primary));
		color: white;
		border: none;
		padding: 10px;
		cursor: pointer;
	}

	.footer-bottom {
		display: flex;
		flex-wrap: wrap;
		justify-content: space-between;
		align-items: center;
		margin-top: 20px;
		border-top: 1px solid #ddd;
		padding-top: 20px;
	}

	.footer-social {
		display: flex;
		margin: 10px 0;
	}

	.social-icon {
		background-color: #333;
		color: white;
		border-radius: 50%;
		width: 30px;
		height: 30px;
		display: flex;
		align-items: center;
		justify-content: center;
		margin: 0 5px;
		text-decoration: none;
	}

	.footer-note {
		text-align: right;
		flex: 1 1 100%;
		margin: 10px 0;
	}

	.footer-brand {
		color: #00c0c0;
		font-weight: bold;
	}

	@media (max-width: 768px) {
		.footer-content {
			flex-direction: column;
		}

		.footer-section {
			flex: 1 1 100%;
			margin: 10px 0;
		}

		.footer-bottom {
			flex-direction: column;
			text-align: center;
		}

		.footer-note {
			text-align: center;
			flex: 1 1 100%;
		}
	}
</style>
