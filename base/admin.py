# admin.py
from django.contrib import admin
from .models import ( ImageEditor, OTPVerification, PathManager, FolderManager, 
                     Comments, LeaderBoard, Rating, McqQuestionBase,
                      Config, UserSubscription, Report, PaymentDb, LatestUpdate, Contact )

admin.site.register(ImageEditor)
admin.site.register(OTPVerification)
admin.site.register(PathManager)
admin.site.register(FolderManager)
admin.site.register(Comments)
admin.site.register(LeaderBoard)
admin.site.register(Rating)
admin.site.register(McqQuestionBase)
admin.site.register(Config)
admin.site.register(UserSubscription)
admin.site.register(Report)
admin.site.register(PaymentDb)
admin.site.register(LatestUpdate)
admin.site.register(Contact)
