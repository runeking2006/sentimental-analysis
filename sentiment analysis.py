import sys

try:
	from textblob import TextBlob
except Exception:
	print(
		"Missing dependency 'textblob'. Install it with: python -m pip install textblob",
		file=sys.stderr,
	)
	sys.exit(1)

try:
	from newspaper import Article
except Exception:
	print(
		"Missing dependency 'newspaper3k' or one of its extras.\n"
		"Install with: python -m pip install newspaper3k lxml_html_clean",
		file=sys.stderr,
	)
	sys.exit(1)


def analyze_url(url: str) -> int:
	"""Download article at `url`, print a summary and sentiment polarity.

	Returns 0 on success, non-zero on failure.
	"""
	try:
		article = Article(url)
		article.download()
		article.parse()
		# NLP step (may fail if article is empty or network issues)
		try:
			article.nlp()
		except Exception:
			# newspaper3k's nlp can fail silently; continue with parsed text
			pass

		text = article.summary or article.text or ""
		if not text.strip():
			print("No summary or article text could be extracted.")
			return 2

		print("Article Summary:")
		print(text)
		print("-" * 20)  # Separator

		blob = TextBlob(text)
		sentiment = blob.sentiment.polarity  # Value between -1 and 1
		print(f"Sentiment Polarity: {sentiment}")
		return 0

	except Exception as exc:
		print(f"Error while processing the article: {exc}", file=sys.stderr)
		return 1


if __name__ == "__main__":
	# Default URL (change as needed)
	url = (
		"https://www.dinamalar.com/news/india-tamil-news/aiadmks-brahmastra-is-a-double-leaf-says-rajini-/3788417"
	)
	sys.exit(analyze_url(url))