import usaddress
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.exceptions import ParseError


class Home(TemplateView):
    template_name = 'parserator_web/index.html'


class AddressParse(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        input_string = request.query_params.get('address')
        if not input_string:
            raise ParseError("No address provided")

        try:
            address_components, address_type = self.parse(input_string)
            return Response({
                'input_string': input_string,
                'address_components': address_components,
                'address_type': address_type
            })
        except usaddress.RepeatedLabelError:
            raise ParseError("Invalid address: contains repeated components")
       

    def parse(self, address):
        try:
            parsed, address_type = usaddress.tag(address)
            address_components = dict(parsed)
            return address_components, address_type
        except usaddress.RepeatedLabelError:
            raise
