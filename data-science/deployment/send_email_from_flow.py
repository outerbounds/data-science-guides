
import os
from metaflow import FlowSpec, step, current, card, Flow
from metaflow.cards import Markdown, Image, get_cards
import requests
#highlight-next-line
from emailer import send_email

CAT = 'https://upload.wikimedia.org' + \
      '/wikipedia/commons/b/b9/CyprusShorthair.jpg'

class EmailCardFlow(FlowSpec):

    @card(type='blank')
    @step
    def start(self):
        resp = requests.get(CAT, 
            headers = {'user-agent': 'metaflow-example'})
        current.card.append(Markdown("# Meow mail 🐈"))
        current.card.append(Image(resp.content))
        self.next(self.end)

    @step
    def end(self):
        send_email(
            'your-email@company.com', # put your email
            'elon@tesla.com',   # put receiver's email
            'hi Elon',              # put message body
            #highlight-start
            get_cards(
                Flow(current.flow_name)[
                     current.run_id]['start'].task)[0]
            .get(),
            #highlight-end
            os.environ.get('SENDGRID_API_KEY')
        )

if __name__ == '__main__':
    EmailCardFlow()
