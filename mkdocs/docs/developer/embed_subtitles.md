# Summary of embed subtitles feature
- Merging subtitles as a feature to support Plex

## yt-dlp cli options
- duplicate the cli functionality of the yt-dlp command
```shell
yt-dlp --format bestvideo[height=720][vcodec*=av01]+bestaudio[acodec*=mp4a] --write-subs --sub-langs en-US --embed-subs --embed-thumbnail --embed-metadata --merge-output-format mp4 https://youtu.be/VIDEO_ID
```
## yt-dlp cli_to_api
- convert the cli options to api options
```shell
(.venv) username@host:~/github/yt-dlp/yt-dlp/devscripts$ python cli_to_api.py --format bestvideo[height=720][vcodec*=av01]+bestaudio[acodec*=mp4a] --write-subs --sub-langs en-US --embed-subs --embed-thumbnail --embed-metadata --merge-output-format mp4

The arguments passed translate to:

{'format': 'bestvideo[height=720][vcodec*=av01]+bestaudio[acodec*=mp4a]',
 'merge_output_format': 'mp4',
 'outtmpl': {'pl_thumbnail': ''},
 'postprocessors': [{'already_have_subtitle': True,
                     'key': 'FFmpegEmbedSubtitle'},
                    {'add_chapters': True,
                     'add_infojson': 'if_exists',
                     'add_metadata': True,
                     'key': 'FFmpegMetadata'},
                    {'already_have_thumbnail': False, 'key': 'EmbedThumbnail'}],
 'subtitleslangs': ['en-US'],
 'writesubtitles': True,
 'writethumbnail': True}

Combining these with the CLI defaults gives:

{'extract_flat': 'discard_in_playlist',
 'format': 'bestvideo[height=720][vcodec*=av01]+bestaudio[acodec*=mp4a]',
 'fragment_retries': 10,
 'ignoreerrors': 'only_download',
 'merge_output_format': 'mp4',
 'outtmpl': {'pl_thumbnail': ''},
 'postprocessors': [{'already_have_subtitle': True,
                     'key': 'FFmpegEmbedSubtitle'},
                    {'add_chapters': True,
                     'add_infojson': 'if_exists',
                     'add_metadata': True,
                     'key': 'FFmpegMetadata'},
                    {'already_have_thumbnail': False, 'key': 'EmbedThumbnail'},
                    {'key': 'FFmpegConcat',
                     'only_multi_video': True,
                     'when': 'playlist'}],
 'retries': 10,
 'subtitleslangs': ['en-US'],
 'warn_when_outdated': True,
 'writesubtitles': True,
 'writethumbnail': True}
```

## Implementation
### `frontend/src/pages/SettingsApplication.tsx`
```python
  const [embedSubtitle, setEmbedSubtitle] = useState(false);

    setEmbedSubtitle(appSettingsConfigData?.downloads.embed_subtitle || false);

                  <div className="settings-box-wrapper">
                    <div>
                      <p>Embed subtitle to video</p>
                    </div>
                    <ToggleConfig
                      name="downloads.embed_subtitle"
                      value={embedSubtitle}
                      updateCallback={handleUpdateConfig}
                    />
                  </div>
```
### `frontend/src/api/loader/loadAppsettingsConfig.ts`
```python
    embed_subtitle: boolean;
```
### `backend/video/src/subtitle.py`
```python
    def embed_subtitle_to_video(self):
        """embed subtitle file into video file"""
        # This function will be implemented based on further instructions
        pass

    def delete(self, subtitles=False):
        """delete subtitles from index and filesystem"""
        youtube_id = self.video.youtube_id

        if not subtitles:
            return False

        indexed = []
        paths = []

        # delete from ES
        for subtitle in subtitles:
            media_url = subtitle.get("media_url")
            lang = subtitle.get("lang")
            paths.append(media_url)
            indexed.append(f"{youtube_id}-{lang}-")

        if indexed:
            # delete from index
            query = {
                "query": {
                    "bool": {"should": []}
                }
            }
            for idx in indexed:
                match = {"prefix": {"subtitle_fragment_id": idx}}
                query["query"]["bool"]["should"].append(match)

            response, status_code = ElasticWrap("ta_subtitle/_delete_by_query").post(
                query
            )
            if not status_code == 200:
                print(response)

        # delete files
        videos_base = EnvironmentSettings.MEDIA_DIR
        for file_name in paths:
            file_path = os.path.join(videos_base, file_name)
            try:
                os.remove(file_path)
            except FileNotFoundError:
                print(f"{youtube_id}: {file_path} failed to delete")
```
### `backend/appsettings/src/config.py`
```python
    embed_subtitle: bool

            "embed_subtitle": False,
```
### `backend/download/src/yt_dlp_handler.py`
```python
        # Configure subtitle settings
        subtitle_language = self.config["downloads"]["subtitle"]
        if subtitle_language:
            # If subtitle language is set, enable writing and embedding subtitles
            self.obs["writesubtitles"] = True
            self.obs["embedsubtitles"] = True
            self.obs["subtitleslangs"] = [s.strip() for s in subtitle_language.split(",")]
        else:
            # If subtitle language is not set, disable subtitle features
            self.obs["writesubtitles"] = False
            self.obs["embedsubtitles"] = False
```