from transformers import pipeline
import time

# Initialize the summarization pipeline with the BART model
summarizer = pipeline("summarization", model="t5-small", tokenizer="t5-small", framework="pt")

# Function to generate key points from the summary
def generate_key_points(text):
    # Split the summary into sentences
    sentences = text.split('. ')
    # Create key points by selecting the first sentence from each key section
    key_points = [sentence for sentence in sentences if len(sentence) > 0]
    return key_points

# If needed, wrap the whole process in a function for reuse
def summarize_and_generate_points(input_text):
    summary = summarizer(input_text, max_length=200, min_length=80, do_sample=False)
    summary_text = summary[0]['summary_text']
    key_points = generate_key_points(summary_text)
    return key_points

start_time = time.time()

# Example usage
input_text = """name: HP Smart Tank 670 All-in-One Auto Duplex WiFi Integrated Ink Tank Colour Printer, Scanner, Copier- High Capacity Tank (6000 Black, 8000 Colour) with Automatic Ink Sensor
price: ₹17,999.00
short_description: About this item 【All-in-One printer】Conveniently print, scan, copy, and enjoy wireless functionality with this all-in-one printer. Print clear documents and easily scan with a flatbed scanner. 【Seamless connectivity】This printer is perfect for home use with its Wi-Fi, 2 Hi-Speed USB 2.0, and Bluetooth connectivity options, ensuring uninterrupted workflow and easy sharing. 【Quality prints】Experience high-quality, clear, and vibrant prints with compatible HP GT53 90-ml Black bottle and HP GT52 70-ml Cyan/Magenta/Yellow bottles. 【Warranty and support】Benefit from a 1-year warranty and print with ultimate peace of mind. For any assistance, reach out to our 12x7 voice support or 24x7 chat support for quick help. 【Fast printing】Print quickly with speeds up to 12 ppm (black) and 7 ppm (color). Get your documents ready in no time with duplex printing. 【Input and output】This printer has a 60-sheet input tray and a 25-sheet output tray. It also supports standard media sizes like A4, A5, A6, B5 (JIS), envelopes, and more. 【Easy-to-use interface】Navigate effortlessly with the 2-line LCD with smart guided buttons. Whether it's a quick print or a complex task, the intuitive buttons make it simple. 【Compatible OS】This printer is compatible with Windows 11/10/7 and macOS 10.14/10.15/11, ensuring seamless operation with your setup. 【3,000-page duty cycle】 With a 3000-page monthly duty cycle, this printer is built to handle high-volume printing, making it an ideal choice for home. Show More
images: {"https://m.media-amazon.com/images/I/71iTKGrwrFL._SX679_.jpg":[464,679],"https://m.media-amazon.com/images/I/71iTKGrwrFL._SX466_.jpg":[318,466],"https://m.media-amazon.com/images/I/71iTKGrwrFL._SX522_.jpg":[356,522],"https://m.media-amazon.com/images/I/71iTKGrwrFL._SX450_.jpg":[307,450],"https://m.media-amazon.com/images/I/71iTKGrwrFL._SX355_.jpg":[242,355],"https://m.media-amazon.com/images/I/71iTKGrwrFL._SX569_.jpg":[389,569],"https://m.media-amazon.com/images/I/71iTKGrwrFL._SX425_.jpg":[290,425]}
rating: 4.0 out of 5 stars
number_of_reviews: 1,469 ratings
variants: None
product_description: None
sales_rank: None
link_to_all_reviews: /HP-Integrated-Printer-Capacity-Automatic/product-reviews/B09MFHQL9J/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews
top_positive_review: I have been using HP DJ 1050 for 20 years ( yes, twenty ! ) . It is still working good. Paper try was broken few years ago , still able to use it. Only concern was high cartridge use. Usage has increased, hence wanted to go for new one. Question was, which brand I should go for .. none other than the one which lasted for more than 20 years ! The new HP smart tank 670 printer was my choice.. - It has ink tank expecting lesser printing cost - It can be connected via WiFi and Wifi Direct, no hazzeles of wires . When you use WiFi direct, you don't need a wifi router. Also if needed you can connect via USB ( and I guess via Bluetooth too, eventhough I have not tried to configure it) - It has duplex printing, without manual intervention, lot of paper and effort saving. - Colour Amazon delivery was as expected, dot on the date of delivery. Initially I thought of waiting for HP person to install the printer. However I wanted to give a try before that.  As mentioned in the manual sheet, installed HP smart app in my laptop. And followed evey instruction by the app, starting from removing the safety tapes, cardboard etc inside the printer , filling the ink , installing printer head, etc. to final test print , wifi configuration and all. At every point, app on the laptop says successful or not. It was a super smooth installation without any hic ups. Being an ex IT person helped me or rather gave me a confidence to take a chance to install by my own.  HP installation technician called me to visit next day, which I said not necessary. Today is the 4th day of installation, I have taken nearly 50 pages of print outs , I'm quite happy about my choice !
top_critical_review: Very useless printer, wifi setup is very complex, and if you change your router or wifi, then you will never be able to setup wifi again, it will be disabled permanently. No online solution is avaiable, I m struggling from last few days, seems I need to call support people now and don't know how much they will charge to fix, or if it will be fixed or not no clue, with one more HP printer I faced same issue, and I had to replace my printer as it is not possible to enable the wifi by technician, as it has to be done as hard reset.
next_page: None"""

key_points = summarize_and_generate_points(input_text)

end_time = time.time()

print("\nGenerated Key Points:")
for i, point in enumerate(key_points, 1):
    print(f"{i}. {point.strip()}.")

print(f"Time taken: {end_time - start_time:.2f} seconds")
