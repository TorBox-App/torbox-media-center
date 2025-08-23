# Changelog

## [1.3.0](https://github.com/TorBox-App/torbox-media-center/compare/v1.2.0...v1.3.0) (2025-08-23)


### Features

* adds debug values ([d794280](https://github.com/TorBox-App/torbox-media-center/commit/d794280ed4d3cd6baf45b3e3083d845d6fd52a3f))
* uses locks to prevent database issues ([0651cb1](https://github.com/TorBox-App/torbox-media-center/commit/0651cb175e5581fb62bc347d6038e66492aaf939))


### Bug Fixes

* better logging for failures ([fa7e3b5](https://github.com/TorBox-App/torbox-media-center/commit/fa7e3b5a096fd18f6da6e3203bc57bc84290c665))
* cached_links have a ttl of 3 hours ([61ca58f](https://github.com/TorBox-App/torbox-media-center/commit/61ca58fb862439dda07b90b27b1d2e515495d524))
* fixes None year issue as it is a string ([ad8caac](https://github.com/TorBox-App/torbox-media-center/commit/ad8caacc8f2009e1a25496c0580cf45860031ca9))
* handles missing files ([feac777](https://github.com/TorBox-App/torbox-media-center/commit/feac7778272e3f2a409c36949d971d1fb619bff8))
* handles specific medias properly ([c704bcf](https://github.com/TorBox-App/torbox-media-center/commit/c704bcf6252ab20c121384a5b85679997d455482))

## [1.2.0](https://github.com/TorBox-App/torbox-media-center/compare/v1.1.0...v1.2.0) (2025-06-26)


### Features

* adds easy scripts and troubleshooting section in readme ([393a85f](https://github.com/TorBox-App/torbox-media-center/commit/393a85fc0fbcba9d757419e65c0032f5ff940d82))
* adds retries to http transport ([39c3fef](https://github.com/TorBox-App/torbox-media-center/commit/39c3fef6ca587a0ed8e6fec77c93fba3c8d23e30))
* processes files in parallel for faster processing ([fcf5936](https://github.com/TorBox-App/torbox-media-center/commit/fcf5936e8cbc868465d1582aef90f6789a00cf7e))


### Bug Fixes

* adds timeout exception handling ([bc31cc5](https://github.com/TorBox-App/torbox-media-center/commit/bc31cc5d4b6c059f97d4fc39cef4e0dfba6b2986))
* handles when year is None, uses traceback in error ([da43d07](https://github.com/TorBox-App/torbox-media-center/commit/da43d075c39eae9e6ea77679eee328670ee14710))

## [1.1.0](https://github.com/TorBox-App/torbox-media-center/compare/v1.0.0...v1.1.0) (2025-05-09)


### Features

* ability to change mount refresh time ([6c6692e](https://github.com/TorBox-App/torbox-media-center/commit/6c6692ed86e81becfccefb7f695835ba66a1a1be))
* adds banner ([407081f](https://github.com/TorBox-App/torbox-media-center/commit/407081fdf085c91d46251a49faf2efe20c0a6c02))
* adds docker support back for linux/arm/v8 and linux/arm/v7 ([8c6bf74](https://github.com/TorBox-App/torbox-media-center/commit/8c6bf74e1406cf8c1a6c70eebaec1c1b84836e2f))
* builds for linux/arm64 and linux/arm/v8 ([8dd4719](https://github.com/TorBox-App/torbox-media-center/commit/8dd4719242d602d41bba63128e60126daeb3849c))
* gets all user files by iteration ([57c2b32](https://github.com/TorBox-App/torbox-media-center/commit/57c2b32da462f7adf924254379b7763084148dfd))
* support for windows and macos by splitting mounting methods and importing safely ([badc443](https://github.com/TorBox-App/torbox-media-center/commit/badc4438b5dd19dad7f2d275f7e6b6c8fa7dcdaf))
* uses search by file with full file name for better accuracy ([5f046d1](https://github.com/TorBox-App/torbox-media-center/commit/5f046d166959c50f0d230a6ce544cab0a18f2e9d))


### Bug Fixes

* adds timeout handling ([29aaf7b](https://github.com/TorBox-App/torbox-media-center/commit/29aaf7b7a04cf65ce17b747e0ce9fb0122f5eca4))
* cannot build on osx apple silicon ([d83aba0](https://github.com/TorBox-App/torbox-media-center/commit/d83aba0e1084a1107ad8560e057a4a54b154ba3a))
* cleans titles with invalid characters and code optimizaitons, handling error ([2b2e49a](https://github.com/TorBox-App/torbox-media-center/commit/2b2e49a65e9e5881333bf80d21557e72bd19d48a))
* cleans year to be single year only ([639d567](https://github.com/TorBox-App/torbox-media-center/commit/639d56775e14882c5a4f118de47d6e004682f365))
* darwin doesn't use unsupported parameter Cannot build on Apple Silicon Mac [#4](https://github.com/TorBox-App/torbox-media-center/issues/4) ([c1fc966](https://github.com/TorBox-App/torbox-media-center/commit/c1fc9663da8b477e404e22fc0c104a5f99f6f43c))
* falls back to short_name of item if no title, fixes Crashing with TypeError [#5](https://github.com/TorBox-App/torbox-media-center/issues/5) ([b13b372](https://github.com/TorBox-App/torbox-media-center/commit/b13b372daf5d504b9cb67c686676cf373486c933))
* handles errors when generating strm files ([6c9698e](https://github.com/TorBox-App/torbox-media-center/commit/6c9698e84b499133561b1d779a355f3cbc60da5f))
* handles when item name is the hash ([39af017](https://github.com/TorBox-App/torbox-media-center/commit/39af0177329a72d3377d55ab940bc348ee68c1a2))
* proper egg when installing on mac resolves Cannot build on Apple Silicon Mac [#4](https://github.com/TorBox-App/torbox-media-center/issues/4) ([c8127d4](https://github.com/TorBox-App/torbox-media-center/commit/c8127d443e1e416a52da4c0ecc3e10bc007fdf95))
* proper error when using fuse on Windows ([7669691](https://github.com/TorBox-App/torbox-media-center/commit/7669691776d0a54587b69a373d86291f113bfbf6))
* removes meta_title which had no bearing ([8f74ff3](https://github.com/TorBox-App/torbox-media-center/commit/8f74ff3955fe14bdd41913fbab60c801d2c3bc6f))
* uses a slim bookworm docker image ([1c83020](https://github.com/TorBox-App/torbox-media-center/commit/1c83020679eca0bcb92e6f906b4060e9691035e9))

## 1.0.0 (2025-05-06)


### Features

* adds docker comands, docker compose and updated installtion in readme ([c2215ee](https://github.com/TorBox-App/torbox-media-center/commit/c2215ee1702c8448e0c6217c5cf9e877873737d5))
* adds fuse mounting ([78a8842](https://github.com/TorBox-App/torbox-media-center/commit/78a8842d7a33f2f6818879cf307c55828ee8884d))
* adds mount path ([3a1e7ce](https://github.com/TorBox-App/torbox-media-center/commit/3a1e7ce84d47d7c619f2af1af9d109041f6c7b93))
* adds proper logging ([a570254](https://github.com/TorBox-App/torbox-media-center/commit/a57025407cc00514df434f16a42665a36bcc031b))
* better readme with links ([49cee8a](https://github.com/TorBox-App/torbox-media-center/commit/49cee8a92a63ffa9ad865d7d8c6993db9736e51f))
* cleans up strm files when exiting ([9cbc648](https://github.com/TorBox-App/torbox-media-center/commit/9cbc648a6387063829806107b77fa290dd2d98af))
* functions for retrieving user files with metadata ([7f6d2c4](https://github.com/TorBox-App/torbox-media-center/commit/7f6d2c4970cc3b52be46db54a6501839c032f8a6))
* path for folders, generates strem links ([fc1d476](https://github.com/TorBox-App/torbox-media-center/commit/fc1d476ba584f0bed07caa530723aed65c6464e4))
* properly returns file metadata for storage use ([44a56cf](https://github.com/TorBox-App/torbox-media-center/commit/44a56cfd21b23f60cc9a2168abbc8628de999d61))
* readme with basic information ([0b59229](https://github.com/TorBox-App/torbox-media-center/commit/0b59229dfd8aff53b25c0e84295b9b9100a0adeb))
* refreshes vfs in the background to reflect new files ([e3838aa](https://github.com/TorBox-App/torbox-media-center/commit/e3838aaa3e7de318d2c2f08d5ff63cd790b72c84))
* runs strm on boot ([8773e16](https://github.com/TorBox-App/torbox-media-center/commit/8773e160f509bfc3de8e3756e2c7c558ad9cf513))
* start of using fuse as alternative mounting method ([59e4f8d](https://github.com/TorBox-App/torbox-media-center/commit/59e4f8df3fa6fb2a5ba4ce3018025a11b00fe90a))
* uses internal database and gets fresh data on boot ([138400f](https://github.com/TorBox-App/torbox-media-center/commit/138400f007876f673037f23f9d9d47a2aa83d900))


### Bug Fixes

* bigger time between vfs refreshes ([e1bcf59](https://github.com/TorBox-App/torbox-media-center/commit/e1bcf59a086bb780790c3487709900093e5885e4))
* doesn't delete folder, only items inside ([be25b6f](https://github.com/TorBox-App/torbox-media-center/commit/be25b6f03133187fcbc01573f1672abbcc8577c1))
* properly gets episode and season ([aa0bb46](https://github.com/TorBox-App/torbox-media-center/commit/aa0bb46dc9eb4f14fd9c7cad4bd4aac8beb8d995))
* removes all files in directory on bootup ([effc502](https://github.com/TorBox-App/torbox-media-center/commit/effc5028e84d6a7c2032d9e2de8bd372ea820c7d))
* unpacks tuple ([aef17ff](https://github.com/TorBox-App/torbox-media-center/commit/aef17ff2669400bdebf8c7d3b69e3682d2b0bfc6))
