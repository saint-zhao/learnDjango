# from blog.models import Category

# from django.contrib.auth.models import User

# user = User.objects.all().first()

# Category.objects.bulk_create([
#    Category(name='cate%s'%i, owner=user , status=Category.STATUS_NORMAL) for i in range(10000)
# ])

# cate = Category.objects.filter(name__contains='cate')
# cate.delete()

import logging

FORMAT = '%(asctime) - 15s %(clientip)s %(user) -8s %(message)s'
logging.basicConfig(format=FORMAT)
d = {'clientip': '127.0.0.1', 'user': 'saint'}
logger = logging.getLogger(__name__)

logger.info('the is %s level', 'info', extra=d)
