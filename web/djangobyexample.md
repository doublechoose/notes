django

user = User.objects.get(username='admin')

如果没有找到，则会抛出异常DoesNotExist,如果大于一个结果，则是抛出MultipleObjectsReturned异常

```python
all_posts = Post.objects.all()
Post.objects.filter(publish__year=2018)
Post.objects.filter(publish__year=2018,author__username='admin')
Post.objects.filter(publish__year=2018)\
.filter(author__username='admin')


Post.objects.filter(publish__year=2018)\
.exclude(title__startswith='why')

根据title升序
Post.objects.order_by('title')
降序
Post.objects.order_by('-title')

# delete
post = Post.objects.get(id=1)
post.delete()
```

