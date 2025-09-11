# Summary of merge subtitles feature
- Merging subtitles as a feature was needed to support Plex

## Implementation
1. adding to `frontend/src/pages/SettingsApplication.tsx`
```python
  const [mergeSubtitle, setMergeSubtitle] = useState(false);

    setMergeSubtitle(appSettingsConfigData?.downloads.merge_subtitle || false);

                  <div className="settings-box-wrapper">
                    <div>
                      <p>Merge subtitle to video</p>
                    </div>
                    <ToggleConfig
                      name="downloads.merge_subtitle"
                      value={mergeSubtitle}
                      updateCallback={handleUpdateConfig}
                    />
                  </div>
```
2. adding to `frontend/src/api/loader/loadAppsettingsConfig.ts`
```python
    merge_subtitle: boolean;
```
3. additions to `backend/video/src/subtitle.py`
```python
    def merge_subtitle_to_video(self):
        """merge subtitle file into video file"""
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
4. additions to `backend/appsettings/src/config.py`
```python
    merge_subtitle: bool

            "merge_subtitle": False,
```
5. additions to `backend/download/src/yt_dlp_handler.py`
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