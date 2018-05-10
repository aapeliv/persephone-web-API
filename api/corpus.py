"""
API endpoints for /corpus
This deals with the API access corpus model definitions and metadata
"""
import logging
import zipfile

from .db_models import Corpus
from . import db

logger = logging.getLogger(__name__)

def search():
    print("Request for all available corpus")
    return "Get available corpus not implemented", 501


def post(corpusInfo):
    """Create a Corpus"""
    training_set_IDs = corpusInfo['training']
    testing_set_IDs = corpusInfo['testing']
    validation_set_IDs = corpusInfo['validation']
    return "Corpus creation not implemented", 501

def create_from_zip(zippedFile):
    if zippedFile.mimetype != 'application/zip':
        logger.info("Non zip mimetype from request, got {}".format(zippedFile.mimetype))
        return "File type must be zip", 415
    if not zipfile.is_zipfile(zippedFile):
        logger.info("Zip file corrupted")
        return "File type must be zip", 415
    print("Create corpus from zip file")
    return "Create corpus from zip not implemented", 501
