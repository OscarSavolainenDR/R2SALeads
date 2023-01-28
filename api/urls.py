# Stores all urls local to this app (api)
from django.urls import path
from .views.setup_views import InitDB, UpdateListings
from .views.project_views import GetScrumBoard_2, GetScrumBoardMembers, UpdateScrumBoardBackend, DownloadExcel, GetTableLeads
from .views.auth_views import SignIn, SignOut, SignUp, ForgotPassword, ResetPasswordView
from .views.notification_views import GetNotifications, GetNotificationCount
from .views.subscription_views import GetSubscriptionOptions, UnsubscribeFromCity, AddCitytoBasket
from .views.subscription_views import GetBasket, StripeCheckout #, SaveStripeInfo
from .views.account_views import GetAccountSettingsData, GetAccountSettingsBillingData, UpdatePassword

# API endpoints, tells us where the front-end 
# # sends stuff to get to the backend 
urlpatterns = [
    # Set up URLs
    path('init-db', InitDB.as_view()),
    path('update-listings', UpdateListings.as_view()),

    # Project URLs
    path('project/scrum-board/boards', GetScrumBoard_2.as_view()),
    path('project/scrum-board/members', GetScrumBoardMembers.as_view()),
    path('project/scrum-board/update-backend', UpdateScrumBoardBackend.as_view()),
    path('project/scrum-board/download-excel', DownloadExcel.as_view()),

    # Table View
    path('project/table-view/get-leads', GetTableLeads.as_view()), 

    # See subscriptions
    path('subscriptions/products', GetSubscriptionOptions.as_view()),
    path('subscriptions/unsubscribe', UnsubscribeFromCity.as_view()),
    path('subscriptions/add-to-basket', AddCitytoBasket.as_view()),
    path('subscriptions/get-basket', GetBasket.as_view()),
    path('subscriptions/stripe-checkout', StripeCheckout.as_view()),
    # path('subscriptions/save-stripe-info', SaveStripeInfo.as_view()),    
    
    # Account
    path('account/setting', GetAccountSettingsData.as_view()),
    path('account/setting/billing', GetAccountSettingsBillingData.as_view()),
    path('account/update-password', UpdatePassword.as_view()),
    
    # Notification URLs
    path('notification/list', GetNotifications.as_view()),
    path('notification/count', GetNotificationCount.as_view()),

    # Auth URLs
    path('sign-in', SignIn.as_view()),
    path('sign-out', SignOut.as_view()),
    path('sign-up', SignUp.as_view()),
    path('forgot-password', ForgotPassword.as_view()),
    # path('reset-password/<uidb64>/<token>/', ResetPassword, name='reset-password'), # function, not class
    path('reset-password', ResetPasswordView.as_view()), # function, not class
] 