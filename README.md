# LolCameraSequenceImporter

This is a simple blender addon that adds a lol-camera tab to the viewport menu (press n to open). This menu has an import button, where you can select json files. These json files are expected to have the structure of the https://127.0.0.1:2999/replay/sequence endpoint of the lol-replay-api. The sequence saves files of SkinSpotlights CreatorSuite work as well.

This should allow you to record sequences, skip motion tracking and get right to the work.

## Known Issues 
- The keyframes always match from the first to the last keyframe the start and end of the rendering region. You need to adjust it to the length of the clip or sequence. 
- The keyframes are not put to linear, this part of the Blender API is not well done
- The length of the timespan is calculated by the location/position keyframes, this means if you have a clip that has rotation keyframes after its location keyframes, the timing should be off.
- The normal camera gets automatically adjusted to 40° Field of View. This is equal to the default lol camera, if you change the focal length, this is not taken into account and your motion tracking could be of.
