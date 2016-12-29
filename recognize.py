import tensorflow as tf

from config import config


class Recognizer:
    MODEL_PATH = config['TENSORFLOW_MODEL_PATH']
    LABELS_PATH = '{model_path}/retrained_labels.txt'.format(model_path=MODEL_PATH)
    TRAINED_GRAPH_PATH = '{model_path}/retrained_graph.pb'.format(model_path=MODEL_PATH)

    def __init__(self):
        self.session = tf.Session()
        self.label_lines = [line.rstrip() for line in tf.gfile.GFile(self.LABELS_PATH)]

        with tf.gfile.FastGFile(self.TRAINED_GRAPH_PATH, 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            _ = tf.import_graph_def(graph_def, name='')

        self.softmax_tensor = self.session.graph.get_tensor_by_name('final_result:0')

    def recognize(self, image_data):
        predictions = self.session.run(self.softmax_tensor,
                                       {'DecodeJpeg/contents:0': image_data})
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
        return {self.label_lines[node_id]: int(predictions[0][node_id] * 100) for node_id in top_k}
