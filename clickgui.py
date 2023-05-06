import click

@click.group()
def cli():
    pass

@cli.command()
@click.option('--title', prompt=True, help='Title of the blog post')
@click.option('--content', prompt=True, help='Content of the blog post')
@click.option('--days-from-now', prompt=True, type=int, help='Number of days from now to schedule the post')
def schedule(title, content, days_from_now):
    # Call the schedule_post function from main.py here
    pass

@cli.command()
@click.option('--post-id', prompt=True, help='ID of the blog post')
@click.option('--image-path', prompt=True, help='Path to the image file')
def add_image(post_id, image_path):
    # Call the add_image_to_post function from main.py here
    pass

@cli.command()
@click.option('--post-id', prompt=True, help='ID of the blog post')
@click.option('--video-url', prompt=True, help='URL of the video to embed')
def add_video(post_id, video_url):
    # Call the add_embedded_video_to_post function from main.py here
    pass

if __name__ == '__main__':
    cli()
