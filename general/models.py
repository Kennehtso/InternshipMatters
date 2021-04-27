from django.db import models
from django.db.models.expressions import F, ValueRange
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg
from django.contrib.auth.models import User
# Create your models here.

# TODO - may need to use Login user id

class InternPerson(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=False)
    email = models.EmailField(null=True)
    profilePic = models.ImageField(default="default.png", null=True, blank=True)
    createDate = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return self.name

class HashTags(models.Model):
    name = models.CharField(max_length=200, null=False)
    def __str__(self):
        return self.name

ORGANIZATIONTYPE = (
    ('大專校院諮商(輔導)中心(處、室、組)','大專校院諮商(輔導)中心(處、室、組)'),
    ('心理諮商所','心理諮商所'),
    ('公、私立高中、職、中小學輔導室（處）、教育局處學生諮商中心','公、私立高中、職、中小學輔導室（處）、教育局處學生諮商中心'),
    ('醫療機構','醫療機構'),
    ('社區性心理衛生中心','社區性心理衛生中心'),
    ('政府及事業單位設有心理治療或諮商業務之單位','政府及事業單位設有心理治療或諮商業務之單位'),
    ('財團法人基金會','財團法人基金會'),
)
class Organization(models.Model):
    name = models.CharField(max_length=200, null=False)
    area = models.CharField(max_length=200, null=True)
    # TODO - may better need define in db
    organizationType = models.CharField(null=True, max_length=200, choices=ORGANIZATIONTYPE)
    score = models.FloatField(default=0, null=True, validators=[MaxValueValidator(5), MinValueValidator(0)])
    commentsCount = models.IntegerField(default=0, null=True, validators=[MinValueValidator(0)])
    unitName = models.CharField(max_length=200, null=True)
    unitType = models.CharField(max_length=200, null=True)
    subsidy = models.CharField(max_length=200, null=True)
    internshipContent = models.CharField(max_length=200, null=True)
    hashTags = models.ManyToManyField(HashTags, blank=True)
    detailInfoFromExtUrl = models.CharField(max_length=200, blank=True, null=True)
    isApprove = models.BooleanField(default=False, blank=True, null=True)
    
    """
    def getScore(self):
        comments = Comment.objects.filter(organization__id=self.id)
        self.commentsCount = comments.count()
        avgScore = comments.aggregate(Avg('score'))["score__avg"]
        return 0 if avgScore is None else int(avgScore)

    def getCommentsCount(self):
        return self.commentsCount()
    """
    def __str__(self):
        return self.name

class Comment(models.Model):

    INTERNSHIPTYPE = (
        ('校外課程實習','校外課程實習'),
        ('校外全職實習','校外全職實習'),
        ('校內課程實習','校內課程實習'),
        ('校內全職實習','校內全職實習'),
    )
    # TODO - 1(organization) to 1(Comment)
    organization = models.ForeignKey(Organization, null=True, on_delete=models.SET_NULL)
    # TODO - 1(intern) to 1(Comment)
    # On Delete = If the related user is deleted, delete this record
    intern = models.ForeignKey(InternPerson, null=True, on_delete=models.SET_NULL)
    # TODO -  may better need define in db
    internshipType = models.CharField(null=True,blank=True, max_length=200, choices=INTERNSHIPTYPE)
    # TODO - Many(hashTags) to Many(Comment)
    hashTags = models.ManyToManyField(HashTags, blank=True)
    comments = models.CharField(max_length=200, null=True,blank=True)
    createDate = models.DateTimeField(auto_now_add=True, null=True)
    updatedDate = models.DateTimeField(null=True,blank=True)
    score = models.IntegerField(default=0, null=True, validators=[MaxValueValidator(5), MinValueValidator(0)])
    
    def __str__(self):
        return f"{self.organization}({self.intern})({self.comments})"
        
    def hashTags_names(self):
        return ', '.join([h.name for h in self.hashTags.all()])


