import O365
import sys
import re
import logging
import argparse

log = O365.log

parser = argparse.ArgumentParser()
parser.add_argument("--userid", help="user id that will be used to fetch the secret", type=str, required=True)
parser.add_argument("--secretwords", help="the list of secret words", nargs='+', required=True)

def main():
    args = parser.parse_args()

    scanSection = ['Subject', 'Body.Content']
    restrictedWords = args.secretwords
    userid = args.userid
    log.debug("Redacting messages for {}".format(userid))

    auth = O365.creds.getCredentials(userid)

    inbox = O365.inbox.Inbox(auth)

    inbox.getMessages()

    for message in inbox.messages:
        modifiedSection = dict()
        for section in scanSection:
            msgSection = O365.message.getFromNestedDict(message.json, section)
            log.debug("Scanning '{}'...".format(section))
            for word in restrictedWords:
                regex = re.compile(re.escape(word), re.IGNORECASE|re.MULTILINE)
                if regex.findall(msgSection):
                    msgSection = regex.sub('*** REDACTED ***', msgSection)
                    modifiedSection[section] = msgSection
        if modifiedSection:
            message.updateMessage(modifiedSection)


if __name__ == "__main__":
    sys.exit(main())


