from django.utils import timezone
import pytz

timezone.activate(pytz.timezone("Asia/Seoul"))
timezone.localtime(timezone.now())