import requests
import logging
from typing import List

from sn_agent.job.job_descriptor import JobDescriptor
from sn_agent.service_adapter import ServiceAdapterABC
from sn_agent.ontology import Service
from sn_agent.service_adapter import ServiceAdapterABC, ServiceManager

logger = logging.getLogger(__name__)

r = requests.get("https://aigents.com/al/?rss%20ai")
logger.info(r.status_code)
logger.info(r.headers)
data = r.text
logger.info(data)
logger.info("Done")

