from mycroft import MycroftSkill, intent_file_handler
from Roomba980.roomba import password

class Test(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('test.intent')
    def handle_test(self, message):
        self.speak_dialog('test2')
        self.log.info("Test handler called")
        newpass = password()

    @intent_file_handler('TestColour.intent')
    def handle_test_colour(self, message):
        colour = message.data.get('colour')
        self.log.info("User asked about colour " + colour)

    def initialize(self):
        pass

    def stop(self):
        pass

    def converse(self, utterances, lang):
        self.log.info("Converse called with utterance " + utterances[0])
        return True
        # if utterances and self.voc_match(utterances[0], 'understood'):
        #     self.speak_dialog('great')
        #     return True
        # else:
        #     return False

def create_skill():

    return Test()

