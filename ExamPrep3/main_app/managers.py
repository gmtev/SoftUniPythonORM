# from django.db import models
# in cse of having the manager stored in a different file
#

# class AuthorManager(models.Manager):
#     def get_authors_by_article_count(self):
#         return self.annotate(article_count=models.Count('article')).order_by('-article_count', 'email')
