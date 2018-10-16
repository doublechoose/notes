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

python egg文件，类似java的jar包，将一系列的python源码文件、元数据文件、其他资源文件进行zip压缩，以.egg后缀重新命名，作为一个整体进行发布。



查看linux 版本

```
# 1.
uname -a
# 2.
cat /proc/version

```

解压

```
tar xvzf xxx.tar.gz
```

-x 解压

-v 压缩过程显示文件

-f 使用档名

-z 是否同时具有gzip的属性，是否要用gzip压缩

-j 是否同时具有bzip2的属性，是否需要用bzip2压缩