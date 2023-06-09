import logging
import os

from celery import Celery, bootsteps
import kombu


logger = logging.getLogger(__name__)

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('proj')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


def rabbitmq_conn():
    return app.pool.acquire(block=True)


def rabbitmq_producer():
    return app.producer_pool.acquire(block=True)


def _publish(message, routing_key, exchange):
    with rabbitmq_producer() as producer:
        producer.publish(
            body=message,
            routing_key=routing_key,
            exchange=exchange
        )


with rabbitmq_conn() as conn:
    queue = kombu.Queue(
        name='queue-payment',
        exchange='payment',
        routing_key='paymentgateway_service',
        channel=conn,
        durable=True
    )
    queue.declare()


class PaymentMethodConsumer(bootsteps.ConsumerStep):
    def get_consumers(self, channel):
        return [
            kombu.Consumer(
                channel,
                queues=[queue],
                callbacks=[self.handle_message],
                accept=['json']
            )
        ]

    def handle_message(self, data, message):
        from payment.process_payment import checkout_session
        logging.info('Starting Payment Checkout Session')
        try:
            remote_invoice_id = checkout_session(data)
            data['remote_invoice_id'] = remote_invoice_id
            data['status_id'] = 'e2182812-d1b0-4585-99bf-6510497602ab'
            _publish(message=data, routing_key='checkout_service', exchange='checkout')
        except Exception as e:
            data['remote_invoice_id'] = None
            data['status_id'] = 'e3182812-d1b0-4585-99bf-6510497602ab'
            _publish(message=data, routing_key='checkout_service', exchange='checkout')
            logger.exception(e)

        message.ack()


app.steps['consumer'].add(PaymentMethodConsumer)
