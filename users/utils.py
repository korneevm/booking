# coding: utf-8
from django.conf import settings


def send_mandrill_email(template, to_email=None, to_name=None, merge_vars=[], subject=False, from_email=False, from_name=False, order=False):
        try:
            import mandrill
            mandrill_client = mandrill.Mandrill(settings.MANDRILL_KEY)
            template_content = [{'content': '', 'name': 'tmp'}]
            message = {
                'google_analytics_domains': ['tceh.com'],
                'important': False,
                'inline_css': None,
                'merge': True,
                'merge_vars': [{'rcpt': to_email, 'vars': merge_vars}],
                'metadata': {'website': 'tceh.com'},
                'preserve_recipients': None,
                'to': [{'email': to_email, 'name': to_name, 'type': 'to'}],
                'view_content_link': None
            }
            if from_email:
                message['from_email'] = from_email

            if from_name:
                message['from_name'] = from_name

            if subject:
                message['subject'] = subject

            result = mandrill_client.messages.send_template(
                template_name=template, template_content=template_content, message=message, async=False)

            if order:
                return result
            return True
        except mandrill.Error, e:
            # Mandrill errors are thrown as exceptions
            print 'A mandrill error occurred: %s - %s' % (e.__class__, e)
            raise


def check_mandrill_status(mandrill_id):
    try:
        import mandrill
        mandrill_client = mandrill.Mandrill(settings.MANDRILL_KEY)
        result = mandrill_client.messages.info(id=mandrill_id)
        return result

    except mandrill.Error, e:
        # Mandrill errors are thrown as exceptions
        print 'A mandrill error occurred: %s - %s' % (e.__class__, e)
        return False
