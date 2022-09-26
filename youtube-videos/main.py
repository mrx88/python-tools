#!/usr/bin/env python3
from pytube import Channel
from pytube import YouTube
from pytube import exceptions
import os
import logging
import click
from time import sleep
from multiprocessing import current_process
from multiprocessing import cpu_count
from multiprocessing import get_context
import deepdiff


def get_video(url, resolution, vid_dir):
    """Downloads a video from a given YouTube URL
    and adds it to the current directory <vid_dir>.

    Args:
        url (string): YouTube video URL
    """
    try:
        yt = YouTube(url)
        # get the current process
        process = current_process()
        logging.info(f'Worker is {process.name} with {yt.title} {url}')
        # block for a moment
        sleep(1)
        date = yt.publish_date.astimezone().strftime('%Y-%m-%d')
        # Define directory location
        publish_dir = os.path.join(vid_dir, date)
        logging.info(
            f"Video Title: {yt.title}|Date: {date}|Saving to: {publish_dir}")
        if not os.path.exists(publish_dir):
            logging.info(f"Creating directory: {publish_dir}")
            os.makedirs(publish_dir)
        # Get current file list in directory
        current_files = get_files(publish_dir)

        # Download the video
        if resolution == 'high':
            yt.streams.get_highest_resolution().download(
                output_path=publish_dir, max_retries=5)
            # Get current (new) file list in directory
            new_files = get_files(publish_dir)

        elif resolution == 'low':
            yt.streams.get_lowest_resolution().download(
                output_path=publish_dir, max_retries=5)
            new_files = get_files(publish_dir)

        # Report new video filenames
        diff = deepdiff.DeepDiff(current_files, new_files)
        fileitems = diff.get('iterable_item_added')
        if fileitems:
            for h in fileitems.items():
                print(f"New video added: {h[1]}")
                logging.info(f"New video added: {h[1]}")

    except exceptions.VideoUnavailable as e:
        logging.error(f'Video is unavailable: {e}')
    except exceptions.PytubeError as e:
        logging.error(f'Pytube error: {e}')
    except Exception as e:
        logging.error(f'Get_video other Error: {e}')


def get_files(publish_dir):
    """Get full filenames with directory location

    Args:
        publish_dir (list): Video directory location

    Returns:
        list: full file name with path location
    """
    try:
        filelist = os.listdir(publish_dir)
        curfilelist = []
        for file in filelist:
            fileloc = publish_dir + "/" + file
            file_exists = os.path.exists(fileloc)
            if file_exists:
                curfilelist.append(fileloc)
        return curfilelist

    except Exception as e:
        logging.error(f'Get_files Error: {e}')


def get_channel(url):
    """Get list of YouTube video urls from a YouTube channel

    Args:
        url (string): YouTube channel URL

    Returns:
        list: Return list of video URLs
    """
    try:
        c = Channel(url)
        logging.info(f"Channel name: {c.channel_name}")

        return c.video_urls

    except exceptions.PytubeError as e:
        logging.error(e)
        return None
    except Exception as e:
        logging.error(f'Get_channel other error: {e}')
        return None


def getlogger():
    """Logging details
    """
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        filename='main.log')


@click.command()
@click.option('--url', help='YouTube channel URL', required=True)
@click.option('--resolution', default='high', help='Video resolution',
              type=click.Choice(['low', 'high'], case_sensitive=False))
@click.option('--vid_dir', help='Video <directory> location', default='/')
@click.option('--last', help='Number of last videos to download', type=int)
def main(url, resolution, vid_dir, last):
    """Main function"""
    getlogger()
    try:
        # Get video URLs from a YouTube channel
        yt_url = get_channel(url)
        # Download YouTube videos defined in the channel
        ctx = get_context('spawn')
        pool = ctx.Pool(cpu_count(), initializer=getlogger)
        if last:
            latest = []
            for url in range(last):
                video = yt_url[url]
                latest.append(video)
            processes = [pool.apply_async(get_video, args=(
                url, resolution, vid_dir)) for url in latest]
            result = [p.get() for p in processes]
            print(f"Completed download of last {len(result)} videos")
            logging.info(f"Completed download of last {len(result)} videos")
            pool.close()
            pool.join()

        else:
            processes = [pool.apply_async(get_video, args=(
                url, resolution, vid_dir)) for url in yt_url]
            result = [p.get() for p in processes]
            print(f"Completed download of {len(result)} videos")
            logging.info(f"Completed download of {len(result)} videos")
            pool.close()
            pool.join()

    except Exception as e:
        logging.error(f"Main function error: {e}")


if __name__ == '__main__':
    main()
