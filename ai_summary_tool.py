"""
Simple AI Summary Tool
A beginner-friendly script that generates summaries of paragraphs using basic NLP logic.
"""

import re
from collections import Counter
import argparse
import textwrap

def preprocess_text(text):
    """Convert text to lowercase and normalize whitespace."""
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)
    return text

def split_into_sentences(text):
    """Split text into sentences using punctuation while keeping sentence endings."""
    # Use regex to split while keeping punctuation as part of the sentence
    parts = re.findall(r'[^.!?]+[.!?]?', text)
    sentences = [p.strip() for p in parts if p.strip()]
    return sentences

def get_important_words(text, num_words=10):
    """
    Extract the most important words from text.
    Ignores common stop words and punctuation.
    """
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'be', 'been',
        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
        'should', 'may', 'might', 'can', 'that', 'this', 'it', 'its', 'which',
        'i', 'you', 'we', 'they', 'he', 'she', 'them', 'their', 'our', 'us'
    }

    # Extract words (allowing unicode letters) and normalize
    words = re.findall(r'\b[^\W\d_]+\b', text.lower(), flags=re.UNICODE)
    important_words = [w for w in words if w not in stop_words]
    word_freq = Counter(important_words)
    return word_freq.most_common(num_words)

def score_sentences(sentences, important_words):
    """
    Score each sentence based on how many important words it contains.
    Returns a list of (sentence, score) tuples.
    """
    word_dict = {word: freq for word, freq in important_words}

    scored_sentences = []
    for sentence in sentences:
        words = re.findall(r'\b[^\W\d_]+\b', sentence.lower(), flags=re.UNICODE)
        score = sum(word_dict.get(word, 0) for word in words)
        scored_sentences.append((sentence, score))

    return scored_sentences

def summarize(paragraph, summary_length=2):
    """
    Generate a summary of the paragraph.

    Args:
        paragraph (str): The text to summarize
        summary_length (int): Number of sentences in the summary (default: 2)

    Returns:
        str: The summary text
    """
    paragraph = paragraph.strip()
    if not paragraph:
        return ""

    # Preprocess the text (but keep original for final ordering / punctuation)
    processed_text = preprocess_text(paragraph)

    # Split into sentences using the original paragraph for better punctuation handling
    sentences = split_into_sentences(paragraph)

    if len(sentences) <= summary_length:
        # Return the original paragraph trimmed
        return ' '.join(s.strip() for s in sentences)

    important_words = get_important_words(processed_text)
    scored_sentences = score_sentences(sentences, important_words)

    # Pick top sentences by score
    top_sentences = sorted(scored_sentences, key=lambda x: x[1], reverse=True)[:summary_length]

    # Sort the selected sentences by their original position for coherence
    top_sentences_ordered = sorted(top_sentences, key=lambda x: sentences.index(x[0]))

    # Clean up: ensure each chosen sentence ends with punctuation
    chosen = []
    for s, _ in top_sentences_ordered:
        s = s.strip()
        if not re.search(r'[.!?]$', s):
            s = s + '.'
        chosen.append(s)

    summary = ' '.join(chosen)
    # Capitalize first letter if needed
    if summary:
        summary = summary[0].upper() + summary[1:]

    return summary

def interactive_mode(default_summary_len=2):
    """Runs the interactive CLI mode."""
    print("=" * 60)
    print("Simple AI Summary Tool (interactive mode)")
    print("=" * 60)
    print("Type/paste a paragraph and press Enter. Type 'quit' to exit.\n")

    while True:
        user_input = input("> ").strip()
        if user_input.lower() in {'quit', 'exit'}:
            print("Goodbye!")
            break
        if not user_input:
            print("Please enter some text.")
            continue
        summary = summarize(user_input, summary_length=default_summary_len)
        print("\nSummary:\n" + "-" * 40)
        print(textwrap.fill(summary, width=80))
        print("-" * 40 + "\n")

def main():
    parser = argparse.ArgumentParser(description="AI Summary Tool (simple extractive summarizer).")
    parser.add_argument('--file', '-f', help="Path to a text file to summarize.")
    parser.add_argument('--text', '-t', help="Direct text input to summarize (wrap in quotes).")
    parser.add_argument('--sentences', '-s', type=int, default=2, help="Number of sentences in the summary.")
    parser.add_argument('--interactive', '-i', action='store_true', help="Run in interactive mode.")
    args = parser.parse_args()

    if args.interactive:
        interactive_mode(default_summary_len=args.sentences)
        return

    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading file: {e}")
            return
        print("Original:\n" + "-" * 40)
        print(content.strip())
        print("\nSummary:\n" + "-" * 40)
        print(summarize(content, summary_length=args.sentences))
        return

    if args.text:
        print("Summary:\n" + "-" * 40)
        print(summarize(args.text, summary_length=args.sentences))
        return

    # If no args provided, run interactive mode
    interactive_mode(default_summary_len=args.sentences)

if __name__ == "__main__":
    main()
