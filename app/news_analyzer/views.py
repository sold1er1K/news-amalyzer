from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
import re
import string
import pandas as pd
from .models import News
import joblib
import os



def main_page(request):
    return render(request, 'news_analyzer/main.html')


def history_page(request):
    news_list = News.objects.all()
    paginator = Paginator(news_list, 12)
    page_number = request.GET.get('page', 1)  # По умолчанию 1-я страница
    try:
        page_obj = paginator.get_page(page_number)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)  # Если страница не существует, показываем последнюю

    # Передаем актуальное количество страниц в шаблон
    return render(request, 'news_analyzer/history.html', {
        'page_obj': page_obj,
        'total_pages': paginator.num_pages  # Добавляем общее количество страниц
    })


def output_label(n):
    return "Fake" if n == 0 else "Not Fake"


def wordopt(text):
    text = text.lower()
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r"https?://\S+|www\.\S+", '', text)
    text = re.sub(r'<.*?>+', '', text)
    text = re.sub(r'[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub(r'\n', '', text)
    text = re.sub(r'\w*\d\w*', '', text)
    return text


def predict_news(news):
    vectorization = joblib.load(os.path.join(settings.BASE_DIR, 'news_analyzer', 'training_models', 'vectorizer.pkl'))
    lr = joblib.load(os.path.join(settings.BASE_DIR, 'news_analyzer', 'training_models', 'logistic_regression.pkl'))
    dt = joblib.load(os.path.join(settings.BASE_DIR, 'news_analyzer', 'training_models', 'decision_tree.pkl'))
    gbc = joblib.load(os.path.join(settings.BASE_DIR, 'news_analyzer', 'training_models', 'gradient_boosting.pkl'))
    rfc = joblib.load(os.path.join(settings.BASE_DIR, 'news_analyzer', 'training_models', 'random_forest.pkl'))

    testing_news = {"text": [news]}
    new_def_test = pd.DataFrame(testing_news)
    new_def_test["text"] = new_def_test["text"].apply(wordopt)
    new_x_test = new_def_test["text"]
    new_xv_test = vectorization.transform(new_x_test)

    models = {
        "Logistic Regression": lr,
        "Decision Tree": dt,
        "Gradient Boosting": gbc,
        "Random Forest": rfc,
    }

    fake_count = 0
    not_fake_count = 0
    fake_probabilities = []
    not_fake_probabilities = []

    for name, model in models.items():
        prediction = model.predict(new_xv_test)[0]
        probability = (
            round(model.predict_proba(new_xv_test).max() * 100, 2)
            if hasattr(model, "predict_proba")
            else 25
        )

        if prediction == 0:  # Fake
            fake_count += 1
            fake_probabilities.append(probability)
        else:  # Not Fake
            not_fake_count += 1
            not_fake_probabilities.append(probability)

    if fake_count > not_fake_count:
        is_fake = True
        overall_probability = round(sum(fake_probabilities) / len(fake_probabilities), 2)
    elif fake_count < not_fake_count:
        is_fake = False
        overall_probability = round(sum(not_fake_probabilities) / len(not_fake_probabilities), 2)
    else:
        is_fake = False
        overall_probability = round(sum(not_fake_probabilities) / len(not_fake_probabilities), 2)

    return {
        "is_fake": is_fake,
        "probability": overall_probability,
    }


@csrf_exempt
def analyze_news(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            news_content = data.get('content', '').strip()
            if not news_content:
                return JsonResponse({'error': 'Content is required'}, status=400)

            result = predict_news(news_content)

            return JsonResponse(result, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid HTTP method'}, status=405)


@csrf_exempt
def add_news(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            content = data.get('content', '').strip()
            is_fake = data.get('is_fake')
            probability = data.get('probability')

            if not content or is_fake is None or probability is None:
                return JsonResponse({'error': 'Invalid input data'}, status=400)

            if not isinstance(probability, (int, float)) or probability < 0 or probability > 100:
                return JsonResponse({'error': 'Probability must be a number between 0 and 100'}, status=400)

            news_entry = News.objects.create(
                content=content,
                is_fake=is_fake,
                probability=probability,
            )

            return JsonResponse({
                'message': 'News added successfully',
                'news_id': news_entry.id,
                'created_at': news_entry.created_at,
            }, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid HTTP method. Use POST.'}, status=405)