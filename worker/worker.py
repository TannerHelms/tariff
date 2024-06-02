import asyncio
import os
from bullmq import Worker
from prisma import Prisma
import json
import time
from model import process_product_info
from dotenv import load_dotenv

# Load environment variables from .env file located one directory above
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

async def process(job, job_token):
    # Connect to the database
    db = Prisma()
    await db.connect()

    # Get the job data
    job_id = job.data['jobId']
    name = job.data['name']
    description = job.data['description']
    material = job.data['material']
    use = job.data['use']
    type = job.data['type']

    # Set the job as processing
    await db.job.update(
        where={
            'id': job_id
        },
        data={
            'status': 'PROCESSING'
        }
    )

    # Prepare product information from the job data
    product_info = {
        "product": name,
        "product_description": description,
        "product_material": material,
        "end_use": use,
        "type": type
    }

    # Load section and chapter descriptions
    try:
        with open('section_and_chapter_with_notes.json', 'r', encoding='utf-8') as f:
            section_data = json.load(f)
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        section_data = None

    # Process the product information with the model
    matching_sections, true_chapters, true_hts_matches = process_product_info(product_info, section_data)

    # Update the job status with the results
    await db.job.update(
        where={
            'id': job_id
        },
        data={
            'result': json.dumps({
                'matching_sections': matching_sections,
                'true_chapters': true_chapters,
                'true_hts_matches': true_hts_matches
            }, ensure_ascii=False, indent=4),
            'status': 'COMPLETED'
        }
    )

    print(f"Processing {job.id} with data {job.data}")

async def main():
    print('work is starting...')
    # Feel free to remove the connection parameter, if your redis runs on localhost
    worker = Worker("product", process, {"connection": {
        "host": 'localhost',
        "port": 6379,
    }})

    # This while loop is just for the sake of this example
    # you won't need it in practice.
    while True:  # Add some breaking conditions here
        await asyncio.sleep(1)

    # When no need to process more jobs we should close the worker
    await worker.close()

if __name__ == "__main__":
    asyncio.run(main())