#!pip install --upgrade deeplearning2020
from deeplearning2020 import helpers, Submission

helpers.plot_learning_curve(title, x, y, y_test)

helpers.plot_history(title, history_object)

helpers.plot_images(labeled_images, labels)

Submission('40b2e133647124b0c676925cfde86748', '2', model).submit()