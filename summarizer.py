from transformers import pipeline

summarizer = pipeline('summarization', model='t5-small', tokenizer='t5-small', framework='pt')


def generate_key_points(text):
    sentences = text.split('. ')
    key_points = [sentences for sentences in sentences if len(sentences) > 1]
    return key_points


def summarize_and_generate_points(input_text):
    summary = summarizer(input_text, max_length=200, min_length=80, do_sample=False)
    summary_text = summary[0]['summary_text']
    key_points = generate_key_points(summary_text)
    return key_points


if __name__ == '__main__':
    summarize_and_generate_points()
