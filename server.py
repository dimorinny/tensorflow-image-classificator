from multiprocessing.pool import Pool

from tornado import gen
from tornado import httpclient
from tornado import ioloop
from tornado import web
from tornado.escape import json_encode

from config import config
from recognize import Recognizer
from response import success, error
from util.multiprocessing import exception_handle_task

recognizer = None
pool = None
http_client = httpclient.AsyncHTTPClient()


def init():
    global recognizer
    print('Initializing recognizer...')
    recognizer = Recognizer()


@exception_handle_task
def recognize(image_data):
    return recognizer.recognize(image_data)


# noinspection PyAbstractClass,PyMethodMayBeStatic
class RecognizeHandler(web.RequestHandler):
    async def load_image(self, url):
        request = httpclient.HTTPRequest(url)
        result = await http_client.fetch(request)
        return result

    async def recognize(self, image_data):
        result = await gen.Task(
            lambda callback: pool.apply_async(
                func=recognize,
                args=(image_data,),
                callback=callback
            )
        )
        return result.get_or_die()

    async def get(self):
        image_url = self.get_argument('image')
        image_response = await self.load_image(image_url)
        recognition_result = await self.recognize(image_response.body)
        self.write_json(success(recognition_result))

    async def post(self):
        image = self.request.files['image'][0]
        recognition_result = await self.recognize(image.body)
        self.write_json(success(recognition_result))

    def write_error(self, status_code, **kwargs):
        self.write_json(error())

    def write_json(self, data):
        self.add_header('Content-Type', 'application/json')
        self.write(json_encode(data))
        self.finish()


def application():
    return web.Application([
        (r"/api/v1/recognize", RecognizeHandler),
    ])


def main():
    global pool

    pool = Pool(
        processes=config['PROCESS_POOL_SIZE'],
        initializer=init
    )

    app = application()
    app.listen(config['PORT'])

    print('Listening port {port}...'.format(port=config['PORT']))

    ioloop.IOLoop.current().start()
    pool.close()


if __name__ == '__main__':
    main()
