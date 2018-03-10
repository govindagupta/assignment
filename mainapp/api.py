from django.core.exceptions import ValidationError
from django.views.generic.base import View
from django.http import JsonResponse
from .models import PhoneNumber
import json
from .service import do_input_validation,is_rate_validated
from .decorators import basicauth
from .utils import set_cache,get_cache, get_unique_key, expire_cache


class InboundSMS(View):

    @basicauth
    def post(self, request):

        ret = {'message': '', 'error': ''}
        try:
            data = json.loads(request.body.decode('utf-8'))
            json_input_rules = [{'param': 'from', 'required': True, 'regex': '^.{6,16}$'},
                                {'param': 'to', 'required': True, 'regex': '^.{6,16}$'},
                                {'param': 'text', 'required': True, 'regex': '^.{1,120}$'}]

            do_input_validation(data, json_input_rules)

            # Authenticate for 'to' number in account
            queryset = PhoneNumber.objects.filter(number=data['to']).filter(account_id=request.user.first_name)
            # print([p.id for p in queryset])

            if queryset.count() == 0:
                raise PhoneNumber.DoesNotExist("Phone number not there or account mismatch")

            # Recieved STOP, cache it
            if data['text'].strip() == "STOP":
                unique_key = get_unique_key(data['from'], data['to'])
                set_cache(unique_key, True)
                expire_cache(unique_key, 4*3600)

            # everything good, process the message
            ret['message'] = 'inbound sms ok'
            status_code = 200

        except ValidationError as e:
            print("ValidationError", e.message)
            ret['error'] = e.message
            status_code = 400
        except PhoneNumber.DoesNotExist:
            print('to number not exist')
            ret['error'] = 'to number not exist'
            status_code = 400
        except:
            print ('unknown failure')
            ret['error'] = 'unknown failure'
            status_code = 500

        return JsonResponse(data=ret, status=status_code)


class OutboundSMS(View):

    @basicauth
    def post(self, request):

        ret = {'message': '', 'error': ''}
        try:
            data = json.loads(request.body.decode('utf-8'))
            json_input_rules = [{'param': 'from', 'required': True, 'regex': '^.{6,16}$'},
                                {'param': 'to', 'required': True, 'regex': '^.{6,16}$'},
                                {'param': 'text', 'required': True, 'regex': '^.{1,120}$'}]

            do_input_validation(data, json_input_rules)

            # Authenticate for 'from' number in account
            queryset = PhoneNumber.objects.filter(number=data['from']).filter(account_id=request.user.first_name)
            # print([p.id for p in queryset])

            if queryset.count() == 0:
                raise PhoneNumber.DoesNotExist("Phone number not there or account mismatch")

            # check if to, from has been stopped before
            unique_key = get_unique_key(data['to'], data['from'])
            if get_cache(unique_key):
                err_msg = 'sms from %s to %s blocked by STOP request' % (data['from'], data['to'])
                raise ValidationError(err_msg)

            # check for rate limit. 50 times in 24 hrs
            if not is_rate_validated(data['from']):
                err_msg = 'limit reached for from %s' % data['from']
                raise ValidationError(err_msg)

            # everything good, process the message
            ret['message'] = 'outbound sms ok'
            status_code = 200

        except ValidationError as e:
            print("ValidationError", e.message)
            ret['error'] = e.message
            status_code = 400
        except PhoneNumber.DoesNotExist:
            print('from number not exist')
            ret['error'] = 'from number not exist'
            status_code = 400
        except:
            print ('unknown failure')
            ret['error'] = 'unknown failure'
            status_code = 500

        return JsonResponse(data=ret, status=status_code)
