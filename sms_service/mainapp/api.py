from django.core.exceptions import ValidationError
from django.views.generic.base import View
from django.http import JsonResponse
from django.contrib.auth import authenticate
from .models import PhoneNumber
import json
from .service import do_input_validation
from .decorators import basicauth


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

            #Authenticate for 'to' number in account
            queryset = PhoneNumber.objects.filter(number=data['to']).filter(account_id=request.user.first_name)
            #print([p.id for p in queryset])

            if queryset.count() == 0:
                raise PhoneNumber.DoesNotExist("Phone number not there or account mismatch")

            #everything good, process the message
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

        return JsonResponse(data = ret, status=status_code)


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

            #Authenticate for 'from' number in account
            queryset = PhoneNumber.objects.filter(number=data['from']).filter(account_id=request.user.first_name)
            #print([p.id for p in queryset])

            if queryset.count() == 0:
                raise PhoneNumber.DoesNotExist("Phone number not there or account mismatch")

            #everything good, process the message
            ret['message'] = 'inbound sms ok'
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
