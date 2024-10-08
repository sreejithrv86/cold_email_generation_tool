import re
import base64


def clean_text(text):
    # Remove HTML tags
    text = re.sub(r'<[^>]*?>', '', text)
    # Remove URLs
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    # Remove special characters
    text = re.sub(r'[^a-zA-Z0-9 ]', '', text)
    # Replace multiple spaces with a single space
    text = re.sub(r'\s{2,}', ' ', text)
    # Trim leading and trailing whitespace
    text = text.strip()
    # Remove extra whitespace
    text = ' '.join(text.split())
    return text


def refine_link(result, technical_skills):
    # Extract relevant links using technical skills
    skills = technical_skills
    keywords = []
    for skill in skills:
        words = re.findall(r'\w+', skill.lower())
        keywords.extend(words)

    refined_links = []
    for metadata in result.get('metadatas', []):
        link = metadata[0]['links'].lower()
        if any(keyword in link for keyword in keywords):
            refined_links.append(metadata[0]['links'])

    # Handle any variable named 'set' issue
    try:
        refined_links = list(set(refined_links))
    except TypeError as e:
        print("Error:", e)

    return refined_links


def decode_base64_encode_string(encoded_str):
    decoded_bytes = base64.b64decode(encoded_str)
    decoded_str = decoded_bytes.decode('utf-8')
    return decoded_str


def encode_base64_string(original_str):
    encoded_bytes = base64.b64encode(original_str.encode('utf-8'))
    encoded_str = encoded_bytes.decode('utf-8')
    return encoded_str
