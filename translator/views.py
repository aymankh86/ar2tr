from django.shortcuts import render
from django.http import HttpResponseNotAllowed, JsonResponse
from .models import Phrase, Category, Suggestions
from django.db.models import Q
import pyarabic.araby as araby
from langdetect import detect
from django.db.models import Value
import json
from django.views.decorators.csrf import csrf_exempt


def index(request):
    searchTerm = request.GET.get('searchTerm')
    selected_category = request.GET.get('category')
    page = int(request.GET.get('page', '1'))
    limit = int(request.GET.get('limit', '20'))
    searchTerm = araby.strip_harakat(searchTerm)
    if searchTerm:
        results = Phrase.objects.filter(Q(ar_text_no_harakat__iexact=searchTerm) | Q(tr_text__iexact=searchTerm))
        ids = [i.id for i in results]
        phrase_results = Phrase.objects.exclude(id__in=ids).filter(Q(ar_text_no_harakat__icontains=searchTerm) | Q(tr_text__icontains=searchTerm))

        results = results.annotate(order=Value(1))
        phrase_results = phrase_results.annotate(order=Value(2))
        query_results = results.union(phrase_results).order_by('order')
        total_count = query_results.count()
        context = {
            "searchTerm": searchTerm,
            "total_count": total_count,
            "page": page,
            "has_next": total_count > page * limit,
            "results": query_results[page-1:limit]
        }
    elif selected_category:
        query_results = Phrase.objects.filter(category__id=selected_category)
        total_count = query_results.count()
        context = {
            "selected_category": selected_category,
            "total_count": total_count,
            "has_next": total_count > page * limit,
            "has_prev": page > 1 and total_count > 20,
            "page": page,
            "results": query_results[(page-1)*limit: ((page-1)*limit) + 20]
        }
    else:
        context = {}
    cats = Category.objects.all()
    context.update({'cats': cats})
    return render(request, 'translator/index.html', context)

def search(request):
    query = request.GET.get('query')
    lang = detect(query)
    if lang in ['ar', 'ur', 'fa']:
        suggestions = list(Phrase.objects.filter(ar_text_no_harakat__icontains=query).values_list('ar_text', flat=True))
    else:
        suggestions = list(Phrase.objects.filter(tr_text__icontains=query).values_list('tr_text', flat=True))
    return JsonResponse(suggestions, safe=False)


@csrf_exempt
def suggest(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed("")
    
    data = request.POST

    category = data.get("category")
    phrase = data.get("id")
    ar_text = data.get("ar_text")
    tr_text = data.get("tr_text")
    job_type = data.get("job_type")

    category = Category.objects.get(id=category)
    exists = Phrase.objects.filter(category=category, ar_text=ar_text, tr_text=tr_text).exists()
    print(exists)
    if job_type == 'add' and exists:
        return JsonResponse({"success": False, "msg": "already exists"}, status=500)

    if job_type == 'edit':
        phrase = Phrase.objects.get(id=category)
    else:
        phrase = None

    Suggestions.objects.create(category=category, phrase=phrase, ar_text=ar_text, tr_text=tr_text, job_type=job_type)
    
    return JsonResponse({"success": True}, status=200)