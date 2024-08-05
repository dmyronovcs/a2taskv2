from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda
import json

_LOG = get_logger('HelloWorld-handler')


class HelloWorld(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass
        
    def handle_request(self, event, context):
        """
        Explain incoming event here
        """
        is_http = False
        if ('requestContext' in event and 'http' in event['requestContext']):
            _LOG.info(f'HTTP Request presetns')
            is_http = True
        # todo implement business logic
        if is_http:
            _LOG.info(f'HTTP Request received')
            path = event.get('rawPath')
            method = event.get('requestContext', {}).get('http', {}).get('method')
            _LOG.info(f'Received request with path: {path} and method: {method}')

            headers = {
                'Content-Type': 'application/json'
            }

            if path == '/hello' and method == 'GET':
                response_body = {
                    'statusCode': 200,
                    'message': 'Hello from Lambda'
                }
                _LOG.info('Returning successful response for /hello GET')
                response = {
                    'statusCode': 200,
                    'headers': headers,
                    'body': json.dumps(response_body)
                }
                return response
            else:
                error_message = f'Bad request syntax or unsupported method. Requested path: {path}, HTTP method: {method}'
                _LOG.error(error_message)
                response_body = {
                    'statusCode': 400,
                    'message': error_message
                }
                return {
                    'statusCode': 400,
                    'headers': headers,
                    'body': json.dumps(response_body)
                }
        else:
            _LOG.info(f'HTTP Request not found')
            return 200
    

HANDLER = HelloWorld()


def lambda_handler(event, context):
    _LOG.info('Handler execution started')
    _LOG.info('Event:')
    _LOG.info(event)
    _LOG.info('Context:')
    _LOG.info(context)
    return HANDLER.lambda_handler(event=event, context=context)
    _LOG.info('Handler execution completed')
