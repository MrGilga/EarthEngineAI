import os
import os.path
import requests
import ee

ee.Authenticate()
ee.Initialize()

# Define the geometry of the area for which you would like images.
box = ee.Geometry.Polygon([[8.8694, 45.7969],
                           [8.8694, 45.7844],
                           [8.8888, 45.7844],
                           [8.8888, 45.7969]])

# .select(['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11', 'B12'])
collection = (ee.ImageCollection("COPERNICUS/S2")
              .select(['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11', 'B12'])
              .filter(ee.Filter.date('2017-01-01', '2021-03-31'))
              .filterBounds(box)
              .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 30))
              )

collectionList = collection.toList(collection.size())
collectionSize = collectionList.size().getInfo()
print(collectionSize)
num_img = min(collectionSize, 10)

#if not os.path.exists("dataset"):
# os.makedirs("dataset")

for i in range(num_img):
    img = ee.Image(collectionList.get(i))
    url = img.getDownloadUrl({
        'bands': ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11', 'B12'],
        'region': box,
        'scale': 10,
        'format': 'GEO_TIFF'
    })
    print(url)
    response = requests.get(url)
    with open(os.path.join('dataset', 'multiband' + str(i) + '.tif'), 'wb') as fd:
        fd.write(response.content)