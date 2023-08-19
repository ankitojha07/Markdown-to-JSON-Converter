# How to run
# Create a markdown file at same level as this python script OR Specify location of markdowsn fiel at inpu_file in line number 65

import re
import json

def markdown_to_json(input_file):
    # Read the input Markdown file
    with open(input_file, 'r', encoding='utf-8') as file:
        markdown_text = file.read()

    # Define a pattern to match question sections
    question_pattern = r"@QUESTION_ID:\s*(?P<question_id>[^\n]+).*?" \
                      r"@QUESTION_TYPE:\s*(?P<question_type>[^\n]+).*?" \
                      r"@QUESTION:\s*(?P<question>[^\n]+).*?" \
                      r"@QUESTION_CONTENT_TYPE:\s*(?P<content_type>[^\n]+).*?" \
                      r"(@CODE:\s*(?P<code>.*?))?@OPTION1:(?P<option1>[^\n]+).*?" \
                      r"@OPTION2:(?P<option2>[^\n]+).*?" \
                      r"@OPTION3:(?P<option3>[^\n]+).*?" \
                      r"@OPTION4:(?P<option4>[^\n]+).*?" \
                      r"@CORRECT_OPTIONS:\s*(?P<correct_options>[^\n]+).*?" \
                      r"(@TAG_NAMES:\s*(?P<tag_names>[^\n]+))?(@SKILLS:\s*(?P<skills>[^\n]+))?(@EXPLANATION:\s*(?P<explanation>.*?))?(\n|\Z)"

    # Split the Markdown text into individual question sections
    questions = re.finditer(question_pattern, markdown_text, re.DOTALL)

    # Define a list to store the converted questions
    converted_questions = []

    for question_match in questions:
        question_data = question_match.groupdict()

        # Split the correct options into a list
        correct_options = question_data['correct_options'].split(', ')

        # Create a list of options
        options = [
            {"content": question_data[f"option{i}"], "content_type": question_data['content_type'], "is_correct": str(i) in correct_options, "multimedia": []}
            for i in range(1, 5)
        ]

        # Create a dictionary for the question
        question_dict = {
            "question_id": question_data['question_id'],
            "question_type": question_data['question_type'],
            "question": question_data['question'],
            "question_content_type": question_data['content_type'],
            "code": question_data.get('code', ''),
            "options": options,
            "tag_names": question_data.get('tag_names', '').split(', ') if question_data.get('tag_names') else [],
            "explanation": question_data.get('explanation', ''),
        }

        # Add skills if available
        if question_data.get('skills'):
            question_dict["skills"] = question_data['skills'].split(', ')

        converted_questions.append(question_dict)

    # Print the JSON representation of the questions
    print(json.dumps(converted_questions, indent=4))

if __name__ == "__main__":
    # Input Markdown file path
    input_file = r'C:\Users\ankit\Desktop\readme.md'

    
    # Convert and print the questions as JSON
    markdown_to_json(input_file)
