from mycroft import MycroftSkill, intent_file_handler
import gkeepapi
from gkeepapi.node import Note, List

class Test(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self._keep = gkeepapi.Keep()

    def initialize(self):
        email = self.settings.get('email')
        password = self.settings.get('password')

        self.log.info("Initialize called")

        if email is None or password is None:
            self.log.info("No username or password. Can't log in")
        else:
            self.log.info("Logging in to Keep")
            self._keep.login(email, password)
            self.log.info("Log in complete")
            self._keep.sync()

    @intent_file_handler('CreateList.intent')
    def handle_test(self, message):
        self.log.info("Attempting to create a list")
        list_name = message.data.get('listname')
        if list_name is None:
            list_name = self.get_response('get_list_name')
            if list_name is not None:
                self.make_list(list_name)
        else:
            self.make_list(list_name)

    @intent_file_handler('add_to_list.intent')
    def handle_add_to_list(self, message):
        list_name = message.data.get('list')
        list_node = self.find_list(list_name)

        if list_node is None:
            self.speak_dialog('list_not_found', {'list': list_name})
            return

        item = message.data.get('item')
        list_node.add(item, False, gkeepapi.node.NewListItemPlacementValue.Bottom)
        self.log.info(list_node)
        self._keep.sync()

    def find_list(self, list_name):
        gnotes = self._keep.all()
        foundNote = None
        for node in gnotes:
            if node.title.lower() == list_name.lower() or node.title.lower() == list_name.lower() + " list":
                if isinstance(node, Note):
                    foundNote = node
                    continue
                return node

        if foundNote is not None:
            self.log.info("Found node, but it's not a list: " + foundNote.title)

        return None


    @intent_file_handler('do_tests.intent')
    def handle_do_tests(self, message):
        gnotes = self._keep.all()
        for node in gnotes:
            self.log.info("Found node: " + node.title)

    def make_list(self, list_name):
        note = self._keep.createNote(list_name, '')
        note.pinned = True
        note.color = gkeepapi.node.ColorValue.Red

        self._keep.sync()
        self.speak_dialog('ListCreated')

    def stop(self):
        pass

def create_skill():

    return Test()

