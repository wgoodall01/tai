import os
import requests
from dotenv import load_dotenv
import urllib.request

# Import the environment variables
load_dotenv()
canvas_token = os.getenv('CANVAS_TOKEN')
canvas_url = os.getenv('CANVAS_URL')


def download_files(course_id):
    """Downloads all files from a specified course id.
    Downloads to a directory named _data/course-{course_id}/files/
    """
    
    # Set up API request for files
    files_url = f'{canvas_url}/courses/{course_id}/files'
    headers = {'Authorization': f'Bearer {canvas_token}'}

    # Loop to account for pagination!
    while(files_url):

        files_response = requests.get(files_url, headers=headers)

        # Break if this is not a link
        if not 'Link' in files_response.headers:
            break

        # More breaking
        links = requests.utils.parse_header_links(files_response.headers['Link'].rstrip('>').replace('>,<', ',<'))
        files_url = None
        for link in links:
            if link['rel'] == 'next':
                files_url = link['url']
                break

        # Get list of files
        files = files_response.json()

        # Create a directory to store the downloaded files
        directory = f'_data/course-{course_id}/files/'
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Iterate through files in files
        for file in files:

            # Set up API request for file
            filepath = os.path.join(directory, file['display_name'])
            if not os.path.exists(filepath):
                print("Downloading: " + file['display_name'] + "...")
                urllib.request.urlretrieve(file['url'], filepath)
            else:
                print("File already exists: " + file['display_name'] + ". Skipping...")    

def download_announcements(course_id):
    """Downloads all announcements from a specified course id.
    Downloads to a directory named _data/course-{course_id}/announcements/
    """

    # Define the API endpoint for discussions
    discussion_url = f'{canvas_url}/courses/{course_id}/discussion_topics?only_announcements=true'

    # Set up the headers with the authorization token
    headers = {"Authorization": f"Bearer {canvas_token}"}

    # Make the API request to get discussion topics
    response = requests.get(discussion_url, headers=headers)
    if response.status_code == 200:
        announcements = response.json()

        # Write HTML content to a file
        directory = f'_data/course-{course_id}/announcements/'
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Generate HTML content
        for announcement in announcements:
            html_content = "<html><body>"
            filepath = os.path.join(directory, f"announcement-{announcement['id']}.html")
            html_content += f"<h2>{announcement['title']}</h2>"
            html_content += f"<p> Posted at: {announcement['posted_at']}</p>"
            html_content += f"<p>{announcement['message']}</p>"
            html_content += "</body></html>"

            print("Downloading: " + str(announcement['id']) + "...")

            with open(filepath, "w") as html_file:
                html_file.write(html_content)

    else:

        print(f"Error fetching announcements. Status code: {response.status_code}")

def download_assignments(course_id):
    """Downloads all assignments from a specified course id.
    Downloads to a directory named _data/course-{course_id}/assignments/
    """

    # Define the API endpoint for assignments
    assignments_url = f'{canvas_url}/courses/{course_id}/assignments'

    # Set up the headers with the authorization token
    headers = {"Authorization": f"Bearer {canvas_token}"}

    # Make the API request to get assignments
    response = requests.get(assignments_url, headers=headers)
    if response.status_code == 200:
        assignments = response.json()

        # Write HTML content to a file
        directory = f'_data/course-{course_id}/assignments/'
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Generate HTML content
        for assignment in assignments:
            html_content = "<html><body>"
            filepath = os.path.join(directory, f"assignment-{assignment['id']}.html")
            html_content += f"<h2>{assignment['name']}</h2>"
            html_content += f"<p> Due at: {assignment['due_at']}</p>"
            html_content += f"<p> Created at: {assignment['created_at']}</p>"
            html_content += f"<p> Description: {assignment['description']}</p>"
            html_content += "</body></html>"

            print("Downloading: " + str(assignment['id']) + "...")

            with open(filepath, "w") as html_file:
                html_file.write(html_content)

    else:

        print(f"Error fetching assignments. Status code: {response.status_code}")

def download_course(course_id):
    """Downloads all relevant information for a course.
    Currently: files and announcements.
    Downloads to a directory named _data/course-{course_id}/
    """

    print("Downloading course data for course id: " + str(course_id) + "...")

    print("Downloading files...")
    download_files(course_id)

    print("Downloading announcements...")
    download_announcements(course_id)

    print("Downloading assignments...")
    download_assignments(course_id)

    print("Finished downloading course data for course id: " + str(course_id) + ".")


download_course(272942)