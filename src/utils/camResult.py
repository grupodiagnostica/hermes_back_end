import numpy as np
import scipy as sp

def cam_result(features, results, gap_weights) -> tuple:
  classes = ['PNEUMONIA', 'COVID19', 'TUBERCULOSE', 'NORMAL']
  def softmax(x: list):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()

  features_for_img = features[0]
  print(softmax(results[0]))
  prediction = [classes[np.argmax(results[0])], str(np.max(softmax(results[0])))]
  class_activation_weights = gap_weights[:,0]
  class_activation_features = sp.ndimage.zoom(features_for_img, (224/14, 224/14, 1), order=2)
  cam_output  = np.dot(class_activation_features, class_activation_weights)
  return prediction, cam_output