class RegExParser(object):
    """Checks record types and parses them using masks"""
    regex_masks = {'SysCrash': "[a-z]{0,32}\s*tty[0-9]\s*(Mon|Tue|Wed|Thu|Fri|Sat|Sun) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} 2(0|1)[0-9]{2} - down\s*\([0-9]{0,2}\+?[0-9]{0,2}:[0-9]{2}\)\s*\B:0\.?0?\b",
                   'SysShutDown': "[a-z]{0,32}\s*system down\s*(Mon|Tue|Wed|Thu|Fri|Sat|Sun) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} 2(0|1)[0-9]{2} - (Mon|Tue|Wed|Thu|Fri|Sat|Sun) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} 2(0|1)[0-9]{2}\s*\([0-9]{0,2}\+?[0-9]{0,2}:[0-9]{2}\)\s*2.6.32-([0-9]{0,3}.){3}el[0-9].i[0-9]{1,3}",
                   'SysReboot': "[a-z]{0,32}\s*system boot\s*(Mon|Tue|Wed|Thu|Fri|Sat|Sun) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} 2(0|1)[0-9]{2} - (Mon|Tue|Wed|Thu|Fri|Sat|Sun) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} 2(0|1)[0-9]{2}\s*\([0-9]{0,2}\+?[0-9]{0,2}:[0-9]{2}\)\s*2.6.32-([0-9]{0,3}.){3}el[0-9].i[0-9]{1,3}",
                   'SysRunLvlChange': "runlevel \(to lvl [0-9]\)\s*(Mon|Tue|Wed|Thu|Fri|Sat|Sun) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} 2(0|1)[0-9]{2} - (Mon|Tue|Wed|Thu|Fri|Sat|Sun) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} 2(0|1)[0-9]{2}\s*\([0-9]{0,2}\+?[0-9]{0,2}:[0-9]{2}\)\s*2.6.32-([0-9]{0,3}.){3}el[0-9].i[0-9]{1,3}",
                   'LgnKnwnCrash': "[a-z]{0,32}\s*(pts\/)[0-9]+\s*(Mon|Tue|Wed|Thu|Fri|Sat|Sun) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} 2(0|1)[0-9]{2} - down\s*\([0-9]{0,2}\+?[0-9]{0,2}:[0-9]{2}\)\s*(((([0-9]|[a-zA-Z])+)+(.|-)?)+([0-9]|[a-zA-Z])*)",
                   'LgnKnwnComplete': "[a-z]{0,32}\s*(pts\/)[0-9]+\s*(Mon|Tue|Wed|Thu|Fri|Sat|Sun) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} 2(0|1)[0-9]{2} - (Mon|Tue|Wed|Thu|Fri|Sat|Sun) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} 2(0|1)[0-9]{2}\s*\([0-9]{0,2}\+?[0-9]{0,2}:[0-9]{2}\)\s*(((([0-9]|[a-zA-Z])+)+(.|-)?)+([0-9]|[a-zA-Z])*)",
                   'LgnKnwnIncomplete': "[a-z]{0,32}\s*(pts\/)[0-9]+\s*(Mon|Tue|Wed|Thu|Fri|Sat|Sun) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} 2(0|1)[0-9]{2} - (Mon|Tue|Wed|Thu|Fri|Sat|Sun) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} 2(0|1)[0-9]{2}\s*\([0-9]{0,2}\+?[0-9]{0,2}:[0-9]{2}\)$",
                   'LgnUnknwnComplete': "[a-z]{0,32}\s*(pts\/)[0-9]+\s*(Mon|Tue|Wed|Thu|Fri|Sat|Sun) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} 2(0|1)[0-9]{2}\s*still logged in\s*(((([0-9]|[a-zA-Z])+)+(.|-)?)+([0-9]|[a-zA-Z])*)"}

    def checkRecord(record):
        
        #return record type
        pass

    def parseRecord(record, record_type):

        #return [parsed_record, flags, flagged_rows]
        pass


