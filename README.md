![Logo](https://raw.githubusercontent.com/TorBox-App/torbox-media-center/main/assets/header.png)

## 📚 About

The TorBox Media Center allows you to easily mount your TorBox media in a no-frills way. This mounts your playable media files to your filesystem for use with [Jellyfin](https://jellyfin.org/), [Emby](https://emby.media/), [Plex](https://www.plex.tv), [Infuse](https://firecore.com/infuse), [VLC](https://www.videolan.org/vlc/), or any other media player. With TorBox's custom built solution you can mount files as virtual files (which take up zero storage space), or as '.strm' files (which take up less than 1GB for libraries of any size).

> [!IMPORTANT]
> *TorBox does not allow piracy or condone it in any way. This is meant to be used with media you own and have the rights to.*

### ✨ Features

- Organizing your media automatically, using the [TorBox Metadata Search API](https://www.postman.com/wamy-dev/torbox/request/ubj7d6v/get-metadata-by-query)
- Mounting your media simply and safely
- Making sure your media is easily discoverable by media players
- Fast and effecient.
- Proxy for files *(if your connection is slow)*
- Compatible with all systems and OS *(when using the `strm` mount method)*
- No limit on library size
- Automatically updating library and mounts

### 🤖 Comparison to Zurg

- Usability with TorBox
- Latest features for free
- Faster setup *(no config necessary)*
- No reliance on RClone
- Optimized for TorBox
- More video server/player support
- Works with torrents, usenet and web downloads.

### ✖️ What this application does not do

- Folder customization *(limited to 'movies' and 'series')*
- Provides WebDAV server *(use TorBox's WebDAV)*
- Works with all types of files *(limited to video files)*
- Gets you banned from TorBox *(developed by TorBox team)*
- 'Repairing' or 'renewing' your library *(this is against TorBox ToS)*
- Adding new downloads
- Customizing downloads *(update/rename)*
- Manage downloads *(delete)*

## 🔄 Compatibility

### 💻 Compatbility with OS

Compatibility is limited to Linux/Unix/BSD based systems when using the `fuse` option due to requiring [FUSE](https://www.kernel.org/doc./html/next/filesystems/fuse.html). [MacOS is also supported](https://macfuse.github.io/).

The `strm` option is compatible with all systems.

If the `fuse` option is selected and your system is incompatible, the application will give an error and will not run.

> [!NOTE]
> If you are unsure, choose the `strm` option.

### 📺 Compatbility with players / media servers

The `strm` option is geared towards media servers which support '.strm' files such as Jellyfin and Emby. If using either of these options, we recommend using the `strm` mounting method.

The `fuse` option is meant to be a fallback for everything else, Plex, VLC, Infuse, etc. This is due to the fuse method mounting the virtual files right to your filesystem as if they were local. This means that any video player will be able to stream from them and the TorBox Media Center will handle the rest.

> [!TIP]
> Emby / Jellyfin => `strm`
>
> Plex / VLC / Anything else => `fuse`

## 🔌 Choosing a mounting method

[Above](https://github.com/TorBox-App/torbox-media-center/tree/main?tab=readme-ov-file#compatibility) we explained compatibility, which should be the main driving factor for making a decision, but there are few other things we should mention.

1. The virtual filesystem created by the `fuse` mounting method can be slower (playing files, reading files, listing files and directories) and take up more resources as it emulates an entire filesystem. It also may not play well with your [Docker installation](https://github.com/TorBox-App/torbox-media-center/tree/main?tab=readme-ov-file#running-on-docker-recommended) (if going that route).
2. The `strm` mounting method takes up more storage space, and disk reads and writes as they are physical text files. Over longer periods of time it can wear down your disk (not by much, but it is something we should mention). If you have a slow filesystem (hard drive vs SSD), this can be slower if you have a lot of files.

## ❓ Why not use RClone?

We wanted to reduce the number of moving parts required to use this application. [RClone](https://rclone.org/) would only be used for FUSE mounting, but ~~every single~~ most Linux systems ship with some type of FUSE already, so RClone would be redundant. RClone also introduces more challenges, such as configuration, making sure versions are up to date, and you would still need FUSE anyways. This application doesn't provide a WebDAV API, so realistically, RClone isn't necessary here.

## ✅ Requirements

1. A TorBox account. Must be on a paid plan. Sign up [here](https://torbox.app/subscription).
2. A server or computer running Linux/Unix/BSD/[MacOS](https://macfuse.github.io/). Must be able to run Python or has administrator access *(only necessary for Docker installation)*
3. A player in mind you want to use *(for choosing a mounting method)*

## 🔧 Environment Variables

To run this project you will need to add the following environment variables to your `.env` file or to your Docker run command.

`TORBOX_API_KEY` Your TorBox API key used to authenticate with TorBox. You can find this [here](https://torbox.app/settings). This is required.

`MOUNT_METHOD` The mounting method you want to use. Must be either `strm` or `fuse`. Read here for choosing a method. The default is `strm` and is optional.

`MOUNT_PATH` The mounting path where all of your files will be accessible. If inside of Docker, this path needs to be accessible to other applications. If running locally without Docker, this path must be owned.

`MOUNT_REFRESH_TIME` How fast you would like your mount to look for new files. Must be either `slow` for every 3 hours, `normal` for every 2 hours, `fast` for every 1 hour, or `instant` for every 6 minutes. The default is `fast` and is optional.

`MIN_MEDIA_SIZE_MB` The minimum media file size in megabytes. Files smaller than this size will be skipped and no STRM files will be generated for them. The default is `30` MB and is optional.

## 🐳 Running on Docker (recommended)

1. Make sure you have Docker installed on your server/computer. You can find instructions on how to install Docker [here](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-22-04) *(you can change your distribution in the guide)*.
2. Edit the below Docker command with your proper environment variables and options. More Docker run commands can be found [here](https://github.com/TorBox-App/torbox-media-center/blob/main/docker.md).

```bash
docker run -it -d \
    --name=torbox-media-center \
    --restart=always \
    --init \
    -v /home/$(whoami)/torbox:/torbox \
    -e TORBOX_API_KEY=<EDIT_THIS_KEY> \
    -e MOUNT_METHOD=strm \
    -e MOUNT_PATH=/torbox \
    -e MIN_MEDIA_SIZE_MB=30 \
    anonymoussystems/torbox-media-center:latest
```

or if you prefer Docker compose, this is the yaml, also found [here](https://github.com/TorBox-App/torbox-media-center/blob/main/docker-compose.yaml).

```yaml
name: torbox-media-center
services:
    torbox-media-center:
        container_name: torbox-media-center
        stdin_open: true
        tty: true
        restart: always
        volumes:
            - /home/$(whoami)/torbox:/torbox
        environment:
            - TORBOX_API_KEY=<EDIT_THIS_KEY>
            - MOUNT_METHOD=strm
            - MOUNT_PATH=/torbox
            - MIN_MEDIA_SIZE_MB=30
        image: anonymoussystems/torbox-media-center:latest
```

*You may also use the Github repository container found here: ghcr.io/torbox-app/torbox-media-center:main*

3. Wait for the files to be mounted to your local system.

## 🏠 Running Locally (no Docker)

1. Make sure you have Python installed. Anything from v3.6 should be okay.
2. Download or git clone this repository.

```bash
git clone https://github.com/TorBox-App/torbox-media-center.git
```

or download the repository zip file [here](https://github.com/TorBox-App/torbox-media-center/archive/refs/heads/main.zip) and extract the files.

3. Create a `.env` file or rename `.env.example` to `.env`.
4. Edit or add in your environment variables to the `.env` file.
5. Install the requirements.

```bash
pip3 install -r requirements.txt
```

6. Run the `main.py` script.

```bash
python3 main.py
```

7. Wait for the files to be mounted to your local machine.

## 🆘 Support

For support, email [contact@torbox.app](mailto:contact@torbox.app) or join our Discord server [here](https://join-discord.torbox.app). *We will not give sources or help with piracy in any way. This is for technical support only.*

## 🤝 Contributing

Contributions are always welcome!

Please make sure to follow [Conventional Commits](https://conventionalcommits.org/) when creating commit messages. We will authorize most pull requests, so don't hesitate to help out!
