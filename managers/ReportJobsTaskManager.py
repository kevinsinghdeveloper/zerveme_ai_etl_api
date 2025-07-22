from abstractions.IETLServiceManager import IETLServiceManager


class ReportJobTaskManager(IETLServiceManager):
    def __init__(self, etl_config: dict):
        super().__init__(etl_config)



'''
0. Read in dict of all availabable report jobs -- Reports will be managed with this ETL service -- so IDs will need to be mapped here -- db reference the python file?
1. Will be fed job parameters from the .NET worker
2. Locate job configuration
3. Trigger the job ETL service

'''

'''
Jobs

1. We will have to store reports as code
2. We will have a json which points to the config code? Maybe like a mapping? -- 
3. Annoying to maintain since .NET references a report and the ETL references a report in a different location [SOLVE] db reference the python file?????

'''