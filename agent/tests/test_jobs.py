import logging

from sn_agent import ontology
from sn_agent.job.job_descriptor import JobDescriptor
from sn_agent.job.job_descriptor import init_test_jobs
from sn_agent.log import setup_logging
from sn_agent.ontology.service_descriptor import ServiceDescriptor

import tests

log = logging.getLogger(__name__)


# Tests

# Test performance of services - all of them
def test_jobs():
    print()
    setup_logging()
    init_test_jobs()
    test_jobs = JobDescriptor.get_test_jobs(tests.DOCUMENT_SUMMARIZER_ID)
    for job in test_jobs:
        service_id = 0
        if str(job) != "NO_JOB":
            service_id = tests.DOCUMENT_SUMMARIZER_ID

        job_parameters = {'input_type': 'file',
                          'input_url': 'http://test.com/inputs/test_input.txt',
                          'output_type': 'file_url_put',
                          'output_url': 'test_output.txt'}
        job_parameters_2 = {'input_type': 'file',
                            'input_url': 'http://test.com/inputs/test_input.txt',
                            'output_type': 'file_url_put',
                            'output_url': 'test_output.txt'}

        service_id = tests.DOCUMENT_SUMMARIZER_ID

        # Create a new job descriptor with four sets of parameters.
        job_list = [job_parameters, job_parameters, job_parameters, job_parameters]
        new_job = JobDescriptor(ServiceDescriptor(service_id), job_list)

        file_count = 0
        for job_item in new_job:
            if job_item['input_type'] == 'file':
                file_count += 1
            else:
                file_count = 0
        assert (file_count == 4)

        # Cover and test iteration and list item retrieval and length.
        new_job[0] = job_parameters_2
        assert (new_job[0] == job_parameters_2)
        job_count = len(new_job)
        del new_job[1]
        assert (len(new_job) == job_count - 1)

        # Test equality and string conversion functions.
        last_job = new_job
        assert (last_job == new_job)
        assert (str(last_job) == str(new_job))

        test_jobs.append(new_job)
        total_jobs = len(test_jobs)
        test_jobs[0] = new_job
        del test_jobs[total_jobs - 1]

        # Check the string conversion with no ServiceDescriptor...
        new_job = JobDescriptor(None, [job_parameters])
        assert (str(new_job) != "")
