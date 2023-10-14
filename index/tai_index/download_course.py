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

        # Iterate through files in files
        for file in files:
            download_file(course_id, file)

def download_file(course_id, file):
    # Create a directory to store the downloaded files
    directory = f'_data/course-{course_id}/files/'
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Skip video and picture files
    extensions_to_skip = ['.mp4', '.mov', '.avi', '.mkv', '.jpg', '.jpeg', '.png', '.gif', '.zip', '.m4v']
    if any(file['display_name'].lower().endswith(ext) for ext in extensions_to_skip):
        print("Skipping: " + file['display_name'] + "...")
        return

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

        # Generate HTML content
        for announcement in announcements:
            download_announcement(course_id, announcement)

    else:

        print(f"Error fetching announcements. Status code: {response.status_code}")

def download_announcement(course_id, announcement):
    # Write HTML content to a file
    directory = f'_data/course-{course_id}/announcements/'
    if not os.path.exists(directory):
        os.makedirs(directory)

    html_content = "<html><body>"
    filepath = os.path.join(directory, f"announcement-{announcement['id']}.html")
    html_content += f"<h2>{announcement['title']}</h2>"
    html_content += f"<p> Posted at: {announcement['posted_at']}</p>"
    html_content += f"<p>{announcement['message']}</p>"
    html_content += "</body></html>"

    print("Downloading: " + str(announcement['id']) + "...")

    with open(filepath, "w") as html_file:
        html_file.write(html_content)

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

        # Generate HTML content
        for assignment in assignments:
            download_assignment(course_id, assignment)

    else:

        print(f"Error fetching assignments. Status code: {response.status_code}")

def download_assignment(course_id, assignment):

    # Write HTML content to a file
    directory = f'_data/course-{course_id}/assignments/'
    if not os.path.exists(directory):
        os.makedirs(directory)

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
def download_homepage(course_id):
    """Downloads the homepage from a specified course id.
    Downloads to a directory named _data/course-{course_id}/homepage/
    """

    # Define the API endpoint for homepage
    homepage_url = f'{canvas_url}/courses/{course_id}/front_page'

    # Set up the headers with the authorization token
    headers = {"Authorization": f"Bearer {canvas_token}"}

    # Make the API request to get homepage
    response = requests.get(homepage_url, headers=headers)
    if response.status_code == 200:
        homepage = response.json()

        # Write HTML content to a file
        directory = f'_data/course-{course_id}/pages/'
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Generate HTML content
        html_content = "<html><body>"
        filepath = os.path.join(directory, f"homepage.html")
        html_content += f"<h2>{homepage['title']}</h2>"
        html_content += f"<p> {homepage['body']}</p>"
        html_content += "</body></html>"

        with open(filepath, "w") as html_file:
            html_file.write(html_content)

    else:

        print(f"Error fetching homepage. Status code: {response.status_code}")

def download_syllabus(course_id):
    """Downloads the syllabus from a specified course id.
    Downloads to a directory named _data/course-{course_id}/syllabus/
    """

    # Define the API endpoint for syllabus
    syllabus_url = f'{canvas_url}/courses/{course_id}?include[]=syllabus_body'

    # Set up the headers with the authorization token
    headers = {"Authorization": f"Bearer {canvas_token}"}

    # Make the API request to get syllabus
    response = requests.get(syllabus_url, headers=headers)
    if response.status_code == 200:
        syllabus = response.json()

        # Write HTML content to a file
        directory = f'_data/course-{course_id}/pages/'
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Generate HTML content
        html_content = "<html><body>"
        filepath = os.path.join(directory, f"syllabus.html")
        html_content += f"<h2>{syllabus['name']}</h2>"
        html_content += f"<p> {syllabus['syllabus_body']}</p>"
        html_content += "</body></html>"

        with open(filepath, "w") as html_file:
            html_file.write(html_content)

    else:

        print(f"Error fetching syllabus. Status code: {response.status_code}")

def download_page(course_id, page):
    # Write HTML content to a file
    directory = f'_data/course-{course_id}/pages/'
    if not os.path.exists(directory):
        os.makedirs(directory)

    html_content = "<html><body>"
    filepath = os.path.join(directory, f"page-{page['id']}.html")
    html_content += f"<h2>{page['title']}</h2>"
    html_content += f"<p> {page['body']}</p>"
    html_content += "</body></html>"

    print("Downloading: " + str(page['id']) + "...")

    with open(filepath, "w") as html_file:
        html_file.write(html_content)

def download_modules(course_id):
    """Downloads all modules from a specified course id.
    Downloads to a directory named _data/course-{course_id}/modules/
    """

    # Set the API endpoint for retrieving module items
    endpoint = f'{canvas_url}/courses/{course_id}/modules'

    # Create the request headers with the access token
    headers = {
        'Authorization': f'Bearer {canvas_token}'
    }

    # Send a GET request to retrieve the module items
    response = requests.get(endpoint, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Extract the module items from the response
        modules = response.json()
        # Iterate over the module items
        for module in modules:

            items_response = requests.get(module['items_url'], headers=headers)
            
            if response.status_code != 200:
                continue

            module_items = items_response.json()

            for module_item in module_items:
                item_url = module_item['url']
                # # Retrieve the details of each module item
                # module_item_id = module_item['id']
                # module_item_title = module_item['title']
                # module_item_type = module_item['type']

                # if(module_item_type == 'Page'):
                #     download_page(course_id, module_item)
                # elif(module_item_type == 'File'):
                #     download_file(course_id, module_item)
                # elif(module_item_type == 'Assignment'):
                #     download_assignment(course_id, module_item)
                # else:
                #     print("Unsupported type: " + module_item_type + ". Skipping " + module_item_title + "...")
                # Print the details of the module item
                print(f"Module Url: {item_url}")

    else:
        # Print an error message if the request was unsuccessful
        print(f"Failed to retrieve module items. Error: {response.status_code}")


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

    print("Downloading homepage...")
    download_homepage(course_id)

    print("Downloading syllabus...")
    download_syllabus(course_id)

    # print("Downloading modules...")
    # download_modules(course_id)

    print("Finished downloading course data for course id: " + str(course_id) + ".")

