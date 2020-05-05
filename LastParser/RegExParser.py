import re
from Records.LgnKnwnCompleteRecord import LgnKnwnCompleteRecord
from Records.LgnUnknwnCompleteRecord import LgnUnknwnCompleteRecord
from Records.LgnKnwnIncompleteRecord import LgnKnwnIncompleteRecord

class RegExParser(object):
    """Checks record types and parses them using masks"""
    regex_masks = {'SysCrash': "[a-z]{0,32}\s*tty[0-9]\s*(Mon|Tue|Wed|Thu|Fri|Sat|Sun) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} 2(0|1)[0-9]{2} - down\s*\([0-9]{0,2}\+?[0-9]{0,2}:[0-9]{2}\)\s*\B:0\.?0?\b",
                   'SysShutDown': "[a-z]{0,32}\s*system down\s*(Mon|Tue|Wed|Thu|Fri|Sat|Sun) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} 2(0|1)[0-9]{2} - (Mon|Tue|Wed|Thu|Fri|Sat|Sun) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} 2(0|1)[0-9]{2}\s*\([0-9]{0,2}\+?[0-9]{0,2}:[0-9]{2}\)\s*2.6.32-([0-9]{0,3}.){3}el[0-9].i[0-9]{1,3}",
                   'SysReboot': "[a-z]{0,32}\s*system boot\s*(Mon|Tue|Wed|Thu|Fri|Sat|Sun) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} 2(0|1)[0-9]{2} - (Mon|Tue|Wed|Thu|Fri|Sat|Sun) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} 2(0|1)[0-9]{2}\s*\([0-9]{0,2}\+?[0-9]{0,2}:[0-9]{2}\)\s*2.6.32-([0-9]{0,3}.){3}el[0-9].i[0-9]{1,3}",
                   'SysRunLvlChange': "runlevel \(to lvl [0-9]\)\s*(Mon|Tue|Wed|Thu|Fri|Sat|Sun) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} 2(0|1)[0-9]{2} - (Mon|Tue|Wed|Thu|Fri|Sat|Sun) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} 2(0|1)[0-9]{2}\s*\([0-9]{0,2}\+?[0-9]{0,2}:[0-9]{2}\)\s*2.6.32-([0-9]{0,3}.){3}el[0-9].i[0-9]{1,3}",
                   'LgnKnwnCrash': "[a-z]{0,32}\s*(pts\/)[0-9]+\s*(Mon|Tue|Wed|Thu|Fri|Sat|Sun) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} 2(0|1)[0-9]{2} - down\s*\([0-9]{0,2}\+?[0-9]{0,2}:[0-9]{2}\)\s*(((([0-9]|[a-zA-Z])+)+(.|-)?)+([0-9]|[a-zA-Z])*)",
                   'LgnKnwnComplete': "[a-z]{0,32}\s*(pts\/)[0-9]+\s*(Mon|Tue|Wed|Thu|Fri|Sat|Sun) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} 2(0|1)[0-9]{2} - (Mon|Tue|Wed|Thu|Fri|Sat|Sun) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} 2(0|1)[0-9]{2}\s*\([0-9]{0,2}\+?[0-9]{0,2}:[0-9]{2}\)\s*(((([0-9]|[a-zA-Z])+)+(.|-)?)+([0-9]|[a-zA-Z])*)",
                   'LgnUnknwnComplete': "[a-z]{0,32}\s*(pts\/)[0-9]+\s*(Mon|Tue|Wed|Thu|Fri|Sat|Sun) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} 2(0|1)[0-9]{2} - (Mon|Tue|Wed|Thu|Fri|Sat|Sun) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} 2(0|1)[0-9]{2}\s*\([0-9]{0,2}\+?[0-9]{0,2}:[0-9]{2}\)$",
                   'LgnKnwnIncomplete': "[a-z]{0,32}\s*(pts\/)[0-9]+\s*(Mon|Tue|Wed|Thu|Fri|Sat|Sun) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} 2(0|1)[0-9]{2}\s*still logged in\s*(((([0-9]|[a-zA-Z])+)+(.|-)?)+([0-9]|[a-zA-Z])*)"}


    #Checks record against mask, returning the corresponding record type if a match, else -1
    @staticmethod
    def checkRecord(record):
        for mask in RegExParser.regex_masks:
            pattern = re.compile(RegExParser.regex_masks[mask])
            if pattern.match(record):
                return mask

        return -1
    
    @staticmethod
    def parseRecord(record, record_type):
        return RegExParser.record_parsers[record_type](record)

    @staticmethod
    def checkAndParseRecords(records):
        parsed_records = []

        for record in records:
            type = RegExParser.checkRecord(record)
            if type != -1:
                parsed_record = RegExParser.parseRecord(record, type)
                parsed_records.append(parsed_record)

        return parsed_records

    def parseLgnKnwnIncomplete(record):
        parsedRecord = {'incomplete': {'user': '', 'pts-terminal': '', 'start-session': {'date': {'year': '', 'month': '', 'day': '', 'weekday': ''}, 'time': {'hr': '', 'mn': '', 'sec': ''}}, 'remote-terminal': ''}}
        record_arr = record.split()

        parsedRecord['incomplete']['user'] = record_arr[0]
        parsedRecord['incomplete']['pts-terminal'] = record_arr[1].split('/')[1]
        parsedRecord['incomplete']['start-session']['date']['year'] = record_arr[6]
        parsedRecord['incomplete']['start-session']['date']['month'] = record_arr[3]
        parsedRecord['incomplete']['start-session']['date']['day'] = record_arr[4]
        parsedRecord['incomplete']['start-session']['date']['weekday'] = record_arr[2]
        parsedRecord['incomplete']['start-session']['time']['hr'] = record_arr[5].split(':')[0]
        parsedRecord['incomplete']['start-session']['time']['mn'] = record_arr[5].split(':')[1]
        parsedRecord['incomplete']['start-session']['time']['sec'] = record_arr[5].split(':')[2]
        parsedRecord['incomplete']['remote-terminal'] = record_arr[10]


        return LgnKnwnIncompleteRecord(parsedRecord)

    
    def parseLgnKnwnComplete(record):
        parsedRecord = {'complete': {'user': '', 'pts-terminal': '', 'start-session': {'date': {'year': '', 'month': '', 'day': '', 'weekday': ''}, 'time': {'hr': '', 'mn': '', 'sec': ''}}, 'end-session': {'date': {'year': '', 'month': '', 'day': '', 'weekday': ''}, 'time': {'hr': '', 'mn': '', 'sec': ''}}, 'duration': {}, 'remote-terminal': ''}}
        record_arr = record.split()

        parsedRecord['complete']['user'] = record_arr[0]
        parsedRecord['complete']['pts-terminal'] = record_arr[1].split('/')[1]
        parsedRecord['complete']['start-session']['date']['year'] = record_arr[6]
        parsedRecord['complete']['start-session']['date']['month'] = record_arr[3]
        parsedRecord['complete']['start-session']['date']['day'] = record_arr[4]
        parsedRecord['complete']['start-session']['date']['weekday'] = record_arr[2]
        parsedRecord['complete']['start-session']['time']['hr'] = record_arr[5].split(':')[0]
        parsedRecord['complete']['start-session']['time']['mn'] = record_arr[5].split(':')[1]
        parsedRecord['complete']['start-session']['time']['sec'] = record_arr[5].split(':')[2]
        parsedRecord['complete']['end-session']['date']['year'] = record_arr[12]
        parsedRecord['complete']['end-session']['date']['month'] = record_arr[9]
        parsedRecord['complete']['end-session']['date']['day'] = record_arr[10]
        parsedRecord['complete']['end-session']['date']['weekday'] = record_arr[8]
        parsedRecord['complete']['end-session']['time']['hr'] = record_arr[11].split(':')[0]
        parsedRecord['complete']['end-session']['time']['mn'] = record_arr[11].split(':')[1]
        parsedRecord['complete']['end-session']['time']['sec'] = record_arr[11].split(':')[2]
        parsedRecord['complete']['remote-terminal'] = record_arr[10]
        duration = record_arr[13][1:-1].split(':')
        if duration[0] != '00':
            parsedRecord['complete']['duration']['hr'] = duration[0]
        parsedRecord['complete']['duration']['mn'] = duration[1]


        return LgnKnwnCompleteRecord(parsedRecord)

    def parseLgnUnknwnComplete(record):
        parsedRecord = {'complete': {'user': '', 'pts-terminal': '', 'start-session': {'date': {'year': '', 'month': '', 'day': '', 'weekday': ''}, 'time': {'hr': '', 'mn': '', 'sec': ''}}, 'end-session': {'date': {'year': '', 'month': '', 'day': '', 'weekday': ''}, 'time': {'hr': '', 'mn': '', 'sec': ''}}, 'duration': {}}}
        record_arr = record.split()

        parsedRecord['complete']['user'] = record_arr[0]
        parsedRecord['complete']['pts-terminal'] = record_arr[1].split('/')[1]
        parsedRecord['complete']['start-session']['date']['year'] = record_arr[6]
        parsedRecord['complete']['start-session']['date']['month'] = record_arr[3]
        parsedRecord['complete']['start-session']['date']['day'] = record_arr[4]
        parsedRecord['complete']['start-session']['date']['weekday'] = record_arr[2]
        parsedRecord['complete']['start-session']['time']['hr'] = record_arr[5].split(':')[0]
        parsedRecord['complete']['start-session']['time']['mn'] = record_arr[5].split(':')[1]
        parsedRecord['complete']['start-session']['time']['sec'] = record_arr[5].split(':')[2]
        parsedRecord['complete']['end-session']['date']['year'] = record_arr[12]
        parsedRecord['complete']['end-session']['date']['month'] = record_arr[9]
        parsedRecord['complete']['end-session']['date']['day'] = record_arr[10]
        parsedRecord['complete']['end-session']['date']['weekday'] = record_arr[8]
        parsedRecord['complete']['end-session']['time']['hr'] = record_arr[11].split(':')[0]
        parsedRecord['complete']['end-session']['time']['mn'] = record_arr[11].split(':')[1]
        parsedRecord['complete']['end-session']['time']['sec'] = record_arr[11].split(':')[2]
        duration = record_arr[13][1:-1].split(':')
        if duration[0] != '00':
            parsedRecord['complete']['duration']['hr'] = duration[0]
        parsedRecord['complete']['duration']['mn'] = duration[1]


        return LgnUnknwnCompleteRecord(parsedRecord)
    
    
    
    #Dispatch table for record specific parsers
    record_parsers = {'LgnKnwnComplete': parseLgnKnwnComplete, 'LgnUnknwnComplete': parseLgnUnknwnComplete, 'LgnKnwnIncomplete': parseLgnKnwnIncomplete}
