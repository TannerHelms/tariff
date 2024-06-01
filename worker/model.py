import os
import json
from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv

# Load environment variables from .env file located one directory above
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

os.environ['PYTHONIOENCODING'] = 'utf-8'
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("API key is not set in the environment variables.")

client = OpenAI(api_key=api_key)

def safe_api_call(call, *args, **kwargs):
    try:
        response = call(*args, **kwargs)
        print(f"Response: {json.dumps(response.model_dump_json(indent=2), ensure_ascii=False)}")
        return response
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def gpt_contextual_match(product_info, section_info, client, model="gpt-4o"):
    messages = [
        {
            "role": "system",
            "content": "You are an HTSUS customs broker assistant designed to output JSON."
        },
        {
            "role": "user",
            "content": f"""
            Given the product information and section description below, respond with a JSON object containing the section number and a "fit" value of 1 if the product (based on its description, material, end use, and type) could possibly fall into this section, otherwise respond with a "fit" value of 0.

            Product: {product_info['product']}
            Description: {product_info['product_description']}
            Material: {product_info['product_material']}
            End Use: {product_info['end_use']}
            Type: {product_info['type']}

            Section: {section_info['title']}
            Section Number: {section_info['section']}
            Section Notes: {section_info['section_notes']}
            """
        }
    ]

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=50,
            n=1,
            temperature=0,
        )

        if response and len(response.choices) > 0:
            content = response.choices[0].message.content.strip()
            print(f"Response content: {content}")

            try:
                if content.startswith("```json"):
                    content = content[7:-3].strip()
                elif content.startswith("{"):
                    content = content.strip()
                result = json.loads(content)

                result = {k.lower(): v for k, v in result.items()}

                return result.get('section_number', section_info['section']), result.get('fit', 0)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                return section_info['section'], 0
        else:
            print("No valid response content found.")
            return section_info['section'], 0

    except Exception as e:
        print(f"API error: {e}")
        return section_info['section'], 0

def gpt_chapter_match(product_info, chapter_info, client, model="gpt-4o"):
    messages = [
        {
            "role": "system",
            "content": "You are an HTSUS customs broker assistant designed to output JSON."
        },
        {
            "role": "user",
            "content": f"""
            Given the product information and chapter description below, respond with a JSON object containing the chapter number and a "fit" value of 1 if the product (based on its description, material, end use, and type) could possibly fall into this chapter, otherwise respond with a "fit" value of 0. Be generous with material.

            Product: {product_info['product']}
            Description: {product_info['product_description']}
            Material: {product_info['product_material']}
            End Use: {product_info['end_use']}
            Type: {product_info['type']}

            Chapter: {chapter_info['title']}
            Chapter Number: {chapter_info['chapter']}
            """
        }
    ]

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=50,
            n=1,
            temperature=0,
        )

        if response and len(response.choices) > 0:
            content = response.choices[0].message.content.strip()
            print(f"Response content: {content}")

            try:
                if content.startswith("```json"):
                    content = content[7:-3].strip()
                elif content.startswith("{"):
                    content = content.strip()
                result = json.loads(content)

                result = {k.lower(): v for k, v in result.items()}

                return result.get('chapter_number', chapter_info['chapter']), result.get('fit', 0)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                return chapter_info['chapter'], 0
        else:
            print("No valid response content found.")
            return chapter_info['chapter'], 0

    except Exception as e:
        print(f"API error: {e}")
        return chapter_info['chapter'], 0

