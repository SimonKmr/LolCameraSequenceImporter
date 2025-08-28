# LolCameraSequenceImporter

This is a simple blender addon that adds a lol-camera tab to the viewport menu (press n to open). This menu has an import button, where you can select json files. These json files are expected to have the structure of the https://127.0.0.1:2999/replay/sequence endpoint of the lol-replay-api. The sequence saves files of SkinSpotlights CreatorSuite work as well.

This should allow you to record sequences, skip motion tracking and get right to the work.

![grafik](https://user-images.githubusercontent.com/41740705/208783617-1d4d9136-8873-4972-8645-d84f74c12d7a.png)

## Known Issues 
- The keyframes are not put to linear instead smoothed by a bezir curve
  - This means, select all keyframes and change the interpolation to linear to fix.
- I don't know how the interpolation works in the programs, for the most accurate results use the client.
- The Start of the sequence is determined by the first Position Keyframe. If you got Keyframes before that, they are before Frame one.
- The normal camera gets automatically adjusted to 40° Field of View. This is equal to the default lol camera, if you change the focal length, this is not taken into account and your motion tracking could be of.

## Installation

[YouTube Tutorial](https://www.youtube.com/watch?v=OCTvyo2FVFw)

## How to use

tbd
