import re
from Records.LgnKnwnCompleteRecord import LgnKnwnCompleteRecord
from Records.LgnKnwnCrashRecord import LgnKnwnCrashRecord
from Records.LgnKnwnIncompleteRecord import LgnKnwnIncompleteRecord
from Records.LgnUnknwnCompleteRecord import LgnUnknwnCompleteRecord
from Records.SysCrashRecord import SysCrashRecord
from Records.SysRebootRecord import SysRebootRecord
from Records.SysRunLvlChangeRecord import SysRunLvlChangeRecord
from Records.SysShutDownRecord import SysShutDownRecord

class RegExParser(object):
    """Checks record types and parses them using masks"""
    regex_masks = {'SysCrash': "root\s*tty[0-9]\s*(Mon|Tue|Wed|Thu|Fri|Sat|Sun) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} 2(0|1)[0-9]{2} - down\s*\([0-9]{0,2}\+?[0-9]{0,2}:[0-9]{2}\)\s*:0\.?0?",
                   'SysShutDown': "[a-z]{0,32}\s*system down\s*(Mon|Tue|Wed|Thu|Fri|Sat|Sun) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} 2(0|1)[0-9]{2} - (Mon|Tue|Wed|Thu|Fri|Sat|Sun) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} 2(0|1)[0-9]{2}\s*\([0-9]{0,2}\+?[0-9]{0,2}:[0-9]{2}\)\s*2.6.32-([0-9]{0,3}.){3}el[0-9].i[0-9]{1,3}",
                   'SysReboot': "reboot\s*[a-z\s]{0,32}\s*(Mon|Tue|Wed|Thu|Fri|Sat|Sun) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} 2(0|1)[0-9]{2} - (Mon|Tue|Wed|Thu|Fri|Sat|Sun) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} 2(0|1)[0-9]{2}\s*\([0-9]{0,2}\+?[0-9]{0,2}:[0-9]{2}\)\s*2.6.32-([0-9]{0,3}.){3}el[0-9].i[0-9]{1,3}",
                   'SysRunLvlChange': "runlevel \(to lvl [0-9]\)\s*(Mon|Tue|Wed|Thu|Fri|Sat|Sun) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} 2(0|1)[0-9]{2} - (Mon|Tue|Wed|Thu|Fri|Sat|Sun) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} 2(0|1)[0-9]{2}\s*\([0-9]{0,2}\+?[0-9]{0,2}:[0-9]{2}\)\s*2.6.32-([0-9]{0,3}.){3}el[0-9].i[0-9]{1,3}",
                   'LgnKnwnCrash': "[a-z0-9]{0,32}\s*(pts\/)[0-9]+\s*(Mon|Tue|Wed|Thu|Fri|Sat|Sun) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} 2(0|1)[0-9]{2} - down\s*\([0-9]{0,2}\+?[0-9]{0,2}:[0-9]{2}\)\s*(((([0-9]|[a-zA-Z])+)+(.|-)?)+([0-9]|[a-zA-Z])*)",
                   'LgnKnwnComplete': "[a-z0-9]{0,32}\s*(pts\/)[0-9]+\s*(Mon|Tue|Wed|Thu|Fri|Sat|Sun) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} 2(0|1)[0-9]{2} - (Mon|Tue|Wed|Thu|Fri|Sat|Sun) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} 2(0|1)[0-9]{2}\s*\([0-9]{0,2}\+?[0-9]{0,2}:[0-9]{2}\)\s*(((([0-9]|[a-zA-Z])+)+(.|-)?)+([0-9]|[a-zA-Z])*)",
                   'LgnUnknwnComplete': "[a-z0-9]{0,32}\s*(pts\/)[0-9]+\s*(Mon|Tue|Wed|Thu|Fri|Sat|Sun) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} 2(0|1)[0-9]{2} - (Mon|Tue|Wed|Thu|Fri|Sat|Sun) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} 2(0|1)[0-9]{2}\s*\([0-9]{0,2}\+?[0-9]{0,2}:[0-9]{2}\)$",
                   'LgnKnwnIncomplete': "[a-z0-9]{0,32}\s*(pts\/)[0-9]+\s*(Mon|Tue|Wed|Thu|Fri|Sat|Sun) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} 2(0|1)[0-9]{2}\s*still logged in\s*(((([0-9]|[a-zA-Z])+)+(.|-)?)+([0-9]|[a-zA-Z])*)"}


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
        unparsed_records = []
        errors = []

        for record in range(0, len(records)):
            type = RegExParser.checkRecord(records[record])
            if type != -1:
                try:
                    parsed_record = RegExParser.parseRecord(records[record], type)
                    parsed_records.append(parsed_record)
                except:
                    unparsed_records.append(records[record] + '\n')
                    errors.append("Failed to parse record #{0}\n".format(record))
            else:
                unparsed_records.append(records[record] + '\n')
                errors.append("Failed to identify type for record #{0}\n".format(record))

        return [parsed_records, unparsed_records, errors]

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
    
    def parseLgnKnwnCrash(record):
        parsedRecord = {'complete': {'user': '', 'pts-terminal': '', 'start-session': {'date': {'year': '', 'month': '', 'day': '', 'weekday': ''}, 'time': {'hr': '', 'mn': '', 'sec': ''}}, 'end-session': {}, 'duration': {}, 'remote-terminal': ''}}
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
        parsedRecord['complete']['remote-terminal'] = record_arr[10]
        duration = record_arr[9][1:-1].split(':')
        if duration[0] != '00':
            parsedRecord['complete']['duration']['hr'] = duration[0]
        parsedRecord['complete']['duration']['mn'] = duration[1]


        return LgnKnwnCrashRecord(parsedRecord)

    def parseSysCrash(record):
        parsedRecord = {'system-crash': {'user': '', 'physical-terminal': '', 'start-session': {'date': {'year': '', 'month': '', 'day': '', 'weekday': ''}, 'time': {'hr': '', 'mn': '', 'sec': ''}}, 'end-session': {}, 'duration': {}, 'user-terminal': ''}}
        record_arr = record.split()

        parsedRecord['system-crash']['user'] = record_arr[0]
        parsedRecord['system-crash']['physical-terminal'] = record_arr[1]
        parsedRecord['system-crash']['start-session']['date']['year'] = record_arr[6]
        parsedRecord['system-crash']['start-session']['date']['month'] = record_arr[3]
        parsedRecord['system-crash']['start-session']['date']['day'] = record_arr[4]
        parsedRecord['system-crash']['start-session']['date']['weekday'] = record_arr[2]
        parsedRecord['system-crash']['start-session']['time']['hr'] = record_arr[5].split(':')[0]
        parsedRecord['system-crash']['start-session']['time']['mn'] = record_arr[5].split(':')[1]
        parsedRecord['system-crash']['start-session']['time']['sec'] = record_arr[5].split(':')[2]
        parsedRecord['system-crash']['user-terminal'] = record_arr[10]
        duration = record_arr[9][1:-1].split(':')
        if duration[0] != '00':
            parsedRecord['system-crash']['duration']['hr'] = duration[0]
        parsedRecord['system-crash']['duration']['mn'] = duration[1]


        return SysCrashRecord(parsedRecord)

    def parseSysReboot(record):
        parsedRecord = {'system-reboot': {'start-session': {'date': {'year': '', 'month': '', 'day': '', 'weekday': ''}, 'time': {'hr': '', 'mn': '', 'sec': ''}}, 'end-session': {'date': {'year': '', 'month': '', 'day': '', 'weekday': ''}, 'time': {'hr': '', 'mn': '', 'sec': ''}}, 'duration': {}, 'serial-number': ''}}
        record_arr = record.split()


        parsedRecord['system-reboot']['start-session']['date']['year'] = record_arr[7]
        parsedRecord['system-reboot']['start-session']['date']['month'] = record_arr[4]
        parsedRecord['system-reboot']['start-session']['date']['day'] = record_arr[5]
        parsedRecord['system-reboot']['start-session']['date']['weekday'] = record_arr[3]
        parsedRecord['system-reboot']['start-session']['time']['hr'] = record_arr[6].split(':')[0]
        parsedRecord['system-reboot']['start-session']['time']['mn'] = record_arr[6].split(':')[1]
        parsedRecord['system-reboot']['start-session']['time']['sec'] = record_arr[6].split(':')[2]
        parsedRecord['system-reboot']['end-session']['date']['year'] = record_arr[13]
        parsedRecord['system-reboot']['end-session']['date']['month'] = record_arr[10]
        parsedRecord['system-reboot']['end-session']['date']['day'] = record_arr[11]
        parsedRecord['system-reboot']['end-session']['date']['weekday'] = record_arr[9]
        parsedRecord['system-reboot']['end-session']['time']['hr'] = record_arr[12].split(':')[0]
        parsedRecord['system-reboot']['end-session']['time']['mn'] = record_arr[12].split(':')[1]
        parsedRecord['system-reboot']['end-session']['time']['sec'] = record_arr[12].split(':')[2]
        parsedRecord['system-reboot']['serial-number'] = record_arr[15]
        duration = record_arr[14][1:-1].split(':')
        if duration[0] != '00':
            parsedRecord['system-reboot']['duration']['hr'] = duration[0]
        parsedRecord['system-reboot']['duration']['mn'] = duration[1]


        return SysRebootRecord(parsedRecord)

    def parseSysShutDown(record):
        parsedRecord = {'system-shutdown': {'start-session': {'date': {'year': '', 'month': '', 'day': '', 'weekday': ''}, 'time': {'hr': '', 'mn': '', 'sec': ''}}, 'end-session': {'date': {'year': '', 'month': '', 'day': '', 'weekday': ''}, 'time': {'hr': '', 'mn': '', 'sec': ''}}, 'duration': {}, 'serial-number': ''}}
        record_arr = record.split()


        parsedRecord['system-shutdown']['start-session']['date']['year'] = record_arr[7]
        parsedRecord['system-shutdown']['start-session']['date']['month'] = record_arr[4]
        parsedRecord['system-shutdown']['start-session']['date']['day'] = record_arr[5]
        parsedRecord['system-shutdown']['start-session']['date']['weekday'] = record_arr[3]
        parsedRecord['system-shutdown']['start-session']['time']['hr'] = record_arr[6].split(':')[0]
        parsedRecord['system-shutdown']['start-session']['time']['mn'] = record_arr[6].split(':')[1]
        parsedRecord['system-shutdown']['start-session']['time']['sec'] = record_arr[6].split(':')[2]
        parsedRecord['system-shutdown']['end-session']['date']['year'] = record_arr[13]
        parsedRecord['system-shutdown']['end-session']['date']['month'] = record_arr[10]
        parsedRecord['system-shutdown']['end-session']['date']['day'] = record_arr[11]
        parsedRecord['system-shutdown']['end-session']['date']['weekday'] = record_arr[9]
        parsedRecord['system-shutdown']['end-session']['time']['hr'] = record_arr[12].split(':')[0]
        parsedRecord['system-shutdown']['end-session']['time']['mn'] = record_arr[12].split(':')[1]
        parsedRecord['system-shutdown']['end-session']['time']['sec'] = record_arr[12].split(':')[2]
        parsedRecord['system-shutdown']['serial-number'] = record_arr[15]
        duration = record_arr[14][1:-1].split(':')
        if duration[0] != '00':
            parsedRecord['system-shutdown']['duration']['hr'] = duration[0]
        parsedRecord['system-shutdown']['duration']['mn'] = duration[1]


        return SysShutDownRecord(parsedRecord)

    def parseSysRunLvlChange(record):
        parsedRecord = {'runlevel-change': {'level': '', 'start-session': {'date': {'year': '', 'month': '', 'day': '', 'weekday': ''}, 'time': {'hr': '', 'mn': '', 'sec': ''}}, 'end-session': {'date': {'year': '', 'month': '', 'day': '', 'weekday': ''}, 'time': {'hr': '', 'mn': '', 'sec': ''}}, 'duration': {}, 'serial-number': ''}}
        record_arr = record.split()

        parsedRecord['runlevel-change']['level'] = record_arr[3][:-1]
        parsedRecord['runlevel-change']['start-session']['date']['year'] = record_arr[8]
        parsedRecord['runlevel-change']['start-session']['date']['month'] = record_arr[5]
        parsedRecord['runlevel-change']['start-session']['date']['day'] = record_arr[6]
        parsedRecord['runlevel-change']['start-session']['date']['weekday'] = record_arr[4]
        parsedRecord['runlevel-change']['start-session']['time']['hr'] = record_arr[7].split(':')[0]
        parsedRecord['runlevel-change']['start-session']['time']['mn'] = record_arr[7].split(':')[1]
        parsedRecord['runlevel-change']['start-session']['time']['sec'] = record_arr[7].split(':')[2]
        parsedRecord['runlevel-change']['end-session']['date']['year'] = record_arr[14]
        parsedRecord['runlevel-change']['end-session']['date']['month'] = record_arr[11]
        parsedRecord['runlevel-change']['end-session']['date']['day'] = record_arr[12]
        parsedRecord['runlevel-change']['end-session']['date']['weekday'] = record_arr[10]
        parsedRecord['runlevel-change']['end-session']['time']['hr'] = record_arr[13].split(':')[0]
        parsedRecord['runlevel-change']['end-session']['time']['mn'] = record_arr[13].split(':')[1]
        parsedRecord['runlevel-change']['end-session']['time']['sec'] = record_arr[13].split(':')[2]
        parsedRecord['runlevel-change']['serial-number'] = record_arr[16]
        duration = record_arr[15][1:-1].split(':')
        if duration[0] != '00':
            parsedRecord['runlevel-change']['duration']['hr'] = duration[0]
        parsedRecord['runlevel-change']['duration']['mn'] = duration[1]


        return SysRunLvlChangeRecord(parsedRecord)
    



    #Dispatch table for record specific parsers
    record_parsers = {'LgnKnwnComplete': parseLgnKnwnComplete, 'LgnUnknwnComplete': parseLgnUnknwnComplete, 'LgnKnwnIncomplete': parseLgnKnwnIncomplete, 'LgnKnwnCrash': parseLgnKnwnCrash,
                      'SysCrash': parseSysCrash, 'SysReboot': parseSysReboot, 'SysShutDown': parseSysShutDown, 'SysRunLvlChange': parseSysRunLvlChange}
