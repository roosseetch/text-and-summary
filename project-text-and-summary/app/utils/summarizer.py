from loguru import logger
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.core.config import settings
from app.utils.redis import init_redis_client


def text_summarizer_lsa(document_id: int) -> str:
    """
    Latent Semantic Analysis, LSA algorithm for text summarization
    """
    try:
        db: Session = next(deps.get_db())
        document = crud.document.get(db=db, id=document_id)
        if not document:
            return

        parser = PlaintextParser.from_string(document.text, Tokenizer(settings.lsa.LANGUAGE))
        stemmer = Stemmer(settings.lsa.LANGUAGE)

        summarizer = Summarizer(stemmer)
        summarizer.stop_words = get_stop_words(settings.lsa.LANGUAGE)

        summary = '\n'.join([str(s) for s in summarizer(parser.document, settings.lsa.SENTENCES_COUNT)])
        crud.document.update(db=db, db_obj=document, obj_in={'summary': summary})
    except Exception:
        redis_cli = init_redis_client()
        redis_cli.lpush(settings.redis.summary_fail_key, document.id)
        logger.exception('Text summarization failed')
