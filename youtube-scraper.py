"""
YouTube Video Scraper Script
Downloads multiple YouTube videos concurrently from a text file containing URLs.
Uses yt_dlp with ThreadPoolExecutor for concurrent downloads with 10 workers.
"""

import os
import sys
import argparse
import threading
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from yt_dlp import YoutubeDL


def download_video(url, output_path="./downloads", quality="best", audio_only=False, worker_id=None):
    """
    Download a YouTube video using yt_dlp.
    
    Args:
        url (str): YouTube video URL
        output_path (str): Directory to save the downloaded file
        quality (str): Video quality preference ('best', 'worst', '720p', '480p', etc.)
        audio_only (bool): If True, download only audio
        worker_id (int): Worker thread ID for logging
    
    Returns:
        tuple: (url, success, error_message)
    """
    
    Path(output_path).mkdir(parents=True, exist_ok=True)
    
    ydl_opts = {
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'format': 'bestaudio/best' if audio_only else f'{quality}[ext=mp4]/best[ext=mp4]/best',
        'quiet': True,
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
            
            worker_info = f"[Worker {worker_id}]" if worker_id else "[Main]"
            print(f"{worker_info} Starting download: {title}")
            print(f"{worker_info} Duration: {duration // 60}:{duration % 60:02d}")
            
            ydl.download([url])
            print(f"{worker_info} ✓ Completed: {title}")
            
            return (url, True, None)
            
    except Exception as e:
        error_msg = str(e)
        worker_info = f"[Worker {worker_id}]" if worker_id else "[Main]"
        print(f"{worker_info} ✗ Failed: {url} - {error_msg}")
        return (url, False, error_msg)


def read_urls_from_file(file_path):
    """
    Read YouTube URLs from a text file.
    
    Args:
        file_path (str): Path to the text file containing URLs
    
    Returns:
        list: List of valid YouTube URLs
    """
    urls = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                
                if not line or line.startswith('#'):
                    continue
                
                if line.startswith(('https://www.youtube.com/', 'https://youtu.be/', 'https://youtube.com/')):
                    urls.append(line)
                else:
                    print(f"Warning: Line {line_num} is not a valid YouTube URL: {line}")
    
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        sys.exit(1)
    
    return urls


def download_concurrently(urls, output_path="./downloads", quality="best", audio_only=False, max_workers=10):
    """
    Download multiple videos concurrently using ThreadPoolExecutor.
    
    Args:
        urls (list): List of YouTube URLs to download
        output_path (str): Directory to save downloaded files
        quality (str): Video quality preference
        audio_only (bool): If True, download only audio
        max_workers (int): Maximum number of concurrent workers
    
    Returns:
        tuple: (successful_downloads, failed_downloads)
    """
    
    print(f"Starting concurrent download of {len(urls)} videos with {max_workers} workers...")
    print(f"Output directory: {output_path}")
    print("-" * 60)
    
    successful_downloads = []
    failed_downloads = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {}
        for i, url in enumerate(urls):
            future = executor.submit(
                download_video, 
                url, 
                output_path, 
                quality, 
                audio_only, 
                worker_id=i+1
            )
            future_to_url[future] = url
        
        for future in as_completed(future_to_url):
            url, success, error_msg = future.result()
            
            if success:
                successful_downloads.append(url)
            else:
                failed_downloads.append((url, error_msg))
    
    return successful_downloads, failed_downloads


def main():
    """Main function to handle command line arguments and execute concurrent downloads."""
    
    parser = argparse.ArgumentParser(
        description="Download multiple YouTube videos concurrently from a text file",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python youtube-scraper.py urls.txt
  python youtube-scraper.py urls.txt --output ./my_videos
  python youtube-scraper.py urls.txt --quality 720p --workers 5
  python youtube-scraper.py urls.txt --audio-only
        """
    )
    
    parser.add_argument(
        'url_file',
        help='Text file containing YouTube URLs (one per line)'
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
        '--workers', '-w',
        type=int,
        default=10,
        help='Number of concurrent workers (default: 10)'
    )
    
    parser.add_argument(
        '--list-urls',
        action='store_true',
        help='List URLs from file without downloading'
    )
    
    args = parser.parse_args()
    urls = read_urls_from_file(args.url_file)
    
    if not urls:
        print("No valid YouTube URLs found in the file.")
        sys.exit(1)
    
    print(f"Found {len(urls)} valid YouTube URLs")
    
    if args.list_urls:
        print("\nURLs to be downloaded:")
        for i, url in enumerate(urls, 1):
            print(f"{i:2d}. {url}")
        return
    
    if args.workers < 1 or args.workers > 20:
        print("Warning: Workers count should be between 1 and 20. Using 10.")
        args.workers = 10
    
    successful_downloads, failed_downloads = download_concurrently(
        urls=urls,
        output_path=args.output,
        quality=args.quality,
        audio_only=args.audio_only,
        max_workers=args.workers
    )
    
    print("\n" + "=" * 60)
    print("DOWNLOAD SUMMARY")
    print("=" * 60)
    print(f"Total URLs processed: {len(urls)}")
    print(f"Successful downloads: {len(successful_downloads)}")
    print(f"Failed downloads: {len(failed_downloads)}")
    
    if failed_downloads:
        print("\nFailed downloads:")
        for url, error in failed_downloads:
            print(f"  - {url}: {error}")
    
    if successful_downloads:
        print(f"\nAll successful downloads saved to: {args.output}")
    
    if failed_downloads:
        sys.exit(1)


if __name__ == "__main__":
    main()
