import google.auth
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import logging

# Set up logging.
logging.basicConfig(filename='blog_manager.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

# Replace the values below with your own.
BLOG_ID = 'YOUR_BLOG_ID'
SCOPES = ['https://www.googleapis.com/auth/blogger']
SERVICE_ACCOUNT_FILE = 'PATH_TO_YOUR_JSON_KEY_FILE'

# Authenticate and build the service.
creds = None
creds, project_id = google.auth.default(scopes=SCOPES)
if creds is None:
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('blogger', 'v3', credentials=creds)

# Function to create a new post.
def create_post(title, content):
    post = {
        'title': title,
        'content': content,
        'labels': ['example', 'automated'],
        'status': 'DRAFT'
    }
    try:
        result = service.posts().insert(blogId=BLOG_ID, body=post).execute()
        logging.info(f"Post created successfully: {result['id']}")
        return result['id']
    except Exception as e:
        logging.error(f"Error creating post: {e}")
        raise e

# Function to get the latest post date.
def get_latest_post_date():
    try:
        posts = service.posts().list(blogId=BLOG_ID).execute()
        latest_post = posts['items'][0]
        latest_post_date_str = latest_post['published']
        latest_post_date = datetime.strptime(latest_post_date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
        return latest_post_date
    except Exception as e:
        logging.error(f"Error retrieving latest post date: {e}")
        raise e

# Schedule a new post to be created.
def schedule_post(title, content, days_from_now):
    publish_date = datetime.utcnow() + timedelta(days=days_from_now)
    latest_post_date = get_latest_post_date()
    if publish_date < latest_post_date:
        msg = f"Post date is before latest post date ({latest_post_date})"
        logging.error(msg)
        raise ValueError(msg)
    try:
        post_id = create_post(title, content)
        service.posts().publish(blogId=BLOG_ID, postId=post_id).execute()
        service.posts().update(blogId=BLOG_ID, postId=post_id, body={'status': 'SCHEDULED', 'published': publish_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')}).execute()
        logging.info(f"Post scheduled successfully: {post_id} for {publish_date}")
    except Exception as e:
        logging.error(f"Error scheduling post: {e}")
        raise e

# Function to add an image to a post.
def add_image_to_post(post_id, image_path):
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()
    try:
        media = service.media().upload(blogId=BLOG_ID, media_body=googleapiclient.http.MediaIoBaseUpload(io.BytesIO(image_data), mimetype='image/jpeg')).execute()
        post = service.posts().get(blogId=BLOG_ID, postId=post_id).execute()
        post['images'].append(media['url'])
        service.posts().update(blogId=BLOG_ID, postId=post_id, body=post).execute()
        logging.info(f"Image added to post successfully
