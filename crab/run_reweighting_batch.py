import sys
from Utilities.General.cmssw_das_client import get_data as das_query

MAX_NEVENTS_PER_JOB = 500000

dataset = sys.argv[1]

query = das_query("file dataset=%s/NANOAODSIM"%dataset)
if not 'data' in query:
    raise Exception('Your das query has not worked properly - check your proxy is valid')

files = [each['file'][0] for each in query['data']]

try:
    total_nEvents = sys.argv[2]
except:
    total_nEvents = sum([f['nevents'] for f in files])

jobs = []

end_request = False
counter = 0 #count number of events assigned to jobs so far

for f in files:
    if not end_request:
        file_nEvents = f['nevents']
        for start in range(0, file_nEvents, MAX_NEVENTS_PER_JOB):
            nEvents_to_end_request = total_nEvents - counter
            nEvents_to_end_file = file_nEvents - start
            possible_job_sizes = [nEvents_to_end_request, nEvents_to_end_file, MAX_NEVENTS_PER_JOB]

            job_size = min(possible_job_sizes)

            job = {"name": f['name'],
                    "start": start,
                    "jobsize": job_size}
            jobs.append(job)
            
            counter += job_size
            if counter==total_nEvents:
                end_request = True
                break
    else:
        break

def printJobs(jobs):
    for job in jobs:
        print(job['name'][-20:], job['start'], job['end'])

printJobs(jobs)
