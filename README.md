# YouTube Downloader Scripts

A collection of Python scripts for downloading YouTube videos with different approaches - single video downloads and concurrent batch downloads.

## 📁 Files Overview

- **`simple-youtube-scraper.py`** - Single video downloader with command-line interface
- **`youtube-scraper.py`** - Concurrent batch downloader that reads URLs from a text file
- **`example_urls.txt`** - Example text file with YouTube URLs for batch downloading
- **`requirements.txt`** - Python dependencies

## 🚀 Quick Start

### Installation

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Single Video Download

```bash
python simple-youtube-scraper.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Batch Download

```bash
python youtube-scraper.py example_urls.txt
```

## 📋 Requirements

- Python 3.7+
- yt-dlp (YouTube downloader library)
- FFmpeg (for audio extraction)

### Installing FFmpeg

**Windows:**
- Download from [FFmpeg website](https://ffmpeg.org/download.html)
- Add to your system PATH

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

## 🔧 Script Details

### simple-youtube-scraper.py

A single-threaded YouTube video downloader with comprehensive options.

#### Features
- Download single videos with custom quality settings
- Audio-only downloads (MP3 format)
- Custom output directory
- Format listing without downloading
- Detailed progress information

#### Usage Examples

```bash
# Basic download
python simple-youtube-scraper.py "https://www.youtube.com/watch?v=VIDEO_ID"

# Download with specific quality
python simple-youtube-scraper.py "https://www.youtube.com/watch?v=VIDEO_ID" --quality 720p

# Audio-only download
python simple-youtube-scraper.py "https://www.youtube.com/watch?v=VIDEO_ID" --audio-only

# Custom output directory
python simple-youtube-scraper.py "https://www.youtube.com/watch?v=VIDEO_ID" --output ./my_videos

# List available formats
python simple-youtube-scraper.py "https://www.youtube.com/watch?v=VIDEO_ID" --list-formats
```

#### Command Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--output` | `-o` | Output directory | `./downloads` |
| `--quality` | `-q` | Video quality | `best` |
| `--audio-only` | `-a` | Download audio only | `False` |
| `--list-formats` | | List available formats | `False` |

### youtube-scraper.py

A concurrent YouTube video downloader that processes multiple URLs from a text file.

#### Features
- Concurrent downloads with configurable worker threads (default: 10)
- Text file input for batch processing
- Progress tracking with worker IDs
- Error handling and summary reporting
- Support for comments and empty lines in URL files

#### Usage Examples

```bash
# Basic batch download
python youtube-scraper.py example_urls.txt

# Custom output directory and quality
python youtube-scraper.py example_urls.txt --output ./my_videos --quality 720p

# Audio-only downloads with 5 workers
python youtube-scraper.py example_urls.txt --audio-only --workers 5

# List URLs without downloading
python youtube-scraper.py example_urls.txt --list-urls
```

#### Command Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--output` | `-o` | Output directory | `./downloads` |
| `--quality` | `-q` | Video quality | `best` |
| `--audio-only` | `-a` | Download audio only | `False` |
| `--workers` | `-w` | Number of concurrent workers | `10` |
| `--list-urls` | | List URLs without downloading | `False` |

## 📝 URL File Format

The `youtube-scraper.py` script reads URLs from a text file with the following format:

```
# This is a comment line (ignored)
https://www.youtube.com/watch?v=VIDEO_ID_1
https://www.youtube.com/watch?v=VIDEO_ID_2

# Another comment
https://youtu.be/VIDEO_ID_3

# Empty lines are also ignored
https://www.youtube.com/watch?v=VIDEO_ID_4
```

### Supported URL Formats
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://youtube.com/watch?v=VIDEO_ID`

## 🎯 Quality Options

Both scripts support various quality settings:

- `best` - Highest available quality (default)
- `worst` - Lowest available quality
- `720p` - 720p resolution
- `480p` - 480p resolution
- `360p` - 360p resolution
- `bestaudio` - Best audio quality only

## 📊 Performance

### Concurrent Downloads

The `youtube-scraper.py` script uses `ThreadPoolExecutor` for concurrent downloads:

- **Default**: 10 concurrent workers
- **Range**: 1-20 workers (configurable)
- **Benefit**: Significantly faster for multiple downloads
- **Resource**: Uses more bandwidth and CPU

### Recommended Settings

- **Low-end systems**: 3-5 workers
- **Standard systems**: 8-10 workers
- **High-end systems**: 15-20 workers
- **Bandwidth-limited**: 2-3 workers

## 🛠️ Troubleshooting

### Common Issues

1. **"FFmpeg not found" error**
   - Install FFmpeg and add it to your system PATH
   - Required for audio extraction

2. **"No valid YouTube URLs found"**
   - Check URL format in your text file
   - Ensure URLs start with supported prefixes

3. **Download failures**
   - Check internet connection
   - Verify video is not private/restricted
   - Try reducing the number of workers

4. **Permission errors**
   - Ensure write permissions for output directory
   - Run as administrator if necessary

### Error Handling

Both scripts include comprehensive error handling:
- Invalid URLs are skipped with warnings
- Failed downloads don't stop other downloads
- Detailed error messages for troubleshooting
- Summary reports show success/failure counts

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is for educational and personal use only. Please respect YouTube's Terms of Service and copyright laws. Users are responsible for ensuring they have the right to download content.