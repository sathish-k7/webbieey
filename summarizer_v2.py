"""
with open('output.txt', 'r', encoding='UTF-8') as f:
    lines = f.read().split('\n\n')
    for line in lines:
        print(line+ "\n")"""
from transformers import pipeline
import time
import json

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
start_time = time.time()
with open('output.json', 'r', encoding='UTF-8') as f, open('output1.txt', 'w') as f1:
    datas = json.load(f)
    for data in datas:
        key_points = summarize_and_generate_points(data['short_description'])
        print("\nGenerated Key Points:")
        for i, point in enumerate(key_points, 1):
            print(f"{i}. {point.strip()}.")
            f1.write(f"{i}. {point.strip()}\n")
        f1.write('\n')

end_time = time.time()
print(f"Time taken to summarize {len(datas)} products: {end_time - start_time:.2f} seconds")

