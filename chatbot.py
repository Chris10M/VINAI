from watson_developer_cloud import ConversationV1
import json


class ChatBot():
    def __init__(self):
        self.conversation = ConversationV1(
            username='ec03d343-5f39-47c6-9c7c-e8e4a07fd4da',
            password='X6pP3CuMtOgk',
            version='2018-02-16'
        )
        self.workspace_id = '87f0e85e-af1c-4ea4-a5e9-9311aab29642'

    def run(self, input):
        response = self.conversation.message(
            workspace_id=self.workspace_id,
            input={
                'text': input
            }
        )

        return response['output']['text']


if __name__ == '__main__':
    chat_bot = ChatBot()
    print(chat_bot.run(input='hi'))