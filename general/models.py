from django.db import models
# Create your models here.

# TODO - may need to use Login user id

class Intern(models.Model):
    name = models.CharField(max_length=200, null=False)
    email = models.EmailField(null=True)
    def __str__(self):
        return self.name

class Organization(models.Model):
    ORGANIZATIONTYPE = (
        ('各級學校諮商','各級學校諮商'),
        ('社區性心理衛生中心或諮商機構','社區性心理衛生中心或諮商機構'),
        ('已立案之社會福利相關機構','已立案之社會福利相關機構'),
        ('醫療機構','醫療機構'),
        ('司法院或法務部所屬相關單位','司法院或法務部所屬相關單位'),
        ('企業單位及所屬基金會','企業單位及所屬基金會'),
    )
    name = models.CharField(max_length=200, null=False)
    area = models.CharField(max_length=200, null=True)
    # TODO - may better need define in db
    organizationType = models.CharField(null=True, max_length=200, choices=ORGANIZATIONTYPE)
    score = models.FloatField(default=0, null=True)

    def __str__(self):
        return self.name

class HashTags(models.Model):
    name = models.CharField(max_length=200, null=False)
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
    intern = models.ForeignKey(Intern, null=True, on_delete=models.SET_NULL)
    # TODO -  may better need define in db
    internshipType = models.CharField(null=True, max_length=200, choices=INTERNSHIPTYPE)
    # TODO - Many(hashTags) to Many(Comment)
    hashTags = models.ManyToManyField(HashTags)
    comments = models.CharField(max_length=200, null=True,blank=True)
    createDate = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return f"{self.organization}({self.intern})({self.comments})"
        

