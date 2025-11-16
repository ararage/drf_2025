from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

class ReviewCreateThrottle(UserRateThrottle):
    scope = "review-create"
    rate = '5/day'
    

class ReviewListThrottle(UserRateThrottle):
    scope = "review-list"
    rate = '100/day'
