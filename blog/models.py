from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

from ckeditor_uploader.fields import RichTextUploadingField
from mdeditor.fields import MDTextField

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    

class Tag(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    

class Post(models.Model):
    '''文章'''
    
    # 文章标题
    title = models.CharField('标题',max_length=70)
    
    # 文章正文，我们使用了 TextField。
    # 存储比较短的字符串可以使用 CharField，但对于文章的正文来说可能会是一大段文本，因此使用 TextField 来存储大段文本。
    # body = RichTextUploadingField(config_name='default')
    # body = models.TextField()
    body = MDTextField()

    # 在models里添加picture字段
    # upload_to 将图片上传到static文件下的images
    picture = models.ImageField(upload_to='media',blank=True)
    
    # 这两个列分别表示文章的创建时间和最后一次修改时间，存储时间的字段用 DateTimeField 类型。
    created_time = models.DateTimeField('创建时间',default=timezone.now)
    modified_time = models.DateTimeField('修改时间')
    
    # 文章摘要，可以没有文章摘要，但默认情况下 CharField 要求我们必须存入数据，否则就会报错。
    # 指定 CharField 的 blank=True 参数值后就可以允许空值了。
    excerpt = models.CharField(max_length=200,blank=True)
    
    # 我们在这里把文章对应的数据库表和分类、标签对应的数据库表关联了起来，但是关联形式稍微有点不同。
    # 我们规定一篇文章只能对应一个分类，但是一个分类下可以有多篇文章，所以我们使用的是 ForeignKey，即一对多的关联关系。
    # 而对于标签来说，一篇文章可以有多个标签，同一个标签下也可能有多篇文章，所以我们使用 ManyToManyField，表明这是多对多的关联关系。
    # 同时我们规定文章可以没有标签，因此为标签 tags 指定了 blank=True。
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag,blank=True)
    
    # 文章作者，这里 User 是从 django.contrib.auth.models 导入的。
    # django.contrib.auth 是 Django 内置的应用，专门用于处理网站用户的注册、登录等流程，User 是 Django 为我们已经写好的用户模型。
    # 这里我们通过 ForeignKey 把文章和 User 关联了起来。
    # 因为我们规定一篇文章只能有一个作者，而一个作者可能会写多篇文章，因此这是一对多的关联关系，和 Category 类似。
    author = models.ForeignKey(User,on_delete=models.CASCADE)

    views = models.PositiveIntegerField(default=0, editable=False)

    top_symbol = models.IntegerField(default=0,blank=True)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-top_symbol','-created_time']
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"pk": self.pk})

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])


class visitCount(models.Model):

    count = models.PositiveIntegerField(default=0, editable=True)
    print('count call:',count)

    def __str__(self):
        return str(self.count)

    def save(self,*args, **kwargs):
        self.count += 1
        super().save(*args, **kwargs)
        return self.count

    # def increase_views(self):
    #     self.count += 1
    #     self.save(update_fields=['count'])
    #     return self.count

class viewIP(models.Model):
    ip = models.CharField('访问者IP',max_length=500)
    view_time = models.DateTimeField('访问时间', default=timezone.now)




    