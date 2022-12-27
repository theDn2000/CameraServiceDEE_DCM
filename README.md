# Drone Engineering Ecosystem
![software-arch](https://user-images.githubusercontent.com/32190349/155320787-f8549148-3c93-448b-b79a-388623ca5d3f.png)

## Demo

[Drone Engineering Ecosystem demo](https://www.youtube.com/playlist?list=PL64O0POFYjHpXyP-T063RdKRJXuhqgaXY)

## CameraController

This module is responsible for managing the camera from the drone.
We can have 4 different valid messages arriving to this module:

- *connectPlatform*: We subscribe to retrieve the different commands
- *takePicture*: We take a picture and publish it, so that the users subscribed can retrieve it
- *startVideoStream*: Start a video stream of what the drone is recording
- *stopVideoStream*: Stop the current video stream

## Example and tutorials

The basics of MQTT can be found here:
[MQTT](https://www.youtube.com/watch?v=EIxdz-2rhLs)

This is a good example to start using MQTT (using a public broker):
[Example](https://www.youtube.com/watch?v=kuyCd53AOtg)
