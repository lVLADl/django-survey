from django.urls import path, include
from . import views

def temp_view(request):
    pass
urlpatterns = [
    path('surveys/', include([
        path('', views.SurveyView.as_view()), # GET/POST new survey
        path('<int:survey_id>/', include([ # GET/PUT/DELETE survey
            path('', views.SurveyDetailView.as_view()),
            path('question/', include([
                path('<int:question_id>/', include([
                    path('', views.QuestionView.as_view()), # GET question / POST answer / DELETE question / PUT question
                    path('options/', include([
                        path('', views.OptionView.as_view()), # POST (create) OPTION
                        path('<int:option_id>/', views.OptionView.as_view()), # GET OPTION / DELETE OPTION / PUT OPTION
                    ])),
                ]))
            ])) # POST create new question in survey
        ])),
        path('get_finished_by_user/<int:user_id>/', views.user_surveys)
    ])),
]