## Tensorflow image classificator


Http proxy for Tensorflow image classification model that can used as microservice in your app. Classification model that you will pass to container should be based on Google [inception](https://github.com/tensorflow/models/tree/master/inception) model. For more information you can read [docs](https://www.tensorflow.org/tutorials/image_recognition/) or watch [guide](https://www.youtube.com/watch?v=QfNvhPx5Px8).

### Run

```
docker run -d -v <graph-path>:/project/graph dimorinny/tensorflow-image-classificator
```

**Graph path should contains:**

* Protobuf graph file retrained_graph.pb
* Labels text file retrained_labels.txt

**Environment parameters:**

* **PROCESS\_POOL\_SIZE** - Count of worker processes for recognition (by default using count of cpus)
* **TENSORFLOW\_MODEL\_PATH** - Path to graph and text file with recognition labels (by default /project/graph)
* **PORT** - Http proxy port (80 by default)
