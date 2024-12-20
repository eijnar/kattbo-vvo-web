import logging

from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

from core.database.base import AsyncSessionLocal
from core.messaging.template_service import TemplateService
from core.messaging.telegram_service import TelegramService
from core.messaging.email_service import EmailService
from core.messaging.factory import MessagingServiceFactory
from core.config import settings


logger = logging.getLogger(__name__)
#nest_asyncio.apply()

# @shared_task(serializer='json')
# def send_notification_task(service_name: str, recipients: list, template_name: str, context: dict):
#     loop = asyncio.get_event_loop()
#     if loop.is_running():
#         loop.run_until_complete(_send_notification(service_name, recipients, template_name, context))
#     else:
#         asyncio.run(_send_notification(service_name, recipients, template_name, context))

async def send_notification_task(service_name: str, recipients: list, template_name: str, context: dict):
    try:
        async with AsyncSessionLocal() as db:  # Ensure AsyncSessionLocal is set up properly
            template_service = TemplateService(db)
            
            email_service = EmailService(
                smtp_server=settings.SMTP_SERVER,
                smtp_port=settings.SMTP_PORT,
                username=settings.SMTP_USERNAME,
                password=settings.SMTP_PASSWORD,
                template_service=template_service
            )
            
            telegram_service = TelegramService(
                bot_token=settings.TELEGRAM_BOT_TOKEN,
                template_service=template_service
            )

            service_factory = MessagingServiceFactory()
            service_factory.register_service('email', email_service)
            service_factory.register_service('telegram', telegram_service)

            messaging_service = service_factory.get_service(service_name)

            subject, full_message = await messaging_service.set_template(template_name, context)
            
            for recipient in recipients:
                try:
                    await messaging_service.send_message(recipient, subject, full_message)
                    logger.info(f"Message sent to {recipient} via {service_name}.")
                except Exception as e:
                    logger.error(f"Failed to send message to {recipient} via {service_name}. Error: {str(e)}")
                
    except SQLAlchemyError as e:
        logger.error(f"Database error occurred: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )