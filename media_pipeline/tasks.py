from celery import shared_task
from django.conf import settings
from django.utils import timezone
from content.models import Content, VideoAsset
from reels.models import Reel
from .models import MediaJob


def build_media_url(file_field):
    if not file_field:
        return ''
    cdn = getattr(settings, 'UMBRELLA_CDN_BASE_URL', '')
    return f'{cdn}{file_field.url}' if cdn else file_field.url


@shared_task
def process_content_video(content_id):
    content = Content.objects.get(id=content_id)
    job = MediaJob.objects.create(job_type=MediaJob.JobType.CONTENT_TRANSCODE, content=content, status=MediaJob.Status.PROCESSING, source_path=str(content.source_video_file))
    try:
        asset, _ = VideoAsset.objects.get_or_create(content=content)
        asset.mp4_url = asset.mp4_url or build_media_url(content.source_video_file)
        asset.hls_manifest_url = asset.hls_manifest_url or asset.mp4_url
        asset.processing_status = VideoAsset.ProcessingStatus.READY
        asset.save(update_fields=['mp4_url', 'hls_manifest_url', 'processing_status', 'updated_at'])
        content.status = Content.Status.PENDING_REVIEW
        content.save(update_fields=['status', 'updated_at'])
        job.status = MediaJob.Status.DONE
        job.output_mp4_url = asset.mp4_url
        job.output_hls_url = asset.hls_manifest_url
        job.save(update_fields=['status', 'output_mp4_url', 'output_hls_url', 'updated_at'])
    except Exception as exc:
        job.status = MediaJob.Status.FAILED
        job.error_message = str(exc)
        job.save(update_fields=['status', 'error_message', 'updated_at'])
        raise


@shared_task
def process_reel_video(reel_id):
    reel = Reel.objects.get(id=reel_id)
    job = MediaJob.objects.create(job_type=MediaJob.JobType.REEL_TRANSCODE, reel=reel, status=MediaJob.Status.PROCESSING, source_path=str(reel.video_file))
    try:
        reel.video_url = reel.video_url or build_media_url(reel.video_file)
        reel.hls_manifest_url = reel.hls_manifest_url or reel.video_url
        reel.status = Reel.Status.PENDING_REVIEW
        reel.save(update_fields=['video_url', 'hls_manifest_url', 'status', 'updated_at'])
        job.status = MediaJob.Status.DONE
        job.output_mp4_url = reel.video_url
        job.output_hls_url = reel.hls_manifest_url
        job.save(update_fields=['status', 'output_mp4_url', 'output_hls_url', 'updated_at'])
    except Exception as exc:
        job.status = MediaJob.Status.FAILED
        job.error_message = str(exc)
        job.save(update_fields=['status', 'error_message', 'updated_at'])
        raise
