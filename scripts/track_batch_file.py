import openai
import json
import time

client = openai.OpenAI(api_key='sk-proj-aVUhwdGusqIJ0fvL5eJpT3BlbkFJTplonfqJbqj4Scjsaxs5')

batch_file_path = "batch_files/batch_input.jsonl"


# Upload the batch input file
batch_input_file = client.files.create(
    file=open(batch_file_path, "rb"),
    purpose="batch"
)
batch_input_file_id = batch_input_file.id
print(f"Uploaded batch input file: {batch_input_file_id}")

# Create the batch
batch = client.batches.create(
    input_file_id=batch_input_file_id,
    endpoint="/v1/chat/completions",
    completion_window="24h",
    metadata={
        "description": "satellite image captioning"
    }
)
batch_id = batch.id
print(f"Created batch: {batch_id}")

# Check the status of the batch
batch_status = client.batches.retrieve(batch_id)
print(f"Batch status: {batch_status.status}")

# You can check the status of the batch periodically until it's completed
while batch_status.status not in ['completed', 'failed', 'cancelled']:
    time.sleep(60)  # Wait for 60 seconds before checking the status again
    batch_status = client.batches.retrieve(batch_id)
    print(f"Batch status: {batch_status.status['status']}")

# Retrieve the results once the batch is completed
if batch_status.status == 'completed':
    output_file_id = batch_status.output_file_id
    content = client.files.content(output_file_id)
    content.write_to_file("batch_output.jsonl")
    print("Batch results saved to batch_output.jsonl")
else:
    print(f"Batch failed with status: {batch_status['status']}")