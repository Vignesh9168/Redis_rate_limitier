import time 
import redis 
from django.http import JsonResponse 
from django.conf import settings 


class RateLimitMiddleware:

    def __init__(self,get_response):
        self.get_response = get_response 
        self.redis = redis.StrictRedis.from_url(settings.REDIS_URL, decode_responses=True)
        self.rate = getattr(settings,"RATE_LIMIT",10)
        self.window = getattr(settings,"WINDOW",60)

    def __call__(self,request):
        # take client ip     
        ip = self.get_client_ip(request)     #identify the user
        key = f"rl:{ip}"                    #bilds the redis key

        pipe = self.redis.pipeline()       
        current = pipe.incr(key)               #Atomically increment number of requests in current time window
        results = pipe.execute()             #This sends all commands in the pipeline to Redis in one go


        new_value = results[0]

        if new_value == 1 :
            try :
                self.redis.expire(key,self.window)
            except Exception:
                pass

        if new_value > self.rate :
            ttl = self.redis.ttl(key)
            retry_after =  ttl if ttl and ttl > 0 else self.window 
            response = JsonResponse({"status": 429, "message":"To many requests","retry_after": f"{retry_after} seconds"},status= 429)   

            response['retry_after'] = str(retry_after)


            return response 
        
        response = self.get_response(request)
        return response


    def get_client_ip(self,request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for :
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')

        return ip 
        



