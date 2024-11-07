from django.shortcuts import render
from django.http import JsonResponse

def index(request):
    return render(request, 'p4ds/index.html')

# def submit_data(request):
#     if request.method == 'POST':
#         data = request.POST.get('data')  # 'data'는 보내는 정보의 키
#         # 여기에서 필요한 로직을 수행합니다.
#         return JsonResponse({'status': 'success', 'data': data})
#     return JsonResponse({'status': 'failed'})

# def problem_solving_view(request):
#     return render(request, 'p4ds/problem_solving.html')