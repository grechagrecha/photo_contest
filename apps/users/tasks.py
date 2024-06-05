from core.celery import app
from core.models import Post


@app.task
def delete_post(slug):
    post = Post.objects.get(slug=slug)
    post.delete()
    return f'Post {post} has been successfully deleted.'
