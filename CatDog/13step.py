#13 Steps to build CNN

#Step 1: Import the required packages

from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense

# Step 2: Initialising the CNN
model = Sequential()

# Step 3: Convolution
model.add(Conv2D(32, (3, 3), input_shape = (50, 50, 3), activation = 'relu'))

# Step 4: Pooling
model.add(MaxPooling2D(pool_size = (2, 2)))

# Step 5: Second convolutional layer
model.add(Conv2D(32, (3, 3), activation = 'relu'))
model.add(MaxPooling2D(pool_size = (2, 2)))

# Step 6: Flattening
model.add(Flatten())

# Step 7: Full connection
model.add(Dense(units = 128, activation = 'relu'))
model.add(Dense(units = 1, activation = 'sigmoid'))

# Step 8: Compiling the CNN
model.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

# Step 9: ImageDataGenerator
from keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(rescale = 1./255, shear_range = 0.2, zoom_range = 0.2, horizontal_flip = True)

# Step 10: Load the training Set
training_set = train_datagen.flow_from_directory('./train3', target_size =(50, 50), batch_size = 32, class_mode = 'binary')

# Step 11: Classifier Training 
model.fit_generator(training_set, steps_per_epoch = 4000, epochs = 2, validation_steps = 2000)

# Step 12: Convert the Model to json
model_json = model.to_json()
with open("./model.json","w") as json_file:
  json_file.write(model_json)

# Step 13: Save the weights in a seperate file
model.save_weights("./model.h5")

print("Classifier trained Successfully!")


# Step 1: Import the packages
from keras.models import model_from_json
import cv2
import numpy as np

# Step 2: Load the Model from Json File
json_file = open('./model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)

# Step 3: Load the weights
loaded_model.load_weights("./model.h5")
print("Loaded model from disk")

# Step 4: Compile the model
loaded_model.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

# Step 5: load the image you want to test
image = cv2.imread('2.jpg')
image = cv2.resize(image, (50,50))
image = image.reshape(1, 50, 50, 3)

cv2.imshow("Input Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
# Step 6: Predict to which class your input image has been classified
result = loaded_model.predict_classes(image)
if(result[0][0] == 1):
    print("I guess this must be a Dog!")
else:
    print("I guess this must be a Cat!")
