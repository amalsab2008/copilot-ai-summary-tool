"""
Simple AI Summary Tool
A beginner-friendly script that generates summaries of paragraphs using basic NLP logic.
"""

import re
from collections import Counter


def preprocess_text(text):
    """Convert text to lowercase and remove extra whitespace."""
    text = text.lower()
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def split_into_sentences(text):
    """Split text into sentences using common punctuation."""
    sentences = re.split(r'[.!?]+', text)
    # Remove empty strings and strip whitespace
    sentences = [s.strip() for s in sentences if s.strip()]
    return sentences


def get_important_words(text, num_words=10):
    """
    Extract the most important words from text.
    Ignores common stop words and punctuation.
    """
    # Common English stop words to ignore
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'be', 'been',
        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
        'should', 'may', 'might', 'can', 'that', 'this', 'it', 'its', 'which'
    }
    
    # Extract words and remove punctuation
    words = re.findall(r'\b[a-z]+\b', text.lower())
    
    # Filter out stop words and count remaining words
    important_words = [w for w in words if w not in stop_words]
    word_freq = Counter(important_words)
    
    # Return the most common words
    return word_freq.most_common(num_words)


def score_sentences(sentences, important_words):
    """
    Score each sentence based on how many important words it contains.
    Returns a list of (sentence, score) tuples.
    """
    word_dict = {word: freq for word, freq in important_words}
    
    scored_sentences = []
    for sentence in sentences:
        words = re.findall(r'\b[a-z]+\b', sentence.lower())
        score = sum(word_dict.get(word, 0) for word in words)
        scored_sentences.append((sentence, score))
    
    return scored_sentences


def summarize(paragraph, summary_length=3):
    """
    Generate a summary of the paragraph.
    
    Args:
        paragraph (str): The text to summarize
        summary_length (int): Number of sentences in the summary (default: 3)
    
    Returns:
        str: The summary text
    """
    # Preprocess the text
    processed_text = preprocess_text(paragraph)
    
    # Split into sentences
    sentences = split_into_sentences(processed_text)
    
    # Handle edge case: if paragraph has fewer sentences than requested
    if len(sentences) <= summary_length:
        return paragraph
    
    # Get important words
    important_words = get_important_words(processed_text)
    
    # Score sentences
    scored_sentences = score_sentences(sentences, important_words)
    
    # Sort by score and get top sentences
    top_sentences = sorted(scored_sentences, key=lambda x: x[1], reverse=True)[:summary_length]
    
    # Sort by original order (to maintain coherence)
    top_sentences_ordered = sorted(top_sentences, key=lambda x: sentences.index(x[0]))
    
    # Extract just the sentence text and join them
    summary = '. '.join([sent[0] for sent in top_sentences_ordered])
    
    # Capitalize first letter and ensure it ends with a period
    if summary:
        summary = summary[0].upper() + summary[1:] + '.'
    
    return summary


def main():
    """Main function with example usage."""
    print("=" * 60)
    print("Simple AI Summary Tool")
    print("=" * 60)
    
    # Example paragraph
    example_text = """
    Artificial intelligence is transforming the world in remarkable ways.
    Machine learning algorithms can now recognize faces, understand language,
    and make predictions with incredible accuracy. Companies are using AI to
    improve customer service, optimize supply chains, and develop new products.
    However, AI also raises important questions about privacy, bias, and job
    displacement. As AI technology continues to evolve, society must grapple
    with both its tremendous potential and serious ethical challenges.
    """
    
    print("\nOriginal Text:")
    print("-" * 60)
    print(example_text.strip())
    
    print("\n\nSummary:")
    print("-" * 60)
    summary = summarize(example_text, summary_length=3)
    print(summary)
    
    print("\n\n" + "=" * 60)
    print("Try it yourself!")
    print("=" * 60)
    
    while True:
        print("\nEnter a paragraph (or 'quit' to exit):")
        user_input = input("> ").strip()
        
        if user_input.lower() == 'quit':
            print("Goodbye!")
            break
        
        if not user_input:
            print("Please enter some text.")
            continue
        
        summary = summarize(user_input, summary_length=2)
        print(f"\nSummary: {summary}")


if __name__ == "__main__":
    main()
quit