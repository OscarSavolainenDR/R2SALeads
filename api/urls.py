# Stores all urls local to this app (api)
from django.urls import path
from .views.setup_views import InitDB, UpdateListings
from .views.project_views import UpdateScrumBoardBackend, DownloadExcel, GetTableLeads, UpdateLeadsListBackend
from .views.auth_views import SignIn, SignOut, SignUp, ForgotPassword, ResendConfirmEmail, ResetPasswordView, ConfirmEmail_api, GetEmailStatus
from .views.subscription_views import GetSubscriptionOptions, UnsubscribeFromCity, AddCitytoBasket
from .views.subscription_views import GetBasket, CheckoutBasket#, StripeCheckout #, CreateStripePaymentIntent#, SaveStripeInfo
from .views.account_views import GetAccountSettingsData, GetAccountSettingsBillingData, UpdatePassword
from .views.stripe_webhook import stripe_webhook
from .views.test_views import Test 
from .views.feedback_views import Feedback

# API endpoints, tells us where the front-end 
# # sends stuff to get to the backend 
urlpatterns = [
    # Set up URLs
    path('init-db', InitDB.as_view()),
    path('update-listings', UpdateListings.as_view()),

    # Project URLs
    # path('project/scrum-board/boards', GetScrumBoard.as_view()),
    path('project/scrum-board/update-backend', UpdateScrumBoardBackend.as_view()),
    path('project/scrum-board/download-excel', DownloadExcel.as_view()),
    path('project/leads-list/update-backend', UpdateLeadsListBackend.as_view()),

    # Table View
    path('project/table-view/get-leads', GetTableLeads.as_view()), 

    # Stripe webook
    path('webhooks/stripe', stripe_webhook, name='stripe-webhook'),

    # See subscriptions
    path('subscriptions/products', GetSubscriptionOptions.as_view()),
    path('subscriptions/unsubscribe', UnsubscribeFromCity.as_view()),
    path('subscriptions/add-to-basket', AddCitytoBasket.as_view()),
    path('subscriptions/get-basket', GetBasket.as_view()),
    # path('subscriptions/stripe-checkout', StripeCheckout.as_view()), # old version
    # path('subscriptions/checkout', CreateStripePaymentIntent.as_view()),
    path('subscriptions/checkout', CheckoutBasket.as_view()),
    # path('subscriptions/save-stripe-info', SaveStripeInfo.as_view()),    
    
    # Account
    path('account/setting', GetAccountSettingsData.as_view()),
    path('account/setting/billing', GetAccountSettingsBillingData.as_view()),
    path('account/update-password', UpdatePassword.as_view()),

    # Auth URLs
    path('sign-in', SignIn.as_view()),
    path('sign-out', SignOut.as_view()),
    path('sign-up', SignUp.as_view()),
    path('forgot-password', ForgotPassword.as_view()),
    # path('reset-password/<uidb64>/<token>/', ResetPassword, name='reset-password'), # function, not class
    path('reset-password', ResetPasswordView.as_view()),
    path('get-email-status', GetEmailStatus.as_view()),
    path('confirm-email', ConfirmEmail_api.as_view()),
    path('resend-confirm-email', ResendConfirmEmail.as_view()),
    

    path('feedback/submit', Feedback.as_view()),

    path('test', Test.as_view())
] 