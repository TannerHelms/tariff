import os
import json
import time
import re
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file located one directory above
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

os.environ['PYTHONIOENCODING'] = 'utf-8'
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("API key is not set in the environment variables.")

client = OpenAI(api_key=api_key)

# Function to format the document names
def format_document_name(doc_name):
    if "chapter_notes_" in doc_name:
        number = re.search(r'\d+', doc_name).group()
        return f"Chapter Notes {number}"
    elif "section_" in doc_name and "_notes" in doc_name:
        numeral = re.search(r'(?<=section_)\w+', doc_name).group().upper()
        return f"Section {numeral} Notes"
    elif "section_" in doc_name and "_explanatory_notes" in doc_name:
        numeral = re.search(r'(?<=section_)\w+', doc_name).group().upper()
        return f"Section {numeral} Explanatory Notes"
    elif "chapter_" in doc_name and "_explanatory_notes" in doc_name:
        number = re.search(r'\d+', doc_name).group()
        return f"Chapter {number} Explanatory Notes"
    else:
        return doc_name

# Function to run an assistant and get the JSON response
def run_assistant(assistant_id, product_info, output_list, index):
    try:
        # Retrieve the Assistant
        my_assistant = client.beta.assistants.retrieve(assistant_id)
        
        # Create a New Thread
        thread = client.beta.threads.create()
        
        # Add User Message to Thread
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user", 
            content=product_info
        )
        
        # Create a Run
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=my_assistant.id
        )
        
        # Poll the run status until it is completed
        while run.status != "completed":
            time.sleep(1)  # Add a small delay to avoid hitting the API rate limit
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        
        # Retrieve the assistant's response messages
        response_messages = client.beta.threads.messages.list(thread_id=thread.id)
        
        # Extract and store the JSON response from the assistant
        for message in response_messages.data:
            if message.role == "assistant":
                # Iterate over the message content to find the JSON block
                for content_block in message.content:
                    if content_block.type == "text" and "```json" in content_block.text.value:
                        json_start = content_block.text.value.find("```json")
                        json_end = content_block.text.value.find("```", json_start + 6)
                        if json_start != -1 and json_end != -1:
                            json_content = content_block.text.value[json_start + 6:json_end].strip()
                            json_content = json_content.replace("n\n", "").strip()  # Clean the JSON content
                            if json_content:
                                try:
                                    parsed_content = json.loads(json_content)
                                    # Format the document names
                                    for item in parsed_content:
                                        item["document"] = format_document_name(item["document"])
                                    output_list[index] = parsed_content
                                except json.JSONDecodeError as e:
                                    output_list[index] = {"error": str(e), "json_content": json_content}
                            else:
                                output_list[index] = {"error": "Empty JSON content"}
                            return
        output_list[index] = {"error": "No valid JSON response found"}
    except Exception as e:
        output_list[index] = {"error": str(e)}

def safe_api_call(call, *args, **kwargs):
    try:
        response = call(*args, **kwargs)
        print(f"Response: {json.dumps(response.model_dump_json(indent=2), ensure_ascii=False)}")
        return response
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def gpt_contextual_match(product_info, section_info, relevant_notes, client, model="gpt-4o"):
    messages = [
        {
            "role": "system",
            "content": "You are an HTSUS customs broker assistant designed to output JSON."
        },
        {
            "role": "user",
            "content": f"""
            Given the product information and section description below, respond with a JSON object containing the section number and a "fit" value of 1 if the product (based on its description, relevant notes, material, end use, and type) could possibly fall into this section, otherwise respond with a "fit" value of 0.

            Product: {product_info['product']}
            Description: {product_info['product_description']}
            Material: {product_info['product_material']}
            End Use: {product_info['end_use']}
            Type: {product_info['type']}

            Relevant Notes: {json.dumps(relevant_notes)}

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

def gpt_chapter_match(product_info, chapter_info, relevant_notes, client, model="gpt-4o"):
    messages = [
        {
            "role": "system",
            "content": "You are an HTSUS customs broker assistant designed to output JSON."
        },
        {
            "role": "user",
            "content": f"""
            Given the product information and chapter description below, respond with a JSON object containing the chapter number and a "fit" value of 1 if the product (based on its description, relevant notes, material, end use, and type) could possibly fall into this chapter, otherwise respond with a "fit" value of 0.

            Product: {product_info['product']}
            Description: {product_info['product_description']}
            Material: {product_info['product_material']}
            End Use: {product_info['end_use']}
            Type: {product_info['type']}

            Relevant Notes: {json.dumps(relevant_notes)}

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

def gpt_hts_code(product_info, htsus_text, relevant_notes, client, model="gpt-4o"):
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

            Relevant Notes: {json.dumps(relevant_notes)}

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
    # List to hold the responses from new assistants
    responses = [None, None]

    # Define assistant IDs
    en_assistant = "asst_54JwBC4fyfoVrAVdMJ0JZY0N"
    notes_assistant = "asst_ofjnsJb6AygWWv5PXHBRgNJL"

    # Create threads for both assistants
    thread_1 = threading.Thread(target=run_assistant, args=(en_assistant, product_info, responses, 0))
    thread_2 = threading.Thread(target=run_assistant, args=(notes_assistant, product_info, responses, 1))

    # Start the threads
    thread_1.start()
    thread_2.start()

    # Wait for both threads to complete
    thread_1.join()
    thread_2.join()

    # Combine the outputs into a single JSON object
    combined_response = {
        "Explanatory Notes": responses[0],
        "Chapter and Section Notes": responses[1]
    }

    # Print the combined JSON object
    print(json.dumps(combined_response, indent=4))

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
                futures.append(executor.submit(gpt_contextual_match, product_info, section_info, combined_response, client))

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
                        futures.append(executor.submit(gpt_chapter_match, product_info, chapter_info, combined_response, client))

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
                        futures.append(executor.submit(gpt_hts_code, product_info, htsus_text, combined_response, client))
                except FileNotFoundError as e:
                    print(f"File not found: {e}")

            for future in as_completed(futures):
                try:
                    hts_match = future.result()
                    if hts_match:
                        true_hts_matches.append(hts_match)
                except Exception as e:
                    print(f"Error in future result: {e}")

    return matching_sections, true_chapters, true_hts_matches, combined_response

def main(product_info, section_data):
    matching_sections, true_chapters, true_hts_matches, combined_response = process_product_info(product_info, section_data)

    with open('true_sections.json', 'w', encoding='utf-8') as f:
        json.dump(matching_sections, f, indent=4, ensure_ascii=False)

    with open('true_chapters.json', 'w', encoding='utf-8') as f:
        json.dump(true_chapters, f, indent=4, ensure_ascii=False)

    with open('true_hts_matches.json', 'w', encoding='utf-8') as f:
        json.dump(true_hts_matches, f, indent=4, ensure_ascii=False)

    with open('combined_response.json', 'w', encoding='utf-8') as f:
        json.dump(combined_response, f, indent=4, ensure_ascii=False)

    print(f"Matching sections saved to true_sections.json")
    print(f"True chapters saved to true_chapters.json")
    print(f"True HTS matches saved to true_hts_matches.json")
    print(f"Combined response saved to combined_response.json")

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
