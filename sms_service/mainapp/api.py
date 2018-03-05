from django.core.exceptions import ValidationError
from django.views.generic.base import View
from django.http import JsonResponse
from .models import PhoneNumber
import json
from .service import do_input_validation

class InboundSMS(View):

    def post(self, request):

        ret = {'message': '', 'error': ''}
        try:
            data = json.loads(request.body.decode('utf-8'))
            json_input_rules = [{'param': 'from', 'required': True, 'regex': '^.{6,16}$'},
                                {'param': 'to', 'required': True, 'regex': '^.{6,16}$'},
                                {'param': 'text', 'required': True, 'regex': '^.{1,120}$'}]

            do_input_validation(data, json_input_rules)

            # TODO -  Authentication against account
            PhoneNumber.objects.get(number=data['to'])

            #everything good, process the message
            ret['message'] = 'inbound sms ok'

        except ValidationError as e:
            print("ValidationError", e.message)
            ret['error'] = e.message
        except PhoneNumber.DoesNotExist:
            print('to number not exist')
            ret['error'] = 'to number not exist'
        except:
            print ('unknown failure')
            ret['error'] = 'unknown failure'

        return JsonResponse(ret)


class OutboundSMS(View):

    def post(self, request):

        ret = {'message': '', 'error': ''}
        try:
            data = json.loads(request.body.decode('utf-8'))
            json_input_rules = [{'param': 'from', 'required': True, 'regex': '^.{6,16}$'},
                                {'param': 'to', 'required': True, 'regex': '^.{6,16}$'},
                                {'param': 'text', 'required': True, 'regex': '^.{1,120}$'}]

            do_input_validation(data, json_input_rules)

            #TODO -  Authentication against account
            PhoneNumber.objects.get(number=data['from'])

            #everything good, process the message
            ret['message'] = 'inbound sms ok'

        except ValidationError as e:
            print("ValidationError", e.message)
            ret['error'] = e.message
        except PhoneNumber.DoesNotExist:
            print('to number not exist')
            ret['error'] = 'to number not exist'
        except:
            print ('unknown failure')
            ret['error'] = 'unknown failure'

        return JsonResponse(ret)
