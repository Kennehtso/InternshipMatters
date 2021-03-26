# 0. Can using command to launch the django shell to access db
python manage.py shell

# 1. import all models
from general.models import *

# 2.Search 'All' 
## items of One Table (Model)
org = Organization.objects.all()
# use print to out put the dict format result
print(org)

# 3. Get First or Last target
## we can use .first() or .last() to retrive data
org.first()
org.last()

# 4. Search by get() Method
## we can get speical target by get() method:
intern_1 = Intern.objects.get(name='kso')
intern_1 = Intern.objects.get(id=1)
### be aware that if name are not unique, there will cause error

# 5. use _set.all() to get target data
## format as: targets = {parent variable}.{Target Table name in small cap}_set.all()
comments = intern_1.comment_set().all()
print(comments)

# 6. Get Data from Child (comment) to Parent (Intern)
## Get parent variable by foreign key mapping already
comment = Comment.objects.first()
comment.
intern_name = comment.intern.name
print(intern_name)

# 7. Filtering data
## empty parameter = all() action
comments = Comment.objects.filter(comments=None)
comments = Comment.objects.filter(intern__name='kso')
print(comments)

# 8. Sort data
comments = Comment.objects.all().order_by('score')
## Reverse
comments = Comment.objects.all().order_by('-score')

# 9. Filtering Many to Many 
## Format: {fields}__{field.variable}='{target}'
comments = Comment.objects.filter(hashTags__name='講座多')

# 10. Query from parent with other parent
## As we want to count all Counts of the org,
## that the target intern has left
comments = Comment.objects.filter(intern__name='kso')
orgCount = {}
for cmt in comments:
    orgName = cmt.organization.name
    if orgName and orgName in orgCount:
        orgCount[orgName] += 1
    else:
        orgCount[orgName] = 1
print(orgCount)
