"""
YouTube Video Downloader Script
Uses yt_dlp to download YouTube videos with various quality options.
"""

import os
import sys
import argparse
from pathlib import Path
from yt_dlp import YoutubeDL


def download_video(url, output_path="./downloads", quality="best", audio_only=False):
    """
    Download a YouTube video using yt_dlp.
    
    Args:
        url (str): YouTube video URL
        output_path (str): Directory to save the downloaded file
        quality (str): Video quality preference ('best', 'worst', '720p', '480p', etc.)
        audio_only (bool): If True, download only audio
    """
    
    Path(output_path).mkdir(parents=True, exist_ok=True)
    
    ydl_opts = {
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'format': 'bestaudio/best' if audio_only else f'{quality}[ext=mp4]/best[ext=mp4]/best',
    }
    
    if audio_only:
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'Unknown')
            duration = info.get('duration', 0)
            
            print(f"Title: {title}")
            print(f"Duration: {duration // 60}:{duration % 60:02d}")
            print(f"Downloading to: {output_path}")
            print("-" * 50)
            
            ydl.download([url])
            print("Download completed successfully!")
            
    except Exception as e:
        print(f"Error downloading video: {str(e)}")
        return False
    
    return True


def main():
    """Main function to handle command line arguments and execute download."""
    
    parser = argparse.ArgumentParser(
        description="Download YouTube videos using yt_dlp",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python simple-youtube-scraper.py "https://www.youtube.com/watch?v=VIDEO_ID"
  python simple-youtube-scraper.py "https://www.youtube.com/watch?v=VIDEO_ID" --quality 720p
  python simple-youtube-scraper.py "https://www.youtube.com/watch?v=VIDEO_ID" --audio-only
  python simple-youtube-scraper.py "https://www.youtube.com/watch?v=VIDEO_ID" --output ./my_videos
        """
    )
    
    parser.add_argument(
        'url',
        help='YouTube video URL to download'
    )
    
    parser.add_argument(
        '--output', '-o',
        default='./downloads',
        help='Output directory for downloaded files (default: ./downloads)'
    )
    
    parser.add_argument(
        '--quality', '-q',
        default='best',
        help='Video quality preference (default: best). Options: best, worst, 720p, 480p, 360p, etc.'
    )
    
    parser.add_argument(
        '--audio-only', '-a',
        action='store_true',
        help='Download only audio (MP3 format)'
    )
    
    parser.add_argument(
        '--list-formats',
        action='store_true',
        help='List available formats for the video without downloading'
    )
    
    args = parser.parse_args()

    if not args.url.startswith(('https://www.youtube.com/', 'https://youtu.be/', 'https://youtube.com/')):
        print("Error: Please provide a valid YouTube URL")
        sys.exit(1)
    
    if args.list_formats:
        try:
            with YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(args.url, download=False)
                formats = info.get('formats', [])
                
                print(f"Available formats for: {info.get('title', 'Unknown')}")
                print("-" * 80)
                print(f"{'Format ID':<12} {'Extension':<10} {'Quality':<15} {'Size':<10}")
                print("-" * 80)
                
                for fmt in formats:
                    format_id = fmt.get('format_id', 'N/A')
                    ext = fmt.get('ext', 'N/A')
                    quality = fmt.get('format_note', fmt.get('resolution', 'N/A'))
                    filesize = fmt.get('filesize')
                    size_str = f"{filesize // (1024*1024)}MB" if filesize else "Unknown"
                    
                    print(f"{format_id:<12} {ext:<10} {quality:<15} {size_str:<10}")
                    
        except Exception as e:
            print(f"Error listing formats: {str(e)}")
            sys.exit(1)
        
        return
    
    success = download_video(
        url=args.url,
        output_path=args.output,
        quality=args.quality,
        audio_only=args.audio_only
    )
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
