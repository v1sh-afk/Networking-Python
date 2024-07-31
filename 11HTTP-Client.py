from twisted.internet import reactor
from twisted.web.client import Agent
from twisted.web.client import readBody


def download_web_page(url):
    agent = Agent(reactor)

    def handle_response(response):
        d = readBody(response)  # Read the response body

        def process_body(body):
            print(body.decode())  # Process the received data
            reactor.stop()

        d.addCallback(process_body)
        return d

    def handle_error(error):
        print(f"An error occurred: {error}")  # Handle any errors
        reactor.stop()

    d = agent.request(b"GET", url.encode())  # Make an HTTP GET request
    d.addCallbacks(handle_response, handle_error)

    reactor.run()


if __name__ == "__main__":
    download_web_page("http://www.google.com/")
