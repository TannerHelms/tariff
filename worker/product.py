import asyncio
import os
from bullmq import Worker
from prisma import Prisma
import json
import time

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

    # Process the Job
    time.sleep(1)

    # Update the job status
    await db.job.update(
        where={
            'id': job_id
        },
        data={
            'result': json.dumps({'code': '1234'}),
            'status': 'COMPLETED'
        }
    )
    
    # Print out that the job has been completed
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
