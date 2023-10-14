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

            print("Downloading: " + file['display_name'] + "...")
            
            # Set up API request for file
            filepath = os.path.join(directory, file['display_name'])
            if not os.path.exists(filepath):
                urllib.request.urlretrieve(file['url'], filepath)

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

        # Generate HTML content
        html_content = "<html><body>"
        for announcement in announcements:
            html_content += f"<h2>{announcement['title']}</h2>"
            html_content += f"<p>{announcement['message']}</p>"
        html_content += "</body></html>"

        # Write HTML content to a file
        directory = f'_data/course-{course_id}/announcements/'
        if not os.path.exists(directory):
            os.makedirs(directory)

        filepath = os.path.join(directory, "announcements.html")

        with open(filepath, "w") as html_file:
            html_file.write(html_content)

        print("Announcements saved to announcements.html.")

    else:

        print(f"Error fetching announcements. Status code: {response.status_code}")

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

    print("Finished downloading course data for course id: " + str(course_id) + ".")