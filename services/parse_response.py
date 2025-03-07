import re

def parse_text(input_text):
    sections = re.split(r'(?m)^## ', input_text)
    parsed = []
    
    current = {}
    user_story_match = re.search(r'### (User Story*?)\n', input_text)
    user_story = user_story_match.group(1).strip() if user_story_match else ''

    for section in sections:
        if section.strip():
            title, *content = section.split('\n', 1)
            content = content[0].strip() if content else ''

            if title.strip() == 'Title':
                if current:
                    parsed.append(current)
                title_content = content.replace('---------------', '').strip()
                current = {'Title': f"{user_story} - {title_content}" if user_story else title_content}
            elif title.strip() == 'Description':
                current['Description'] = content.replace('---', '').strip()
            elif 'Estimated Time' in title.strip():
                time_match = re.search(r'Estimated Time[:\s]*(.*)', section, re.DOTALL)
                current['Estimated Time'] = time_match.group(1).strip() if time_match and time_match.group(1).strip() else 'Not provided'
                additional_notes_match = re.search(r'### Additional Notes\s*(.*?)$', content, re.DOTALL)
                if additional_notes_match:
                    current['Additional Notes'] = additional_notes_match.group(1).strip()

    # Fallback when no ## Title section exists but user story is present
    if user_story and not any(item.get('Title') for item in parsed):
        if current:
            current['Title'] = user_story
        else:
            parsed.append({'Title': user_story})

    if current:
        parsed.append(current)

    return parsed