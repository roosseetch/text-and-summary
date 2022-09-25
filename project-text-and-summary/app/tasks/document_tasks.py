from celery import shared_task

from app.utils.summarizer import text_summarizer_lsa


@shared_task
def generate_summary_for_text(document_id: int) -> None:
    text_summarizer_lsa(document_id)
