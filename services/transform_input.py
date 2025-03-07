def transform_input(data):
    transformed = []
    for role, stories in data.get("stories", {}).items():
        for story in stories:
            transformed.append({
                "Title": story.get("Title"),
                "Role": role,
                "Description": story.get("Description"),
                "Estimated Time": story.get("Estimated Time")
            })
    return transformed