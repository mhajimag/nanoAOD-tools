import sys
from Utilities.General.cmssw_das_client import get_data as das_query
import os

def produceJobs(dataset, totalN, jobN):
    query = das_query("file dataset=%s/NANOAODSIM"%dataset)
    if not 'data' in query:
        raise Exception('Your das query has not worked properly - check your proxy is valid')

    files = [each['file'][0] for each in query['data']]

    if totalN==None:
        totalN = sum([f['nevents'] for f in files])

    jobs = []

    end_request = False
    counter = 0 #count number of events assigned to jobs so far

    for f in files:
        if not end_request:
            fileN = f['nevents']
            for start in range(0, fileN, jobN):
                nEvents_to_end_request = totalN - counter
                nEvents_to_end_file = fileN - start
                possible_job_sizes = [nEvents_to_end_request, nEvents_to_end_file, jobN]

                job_size = min(possible_job_sizes)

                job = {"name": f['name'],
                        "start": start,
                        "jobsize": job_size}
                jobs.append(job)
                
                counter += job_size
                if counter==totalN:
                    end_request = True
                    break
        else:
            break
    return jobs

def printJobs(jobs):
    for job in jobs:
        print(job['name'][-20:], job['start'], job['jobsize'])

def runJobs(jobs, rw_path, outDir):
    with open("temp.sub", "w") as f:
        f.write("executable = crab/run.sh \n")
        f.write("arguments = $(outDir) root://xrootd-cms.infn.it/$(in_file) $(rw_path) $(start) $(entries) $(Proxy_path) $(ClusterId) $(ProcId) \n")
        f.write("output = crab/output/rw.$(ClusterId).$(ProcId).out \n")
        f.write("error = crab/error/rw.$(ClusterId).$(ProcId).err \n")
        f.write("log = crab/log/rw.$(ClusterId).log \n")
        f.write("Proxy_path = /afs/cern.ch/user/m/mknight/private/x509up \n")
        f.write("outDir = %s \n"%outDir)
        f.write("rw_path = %s \n\n"%rw_path)

        for job in jobs:
            f.write("in_file = %s \n"%job['name'])
            f.write("start = %s \n"%job['start'])
            f.write("entries = %s \n"%job['jobsize'])
            f.write("queue \n\n")
    
    os.system("condor_submit temp.sub")

if __name__=="__main__":
    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options] dataset rw_path")
    parser.add_option("-o", dest="outDir", type="string", default="batchSkims")
    parser.add_option("-N", "--max-entries", dest="totalN", type="long", default=None)
    parser.add_option("-S", "--events-job", dest="jobN", type="long", default=1000)

    (options, args) = parser.parse_args()
    dataset = args[0]
    rw_path = args[1]

    jobs = produceJobs(dataset, options.totalN, options.jobN)
    printJobs(jobs)
    if raw_input("Proceed?") == "y":
        runJobs(jobs, rw_path, options.outDir)

    

