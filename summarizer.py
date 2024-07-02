from transformers import pipeline
import time
# Initialize the summarization pipeline with the BART model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", tokenizer="facebook/bart-large-cnn", framework="pt")

# Input text to be summarized
input_text = """quality is next level . it took some time to adapt to my PC and mobile . compared with my above 30k bose comfort . ANC is not up to the mark.it cuts fan ac wind sounds but doesn't cut talking sounds . it offers great features and borders on the premium range of headphones . buy sony for same rate . sound clarity and ANC is just awesome . it’s an over the ear headphone with ultra comfortable fitment . the company is washing their hands saying there’s nothing they can do . the message here is : "you have bought a nearly $100 device that has come defective, twice. Now, we do not take any responsibility at all. You, deal with it" utilizo para salir, tienen muy buen sonido, son cómodos a las orejas después de un tiempo puestos, la batera dura bastante. the "right one" arrived quickly in strong packaging . the convenience of having a "flat" case is when it comes to packing . the muffs turn 180 and lie flat against my collar bones . a separate "click" for each cm of extended length would be awesome . the sound is certainly a good thing . a special airplane-use-only ADAPTER is provided along with the std. usb/C charge cable . you cannot use the headphones while charging though but with 50hrs . good value for money on SALE @79.99 . I think the regular price of 99.99 too dear for no EQ or zero use while charging ."""

# Generate summary
summary = summarizer(input_text, max_length=200, min_length=80, do_sample=False)

# Extract the summary text
summary_text = summary[0]['summary_text']

# Function to generate key points from the summary
def generate_key_points(text):
    # Split the summary into sentences
    sentences = text.split('. ')
    # Create key points by selecting the first sentence from each key section
    key_points = [sentence for sentence in sentences if len(sentence) > 0]
    return key_points

# Generate key points
key_points = generate_key_points(summary_text)

# Print the key points in a bullet list format
print("Key Points:")
for i, point in enumerate(key_points, 1):
    print(f"{i}. {point.strip()}.")

# If needed, wrap the whole process in a function for reuse
def summarize_and_generate_points(input_text):
    summary = summarizer(input_text, max_length=200, min_length=80, do_sample=False)
    summary_text = summary[0]['summary_text']
    key_points = generate_key_points(summary_text)
    return key_points
start_time = time.time()
# Example usage
input_text = """quality is next level . it took some time to adapt to my PC and mobile . compared with my above 30k bose comfort . ANC is not up to the mark.it cuts fan ac wind sounds but doesn't cut talking sounds . it offers great features and borders on the premium range of headphones . buy sony for same rate . sound clarity and ANC is just awesome . it’s an over the ear headphone with ultra comfortable fitment . the company is washing their hands saying there’s nothing they can do . the message here is : "you have bought a nearly $100 device that has come defective, twice. Now, we do not take any responsibility at all. You, deal with it" utilizo para salir, tienen muy buen sonido, son cómodos a las orejas después de un tiempo puestos, la batera dura bastante. the "right one" arrived quickly in strong packaging . the convenience of having a "flat" case is when it comes to packing . the muffs turn 180 and lie flat against my collar bones . a separate "click" for each cm of extended length would be awesome . the sound is certainly a good thing . a special airplane-use-only ADAPTER is provided along with the std. usb/C charge cable . you cannot use the headphones while charging though but with 50hrs . good value for money on SALE @79.99 . I think the regular price of 99.99 too dear for no EQ or zero use while charging ."""
key_points = summarize_and_generate_points(input_text)
end_time = time.time()
print("\nGenerated Key Points:")
for i, point in enumerate(key_points, 1):
    print(f"{i}. {point.strip()}.")
print(f"Time taken: {end_time-start_time:.2f} seconds")