def gpt_hts_code(product_info, htsus_text, client, model="gpt-4o"):
    messages = [
        {
            "role": "system",
            "content": "You are an HTSUS customs broker assistant designed to output JSON."
        },
        {
            "role": "user",
            "content": f"""
            Given the following product information and HTSUS text below, output a JSON object with the HTS code of the section which best aligns with the product described. The JSON object should have "HTS_code", "Article_Description", "Unit of Quantity", as well as the original product information "product", "product_description", "product_material", "end_use", "type":

            Product: {product_info['product']}
            Description: {product_info['product_description']}
            Material: {product_info['product_material']}
            End Use: {product_info['end_use']}
            Type: {product_info['type']}

            HTSUS Text: {htsus_text}
            """
        }
    ]

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=1000,
            n=1,
            temperature=0,
        )

        if response and len(response.choices) > 0:
            content = response.choices[0].message.content.strip()
            print(f"Response content: {content}")

            try:
                if content.startswith("```json"):
                    content = content[7:-3].strip()
                elif content.startswith("{"):
                    content = content.strip()
                result = json.loads(content)

                result = {k.lower(): v for k, v in result.items()}

                return result
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                return None
        else:
            print("No valid response content found.")
            return None

    except Exception as e:
        print(f"API error: {e}")
        return None

def process_product_info(product_info, section_data):
    matching_sections = []
    if section_data:
        with ThreadPoolExecutor(max_workers=22) as executor:
            futures = []
            for section in section_data['sections']:
                section_info = {
                    'title': section['title'],
                    'section': section['section'],
                    'section_notes': section.get('section_notes', '')
                }
                futures.append(executor.submit(gpt_contextual_match, product_info, section_info, client))

            for future in as_completed(futures):
                try:
                    section_number, fit = future.result()
                    if fit == 1:
                        matching_sections.append(section_number)
                except Exception as e:
                    print(f"Error in future result: {e}")

    true_chapters = []
    if matching_sections:
        with ThreadPoolExecutor(max_workers=22) as executor:
            futures = []
            for section in section_data['sections']:
                if section['section'] in matching_sections:
                    for chapter in section['chapters']:
                        chapter_info = {
                            'chapter': chapter['chapter'],
                            'title': chapter['title']
                        }
                        futures.append(executor.submit(gpt_chapter_match, product_info, chapter_info, client))

            for future in as_completed(futures):
                try:
                    chapter_number, fit = future.result()
                    if fit == 1:
                        true_chapters.append({
                            'chapter': chapter_number,
                            'title': chapter_info['title']
                        })
                except Exception as e:
                    print(f"Error in future result: {e}")

    true_hts_matches = []
    if true_chapters:
        with ThreadPoolExecutor(max_workers=22) as executor:
            futures = []
            for chapter in true_chapters:
                chapter_number = chapter['chapter']
                try:
                    with open(os.path.join('chapter_full_text', f'{chapter_number}.txt'), 'r', encoding='utf-8') as f:
                        htsus_text = f.read()
                        futures.append(executor.submit(gpt_hts_code, product_info, htsus_text, client))
                except FileNotFoundError as e:
                    print(f"File not found: {e}")

            for future in as_completed(futures):
                try:
                    hts_match = future.result()
                    if hts_match:
                        true_hts_matches.append(hts_match)
                except Exception as e:
                    print(f"Error in future result: {e}")

    return matching_sections, true_chapters, true_hts_matches

def main(product_info, section_data):
    matching_sections, true_chapters, true_hts_matches = process_product_info(product_info, section_data)

    with open('true_sections.json', 'w', encoding='utf-8') as f:
        json.dump(matching_sections, f, indent=4, ensure_ascii=False)

    with open('true_chapters.json', 'w', encoding='utf-8') as f:
        json.dump(true_chapters, f, indent=4, ensure_ascii=False)

    with open('true_hts_matches.json', 'w', encoding='utf-8') as f:
        json.dump(true_hts_matches, f, indent=4, ensure_ascii=False)

    print(f"Matching sections saved to true_sections.json")
    print(f"True chapters saved to true_chapters.json")
    print(f"True HTS matches saved to true_hts_matches.json")

if __name__ == "__main__":
    with open('product.json', 'r', encoding='utf-8') as f:
        product_info = json.load(f)

    try:
        with open('section_and_chapter_with_notes.json', 'r', encoding='utf-8') as f:
            section_data = json.load(f)
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        section_data = None

    main(product_info, section_data)