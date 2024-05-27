import json
from openai import OpenAI
client = OpenAI(api_key='sk-proj-aVUhwdGusqIJ0fvL5eJpT3BlbkFJTplonfqJbqj4Scjsaxs5')

# Retrieve the content from the file using its file ID
file_id = "file-3HlS4nGFlueKU7un0s769o95"
file_content = client.files.content(file_id)
response = openai.File.download(file_id)

# The file content is retrieved as a stream, so we need to read it
file_content = response.read().decode('utf-8')

# The file content is assumed to be in JSON Lines format
# Parse the content
lines = file_content.splitlines()
data = [json.loads(line) for line in lines]

# Write the content to an output.jsonl file
output_file_path = 'output.jsonl'
with open(output_file_path, 'w') as output_file:
    for entry in data:
        json.dump(entry, output_file)
        output_file.write('\n')

print(f"Content written to {output_file_path}")
