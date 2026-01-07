from django.contrib import admin
from .models import CreditProduct, CreditApplication
from django.http import HttpResponse
import openpyxl
from openpyxl.styles import Font

# ========== CreditProduct ==========
@admin.register(CreditProduct)
class CreditProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'min_amount', 'max_amount', 'rate', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name']

# ========== CreditApplication ==========
def export_to_xlsx(modeladmin, request, queryset):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Заявки на кредит"

    headers = ['ID', 'Пользователь', 'Продукт', 'Сумма', 'Телефон', 'Статус', 'Создано']
    ws.append(headers)
    for cell in ws[1]:
        cell.font = Font(bold=True)

    for app in queryset:
        ws.append([
            app.id,
            app.user.username,
            app.product.name,
            float(app.amount),
            app.phone,
            app.get_status_display(),
            app.created_at.strftime('%Y-%m-%d %H:%M')
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=credit_applications.xlsx'
    wb.save(response)
    return response

export_to_xlsx.short_description = "Экспортировать выбранные заявки в XLSX"

@admin.register(CreditApplication)
class CreditApplicationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'amount', 'status', 'created_at']
    list_filter = ['status', 'created_at', 'product']
    search_fields = ['user__username', 'phone']
    readonly_fields = ['created_at', 'updated_at']
    actions = [export_to_xlsx]  