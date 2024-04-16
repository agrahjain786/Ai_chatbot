from django.contrib import admin
from .models import Chat,FAQ,Doubt,ChatMonitor,feedback
import csv
from django.http import HttpResponse

# Register your models here.
# admin.site.register(Chat)
admin.site.register(FAQ)
admin.site.register(Doubt)

def export_chats_to_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="chats.csv"'

    writer = csv.writer(response)
    fields = ['user', 'message', 'response', 'created_at']
    writer.writerow(fields)

    for chat in queryset:
        writer.writerow([chat.user, chat.message, chat.response , chat.created_at])

    return response

export_chats_to_csv.short_description = 'Export Chats to CSV'

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    actions = [export_chats_to_csv]
    
    
def export_chats_to_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="chatmonitor.csv"'

    writer = csv.writer(response)
    fields = ['user', 'message', 'response', 'response_time', 'fallback']
    writer.writerow(fields)

    for chat in queryset:
        writer.writerow([chat.user, chat.message, chat.response , chat.response_time, chat.fallback])

    return response

export_chats_to_csv.short_description = 'Export Chats to CSV'

@admin.register(ChatMonitor)
class ChatMonitorAdmin(admin.ModelAdmin):
    actions = [export_chats_to_csv]
    
def export_chats_to_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="feedback.csv"'

    writer = csv.writer(response)
    fields = ['user', 'rating']
    writer.writerow(fields)

    for feed in queryset:
        writer.writerow([feed.user, feed.rating])

    return response

export_chats_to_csv.short_description = 'Export Chats to CSV'

@admin.register(feedback)
class FeedbackAdmin(admin.ModelAdmin):
    actions = [export_chats_to_csv]