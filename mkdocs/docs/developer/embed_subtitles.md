# Summary of embed subtitles feature
- Embedding subtitles as a feature to support Plex
- My specific use case was a Youtube channel that uses subtitles for additional details during the video.  This channel has no voice audio to be transcribed.
- The implementation adds a new configuration option `add_subtitles` that allows users to embed subtitles directly into downloaded MP4 files during the download process.

### Key Changes Made:

**Backend Configuration (`backend/appsettings/`):**
- Added `add_subtitles: bool` field to configuration schema in `src/config.py:38`
- Added corresponding serializer field in `serializers.py:47`
- Default value set to `False` for backward compatibility

**Download Handler (`backend/download/src/yt_dlp_handler.py`):**
- Enhanced `_build_obs()` method to initialize subtitle-related options:
  - `writesubtitles: False` (default)
  - `subtitleslangs: []` (default empty)
- Modified `_build_obs_postprocessors()` method to conditionally add FFmpegEmbedSubtitle processor:
  - When `add_subtitles` is enabled, adds postprocessor with `already_have_subtitle: True`
  - Sets `subtitleslangs` to configured subtitle language
  - Enables `writesubtitles` option
- Improved error handling in `_progress_hook()` method to handle missing `info_dict` gracefully

**Frontend Interface (`frontend/src/`):**
- Added new state variable `embedSubtitles` in `SettingsApplication.tsx:60`
- Added toggle control in UI with label "Embed Subtitles"
- Updated TypeScript interfaces in `loadAppsettingsConfig.ts:19` and `AppSettingsStore.ts:26`
- Enhanced help text to explain: "Embed subtitles adds the subtitles to the mp4 file."

**Bug Fixes:**
- Fixed variable name typo in `channel/src/remote_query.py:116` (`query` → `queries`)
- Improved error handling for missing video info during download progress reporting

### Technical Implementation Details:

The feature leverages yt-dlp's built-in subtitle embedding capabilities through the `FFmpegEmbedSubtitle` postprocessor. When enabled:

1. Subtitles are downloaded in the configured language
2. FFmpeg embeds the subtitle streams directly into the MP4 container
3. The embedded subtitles remain accessible to media players like Plex
4. Original subtitle files are processed by the existing subtitle indexing system

This implementation follows the established pattern for other embedding features (metadata, thumbnails) and maintains consistency with the existing codebase architecture.

## yt-dlp example
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
### Frontend

**SettingsApplication.tsx:**
```typescript
// State variable (line 60)
const [embedSubtitles, setEmbedSubtitles] = useState(false);

// Initialization from config (line 119)
setEmbedSubtitles(appSettingsConfigData?.downloads.add_subtitles || false);

// UI Component (lines 613-622)
<div className="settings-box-wrapper">
  <div>
    <p>Embed Subtitles</p>
  </div>
  <ToggleConfig
    name="downloads.add_subtitles"
    value={embedSubtitles}
    updateCallback={handleUpdateConfig}
  />
</div>
```

**loadAppsettingsConfig.ts:**
```typescript
// Type definition (line 19)
add_subtitles: boolean;
```

**AppSettingsStore.ts:**
```typescript
// Store field (line 26)
add_subtitles: false,
```

### Backend

**appsettings/src/config.py:**
```python
# Type definition (line 38)
add_subtitles: bool

# Default configuration (line 89)
"add_subtitles": False,
```

**appsettings/serializers.py:**
```python
# Serializer field (line 47)
add_subtitles = serializers.BooleanField()
```

### yt-dlp Handler

**download/src/yt_dlp_handler.py:**

```python
# Enhanced _build_obs() method - default subtitle options (lines 164-167)
"writesubtitles": False,
"writethumbnail": False,
"noplaylist": True,
"color": "no_color",
"subtitleslangs": [],

# New postprocessor logic in _build_obs_postprocessors() (lines 222-231)
if self.config["downloads"]["add_subtitles"]:
    postprocessors.append(
        {
            "key": "FFmpegEmbedSubtitle",
            "already_have_subtitle": True,
        }
    )
    self.obs["subtitleslangs"] = [self.config["downloads"]["subtitle"]]
    self.obs["writesubtitles"] = True

# Improved error handling in _progress_hook() (lines 146-148)
info_dict = response.get("info_dict", {})
title = info_dict.get("title", "Processing")
```