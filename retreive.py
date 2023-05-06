def get_all_posts():
    posts = []
    page_token = None
    while True:
        response = service.posts().list(blogId=BLOG_ID, pageToken=page_token).execute()
        posts += response['items']
        if 'nextPageToken' not in response:
            break
        page_token = response['nextPageToken']
    return posts
