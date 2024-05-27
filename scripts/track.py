import openai
import json
import time
client = openai.OpenAI(api_key='sk-proj-aVUhwdGusqIJ0fvL5eJpT3BlbkFJTplonfqJbqj4Scjsaxs5')

batch_id = "batch_U8svakdlzbW6mKQe50O2md19"
# Check the status of the batch
batch_status = client.batches.retrieve(batch_id)
print(f"Batch status: {batch_status.status}")

# You can check the status of the batch periodically until it's completed
while batch_status.status not in ['completed', 'failed', 'cancelled']:
    time.sleep(60)  # Wait for 60 seconds before checking the status again
    batch_status = client.batches.retrieve(batch_id)
    print(f"Batch status: {batch_status.status}")

# Retrieve the results once the batch is completed
if batch_status.status == 'completed':
    output_file_id = batch_status.output_file_id
    content = client.files.content(output_file_id)
    content.write_to_file("batch_output.jsonl")
    print("Batch results saved to batch_output.jsonl")
else:
    print(f"Batch failed with status: {batch_status.status}")