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

## PreCommit
`pre-commit` is a pretty nice tool that allow us to run different actions in our code before we commit any file.
We will use it for formatting our code, "prettify" json files, etc. To install pre-commit on our code,
which will allow us to NOT commit the files if there is something wrong with them, we have to type on the top directory:

`pre-commit install`

If the pre-commit gets a little annoying, and you just want to commit files, you can deactivate it:

`pre-commit uninstall`

If we want to make sure that we can commit the files, and if not, why, then we need to run the following command:

`pre-commit run --all-files` or `pre-commit run -a`

By doing so, we ensure that, before uploading any file to GitHub, our code is well assembled.

## Example and tutorials

The basics of MQTT can be found here:
[MQTT](https://www.youtube.com/watch?v=EIxdz-2rhLs)

This is a good example to start using MQTT (using a public broker):
[Example](https://www.youtube.com/watch?v=kuyCd53AOtg)
