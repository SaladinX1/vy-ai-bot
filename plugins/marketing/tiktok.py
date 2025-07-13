from vision.actions import click_text, type_text, wait_for_element


class TikTokBot:
    def upload_video(self, video_path, caption):
        click_text("Upload")
        type_text(video_path)
        type_text(caption)
        click_text("Post")